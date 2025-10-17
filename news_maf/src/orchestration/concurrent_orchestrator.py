"""
Concurrent news orchestrator using Microsoft Agent Framework Workflows.

This module demonstrates the official MAF workflow pattern using ConcurrentBuilder
to fan-out work to multiple agents in parallel, then aggregate results.

Key concepts for beginners:
- ConcurrentBuilder: Creates a workflow that runs multiple agents in parallel
- Participants: The agents that run concurrently
- Aggregator: A function that combines results from all participants
- Workflow.run(): Executes the workflow and returns results
"""
import json
import logging
from typing import Any

from agent_framework import ConcurrentBuilder
from agent_framework.azure import AzureOpenAIChatClient

from agents.router_agent import build_router_agent, route_categories
from agents.category_agent import build_category_agent
from agents.summarizer_agent import build_summarizer_agent
from utils.dedup import dedup_articles

# Set up logging for better traceability
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
        self.router = build_router_agent(chat_client)
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
        logger.info(f"[ROUTING] Processing query: {user_query}")
        categories = await route_categories(self.router, user_query)
        logger.info(f"[ROUTING] Selected categories: {categories}")
        return categories

    def _build_category_agents(self, categories: list[str]) -> list[Any]:
        """
        Create a category agent for each selected category.
        
        Args:
            categories: List of category names
            
        Returns:
            List of configured ChatAgent instances
        """
        logger.info(f"[AGENTS] Building {len(categories)} category agents")
        agents = [
            build_category_agent(self.chat_client, f"{cat}_agent", cat)
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
            
            # Extract text from result
            response_text = self._extract_agent_text(agent_result)
            if not response_text:
                logger.warning(f"[{categories[0].upper()}] Empty response")
                return "No articles found."
            
            # Parse articles
            articles = self._parse_article_response(response_text, categories[0])
            if not articles:
                return "No articles found."
            
            # Deduplicate (though unlikely to have duplicates from single source)
            unique_articles = dedup_articles(articles)
            logger.info(f"[DEDUP] {len(unique_articles)} unique articles")
            
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
        """
        Extract and parse article data from workflow results.
        
        Args:
            results: List of AgentExecutorResponse objects
            
        Returns:
            List of article dictionaries
        """
        all_articles = []
        
        for result in results:
            # Get category name from executor ID
            executor_id = getattr(result, "executor_id", "") or ""
            category = executor_id.removesuffix("_agent") if executor_id else "unknown"
            
            # Extract text response from agent
            response_text = self._extract_agent_text(result.agent_run_response)
            
            if not response_text:
                logger.warning(f"[{category.upper()}] Empty response")
                continue
            
            # Parse JSON response
            articles = self._parse_article_response(response_text, category)
            all_articles.extend(articles)
        
        return all_articles

    @staticmethod
    def _extract_agent_text(agent_response) -> str | None:
        """
        Extract text content from agent response.
        
        Handles both message-based and direct text responses.
        
        Args:
            agent_response: AgentRunResponse object
            
        Returns:
            Extracted text or None
        """
        # Try to get from messages first
        messages = list(getattr(agent_response, "messages", []) or [])
        if messages:
            for message in reversed(messages):
                text = getattr(message, "text", None)
                if text:
                    return text
        
        # Fallback to direct text attribute
        return getattr(agent_response, "text", None)

    def _parse_article_response(self, response_text: str, category: str) -> list[dict[str, Any]]:
        """
        Parse JSON article response from category agent.
        
        Args:
            response_text: JSON string from agent
            category: Category name for logging
            
        Returns:
            List of article dictionaries
        """
        # Strip markdown code fences if present
        response_text = response_text.strip()
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            # Remove first line (```json or ```) and last line (```)
            if lines[-1].strip() == "```":
                lines = lines[1:-1]
            else:
                lines = lines[1:]
            response_text = "\n".join(lines).strip()
            logger.info(f"[{category.upper()}] Stripped markdown code fences")
        
        try:
            payload = json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"[{category.upper()}] Failed to parse JSON response")
            logger.error(f"[{category.upper()}] Response text: {response_text[:500]}")
            logger.error(f"[{category.upper()}] JSON error: {e}")
            return []
        
        # Handle error responses
        if isinstance(payload, dict) and payload.get("error"):
            logger.error(f"[{category.upper()}] Error: {payload['error']}")
            return []
        
        # Validate list response
        if not isinstance(payload, list):
            logger.warning(f"[{category.upper()}] Unexpected payload type: {type(payload).__name__}")
            return []
        
        # Add category metadata to articles
        articles = []
        for article in payload:
            if isinstance(article, dict):
                article.setdefault("category", category)
                articles.append(article)
        
        logger.info(f"[{category.upper()}] Successfully fetched {len(articles)} articles")
        return articles

    async def _create_summary(self, articles: list[dict[str, Any]], summarizer: Any) -> str:
        """
        Create executive summary from articles using summarizer agent.
        
        Args:
            articles: List of article dictionaries
            summarizer: Summarizer agent instance
            
        Returns:
            Summary text
        """
        logger.info(f"[SUMMARIZING] Creating executive brief from {len(articles)} articles")
        
        summary_payload = json.dumps(articles)
        
        try:
            summary_result = await summarizer.run(summary_payload)
        except Exception as exc:
            logger.error(f"[SUMMARIZING] Failed: {exc}")
            return f"Failed to summarize results: {exc}"
        
        summary_text = getattr(summary_result, "text", "") or ""
        if not summary_text:
            logger.error("[SUMMARIZING] Summarizer produced no output")
            return "Summarizer produced no output."
        
        logger.info("[SUMMARIZING] Summary created successfully")
        return summary_text
