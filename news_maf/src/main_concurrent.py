"""
Concurrent News Orchestrator Demo - Microsoft Agent Framework

This demonstrates processing news categories in parallel using MAF's ConcurrentBuilder workflow.

BEGINNER TIP: Uncomment the logging setup below to see detailed execution flow!
"""
import asyncio
import logging

from config import build_chat_client
from orchestration.concurrent_orchestrator import ConcurrentNewsOrchestrator

# ============================================================================
# LOGGING SETUP - Uncomment to see detailed execution flow
# ============================================================================
# This shows you what's happening at each step: routing, fetching, summarizing
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s',
    force=True
)
# ============================================================================


async def main():
    """
    Concurrent News Orchestrator Demo using Microsoft Agent Framework Workflows.
    
    This demonstrates:
    1. ConcurrentBuilder workflow for parallel agent execution
    2. Structured logging for debugging
    3. Modular code organization
    
    To see detailed logs, uncomment the logging setup above!
    """
    print("\n" + "="*80)
    print("CONCURRENT NEWS ORCHESTRATOR DEMO (MAF Workflows)")
    print("="*80)
    print("\nTIP: Enable logging (see top of file) to see workflow execution details!\n")
    
    chat_client = build_chat_client()
    orchestrator = ConcurrentNewsOrchestrator(chat_client=chat_client)

    queries = [
        "Round up AI chip and cloud infra news",
        "What happened in sports and health this morning?",
        "Give me business and tech headlines about big tech",
    ]

    for i, query in enumerate(queries, 1):
        print(f"\n{'='*80}")
        print(f"QUERY {i}/{len(queries)}: {query}")
        print(f"{'='*80}\n")
        
        result = await orchestrator.run(query)
        
        print(f"\n{'-'*80}")
        print("RESULT:")
        print(f"{'-'*80}")
        print(result)
        print(f"{'='*80}\n")


if __name__ == "__main__":
    asyncio.run(main())
