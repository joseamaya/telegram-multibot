from langgraph.graph import MessagesState


class StateBot(MessagesState):
    memory_context: str