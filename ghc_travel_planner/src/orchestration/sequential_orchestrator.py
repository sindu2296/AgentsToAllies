"""
Sequential orchestrator for GHC Travel Planner using Microsoft Agent Framework.
Processes travel planning through: Flight Search → Hotel Search → Summary
"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_framework import SequentialBuilder, WorkflowOutputEvent, ChatMessage
from agent_framework.azure import AzureOpenAIChatClient

from agents.flight_agent import build_flight_agent
from agents.hotel_agent import build_hotel_agent
from agents.summary_agent import build_summary_agent


async def run_sequential_travel_workflow(
    chat_client: AzureOpenAIChatClient,
    user_query: str
) -> str:
    """
    Run the sequential GHC travel planning workflow.
    
    Flow: Flight Agent → Hotel Agent → Summary Agent
    
    Args:
        chat_client: Azure OpenAI chat client
        user_query: User's travel planning request with dates and preferences
        
    Returns:
        Formatted output showing the complete travel itinerary
    """
    
    print(f"\n{'='*80}")
    print(f"GHC 2025 Travel Planner - Sequential Workflow")
    print(f"{'='*80}")
    
    # Build the three agents
    flight_agent = build_flight_agent(chat_client)
    hotel_agent = build_hotel_agent(chat_client)
    summary_agent = build_summary_agent(chat_client)
    
    print(f"✓ Created 3 agents: flight_agent → hotel_agent → summary_agent")
    
    # Build sequential workflow using SequentialBuilder
    workflow = (
        SequentialBuilder()
        .participants([flight_agent, hotel_agent, summary_agent])
        .build()
    )
    
    print(f"✓ Workflow built successfully")
    print(f"\nProcessing request: {user_query}")
    print(f"{'-'*80}\n")
    
    # Run the workflow and capture all messages
    all_messages = []
    
    async for event in workflow.run_stream(user_query):
        if isinstance(event, WorkflowOutputEvent):
            # WorkflowOutputEvent.data contains a list of messages
            if isinstance(event.data, list):
                all_messages.extend(event.data)
            else:
                all_messages.append(event.data)
    
    if not all_messages:
        return "❌ Workflow did not produce any output."
    
    print(f"\n{'='*80}")
    print(f"Travel Planning Completed!")
    print(f"{'='*80}")
    print(f"Total messages in workflow: {len(all_messages)}\n")
    
    # Format the output showing the complete conversation
    output_lines = []
    
    for i, msg in enumerate(all_messages, start=1):
        author = msg.author_name or "user"
        role_label = f"[{author}]"
        
        output_lines.append(f"\n{'-'*80}")
        output_lines.append(f"Step {i:02d} {role_label}")
        output_lines.append(f"{'-'*80}")
        output_lines.append(msg.text)
    
    output_lines.append(f"\n{'='*80}")
    
    return "\n".join(output_lines)
