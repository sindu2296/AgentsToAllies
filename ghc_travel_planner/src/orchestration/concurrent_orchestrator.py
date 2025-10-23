"""
Concurrent orchestrator for GHC Travel Planner using Microsoft Agent Framework.
Processes flight and hotel searches in parallel for faster results.
"""
import sys
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_framework import ConcurrentBuilder
from agent_framework.azure import AzureOpenAIChatClient

from agents.flight_agent import build_flight_agent
from agents.hotel_agent import build_hotel_agent
from agents.summary_agent import build_summary_agent


async def run_concurrent_travel_workflow(
    chat_client: AzureOpenAIChatClient,
    user_query: str
) -> str:
    """
    Run the concurrent GHC travel planning workflow.
    
    Flow: (Flight Agent || Hotel Agent) → Summary Agent
    Flight and hotel searches run in parallel for faster results.
    
    Args:
        chat_client: Azure OpenAI chat client
        user_query: User's travel planning request with dates and preferences
        
    Returns:
        Formatted output showing the complete travel itinerary
    """
    
    print(f"\n{'='*80}")
    print(f"GHC 2025 Travel Planner - Concurrent Workflow")
    print(f"{'='*80}")
    
    # Build the agents
    flight_agent = build_flight_agent(chat_client)
    hotel_agent = build_hotel_agent(chat_client)
    summary_agent = build_summary_agent(chat_client)
    
    print(f"✓ Created 3 agents: (flight_agent || hotel_agent) → summary_agent")
    
    # Store results from parallel execution
    parallel_results = []
    
    async def aggregate_travel_results(results):
        """Aggregator function called after flight and hotel agents complete."""
        print(f"[CONCURRENT] Aggregating results from {len(results)} agents")
        
        collected_info = []
        for result in results:
            # Extract agent name and response
            executor_id = getattr(result, "executor_id", "") or ""
            agent_name = executor_id.replace("_agent", "") if executor_id else "unknown"
            
            # Get the response text
            if hasattr(result, 'agent_run_response') and hasattr(result.agent_run_response, 'text'):
                response_text = result.agent_run_response.text
            elif hasattr(result, 'text'):
                response_text = result.text
            else:
                response_text = str(result)
            
            collected_info.append(f"[{agent_name}] {response_text}")
            parallel_results.append({
                "agent": agent_name,
                "response": response_text
            })
        
        return "\n\n".join(collected_info)
    
    # Build concurrent workflow using ConcurrentBuilder with aggregator
    workflow = (
        ConcurrentBuilder()
        .participants([flight_agent, hotel_agent])
        .with_aggregator(aggregate_travel_results)
        .build()
    )
    
    print(f"✓ Concurrent workflow built successfully")
    print(f"\nProcessing request: {user_query}")
    print(f"⚡ Running flight and hotel searches in parallel...")
    print(f"{'-'*80}\n")
    
    # Run the concurrent workflow
    aggregated_results = await workflow.run(user_query)
    
    print(f"\n[CONCURRENT] Parallel searches complete!")
    print(f"[CONCURRENT] Now calling summary agent to create itinerary...\n")
    
    # Now call summary agent with the aggregated results
    summary_input = f"""Based on the following travel search results, create a comprehensive travel itinerary:

User Request: {user_query}

Search Results:
{aggregated_results}

Please create a complete travel itinerary with flight details, hotel information, and helpful travel tips."""
    
    summary_result = await summary_agent.run(summary_input)
    summary_text = summary_result.text if hasattr(summary_result, 'text') else str(summary_result)
    
    print(f"\n{'='*80}")
    print(f"Travel Planning Completed! (Parallel execution)")
    print(f"{'='*80}\n")
    
    # Format the output
    output_lines = [
        f"\n{'-'*80}",
        f"Step 01 [user]",
        f"{'-'*80}",
        user_query,
        f"\n{'-'*80}",
        f"Step 02 [flight_agent & hotel_agent - PARALLEL]",
        f"{'-'*80}",
        aggregated_results,
        f"\n{'-'*80}",
        f"Step 03 [summary_agent]",
        f"{'-'*80}",
        summary_text,
        f"\n{'='*80}"
    ]
    
    return "\n".join(output_lines)
