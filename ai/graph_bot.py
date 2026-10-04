from langchain_core.messages import HumanMessage

from ai.graph import create_workflow_graph
from ai.state import Context


class GraphBot:

    def __init__(self, store, checkpointer):
        self.graph = create_workflow_graph().compile(
            checkpointer=checkpointer,
            store=store,
        )

    async def reply(self, chat_id, user_id, text=None):
        config = {"configurable": {"thread_id": str(chat_id)}}
        await self.graph.ainvoke(
            {"messages": [HumanMessage(content=text)]},
            config,
            context=Context(user_id=str(user_id)),
        )
        output_state = await self.graph.aget_state(config=config)
        return output_state.values["messages"][-1].content
