import asyncio

from config import build_kernel
from plugins.news_plugin import NewsPlugin
from orchestration.pro_orchestrator import ProNewsOrchestrator

async def main():
    # Set up logging
    import logging
    logging.basicConfig(level=logging.INFO, 
                       format='%(asctime)s - %(levelname)s - %(message)s',
                       force=True)
    
    print("\n=== Starting News Processing ===\n")
    kernel = build_kernel()
    kernel.add_plugin(NewsPlugin(), plugin_name="news")

    orch = ProNewsOrchestrator(kernel)

    for query in [
        "Round up AI chip and cloud infra news",
        "What happened in sports and health this morning?",
        "Give me business and tech headlines about big tech",
    ]:
        print("\n" + "="*50)
        print("=== USER QUERY:", query)
        print("="*50 + "\n")
        
        out = await orch.run(query)
        
        print("\n" + "-"*50)
        print("=== FINAL RESULT:")
        print("-"*50)
        print(out)
        print("="*50 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
