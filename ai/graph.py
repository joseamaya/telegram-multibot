from langgraph.constants import START, END
from langgraph.graph import StateGraph

from ai.nodes import memory_extraction_node, memory_injection_node, generate_response
from ai.state import StateBot


def create_workflow_graph():
    graph_builder = StateGraph(StateBot)
    graph_builder.add_node("memory_extraction_node", memory_extraction_node)
    graph_builder.add_node("memory_injection_node", memory_injection_node)
    graph_builder.add_node("generate_response", generate_response)
    graph_builder.add_edge(START, "memory_extraction_node")
    graph_builder.add_edge("memory_extraction_node", "memory_injection_node")
    graph_builder.add_edge("memory_injection_node", "generate_response")
    graph_builder.add_edge("generate_response", END)
    return graph_builder