"""
Concurrent News Orchestrator Demo - Microsoft Agent Framework

This demonstrates processing news categories in parallel using MAF.
Good for: fast, efficient processing when dealing with multiple categories
"""
import asyncio
from config import build_chat_client
from orchestration.concurrent_orchestrator import ConcurrentNewsOrchestrator

async def main():
    """
    Concurrent News Orchestrator Demo using Microsoft Agent Framework
    
    This demonstrates processing news categories in parallel for better performance.
    """
    chat_client = build_chat_client()

    orchestrator = ConcurrentNewsOrchestrator(chat_client=chat_client)

    queries = [
        "Round up AI chip and cloud infra news",
        # "What happened in sports and health this morning?",
        # "Give me business and tech headlines about big tech",
    ]

    for query in queries:
        print("\n" + "="*70)
        print(f"USER QUERY: {query}")
        print("="*70)
        
        result = await orchestrator.run(query)
        
        print("\n" + "-"*70)
        print("RESULT:")
        print("-"*70)
        print(result)
        print("="*70 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
