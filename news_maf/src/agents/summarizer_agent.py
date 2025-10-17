"""
Summarizer agent for creating executive briefs using Microsoft Agent Framework.
"""
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient

def build_summarizer_agent(chat_client: AzureOpenAIChatClient) -> ChatAgent:
    """
    Creates an agent that summarizes news articles into an executive brief.
    
    This agent takes a JSON array of articles and produces a concise,
    well-formatted summary with inline source citations.
    
    Args:
        chat_client: Azure OpenAI chat client
        
    Returns:
        ChatAgent configured for summarization
    """
    instructions = (
        "You are an executive news summarizer. "
        "You receive JSON arrays of news articles with title, author, source, url, and description fields. "
        "Create a concise 5-bullet executive summary that highlights the most important information. "
        "Include inline source citations with URLs in markdown format like [Source Name](url). "
        "If you receive an error key in the JSON, report it clearly. "
        "Be concise, professional, and actionable in your summaries."
    )
    
    return ChatAgent(
        chat_client=chat_client,
        instructions=instructions,
        name="summarizer_agent"
    )
