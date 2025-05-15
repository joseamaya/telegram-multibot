from langgraph.graph import MessagesState


class StateBot(MessagesState):
    answer: str
    memory_context: str
    summary: str