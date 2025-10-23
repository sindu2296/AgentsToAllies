"""
News Gathering Workflow - 4 simple steps.

Step 1: Query Classification → Determine relevant news categories
Step 2: News Gathering       → Fetch articles from multiple sources
Step 3: Data Consolidation   → Remove duplicates
Step 4: Summary Generation   → Create executive summary
"""
import json
import logging
from typing import Any
from dataclasses import dataclass

from agent_framework import ConcurrentBuilder
from agent_framework.azure import AzureOpenAIChatClient

from agents.query_classifier_agent import build_query_classifier_agent, classify_query
from agents.news_gatherer_agent import build_news_gatherer_agent
from agents.summarizer_agent import build_summarizer_agent
from utils.dedup import dedup_articles

logger = logging.getLogger(__name__)


@dataclass
class WorkflowContext:
    """Context data flowing through the 4 workflow steps."""
    user_query: str
    selected_categories: list[str] = None
    raw_articles: list[dict[str, Any]] = None
    unique_articles: list[dict[str, Any]] = None
    executive_summary: str = None


class NewsGatheringWorkflow:
    """
    News gathering workflow with 4 clear steps.
    
    Step 1: Query Classification → Determine relevant news categories
    Step 2: News Gathering       → Fetch articles from multiple sources
    Step 3: Data Consolidation   → Remove duplicates
    Step 4: Summary Generation   → Create executive summary
    """
    
    def __init__(self, chat_client: AzureOpenAIChatClient):
        """Initialize workflow with required AI client."""
        self.chat_client = chat_client
        logger.info("[WORKFLOW] News gathering workflow initialized")
    
    async def execute(self, user_query: str) -> str:
        """
        Execute the complete workflow: Classification → Gathering → Consolidation → Summary.
        
        Args:
            user_query: User's news query
            
        Returns:
            Executive summary with metadata
        """
        context = WorkflowContext(user_query=user_query)
        logger.info(f"[WORKFLOW] Starting workflow: {user_query}")
        
        # STEP 1: Query Classification
        context = await self._step_classify_query(context)
        if not context.selected_categories:
            return "Unable to determine relevant news categories."
        
        # STEP 2: News Gathering
        context = await self._step_gather_news(context)
        if not context.raw_articles:
            return "No news articles found."
        
        # STEP 3: Data Consolidation
        context = await self._step_consolidate_data(context)
        if not context.unique_articles:
            return "No unique articles after consolidation."
        
        # STEP 4: Summary Generation
        context = await self._step_generate_summary(context)
        
        return self._format_output(context)
    
    async def _step_classify_query(self, context: WorkflowContext) -> WorkflowContext:
        """STEP 1: Analyze query to determine relevant news categories."""
        logger.info("[STEP 1] Classifying user query...")
        classifier_agent = build_query_classifier_agent(self.chat_client)
        categories = await classify_query(classifier_agent, context.user_query)
        context.selected_categories = categories
        logger.info(f"[STEP 1] Selected categories: {categories}")
        logger.info("")
        return context
    
    async def _step_gather_news(self, context: WorkflowContext) -> WorkflowContext:
        """STEP 2: Fetch news articles from selected categories (parallel if multiple)."""
        logger.info(f"[STEP 2] Gathering news from {len(context.selected_categories)} categories...")
        
        # Build one agent per category
        agents = [
            build_news_gatherer_agent(self.chat_client, f"{cat}_gatherer", cat)
            for cat in context.selected_categories
        ]
        
        # Execute agents (parallel if 2+, serial if 1)
        if len(agents) >= 2:
            raw_articles = await self._execute_concurrent_agents(agents, context.selected_categories)
        else:
            raw_articles = await self._execute_single_agent(agents[0], context.selected_categories[0])
        
        context.raw_articles = raw_articles
        logger.info(f"[STEP 2] Gathered {len(raw_articles)} articles")
        logger.info("")
        return context
    
    async def _step_consolidate_data(self, context: WorkflowContext) -> WorkflowContext:
        """STEP 3: Remove duplicate articles."""
        logger.info(f"[STEP 3] Deduplicating {len(context.raw_articles)} articles...")
        unique_articles = dedup_articles(context.raw_articles)
        context.unique_articles = unique_articles
        logger.info(f"[STEP 3] Consolidated to {len(unique_articles)} unique articles")
        logger.info("")
        return context
    
    async def _step_generate_summary(self, context: WorkflowContext) -> WorkflowContext:
        """STEP 4: Create executive summary."""
        logger.info(f"[STEP 4] Generating summary from {len(context.unique_articles)} articles...")
        summarizer_agent = build_summarizer_agent(self.chat_client)
        
        try:
            result = await summarizer_agent.run(json.dumps(context.unique_articles))
            # Agent returns prose directly - no parsing needed
            context.executive_summary = result.text or "No summary generated."
            logger.info("[STEP 4] Summary complete")
            logger.info("")
        except Exception as e:
            logger.error(f"[STEP 4] Summary failed: {e}")
            context.executive_summary = f"Summary generation failed: {e}"
        
        return context
    
    async def _execute_concurrent_agents(
        self, 
        agents: list[Any],
        categories: list[str]
    ) -> list[dict[str, Any]]:
        """Execute agents concurrently using ConcurrentBuilder."""
        all_articles = []
        
        async def aggregate_agent_results(results):
            """Aggregate results from parallel agents."""
            logger.info(f"[CONCURRENT] Aggregating {len(results)} agent responses...")
            for result in results:
                executor_id = getattr(result, "executor_id", "") or ""
                category = executor_id.removesuffix("_gatherer") if executor_id else "unknown"
                
                # Agent returns tool result directly
                response_text = result.agent_run_response.text
                if response_text:
                    try:
                        articles = json.loads(response_text.strip())
                        if isinstance(articles, list):
                            for article in articles:
                                if isinstance(article, dict):
                                    article.setdefault("category", category)
                                    all_articles.append(article)
                    except json.JSONDecodeError as e:
                        logger.warning(f"[{category}] JSON parse failed: {e}")
            return all_articles
        
        workflow = (
            ConcurrentBuilder()
            .participants(agents)
            .with_aggregator(aggregate_agent_results)
            .build()
        )
        
        await workflow.run("Gather the latest top headlines for your category.")
        return all_articles
    
    async def _execute_single_agent(self, agent: Any, category: str) -> list[dict[str, Any]]:
        """Execute single agent directly."""
        result = await agent.run("Gather the latest top headlines for your category.")
        
        # Agent returns tool result directly
        response_text = result.text
        if not response_text:
            logger.warning(f"[{category}] Empty response")
            return []
        
        try:
            articles = json.loads(response_text.strip())
            if not isinstance(articles, list):
                return []
            
            # Add category metadata
            for article in articles:
                if isinstance(article, dict):
                    article.setdefault("category", category)
            
            return articles
        except json.JSONDecodeError as e:
            logger.warning(f"[{category}] JSON parse failed: {e}")
            return []
    
    def _format_output(self, context: WorkflowContext) -> str:
        """Format final output with metadata."""
        if len(context.selected_categories) == 1:
            header = f"**Category:** {context.selected_categories[0]}"
        else:
            header = f"**Categories (parallel):** {', '.join(context.selected_categories)}"
        
        stats = (
            f"\n*Statistics: {len(context.raw_articles)} articles gathered, "
            f"{len(context.unique_articles)} unique, {len(context.selected_categories)} categories*\n"
        )
        return f"{header}{stats}\n{context.executive_summary}"
