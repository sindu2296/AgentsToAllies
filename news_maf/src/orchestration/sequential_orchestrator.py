"""
Sequential news orchestrator using Microsoft Agent Framework.
Processes news categories one-by-one in sequence.
"""
import json
import asyncio
from typing import List
from agent_framework.azure import AzureOpenAIChatClient

from agents.router_agent import build_router_agent, route_categories
from agents.category_agent import build_category_agent
from agents.summarizer_agent import build_summarizer_agent
from utils.dedup import dedup_articles

class SequentialNewsOrchestrator:
    """
    Orchestrates news fetching sequentially using Microsoft Agent Framework.
    
    Flow:
    1. Router agent determines relevant categories
    2. Category agents fetch news one-by-one (sequential processing)
    3. Summarizer agent creates an executive brief
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
        
        # Step 2: Fetch news from each category sequentially
        all_articles = []
        for category in categories:
            print(f"\n[FETCHING] Category: {category}")
            
            # Create a category agent for this category
            category_agent = build_category_agent(self.chat_client, f"{category}_agent", category)
            
            # Invoke the agent
            result = await category_agent.run("Fetch the latest news headlines for your assigned category")
            response = result.text
            
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
        
        # Step 4: Summarize using the summarizer agent
        print(f"[SUMMARIZING] Creating executive brief...")
        summarizer = build_summarizer_agent(self.chat_client)
        
        # Pass articles as input data
        articles_json = json.dumps(unique_articles)
        result = await summarizer.run(articles_json)
        summary = result.text
        
        # Step 5: Format final output
        header = f"**Categories analyzed:** {', '.join(categories)}"
        return f"{header}\n\n{summary}"
