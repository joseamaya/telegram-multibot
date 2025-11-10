from langchain_core.messages import HumanMessage
from langgraph.checkpoint.mongodb import AsyncMongoDBSaver

from ai.graph import create_workflow_graph
from config.settings import get_settings

settings = get_settings()


class GraphBot:

    def __init__(self):
        self.graph_builder = create_workflow_graph()

    async def reply(self, chat_id, text=None):
        config = {"configurable": {"thread_id": str(chat_id), "chat_id": str(chat_id)}}
        async with AsyncMongoDBSaver.from_conn_string(
            settings.MONGO_DB_URL,
            db_name=settings.MONGO_DB_NAME
        ) as checkpointer:
            graph = self.graph_builder.compile(checkpointer=checkpointer)
            await graph.ainvoke({"messages": [HumanMessage(content=text)]}, config)
            output_state = await graph.aget_state(config=config)
        response_message = output_state.values["messages"][-1].content
        return response_message
