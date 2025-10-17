"""
Router agent for determining relevant news categories using Microsoft Agent Framework.
"""
import json
from typing import List
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient

CATEGORIES = [
    "technology", "sports", "business", "science", "health", "entertainment", "general",
]

ROUTER_INSTRUCTIONS = (
    "You are a routing brain. Read the user query and output a compact JSON with the key 'targets' "
    "as a list of categories among: technology, sports, business, science, health, entertainment, general. "
    "Pick 1-3 most relevant categories. Respond with JSON ONLY."
)

def build_router_agent(chat_client: AzureOpenAIChatClient) -> ChatAgent:
    """Creates a router agent that determines which news categories to fetch."""
    return ChatAgent(
        chat_client=chat_client,
        instructions=ROUTER_INSTRUCTIONS,
        name="router_agent"
    )

async def route_categories(router: ChatAgent, query: str) -> List[str]:
    """
    Routes a query to relevant news categories.
    
    Args:
        router: The router agent
        query: User's news query
        
    Returns:
        List of category names to fetch from
    """
    import logging
    logger = logging.getLogger(__name__)
    
    result = await router.run(query)
    response = result.text
    
    logger.info(f"[ROUTER] Raw response: {response}")
    
    # Strip markdown code fences if present
    response = response.strip()
    if response.startswith("```"):
        lines = response.split("\n")
        # Remove first line (```json or ```) and last line (```)
        if lines[-1].strip() == "```":
            lines = lines[1:-1]
        else:
            lines = lines[1:]
        response = "\n".join(lines).strip()
        logger.info(f"[ROUTER] Cleaned response: {response}")
    
    try:
        data = json.loads(response)
        targets = data.get("targets", [])
        logger.info(f"[ROUTER] Parsed targets: {targets}")
        filtered = [t for t in targets if t in CATEGORIES]
        logger.info(f"[ROUTER] Filtered targets: {filtered}")
        return filtered or ["general"]
    except Exception as e:
        logger.error(f"[ROUTER] Failed to parse response: {e}")
        logger.error(f"[ROUTER] Attempted to parse: {response[:200]}")
        return ["general"]
