from langchain_core.runnables import RunnableConfig

from ai.chains import get_memory_chain, get_character_chain
from ai.retrievers import get_retriever
from ai.state import StateBot


async def memory_extraction_node(state: StateBot, config: RunnableConfig):
    chain = get_memory_chain()
    response = await chain.ainvoke({"message": state["messages"][-1]})
    if response.is_important:
        chat_id = config["configurable"]["chat_id"]
        retriever = get_retriever()
        retriever.vectorstore.add_texts(
            texts=[response.formatted_memory],
            metadatas=[{"chat_id": int(chat_id)}]
        )
    return {}

async def memory_injection_node(state: StateBot, config: RunnableConfig):
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
    chain = get_character_chain()
    response = await chain.ainvoke(
        {
            "messages": state['messages'],
            "memory_context": memory_context,
        },
        config,
    )
    return {"messages": response}
