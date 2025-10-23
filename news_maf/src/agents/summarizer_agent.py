"""
Summarizer agent - creates executive summary from articles.
"""
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient


def build_summarizer_agent(chat_client: AzureOpenAIChatClient) -> ChatAgent:
    """Create summarizer agent."""
    instructions = (
        "Create 5-bullet executive summary from articles. "
        "Include inline citations [Source](url). Professional tone."
    )
    
    return ChatAgent(
        chat_client=chat_client,
        instructions=instructions,
        name="summarizer_agent"
    )
