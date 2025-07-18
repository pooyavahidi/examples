from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message


class SimpleAgentExecutor(AgentExecutor):
    """Simple Agent Executor for text input/output agents."""

    def __init__(self, agent):
        self.agent = agent

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        user_text = context.get_user_input()
        print(f"Received user input: {user_text}")

        # Invoke the agent with the user input
        result = await self.agent.invoke(user_text)

        # Enqueue the result as a message
        await event_queue.enqueue_event(
            new_agent_text_message(
                result,
                context_id=context.context_id,
                task_id=context.task_id,
            )
        )

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise NotImplementedError("Cancel not supported in this executor")
