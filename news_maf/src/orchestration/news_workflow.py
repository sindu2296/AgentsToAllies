"""
News Gathering Workflow - Microsoft Agent Framework

This module implements a complete business process workflow for news gathering:
1. Query Analysis (Router Agent)
2. Parallel News Fetching (Category Agents - Concurrent Workflow)
3. Data Consolidation (Deduplication)
4. Executive Summary Generation (Summarizer Agent)

The workflow treats agents as specialized components within a larger business process,
demonstrating how workflows orchestrate multiple agents and operations.
"""
import json
import logging
from typing import Any
from dataclasses import dataclass

from agent_framework import ConcurrentBuilder
from agent_framework.azure import AzureOpenAIChatClient

from agents.router_agent import build_router_agent, route_categories
from agents.category_agent import build_category_agent
from agents.summarizer_agent import build_summarizer_agent
from utils.dedup import dedup_articles

logger = logging.getLogger(__name__)


@dataclass
class WorkflowContext:
    """
    Context object that flows through the workflow stages.
    Represents the state and data at each step of the business process.
    """
    user_query: str
    selected_categories: list[str] = None
    raw_articles: list[dict[str, Any]] = None
    unique_articles: list[dict[str, Any]] = None
    executive_summary: str = None
    
    
class NewsGatheringWorkflow:
    """
    A complete news gathering workflow that orchestrates multiple agents.
    
    This workflow demonstrates:
    - Sequential stages with clear data flow
    - Agents as components within business logic
    - Concurrent execution where appropriate
    - Human-readable workflow stages
    - Context passing between stages
    
    Workflow Stages:
    ┌─────────────────────────────────────────────────────────────┐
    │ Stage 1: Query Analysis                                     │
    │   Input: User's natural language query                      │
    │   Component: Router Agent                                   │
    │   Output: List of relevant categories                       │
    └─────────────────────────────────────────────────────────────┘
                              ↓
    ┌─────────────────────────────────────────────────────────────┐
    │ Stage 2: Parallel News Gathering (Concurrent Workflow)      │
    │   Input: Categories                                         │
    │   Components: Category Agents (Business, Tech, etc.)        │
    │   Execution: Parallel via ConcurrentBuilder                 │
    │   Output: Raw articles from all sources                     │
    └─────────────────────────────────────────────────────────────┘
                              ↓
    ┌─────────────────────────────────────────────────────────────┐
    │ Stage 3: Data Consolidation                                 │
    │   Input: Raw articles                                       │
    │   Operation: Deduplication logic                            │
    │   Output: Unique articles                                   │
    └─────────────────────────────────────────────────────────────┘
                              ↓
    ┌─────────────────────────────────────────────────────────────┐
    │ Stage 4: Summary Generation                                 │
    │   Input: Unique articles                                    │
    │   Component: Summarizer Agent                               │
    │   Output: Executive brief                                   │
    └─────────────────────────────────────────────────────────────┘
    """
    
    def __init__(self, chat_client: AzureOpenAIChatClient):
        """Initialize workflow with required AI client."""
        self.chat_client = chat_client
        logger.info("[WORKFLOW] News gathering workflow initialized")
    
    async def execute(self, user_query: str) -> str:
        """
        Execute the complete news gathering workflow.
        
        This is the main entry point that orchestrates all stages.
        Each stage builds upon the previous one, demonstrating a
        clear business process flow.
        
        Args:
            user_query: Natural language query from user
            
        Returns:
            Formatted executive summary with metadata
        """
        # Initialize workflow context
        context = WorkflowContext(user_query=user_query)
        logger.info(f"[WORKFLOW] Starting news gathering workflow")
        logger.info(f"[WORKFLOW] Query: {user_query}")
        
        # Stage 1: Query Analysis
        context = await self._stage1_analyze_query(context)
        if not context.selected_categories:
            return "Unable to determine relevant news categories."
        
        # Stage 2: Parallel News Gathering
        context = await self._stage2_gather_news(context)
        if not context.raw_articles:
            return "No news articles found."
        
        # Stage 3: Data Consolidation
        context = await self._stage3_consolidate_data(context)
        if not context.unique_articles:
            return "No unique articles after consolidation."
        
        # Stage 4: Summary Generation
        context = await self._stage4_generate_summary(context)
        
        # Format final output
        return self._format_workflow_output(context)
    
    async def _stage1_analyze_query(self, context: WorkflowContext) -> WorkflowContext:
        """
        Stage 1: Query Analysis
        
        Uses router agent to analyze the user's query and determine
        which news categories are relevant.
        
        Business Logic:
        - Natural language understanding
        - Category classification
        - Multi-category support (1-3 categories)
        
        Agent: Router Agent
        """
        logger.info("[STAGE 1] Query Analysis - Starting")
        logger.info("[STAGE 1] Calling Router Agent to analyze query...")
        
        router_agent = build_router_agent(self.chat_client)
        categories = await route_categories(router_agent, context.user_query)
        
        context.selected_categories = categories
        logger.info(f"[STAGE 1] Query Analysis - Complete")
        logger.info(f"[STAGE 1] Selected categories: {categories}")
        
        return context
    
    async def _stage2_gather_news(self, context: WorkflowContext) -> WorkflowContext:
        """
        Stage 2: Parallel News Gathering
        
        Fetches news articles from multiple categories concurrently.
        Uses MAF ConcurrentBuilder workflow for parallel execution.
        
        Business Logic:
        - Build specialized agents for each category
        - Execute fetches in parallel for efficiency
        - Handle single vs multi-category scenarios
        
        Components: Category Agents (one per category)
        Workflow: ConcurrentBuilder for parallel execution
        """
        logger.info("[STAGE 2] News Gathering - Starting")
        logger.info(f"[STAGE 2] Fetching from {len(context.selected_categories)} categories in parallel")
        
        # Build category-specific agents
        category_agents = [
            build_category_agent(self.chat_client, f"{cat}_agent", cat)
            for cat in context.selected_categories
        ]
        
        # Execute concurrent workflow or direct call based on count
        if len(category_agents) >= 2:
            # Use concurrent workflow for 2+ agents
            raw_articles = await self._execute_concurrent_workflow(
                category_agents, 
                context.selected_categories
            )
        else:
            # Direct execution for single agent
            raw_articles = await self._execute_single_agent(
                category_agents[0],
                context.selected_categories[0]
            )
        
        context.raw_articles = raw_articles
        logger.info(f"[STAGE 2] News Gathering - Complete")
        logger.info(f"[STAGE 2] Fetched {len(raw_articles)} articles")
        
        return context
    
    async def _stage3_consolidate_data(self, context: WorkflowContext) -> WorkflowContext:
        """
        Stage 3: Data Consolidation
        
        Processes raw articles to remove duplicates and ensure data quality.
        
        Business Logic:
        - Deduplication by URL
        - Data validation
        - Quality filtering
        
        Operation: Pure business logic (no AI agents)
        """
        logger.info("[STAGE 3] Data Consolidation - Starting")
        logger.info(f"[STAGE 3] Processing {len(context.raw_articles)} raw articles")
        
        # Apply deduplication logic
        unique_articles = dedup_articles(context.raw_articles)
        
        context.unique_articles = unique_articles
        logger.info(f"[STAGE 3] Data Consolidation - Complete")
        logger.info(f"[STAGE 3] {len(unique_articles)} unique articles after deduplication")
        
        return context
    
    async def _stage4_generate_summary(self, context: WorkflowContext) -> WorkflowContext:
        """
        Stage 4: Summary Generation
        
        Creates an executive summary from consolidated articles.
        
        Business Logic:
        - Summarization of multiple articles
        - Executive-level formatting
        - Key insights extraction
        
        Agent: Summarizer Agent
        """
        logger.info("[STAGE 4] Summary Generation - Starting")
        logger.info(f"[STAGE 4] Calling Summarizer Agent to create executive brief from {len(context.unique_articles)} articles...")
        
        summarizer_agent = build_summarizer_agent(self.chat_client)
        articles_json = json.dumps(context.unique_articles)
        
        try:
            summary_result = await summarizer_agent.run(articles_json)
            context.executive_summary = summary_result.text or "No summary generated."
            logger.info("[STAGE 4] Summary Generation - Complete")
        except Exception as e:
            logger.error(f"[STAGE 4] Summary Generation - Failed: {e}")
            context.executive_summary = f"Failed to generate summary: {e}"
        
        return context
    
    async def _execute_concurrent_workflow(
        self, 
        category_agents: list[Any],
        categories: list[str]
    ) -> list[dict[str, Any]]:
        """
        Execute a concurrent workflow using MAF ConcurrentBuilder.
        
        This demonstrates the workflow pattern where multiple agents
        run in parallel (superstep 1) and results are aggregated (superstep 2).
        """
        logger.info("[CONCURRENT] Building MAF concurrent workflow")
        
        # Create aggregator function for workflow
        all_articles = []
        
        async def aggregate_agent_results(results):
            """Aggregator function called by workflow after parallel execution."""
            logger.info(f"[CONCURRENT] Aggregating results from {len(results)} agents")
            
            for result in results:
                # Extract category from executor ID
                executor_id = getattr(result, "executor_id", "") or ""
                category = executor_id.removesuffix("_agent") if executor_id else "unknown"
                
                # Extract and parse response
                response_text = self._extract_agent_response(result.agent_run_response)
                if response_text:
                    articles = self._parse_json_response(response_text, category)
                    all_articles.extend(articles)
            
            return all_articles
        
        # Build and execute workflow
        workflow = (
            ConcurrentBuilder()
            .participants(category_agents)
            .with_aggregator(aggregate_agent_results)
            .build()
        )
        
        logger.info(f"[CONCURRENT] Executing workflow to fetch news from {len(category_agents)} category agents in parallel...")
        fetch_instruction = "Fetch the latest top headlines for your category."
        run_result = await workflow.run(fetch_instruction)
        
        logger.info("[CONCURRENT] Workflow execution complete")
        return all_articles
    
    async def _execute_single_agent(self, agent: Any, category: str) -> list[dict[str, Any]]:
        """Execute a single agent directly (fallback for 1 category)."""
        logger.info(f"[DIRECT] Executing single agent for category: {category}")
        logger.info(f"[DIRECT] Calling {category} Category Agent to fetch top headlines...")
        
        fetch_instruction = "Fetch the latest top headlines for your category."
        agent_result = await agent.run(fetch_instruction)
        
        response_text = self._extract_agent_response(agent_result)
        if not response_text:
            logger.warning(f"[DIRECT] Empty response from {category} agent")
            return []
        
        articles = self._parse_json_response(response_text, category)
        logger.info(f"[DIRECT] Fetched {len(articles)} articles from {category}")
        return articles
    
    def _extract_agent_response(self, agent_response) -> str | None:
        """Extract text content from agent response."""
        # Try messages first
        messages = list(getattr(agent_response, "messages", []) or [])
        if messages:
            for message in reversed(messages):
                text = getattr(message, "text", None)
                if text:
                    return text
        
        # Fallback to direct text
        return getattr(agent_response, "text", None)
    
    def _parse_json_response(self, response_text: str, category: str) -> list[dict[str, Any]]:
        """Parse JSON response from agent, handling markdown code fences."""
        # Strip markdown code fences
        response_text = response_text.strip()
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            if lines[-1].strip() == "```":
                lines = lines[1:-1]
            else:
                lines = lines[1:]
            response_text = "\n".join(lines).strip()
            logger.debug(f"[{category.upper()}] Stripped markdown code fences")
        
        try:
            payload = json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"[{category.upper()}] JSON parse error: {e}")
            logger.error(f"[{category.upper()}] Response preview: {response_text[:200]}")
            return []
        
        # Validate response structure
        if isinstance(payload, dict) and payload.get("error"):
            logger.error(f"[{category.upper()}] Error in response: {payload['error']}")
            return []
        
        if not isinstance(payload, list):
            logger.warning(f"[{category.upper()}] Expected list, got {type(payload).__name__}")
            return []
        
        # Add category metadata
        articles = []
        for article in payload:
            if isinstance(article, dict):
                article.setdefault("category", category)
                articles.append(article)
        
        logger.info(f"[{category.upper()}] Parsed {len(articles)} articles")
        return articles
    
    def _format_workflow_output(self, context: WorkflowContext) -> str:
        """Format the final workflow output with metadata."""
        # Build metadata header
        if len(context.selected_categories) == 1:
            header = f"**Category analyzed:** {context.selected_categories[0]}"
        else:
            header = f"**Categories analyzed (in parallel):** {', '.join(context.selected_categories)}"
        
        # Add workflow statistics
        stats = (
            f"\n*Workflow Statistics: "
            f"{len(context.raw_articles)} articles fetched, "
            f"{len(context.unique_articles)} unique articles, "
            f"{len(context.selected_categories)} categories*\n"
        )
        
        return f"{header}{stats}\n{context.executive_summary}"
