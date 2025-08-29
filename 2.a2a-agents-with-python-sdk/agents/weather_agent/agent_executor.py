"""
Building the A2A Agent Executor
The WeatherAgentExecutor serves as a crucial bridge between our intelligent weather agent and the A2A protocol. 
It translates between the agent’s responses and the standardized A2A event system.

A2A systems operate on an event-driven architecture rather than simple request-response patterns.
Every interaction flows through an event queue, enabling sophisticated features like real-time streaming and multi-turn conversations:

"""

from a2a.server.events import EventQueue
from a2a.server.agent_execution import RequestContext, AgentExecutor
from a2a.types import TaskArtifactUpdateEvent, TaskStatusUpdateEvent, TaskStatus, TaskState
from a2a.utils import new_task, new_text_artifact, new_agent_text_message


from .agent import WeatherAgent

class WeatherAgentExecutor(AgentExecutor):
    """
    Executor that bridges the A2A server infrastructure with the WeatherAgent.
    Handles task lifecycle management, event queue orchestration, and multi-turn conversation state.
    """
    
    def __init__(self):
        self.agent = WeatherAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Execute weather agent task with streaming updates."""
        query = context.get_user_input()
        task = context.current_task
        
        if not context.message:
            raise Exception('No message provided')
        
         # Create new task for fresh interactions
        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)

        # Stream agent responses and convert to A2A events
        async for event in self.agent.stream(query, task.context_id):
            if event['is_task_complete']:
                # Send final weather result artifact
                await event_queue.enqueue_event(
                    TaskArtifactUpdateEvent(
                        taskId=task.id,
                        contextId=task.context_id,
                        artifact=new_text_artifact(
                            name='weather_report',
                            description='Current weather information for the requested location.',
                            text=event['content'],
                        ),
                        append=False,
                        lastChunk=True,
                    )
                )

                # Mark task as completed
                await event_queue.enqueue_event(
                    TaskStatusUpdateEvent(
                        taskId=task.id,
                        contextId=task.context_id,
                        status=TaskStatus(state=TaskState.completed),
                        final=True,
                    )
                )
            
            elif event['require_user_input']:
                # Request additional input from user (e.g., location)
                await event_queue.enqueue_event(
                    TaskStatusUpdateEvent(
                        taskId=task.id,
                        contextId=task.context_id,
                        status=TaskStatus(
                            state=TaskState.input_required,
                            message=new_agent_text_message(
                                event['content'],
                                task.context_id,
                                task.id
                            ),
                        ),
                        final=True,
                    )
                )
            
            else:
                # Send progress updates
                await event_queue.enqueue_event(
                    TaskStatusUpdateEvent(
                        taskId=task.id,
                        contextId=task.context_id,
                        status=TaskStatus(
                            state=TaskState.working,
                            message=new_agent_text_message(
                                event['content'],
                                task.context_id,
                                task.id
                            ),
                        ),
                        final=False,
                    )
                )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Cancel operation (not supported in this implementation)."""
        raise Exception('Cancel not supported')
    


    """
    
    Every conversation in A2A is organized around tasks. The executor creates new tasks for fresh conversations and manages their lifecycle from creation to completion. 
    Tasks have unique IDs and maintain context across multiple exchanges.

    The executor manages three types of events:

    1. Completion Events: When the agent successfully provides weather information, it creates a TaskArtifactUpdateEvent containing the formatted weather report.
    2. Input Required Events: When the agent needs additional information (like a specific location), it creates a TaskStatusUpdateEvent with an input_required state.
    3. Progress Events: During processing, the agent sends working status events to keep users informed about what's happening.

    
    This separation of concerns makes the system highly maintainable; the weather logic stays in the agent, while the A2A protocol handling stays in the executor.


    """