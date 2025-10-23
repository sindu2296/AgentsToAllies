"""
News Gatherer agent - fetches news for a specific category.
"""
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from plugins.news_plugin import fetch_top_headlines


def build_news_gatherer_agent(chat_client: AzureOpenAIChatClient, name: str, category: str) -> ChatAgent:
    """Create news gatherer agent for a category."""
    instructions = (
        f"Fetch news for '{category}' using fetch_top_headlines tool with category='{category}'. "
        "Return the tool result EXACTLY as-is. No formatting."
    )
    
    return ChatAgent(
        chat_client=chat_client,
        instructions=instructions,
        name=name,
        tools=[fetch_top_headlines]
    )
