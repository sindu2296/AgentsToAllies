"""
Sequential News Orchestrator Demo - Microsoft Agent Framework

This demonstrates processing news categories one-by-one in sequence using MAF.
Good for: predictable, ordered processing
"""
import asyncio
from config import build_chat_client
from orchestration.sequential_orchestrator import SequentialNewsOrchestrator

async def main():
    """
    Sequential News Orchestrator Demo using Microsoft Agent Framework
    
    This demonstrates processing news categories one-by-one in sequence.
    """
    chat_client = build_chat_client()

    # Create the orchestrator
    orchestrator = SequentialNewsOrchestrator(chat_client=chat_client)

    # Example queries that span multiple categories
    queries = [
        "What's happening in tech and business today?",
        "Show me sports and health news updates",
        "Give me science and tech innovation news"
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
