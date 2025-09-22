import asyncio

from config import build_kernel
from plugins.news_plugin import NewsPlugin
from agents.router_agent import build_router_agent
from agents.summarizer_agent import build_summarizer_agent
from orchestration.sequential_orchestrator import SequentialNewsOrchestrator

async def main():
    kernel = build_kernel()
    kernel.add_plugin(NewsPlugin(), plugin_name="news")

    # Create the router and summarizer agents
    router = build_router_agent(kernel)
    summarizer = build_summarizer_agent(kernel)

    # Create the orchestrator with routing capability
    orchestrator = SequentialNewsOrchestrator(
        kernel=kernel,
        router=router,
        summarizer=summarizer
    )

    # Example queries that can span multiple categories
    for query in [
        "What's happening in tech and business today?",
        "Show me sports and health news updates",
        "Give me science and tech innovation news"
    ]:
        print("\n=== USER QUERY:", query)
        out = await orchestrator.run(query)
        print("\n=== RESULT:\n", out)

if __name__ == "__main__":
    asyncio.run(main())
