import os

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from ai.graph import create_workflow_graph


class GraphBot:

    def __init__(self, store):
        self.store = store
        self.graph_builder = create_workflow_graph()

    async def reply(self, chat_id, text=None):
        config = {"configurable": {"thread_id": str(chat_id), "chat_id": str(chat_id)}}
        DB_URI = os.environ.get('DB_URI')
        async with AsyncPostgresSaver.from_conn_string(DB_URI) as short_term_memory:
            await short_term_memory.setup()
            graph = self.graph_builder.compile(checkpointer=short_term_memory, store=self.store)
            response = await graph.ainvoke({"messages": [HumanMessage(content=text)]}, config)
        return response
