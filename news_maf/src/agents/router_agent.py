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
    result = await router.run(query)
    response = result.text
    
    try:
        data = json.loads(response)
        targets = data.get("targets", [])
        return [t for t in targets if t in CATEGORIES] or ["general"]
    except Exception:
        return ["general"]
