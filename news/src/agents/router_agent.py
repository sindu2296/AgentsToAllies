import json
from typing import List

from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel import Kernel

CATEGORIES = [
    "technology", "sports", "business", "science", "health", "entertainment", "general",
]

ROUTER_INSTRUCTIONS = (
    "You are a routing brain. Read the user query and output a compact JSON with the key 'targets' "
    "as a list of categories among: technology, sports, business, science, health, entertainment, general. "
    "Pick 1-3 most relevant categories. Respond with JSON ONLY."
)

def build_router_agent(kernel: Kernel) -> ChatCompletionAgent:
    return ChatCompletionAgent(
        name="router_agent",
        instructions=ROUTER_INSTRUCTIONS,
        kernel=kernel,
    )

async def route_categories(router: ChatCompletionAgent, query: str) -> List[str]:
    response = ""
    async for msg in router.invoke(query):
        response += msg.content.content
    
    try:
        data = json.loads(response)
        targets = data.get("targets", [])
        return [t for t in targets if t in CATEGORIES] or ["general"]
    except Exception:
        return ["general"]
