"""
Sequential News Orchestrator Demo - Microsoft Agent Framework

This demonstrates processing news categories one-by-one in sequence.

BEGINNER TIP: Uncomment the logging setup below to see detailed execution flow!
This is great for learning as you can see each step happen in order.
"""
import asyncio
import logging

from config import build_chat_client
from orchestration.sequential_orchestrator import SequentialNewsOrchestrator

# ============================================================================
# LOGGING SETUP - Uncomment to see detailed execution flow
# ============================================================================
# This shows you what's happening at each step: routing, fetching, summarizing
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# ============================================================================


async def main():
    """
    Sequential News Orchestrator Demo using Microsoft Agent Framework.
    
    This demonstrates:
    1. Simple sequential processing (one category at a time)
    2. Structured logging for debugging
    3. Modular code organization
    
    Good for: Learning the basics, debugging, rate-limit sensitive scenarios
    To see detailed logs, uncomment the logging setup above!
    """
    print("\n" + "="*80)
    print("SEQUENTIAL NEWS ORCHESTRATOR DEMO (MAF)")
    print("="*80)
    print("\nTIP: Enable logging (see top of file) to see execution details!\n")
    
    chat_client = build_chat_client()
    orchestrator = SequentialNewsOrchestrator(chat_client=chat_client)

    queries = [
        "What's happening in tech and business today?",
        "Show me sports and health news updates",
        "Give me science and tech innovation news"
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
