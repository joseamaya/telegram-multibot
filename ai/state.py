from dataclasses import dataclass

from langgraph.graph import MessagesState


@dataclass
class Context:
    user_id: str


class StateBot(MessagesState):
    memory_context: str
