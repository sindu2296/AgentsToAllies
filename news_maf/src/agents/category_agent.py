"""
Category agent for fetching news using Microsoft Agent Framework.
"""
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from plugins.news_plugin import fetch_top_headlines

def build_category_agent(chat_client: AzureOpenAIChatClient, name: str, category: str) -> ChatAgent:
    """
    Creates an agent that fetches news for a specific category.
    
    The agent uses a function tool to fetch news and returns JSON results.
    
    Args:
        chat_client: Azure OpenAI chat client
        name: Unique name for this agent
        category: News category to fetch (technology, sports, business, etc.)
        
    Returns:
        ChatAgent configured with news fetching capabilities
    """
    instructions = (
        f"You are a news fetcher for the '{category}' category. "
        f"When asked to fetch news, call the fetch_top_headlines function with category='{category}'. "
        "Return the JSON result exactly as received from the function."
    )
    
    return ChatAgent(
        chat_client=chat_client,
        instructions=instructions,
        name=name,
        tools=[fetch_top_headlines]  # MAF function tool
    )
