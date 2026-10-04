from langgraph.graph import END, START, StateGraph

from ai.nodes import generate_response, memory_extraction_node, memory_injection_node
from ai.state import Context, StateBot


def create_workflow_graph():
    graph = StateGraph(StateBot, context_schema=Context)
    graph.add_node("memory_extraction_node", memory_extraction_node)
    graph.add_node("memory_injection_node", memory_injection_node)
    graph.add_node("generate_response", generate_response)
    graph.add_edge(START, "memory_extraction_node")
    graph.add_edge("memory_extraction_node", "memory_injection_node")
    graph.add_edge("memory_injection_node", "generate_response")
    graph.add_edge("generate_response", END)
    return graph
