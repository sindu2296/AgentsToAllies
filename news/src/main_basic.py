import asyncio

from config import build_kernel
from plugins.news_plugin import NewsPlugin
from agents.category_agent import build_category_agent
from semantic_kernel.agents import SequentialOrchestration
from semantic_kernel.agents.runtime import InProcessRuntime

async def main():
    # Initialize kernel and add the news plugin
    kernel = build_kernel()
    kernel.add_plugin(NewsPlugin(), plugin_name="news")

    # Create a single category agent (tech news only)
    tech_agent = build_category_agent(kernel, name="tech_news_agent", category="technology")

    # Create a simple pipeline with just one agent
    pipeline = SequentialOrchestration(members=[tech_agent])
    runtime = InProcessRuntime()
    runtime.start()

    try:
        # Simple query for tech news
        query = "What are the latest technology headlines?"
        print("\n=== Simple Tech News Query ===")
        print("Query:", query)
        
        # Process the query through the pipeline
        result = await pipeline.invoke(task=query, runtime=runtime)
        response = ""
        async for msg in result:
            response += msg.content.content
            
        print("\nResults:")
        print(response)

    finally:
        await runtime.stop_when_idle()

if __name__ == "__main__":
    asyncio.run(main())