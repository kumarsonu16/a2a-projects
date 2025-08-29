"""
Building the A2A Weather Client
Finally, we need a client that can communicate with our weather agent. 
This client will handle the A2A protocol, manage streaming responses, and provide a clean interface for users to get weather information.
"""

#!/usr/bin/env python3

import asyncio
from uuid import uuid4

import click
import httpx
from rich.console import Console

from a2a.client import A2ACardResolver, ClientFactory, ClientConfig
from a2a.types import Message, TextPart, Part, Role, TaskState

console = Console()

def build_message(text: str, task_id: str | None = None, context_id: str | None = None) -> Message:
    """Build message payload for A2A communication."""
    return Message(
        kind="message",
        role=Role.user,
        parts=[Part(root=TextPart(kind="text", text=text))],
        message_id=uuid4().hex,
        task_id=task_id,
        context_id=context_id,
    )

def extract_text_content(update) -> str | None:
    """Extract text content from streaming updates."""
    try:
        if isinstance(update, tuple) and len(update) >= 2:
            task, _ = update
            if hasattr(task, 'artifacts') and task.artifacts:
                for artifact in task.artifacts:
                    if hasattr(artifact, 'parts') and artifact.parts:
                        for part in artifact.parts:
                            if hasattr(part, 'root') and hasattr(part.root, 'text'):
                                return part.root.text
        return None
    except:
        return None

# The client’s conversation handling showcases A2A’s support for complex interactions
async def handle_conversation(client, text: str, task_id: str | None = None, context_id: str | None = None):
    """Handle streaming conversation with the weather agent."""
    message = build_message(text, task_id, context_id)
    
    latest_task_id = None
    latest_context_id = None
    
    console.print(f"[cyan]Processing: {text}[/cyan]")
    
        
    try:
        async for update in client.send_message(message):
            # Extract task info for continuation
            if isinstance(update, tuple):
                task, _ = update
                if task:
                    if hasattr(task, "context_id"):
                        latest_context_id = task.context_id
                    if hasattr(task, "id"):
                        latest_task_id = task.id
                        
                    # Handle task states
                    if hasattr(task, "status") and hasattr(task.status, "state"):
                        if task.status.state == TaskState.completed:
                            # Show final weather report
                            content = extract_text_content(update)
                            if content:
                                console.print(f"\n[green]{content}[/green]")
                            return
                        elif task.status.state == TaskState.input_required:
                            # Show agent's request for more info
                            if hasattr(task.status, "message") and hasattr(task.status.message, "parts"):
                                for part in task.status.message.parts:
                                    if hasattr(part, 'root') and hasattr(part.root, 'text'):
                                        console.print(f"\n[yellow]{part.root.text}[/yellow]")
                            
                            # Get user input and continue conversation
                            follow_up = console.input("\n[bold cyan]Your reply: [/bold cyan]")
                            await handle_conversation(client, follow_up, latest_task_id, latest_context_id)
                            return
    except asyncio.CancelledError:
        # Handle graceful shutdown
        pass
    except Exception as e:
        console.print(f"[red]Stream error: {e}[/red]")
    

async def check_streaming_support(agent_url: str) -> bool:
    """Check if the agent supports streaming."""
    try:
        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(f"{agent_url}/.well-known/agent-card.json")
            if response.status_code == 200:
                agent_info = response.json()
                return agent_info.get("capabilities", {}).get("streaming", False)
    except:
        pass
    return False

# The client starts by discovering the agent’s capabilities
async def main_async(agent_url: str):
    """Main async function for client interaction."""
    console.print(f"[green]Connecting to weather agent...[/green]")


    # Check capabilities
    supports_streaming = await check_streaming_support(agent_url)
    console.print(f"[green]Connected! Streaming: {supports_streaming}[/green]")

    async with httpx.AsyncClient() as http_client:
    
        try:
            # Initialize client
            card_resolver = A2ACardResolver(http_client, agent_url)
            agent_card = await card_resolver.get_agent_card()
            
            config = ClientConfig(httpx_client=http_client)
            factory = ClientFactory(config)
            client = factory.create(agent_card)
            
            console.print("\n[bold blue]Weather Agent Ready![/bold blue]")
            console.print("[dim]Ask about weather anywhere in the world. Type 'exit' to quit.[/dim]\n")

            try:
                while True:
                    try:
                        user_input = console.input("[bold green]Weather query: [/bold green]")
                        
                        if user_input.lower().strip() in ['exit', 'quit', 'q']:
                            console.print("\n[yellow]Goodbye![/yellow]")
                            break
                        
                        if not user_input.strip():
                            console.print("[yellow]Please enter a weather query.[/yellow]")
                            continue
                        
                        await handle_conversation(client, user_input)
                        console.print()  # Add spacing
                            
                    except KeyboardInterrupt:
                        console.print("\n[yellow]Goodbye![/yellow]")
                        break
                    except Exception as e:
                        console.print(f"[red]Error: {e}[/red]")
            finally:
                # Give time for async generators to cleanup
                await asyncio.sleep(0.1)
                        
        except Exception as e:
            console.print(f"[red]Failed to initialize client: {e}[/red]")
            console.print("Please make sure the agent server is running.")


@click.command()
@click.option('--agent-url', required=True, help='URL of the A2A weather agent')
def main(agent_url: str):
    """A2A Client for weather information."""
    try:
        asyncio.run(main_async(agent_url))
    except KeyboardInterrupt:
        # Suppress the traceback for clean exit
        console.print("\n[yellow]Client terminated[/yellow]")
    except Exception as e:
        console.print(f"[red]Client error: {e}[/red]")
    finally:
        # Suppress asyncio cleanup warnings
        import warnings
        warnings.filterwarnings("ignore", message=".*was never awaited.*")
        warnings.filterwarnings("ignore", message=".*aclose.*")

if __name__ == "__main__":
    main()

            
"""
Understanding A2A Streaming Task Updates
When you interact with the WeatherAgent, the communication happens through a series of streaming updates. 
Let’s break down what happens during a typical interaction.

Weather Agent Interaction Flow
1. Task Submission: The client sends a weather query, and the agent responds with a “submitted” status
2. Search Phase: The agent provides updates like “Searching for current weather in New York…”
3. Processing Phase: Status messages show “Processing weather data and formatting response…”
4. Artifact Delivery: The final weather report is delivered as a rich, formatted text artifact
5. Task Completion: A final status update marks the task as completed

Each update contains crucial information:

1. JSON-RPC ID: Unique identifier for the request
2. Context ID: Groups all messages in a conversation
3. Task ID: Unique identifier for the specific task
4. Status/State: Current state of the task (submitted, working, completed)
"""