import json
import asyncio
from typing import List
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent, SequentialOrchestration
from semantic_kernel.agents.runtime import InProcessRuntime

from agents.router_agent import build_router_agent, route_categories
from agents.category_agent import build_category_agent
from agents.summarizer_agent import build_summarizer_agent
from utils.dedup import dedup_articles

class SequentialNewsOrchestrator:
    """
    Orchestrates news fetching sequentially using SequentialOrchestration.
    
    Flow:
    1. Router agent determines relevant categories
    2. Category agents fetch news one-by-one using SequentialOrchestration
    3. Summarizer agent creates an executive brief
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
        
        # Step 2: Fetch news from each category sequentially using SequentialOrchestration
        all_articles = []
        for category in categories:
            print(f"\n[FETCHING] Category: {category}")
            
            # Create a category agent for this category
            category_agent = build_category_agent(self.kernel, f"{category}_agent", category)
            
            # Create a sequential pipeline with just this agent
            pipeline = SequentialOrchestration(members=[category_agent])
            
            # Invoke the pipeline
            orchestration_result = await pipeline.invoke(
                task="Fetch the latest news headlines for your assigned category",
                runtime=self.runtime
            )
            
            # Get the result from OrchestrationResult
            results = await orchestration_result.get()
            
            # Extract response content
            response = ""
            if results:
                # Results should be a list, get the first (and only) result
                result = results[0] if isinstance(results, list) else results
                response = result.content if hasattr(result, 'content') else str(result)
            
            # Parse the JSON response
            try:
                articles = json.loads(response)
                if isinstance(articles, list):
                    all_articles.extend(articles)
                    print(f"[SUCCESS] Found {len(articles)} articles")
            except json.JSONDecodeError:
                print(f"[ERROR] Failed to parse response for {category}")
        
        # Step 3: Deduplicate articles
        unique_articles = dedup_articles(all_articles)
        
        if not unique_articles:
            return "No articles found."
        
        print(f"\n[DEDUP] {len(unique_articles)} unique articles after deduplication")
        
        # Step 4: Summarize using the summarizer agent with SequentialOrchestration
        print(f"[SUMMARIZING] Creating executive brief...")
        summarizer = build_summarizer_agent(self.kernel)
        
        # Create a sequential pipeline with the summarizer
        summary_pipeline = SequentialOrchestration(members=[summarizer])
        
        # Pass articles as input data
        articles_json = json.dumps(unique_articles)
        orchestration_result = await summary_pipeline.invoke(task=articles_json, runtime=self.runtime)
        
        # Get the result from OrchestrationResult
        results = await orchestration_result.get()
        
        # Extract summary content
        summary = ""
        if results:
            result = results[0] if isinstance(results, list) else results
            summary = result.content if hasattr(result, 'content') else str(result)
        
        # Step 5: Format final output
        header = f"**Categories analyzed:** {', '.join(categories)}"
        return f"{header}\n\n{summary}"

    async def cleanup(self):
        """Clean up runtime resources."""
        await self.runtime.stop_when_idle()
