"""
Sequential news orchestrator using Microsoft Agent Framework.

This module demonstrates a simple sequential processing pattern where each
category agent is invoked one-by-one. This is easier to understand for beginners
and useful when parallelism isn't needed or rate limits are a concern.

Key concepts for beginners:
- Sequential processing: One agent at a time, in order
- Explicit control flow: Easy to follow and debug
- Simple error handling: Can handle failures per category
"""
import json
import logging
from typing import Any

from agent_framework.azure import AzureOpenAIChatClient

from agents.router_agent import build_router_agent, route_categories
from agents.category_agent import build_category_agent
from agents.summarizer_agent import build_summarizer_agent
from utils.dedup import dedup_articles

# Set up logging for better traceability
logger = logging.getLogger(__name__)


class SequentialNewsOrchestrator:
    """
    Orchestrates news fetching sequentially (one category at a time).
    
    Processing Steps:
    1. Router agent determines relevant categories
    2. Category agents fetch news one-by-one
    3. Articles are deduplicated
    4. Summarizer agent creates an executive brief
    
    This approach is simpler than concurrent workflows and easier to debug,
    making it ideal for learning and for scenarios where rate limits matter.
    """
    
    def __init__(self, chat_client: AzureOpenAIChatClient):
        """Initialize orchestrator with Azure OpenAI chat client."""
        self.chat_client = chat_client
        self.router = build_router_agent(chat_client)
        logger.info("Sequential orchestrator initialized")

    async def run(self, user_query: str) -> str:
        """
        Process a user query and return a news summary.
        
        Args:
            user_query: Natural language query from the user
            
        Returns:
            Formatted news summary with category header
        """
        # Step 1: Route query to categories
        categories = await self._route_query(user_query)
        if not categories:
            logger.warning("No categories selected for query")
            return "No categories selected."
        
        # Step 2: Fetch articles sequentially
        all_articles = await self._fetch_articles_sequentially(categories)
        
        # Step 3: Deduplicate
        unique_articles = dedup_articles(all_articles)
        if not unique_articles:
            logger.warning("No articles found after deduplication")
            return "No articles found."
        
        logger.info(f"[DEDUP] {len(unique_articles)} unique articles after deduplication")
        
        # Step 4: Summarize
        summary_text = await self._create_summary(unique_articles)
        
        # Step 5: Format output
        header = f"**Categories analyzed:** {', '.join(categories)}"
        return f"{header}\n\n{summary_text}"

    async def _route_query(self, user_query: str) -> list[str]:
        """
        Use router agent to determine which news categories to fetch.
        
        Args:
            user_query: User's natural language query
            
        Returns:
            List of category names (e.g., ['technology', 'business'])
        """
        logger.info(f"[ROUTING] Processing query: {user_query}")
        categories = await route_categories(self.router, user_query)
        logger.info(f"[ROUTING] Selected categories: {categories}")
        return categories

    async def _fetch_articles_sequentially(self, categories: list[str]) -> list[dict[str, Any]]:
        """
        Fetch articles from each category one-by-one.
        
        Args:
            categories: List of category names
            
        Returns:
            List of all articles from all categories
        """
        all_articles = []
        
        for category in categories:
            logger.info(f"[FETCHING] Category: {category}")
            
            # Create agent for this specific category
            category_agent = build_category_agent(
                self.chat_client,
                f"{category}_agent",
                category
            )
            
            # Fetch articles for this category
            articles = await self._fetch_category_articles(category_agent, category)
            all_articles.extend(articles)
        
        return all_articles

    async def _fetch_category_articles(
        self,
        category_agent: Any,
        category: str
    ) -> list[dict[str, Any]]:
        """
        Fetch articles from a single category agent.
        
        Args:
            category_agent: The ChatAgent for this category
            category: Category name for logging
            
        Returns:
            List of article dictionaries
        """
        try:
            # Invoke the agent
            result = await category_agent.run(
                "Fetch the latest news headlines for your assigned category"
            )
            response_text = result.text
            
            # Parse response
            return self._parse_article_response(response_text, category)
            
        except Exception as exc:
            logger.error(f"[{category.upper()}] Failed to fetch: {exc}")
            return []

    def _parse_article_response(self, response_text: str, category: str) -> list[dict[str, Any]]:
        """
        Parse JSON article response from category agent.
        
        Args:
            response_text: JSON string from agent
            category: Category name for logging
            
        Returns:
            List of article dictionaries
        """
        try:
            articles = json.loads(response_text)
        except json.JSONDecodeError:
            logger.error(f"[{category.upper()}] Failed to parse JSON response")
            return []
        
        # Validate response is a list
        if not isinstance(articles, list):
            logger.warning(f"[{category.upper()}] Unexpected response type: {type(articles).__name__}")
            return []
        
        # Add category metadata
        for article in articles:
            if isinstance(article, dict):
                article.setdefault("category", category)
        
        logger.info(f"[{category.upper()}] Successfully fetched {len(articles)} articles")
        return articles

    async def _create_summary(self, articles: list[dict[str, Any]]) -> str:
        """
        Create executive summary from articles using summarizer agent.
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            Summary text
        """
        logger.info(f"[SUMMARIZING] Creating executive brief from {len(articles)} articles")
        
        summarizer = build_summarizer_agent(self.chat_client)
        articles_json = json.dumps(articles)
        
        try:
            result = await summarizer.run(articles_json)
            summary_text = result.text
            
            if not summary_text:
                logger.error("[SUMMARIZING] Summarizer produced no output")
                return "Summarizer produced no output."
            
            logger.info("[SUMMARIZING] Summary created successfully")
            return summary_text
            
        except Exception as exc:
            logger.error(f"[SUMMARIZING] Failed: {exc}")
            return f"Failed to summarize: {exc}"
