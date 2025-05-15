import uuid

from langchain_core.messages import HumanMessage, RemoveMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.store.base import BaseStore

from ai.chains import get_memory_chain, get_character_chain
from ai.prompts import CHARACTER_PROMPT
from ai.retrievers import get_retriever
from ai.state import StateBot


async def memory_extraction_node(state: StateBot, config: RunnableConfig, store: BaseStore):
    chain = get_memory_chain()
    response = await chain.ainvoke({"message": state["messages"][-1]})
    if response.is_important:
        chat_id = config["configurable"]["chat_id"]
        try:
            retriever = get_retriever()
            if retriever and hasattr(retriever, "vectorstore"):
                retriever.vectorstore.add_texts(
                    texts=[response.formatted_memory],
                    metadatas=[{"chat_id": int(chat_id)}]
                )
        except Exception as e:
            print(e)
    return {}

async def memory_injection_node(state: StateBot, config: RunnableConfig, store: BaseStore):
    chat_id = config["configurable"]["chat_id"]
    retriever = get_retriever()
    last_message = state["messages"][-1].content
    relevant_docs = await retriever.ainvoke(
        last_message,
        filter={"chat_id": int(chat_id)},
    )
    memory_context = "\n".join(doc.page_content for doc in relevant_docs)
    return {"memory_context": memory_context}

async def generate_response(state: StateBot, config: RunnableConfig):
    memory_context = state.get('memory_context')
    chain = get_character_chain(state.get("summary", ""))
    response = await chain.ainvoke(
        {
            "prompt": CHARACTER_PROMPT,
            "messages": state['messages'],
            "memory_context": memory_context,
        },
        config,
    )
    return {"answer": response.content, "messages": response}

async def summarize_conversation_node(state: StateBot):
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    summary = state.get("summary", "")
    if summary:
        summary_message = (
            f"This is summary of the conversation to date between Lucía and the user: {summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
        )
    else:
        summary_message = (
            f"Create a summary of the conversation above between Lucía and the user. "
            "The summary must be a short description of the conversation so far, "
            f"but that captures all the relevant information shared between Lucía and the user:"
        )
    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = await model.ainvoke(messages)
    delete_messages = [
        RemoveMessage(id=m.id)
        for m in state["messages"][: 15]
    ]
    return {"summary": response.content, "messages": delete_messages}
