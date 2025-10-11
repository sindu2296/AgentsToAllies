"""
Concurrent news orchestrator using Microsoft Agent Framework.
Processes news categories in parallel for better performance.
"""
import json
import asyncio
from typing import List
from agent_framework.azure import AzureOpenAIChatClient

from agents.router_agent import build_router_agent, route_categories
from agents.category_agent import build_category_agent
from agents.summarizer_agent import build_summarizer_agent
from utils.dedup import dedup_articles

class ConcurrentNewsOrchestrator:
    """
    Orchestrates news fetching concurrently using Microsoft Agent Framework.
    
    Flow:
    1. Router agent determines relevant categories
    2. Category agents fetch news in parallel (concurrent)
    3. Summarizer agent creates an executive brief
    
    This is faster than sequential processing when fetching from multiple categories.
    """
    
    def __init__(self, chat_client: AzureOpenAIChatClient):
        self.chat_client = chat_client
        self.router = build_router_agent(chat_client)

    async def run(self, user_query: str) -> str:
        """Process a user query and return a news summary."""
        
        # Step 1: Determine which categories to fetch
        print(f"\n[ROUTING] Processing query: {user_query}")
        categories = await route_categories(self.router, user_query)
        print(f"[ROUTING] Selected categories: {categories}")
        
        # Step 2: Create category agents for parallel fetching
        category_agents = [
            build_category_agent(self.chat_client, f"{cat}_agent", cat) 
            for cat in categories
        ]
        
        print(f"\n[FETCHING] Fetching from {len(categories)} categories in parallel...")
        
        # Step 3: Fetch from all categories concurrently using asyncio.gather
        async def fetch_category(agent, category):
            try:
                result = await agent.run("Fetch the latest news headlines for your assigned category")
                return result.text, category
            except Exception as e:
                print(f"[ERROR] Failed to fetch {category}: {e}")
                return None, category
        
        fetch_tasks = [
            fetch_category(agent, cat) 
            for agent, cat in zip(category_agents, categories)
        ]
        
        results = await asyncio.gather(*fetch_tasks, return_exceptions=True)
        
        # Step 4: Collect and parse results
        all_articles = []
        for result_tuple in results:
            if isinstance(result_tuple, Exception):
                continue
            
            response, category = result_tuple
            if response is None:
                continue
                
            try:
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
        summarizer = build_summarizer_agent(self.chat_client)
        
        # Pass articles as input data
        articles_json = json.dumps(unique_articles)
        result = await summarizer.run(articles_json)
        summary = result.text
        
        # Step 7: Format final output
        header = f"**Categories analyzed (in parallel):** {', '.join(categories)}"
        return f"{header}\n\n{summary}"
