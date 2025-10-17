"""
Job extractor agent for fetching jobs using Microsoft Agent Framework.
"""
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from plugins.job_board_plugin import search_jobs

def build_job_extractor_agent(chat_client: AzureOpenAIChatClient, name: str = "job_extractor_agent") -> ChatAgent:
    """
    Creates an agent that searches for jobs based on a user profile.
    
    The agent uses the search_jobs function tool to fetch jobs from SerpAPI and returns JSON results.
    
    Args:
        chat_client: Azure OpenAI chat client
        name: Unique name for this agent (default: "job_extractor_agent")
        
    Returns:
        ChatAgent configured with job searching capabilities
    """
    instructions = (
        "You are a job extractor agent in a sequential workflow. "
        "When given a user profile (skills, experience, job title), call the search_jobs function with that profile. "
        "The function will return job postings as JSON. "
        "Return ONLY the JSON output from the function - do not add commentary or ask questions. "
        "Pass the JSON directly to the next agent in the workflow."
    )
    
    return ChatAgent(
        chat_client=chat_client,
        instructions=instructions,
        name=name,
        tools=[search_jobs]  # MAF function tool
    )
