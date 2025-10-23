"""
Sequential news orchestrator - agents run one-by-one.
"""
import json
import logging
from typing import Any

from agent_framework.azure import AzureOpenAIChatClient

from agents.query_classifier_agent import build_query_classifier_agent, classify_query
from agents.news_gatherer_agent import build_news_gatherer_agent
from agents.summarizer_agent import build_summarizer_agent
from utils.dedup import dedup_articles

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
        self.classifier = build_query_classifier_agent(chat_client)
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
        Use query classifier agent to determine which news categories to fetch.
        
        Args:
            user_query: User's natural language query
            
        Returns:
            List of category names (e.g., ['technology', 'business'])
        """
        logger.info(f"[CLASSIFICATION] Processing query: {user_query}")
        categories = await classify_query(self.classifier, user_query)
        logger.info(f"[CLASSIFICATION] Selected categories: {categories}")
        logger.info("")  # Blank line for readability
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
            news_gatherer = build_news_gatherer_agent(
                self.chat_client,
                f"{category}_gatherer",
                category
            )
            
            # Fetch articles for this category
            articles = await self._fetch_category_articles(news_gatherer, category)
            all_articles.extend(articles)
        
        logger.info("")  # Blank line for readability
        return all_articles

    async def _fetch_category_articles(
        self,
        category_agent: Any,
        category: str
    ) -> list[dict[str, Any]]:
        """Fetch articles from a category agent."""
        try:
            result = await category_agent.run(
                "Fetch the latest news headlines for your assigned category"
            )
            
            # Agent returns tool result directly
            response_text = result.text
            if not response_text:
                logger.warning(f"[{category.upper()}] Empty response")
                return []
            
            articles = json.loads(response_text.strip())
            if not isinstance(articles, list):
                return []
            
            # Add category metadata
            for article in articles:
                if isinstance(article, dict):
                    article.setdefault("category", category)
            
            logger.info(f"[{category.upper()}] Fetched {len(articles)} articles")
            return articles
            
        except Exception as exc:
            logger.error(f"[{category.upper()}] Failed: {exc}")
            return []

    async def _create_summary(self, articles: list[dict[str, Any]]) -> str:
        """Create executive summary."""
        logger.info(f"[SUMMARIZING] Creating summary from {len(articles)} articles")
        
        summarizer = build_summarizer_agent(self.chat_client)
        articles_json = json.dumps(articles)
        
        try:
            result = await summarizer.run(articles_json)
            
            # Agent returns prose directly
            summary_text = result.text
            if not summary_text:
                logger.error("[SUMMARIZING] No output")
                return "Summarizer produced no output."
            
            logger.info("[SUMMARIZING] Complete")
            logger.info("")
            return summary_text
            
        except Exception as exc:
            logger.error(f"[SUMMARIZING] Failed: {exc}")
            return f"Failed to summarize: {exc}"
