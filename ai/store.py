from typing import Dict
from langgraph.store.memory import InMemoryStore

_store: Dict[str, InMemoryStore] = {}

def get_store() -> InMemoryStore:
    if "store" not in _store:
        _store["store"] = InMemoryStore()
    return _store["store"]