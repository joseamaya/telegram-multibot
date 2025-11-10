from functools import partial
from typing import Any

from langchain_core.runnables import RunnableConfig
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from ai.nodes import memory_extraction_node, memory_injection_node, generate_response
from ai.retrievers import get_retriever_mongodb
from ai.state import StateBot


async def memory_extraction_handler(state: StateBot, config: RunnableConfig, retriever: Any):
    return await memory_extraction_node(state, retriever, config)

async def memory_injection_handler(state: StateBot, config: RunnableConfig, retriever: Any):
    return await memory_injection_node(state, retriever, config)


def create_workflow_graph(memories_retriever=None):
    graph_builder = StateGraph(StateBot)
    if memories_retriever is None:
        memories_retriever = get_retriever_mongodb(
            k=5, collection_name="memories", index_name="memories-vector-index", filters=["chat_id"]
        )
    graph_builder.add_node("memory_extraction_node", partial(memory_extraction_handler, retriever=memories_retriever))
    graph_builder.add_node("memory_injection_node", partial(memory_injection_handler, retriever=memories_retriever))
    graph_builder.add_node("generate_response", generate_response)
    graph_builder.add_edge(START, "memory_extraction_node")
    graph_builder.add_edge("memory_extraction_node", "memory_injection_node")
    graph_builder.add_edge("memory_injection_node", "generate_response")
    graph_builder.add_edge("generate_response", END)
    return graph_builder