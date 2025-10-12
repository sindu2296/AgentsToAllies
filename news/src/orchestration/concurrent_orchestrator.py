import json
import asyncio
from typing import List
from semantic_kernel import Kernel
from semantic_kernel.agents import ConcurrentOrchestration, ChatCompletionAgent
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.contents import ChatMessageContent

from agents.router_agent import build_router_agent, route_categories
from agents.category_agent import build_category_agent
from agents.summarizer_agent import build_summarizer_agent
from utils.dedup import dedup_articles

class ConcurrentNewsOrchestrator:
    """
    Orchestrates news fetching concurrently using Semantic Kernel's ConcurrentOrchestration.
    
    Flow:
    1. Router agent determines relevant categories
    2. Category agents fetch news in parallel (concurrent)
    3. Summarizer agent creates an executive brief
    
    This is faster than sequential processing when fetching from multiple categories.
    """
    
    def __init__(self, kernel: Kernel):
        self.kernel = kernel
        self.router = build_router_agent(kernel)
        self.runtime = InProcessRuntime()
        self.runtime.start()

    async def run(self, user_query: str) -> str:
        """Process a user query and return a news summary."""
        
        # Step 1: Determine which categories to fetch
        print(f"\n[ROUTING] Processing query: {user_query}")
        categories = await route_categories(self.router, user_query)
        print(f"[ROUTING] Selected categories: {categories}")
        
        # Step 2: Create category agents for parallel fetching
        category_agents = [
            build_category_agent(self.kernel, f"{cat}_agent", cat) 
            for cat in categories
        ]
        
        print(f"\n[FETCHING] Fetching from {len(categories)} categories in parallel...")
        
        # Step 3: Use ConcurrentOrchestration to fetch from all categories at once
        concurrent_orch = ConcurrentOrchestration(members=category_agents)
        
        # Invoke all agents with a meaningful task - each agent already knows its category
        orchestration_result = await concurrent_orch.invoke(
            task="Fetch the latest news headlines for your assigned category",
            runtime=self.runtime
        )
        
        # Step 4: Collect and parse results
        all_articles = []
        results = await orchestration_result.get()
        
        for i, result in enumerate(results):
            category = categories[i]
            try:
                response = result.content if hasattr(result, 'content') else str(result)
                articles = json.loads(response)
                if isinstance(articles, list):
                    all_articles.extend(articles)
                    print(f"[SUCCESS] {category}: {len(articles)} articles")
            except json.JSONDecodeError:
                print(f"[ERROR] Failed to parse response for {category}")
        
        # Step 5: Deduplicate articles
        unique_articles = dedup_articles(all_articles)
        
        if not unique_articles:
            return "No articles found."
        
        print(f"\n[DEDUP] {len(unique_articles)} unique articles after deduplication")
        
        # Step 6: Summarize using the summarizer agent
        print(f"[SUMMARIZING] Creating executive brief...")
        summarizer = build_summarizer_agent(self.kernel)
        
        # Pass articles as input data (not instructions)
        articles_json = json.dumps(unique_articles)
        summary = ""
        async for msg in summarizer.invoke(messages=articles_json):
            summary += msg.content.content
        
        # Step 7: Format final output
        header = f"**Categories analyzed (in parallel):** {', '.join(categories)}"
        return f"{header}\n\n{summary}"

    async def cleanup(self):
        """Clean up runtime resources."""
        await self.runtime.stop_when_idle()

