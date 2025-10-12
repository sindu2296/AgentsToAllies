import asyncio

from config import build_kernel
from plugins.news_plugin import NewsPlugin
from orchestration.concurrent_orchestrator import ConcurrentNewsOrchestrator

async def main():
    """
    Concurrent News Orchestrator Demo
    
    This demonstrates processing news categories in parallel for better performance.
    Good for: fast, efficient processing when dealing with multiple categories
    """
    kernel = build_kernel()
    kernel.add_plugin(NewsPlugin(), plugin_name="news")

    orchestrator = ConcurrentNewsOrchestrator(kernel)

    queries = [
        "Round up AI chip and cloud infra news",
        "What happened in sports and health this morning?",
        "Give me business and tech headlines about big tech",
    ]

    try:
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
    finally:
        await orchestrator.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
