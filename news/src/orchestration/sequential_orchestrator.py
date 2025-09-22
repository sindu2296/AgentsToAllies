import json
from dataclasses import dataclass
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel import Kernel
from typing import List, Dict, Any

from agents.router_agent import route_categories
from agents.category_agent import build_category_agent
from utils.dedup import dedup_articles

@dataclass
class SequentialNewsOrchestrator:
    kernel: Kernel
    router: ChatCompletionAgent
    summarizer: ChatCompletionAgent

    async def _fetch_from_category(self, category: str) -> List[Dict[str, Any]]:
        # Build a category agent for this specific category
        agent = build_category_agent(self.kernel, f"{category}_agent", category)
        
        # Fetch news for this category
        prompt = f"Fetch JSON news for category='{category}'. If needed, call the tool."
        response = ""
        async for msg in agent.invoke(prompt):
            response += msg.content.content
        
        try:
            data = json.loads(response)
            return data if isinstance(data, list) else []
        except Exception:
            return []

    async def run(self, user_query: str) -> str:
        # Route the query to determine relevant categories
        categories = await route_categories(self.router, user_query)
        print(f"\nProcessing categories: {categories}")
        
        # Process each category sequentially
        all_articles = []
        for category in categories:
            print(f"\nFetching news for category: {category}")
            articles = await self._fetch_from_category(category)
            all_articles.extend(articles)
        
        # Deduplicate articles
        unique_articles = dedup_articles(all_articles)
        
        if not unique_articles:
            return "No articles found."
            
        # Summarize the results
        payload = json.dumps(unique_articles)
        summary = ""
        async for msg in self.summarizer.invoke(
            f"Summarize these articles with inline sources (JSON provided):\n{payload}"
        ):
            summary += msg.content.content
            
        return f"Selected categories: {', '.join(categories)}\n\n{summary}"
