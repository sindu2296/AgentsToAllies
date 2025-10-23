"""
Concurrent news orchestrator - agents run in parallel via ConcurrentBuilder.
"""
import json
import logging
from typing import Any

from agent_framework import ConcurrentBuilder
from agent_framework.azure import AzureOpenAIChatClient

from agents.query_classifier_agent import build_query_classifier_agent, classify_query
from agents.news_gatherer_agent import build_news_gatherer_agent
from agents.summarizer_agent import build_summarizer_agent
from utils.dedup import dedup_articles

logger = logging.getLogger(__name__)


class ConcurrentNewsOrchestrator:
    """
    Orchestrates news fetching using MAF Concurrent Workflows.
    
    Workflow Steps:
    1. Router agent determines relevant categories
    2. Category agents fetch news in parallel (using ConcurrentBuilder)
    3. Aggregator combines results and deduplicates articles
    4. Summarizer agent creates an executive brief
    
    This approach uses the official MAF workflow pattern for concurrent execution,
    making it more robust and maintainable than manual asyncio.gather().
    """
    
    def __init__(self, chat_client: AzureOpenAIChatClient):
        """Initialize orchestrator with Azure OpenAI chat client."""
        self.chat_client = chat_client
        self.classifier = build_query_classifier_agent(chat_client)
        logger.info("Concurrent orchestrator initialized")

    async def run(self, user_query: str) -> str:
        """
        Process a user query and return a news summary using concurrent workflows.
        
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

        # Step 2: Build category agents
        category_agents = self._build_category_agents(categories)
        
        # Step 3: Create and run workflow
        logger.info(f"[WORKFLOW] Starting concurrent workflow with {len(categories)} agents")
        workflow_result = await self._run_workflow(category_agents, categories, user_query)
        
        return workflow_result

    async def _route_query(self, user_query: str) -> list[str]:
        """
        Use router agent to determine which news categories to fetch.
        
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

    def _build_category_agents(self, categories: list[str]) -> list[Any]:
        """
        Create a category agent for each selected category.
        
        Args:
            categories: List of category names
            
        Returns:
            List of configured ChatAgent instances
        """
        logger.info(f"[AGENTS] Building {len(categories)} news gatherer agents")
        agents = [
            build_news_gatherer_agent(self.chat_client, f"{cat}_gatherer", cat)
            for cat in categories
        ]
        return agents

    async def _run_workflow(
        self, 
        category_agents: list[Any], 
        categories: list[str],
        user_query: str
    ) -> str:
        """
        Execute the concurrent workflow using ConcurrentBuilder.
        
        This is the core of MAF's concurrent orchestration pattern:
        1. Define participants (category agents)
        2. Define aggregator (how to combine results)
        3. Build and run workflow
        
        Note: ConcurrentBuilder requires at least 2 participants.
        For single-category queries, we fall back to sequential execution.
        
        Args:
            category_agents: List of agents to run in parallel
            categories: Category names for logging
            user_query: Original query to pass to workflow
            
        Returns:
            Final formatted summary
        """
        # Create summarizer agent for aggregation step
        summarizer = build_summarizer_agent(self.chat_client)
        
        # ConcurrentBuilder requires at least 2 participants
        if len(category_agents) < 2:
            logger.info(f"[WORKFLOW] Only 1 category - using direct execution instead of workflow")
            return await self._run_single_agent(category_agents[0], categories, summarizer, user_query)
        
        # Define aggregator function that will be called with all agent results
        async def aggregate_results(results):
            """
            Aggregator function called by workflow after all participants complete.
            
            Args:
                results: List of AgentExecutorResponse objects from participants
                
            Returns:
                Final summary string
            """
            return await self._aggregate_and_summarize(results, categories, summarizer)
        
        # Build workflow using official MAF pattern
        logger.info(f"[WORKFLOW] Building concurrent workflow with {len(category_agents)} agents")
        workflow = (
            ConcurrentBuilder()
            .participants(category_agents)  # Agents to run in parallel
            .with_aggregator(aggregate_results)  # How to combine results
            .build()
        )
        
        # Run workflow with explicit instruction to fetch news
        # (The user's query is used for routing, but agents need clear instructions)
        fetch_instruction = "Fetch the latest top headlines for your category."
        logger.info(f"[WORKFLOW] Running workflow with instruction: {fetch_instruction}")
        run_result = await workflow.run(fetch_instruction)
        
        # Extract string output from workflow results
        outputs = run_result.get_outputs()
        for output in reversed(outputs):
            if isinstance(output, str):
                logger.info("[WORKFLOW] Workflow completed successfully")
                logger.info("")  # Blank line for readability
                return output
        
        logger.error("[WORKFLOW] No output produced by workflow")
        return "No output produced by workflow."

    async def _run_single_agent(
        self,
        agent: Any,
        categories: list[str],
        summarizer: Any,
        user_query: str
    ) -> str:
        """
        Execute a single agent directly (fallback when only 1 category).
        
        ConcurrentBuilder requires at least 2 participants, so we handle
        single-category queries by running the agent directly.
        
        Args:
            agent: Single category agent to run
            categories: Category names (should be length 1)
            summarizer: Summarizer agent instance
            user_query: Original query
            
        Returns:
            Formatted summary string
        """
        logger.info(f"[DIRECT] Running single agent for category: {categories[0]}")
        
        try:
            # Run the single agent with explicit instruction
            fetch_instruction = "Fetch the latest top headlines for your category."
            agent_result = await agent.run(fetch_instruction)
            
            # Agent returns tool result directly
            response_text = agent_result.text
            if not response_text:
                logger.warning(f"[{categories[0].upper()}] Empty response")
                return "No articles found."
            
            # Parse articles
            articles = json.loads(response_text.strip())
            if not isinstance(articles, list):
                return "No articles found."
            
            # Add category metadata
            for article in articles:
                if isinstance(article, dict):
                    article.setdefault("category", categories[0])
            
            # Deduplicate (though unlikely to have duplicates from single source)
            unique_articles = dedup_articles(articles)
            logger.info(f"[DEDUP] {len(unique_articles)} unique articles")
            logger.info("")  # Blank line for readability
            
            # Summarize
            summary_text = await self._create_summary(unique_articles, summarizer)
            
            # Format output
            header = f"**Category analyzed:** {categories[0]}"
            return f"{header}\n\n{summary_text}"
            
        except Exception as exc:
            logger.error(f"[DIRECT] Failed to run single agent: {exc}")
            return f"Failed to process query: {exc}"

    async def _aggregate_and_summarize(
        self,
        results: list[Any],
        categories: list[str],
        summarizer: Any
    ) -> str:
        """
        Aggregate results from all category agents and create summary.
        
        This function is called by the workflow aggregator. It:
        1. Extracts articles from each agent's response
        2. Deduplicates articles
        3. Sends to summarizer agent
        4. Formats final output
        
        Args:
            results: List of AgentExecutorResponse objects
            categories: Category names for header
            summarizer: Summarizer agent instance
            
        Returns:
            Formatted summary string
        """
        logger.info(f"[AGGREGATION] Processing results from {len(results)} agents")
        
        # Step 1: Extract articles from all agents
        all_articles = self._extract_articles_from_results(results)
        
        # Step 2: Deduplicate
        unique_articles = dedup_articles(all_articles)
        if not unique_articles:
            logger.warning("[AGGREGATION] No articles found after deduplication")
            return "No articles found."
        
        logger.info(f"[DEDUP] {len(unique_articles)} unique articles after deduplication")
        
        # Step 3: Summarize
        summary_text = await self._create_summary(unique_articles, summarizer)
        
        # Step 4: Format output
        header = f"**Categories analyzed (in parallel):** {', '.join(categories)}"
        return f"{header}\n\n{summary_text}"

    def _extract_articles_from_results(self, results: list[Any]) -> list[dict[str, Any]]:
        """Extract and parse article data from workflow results."""
        all_articles = []
        
        for result in results:
            executor_id = getattr(result, "executor_id", "") or ""
            category = executor_id.removesuffix("_agent") if executor_id else "unknown"
            
            # Agent returns tool result directly
            response_text = result.agent_run_response.text
            if not response_text:
                logger.warning(f"[{category.upper()}] Empty response")
                continue
            
            try:
                articles = json.loads(response_text.strip())
                if isinstance(articles, list):
                    for article in articles:
                        if isinstance(article, dict):
                            article.setdefault("category", category)
                            all_articles.append(article)
            except json.JSONDecodeError as e:
                logger.warning(f"[{category.upper()}] JSON parse failed: {e}")
        
        return all_articles

    async def _create_summary(self, articles: list[dict[str, Any]], summarizer: Any) -> str:
        """Create executive summary."""
        logger.info(f"[SUMMARIZING] Creating summary from {len(articles)} articles")
        
        summary_payload = json.dumps(articles)
        
        try:
            summary_result = await summarizer.run(summary_payload)
        except Exception as exc:
            logger.error(f"[SUMMARIZING] Failed: {exc}")
            return f"Failed to summarize: {exc}"
        
        # Agent returns prose directly
        summary_text = summary_result.text
        if not summary_text:
            logger.error("[SUMMARIZING] No output")
            return "Summarizer produced no output."
        
        logger.info("[SUMMARIZING] Complete")
        logger.info("")
        return summary_text
