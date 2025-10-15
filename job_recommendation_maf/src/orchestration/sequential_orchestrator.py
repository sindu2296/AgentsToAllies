"""
Sequential job recommendation orchestrator using Microsoft Agent Framework.
Uses SequentialBuilder to create a pipeline of agents.
"""
from agent_framework import SequentialBuilder, WorkflowOutputEvent, ChatMessage
from agent_framework.azure import AzureOpenAIChatClient

from agents.job_extractor_agent import build_job_extractor_agent
from agents.job_recommender_agent import build_job_recommender_agent
from agents.job_summary_agent import build_job_summary_agent


async def run_sequential_job_workflow(chat_client: AzureOpenAIChatClient, user_profile: str) -> str:
    """
    Run the sequential job recommendation workflow.
    
    Flow: Job Extractor -> Job Recommender -> Job Summarizer
    
    Args:
        chat_client: Azure OpenAI chat client
        user_profile: User's skills, experience, and job preferences
        
    Returns:
        Formatted output showing the complete conversation flow
    """
    
    print(f"\n{'='*80}")
    print(f"Building Sequential Workflow")
    print(f"{'='*80}")
    
    # Build the three agents
    extractor = build_job_extractor_agent(chat_client)
    recommender = build_job_recommender_agent(chat_client)
    summarizer = build_job_summary_agent(chat_client)
    
    print(f"✓ Created 3 agents: extractor -> recommender -> summarizer")
    
    # Build sequential workflow using SequentialBuilder
    workflow = (
        SequentialBuilder()
        .participants([extractor, recommender, summarizer])
        .build()
    )
    
    print(f"✓ Workflow built successfully")
    print(f"\nRunning workflow for profile: {user_profile}")
    print(f"{'-'*80}\n")
    
    # Run the workflow and capture all messages
    all_messages = []
    
    async for event in workflow.run_stream(
        f"Search for jobs matching this user profile: {user_profile}"
    ):
        if isinstance(event, WorkflowOutputEvent):
            # WorkflowOutputEvent.data contains a list of messages
            if isinstance(event.data, list):
                all_messages.extend(event.data)
            else:
                all_messages.append(event.data)
    
    if not all_messages:
        return "❌ Workflow did not produce any output."
    
    print(f"\n{'='*80}")
    print(f"Workflow Completed Successfully!")
    print(f"{'='*80}")
    print(f"Total messages captured: {len(all_messages)}\n")
    
    # Format the output showing the complete conversation
    output_lines = []
    
    for i, msg in enumerate(all_messages, start=1):
        author = msg.author_name or "user"
        role_label = f"[{author}]"
        
        output_lines.append(f"\n{'-'*80}")
        output_lines.append(f"Message {i} {role_label}")
        output_lines.append(f"{'-'*80}")
        output_lines.append(msg.text)
    
    output_lines.append(f"\n{'='*80}")
    
    return "\n".join(output_lines)
