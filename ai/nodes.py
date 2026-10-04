from uuid import uuid4

from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime

from ai.chains import get_memory_chain, get_character_chain
from ai.state import Context, StateBot


async def memory_extraction_node(state: StateBot, runtime: Runtime[Context]):
    chain = get_memory_chain()
    response = await chain.ainvoke({"message": state["messages"][-1]})
    if response.is_important:
        namespace = (runtime.context.user_id, "memories")
        try:
            await runtime.store.aput(
                namespace,
                str(uuid4()),
                {"data": response.formatted_memory},
            )
        except Exception as e:
            print(f"Error almacenando memoria: {str(e)}")
    return {}


async def memory_injection_node(state: StateBot, runtime: Runtime[Context]):
    namespace = (runtime.context.user_id, "memories")
    last_message = state["messages"][-1].content
    try:
        items = await runtime.store.asearch(
            namespace, query=last_message, limit=5
        )
        memory_context = "\n".join(item.value["data"] for item in items)
        return {"memory_context": memory_context}
    except Exception as e:
        print(f"Error recuperando memorias: {str(e)}")
        return {"memory_context": ""}


async def generate_response(state: StateBot, config: RunnableConfig):
    memory_context = state.get("memory_context")
    chain = get_character_chain()
    response = await chain.ainvoke(
        {
            "messages": state["messages"],
            "memory_context": memory_context,
        },
        config,
    )
    return {"messages": response}
