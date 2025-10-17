"""
Job recommender agent using Microsoft Agent Framework.
"""
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient

def build_job_recommender_agent(chat_client: AzureOpenAIChatClient, name: str = "job_recommender_agent") -> ChatAgent:
    """
    Creates an agent that recommends jobs from an extracted list based on user profile.
    
    The agent analyzes job matches and ranks them by relevance.
    
    Args:
        chat_client: Azure OpenAI chat client
        name: Unique name for this agent (default: "job_recommender_agent")
        
    Returns:
        ChatAgent configured with job recommendation capabilities
    """
    instructions = (
        "You are a job recommender agent in a sequential workflow. "
        "You will receive input containing: "
        "1. A user profile (their skills, experience, preferences) "
        "2. A list of job postings in JSON format from the previous agent "
        "\n"
        "Your task: "
        "- Analyze the job postings and match them to the user's profile "
        "- Rank the jobs by relevance and fit "
        "- Return the top 3-5 recommended jobs as a JSON array "
        "- Include all original job fields (title, company, location, description, etc.) "
        "- Add a brief 'match_reason' field explaining why each job is a good fit "
        "\n"
        "If the input contains job postings in JSON format, extract them and analyze the match. "
        "Pass the recommended jobs to the next agent in the same JSON format. "
        "Do NOT ask for more information - work with what you receive from the previous agent."
    )
    
    return ChatAgent(
        chat_client=chat_client,
        instructions=instructions,
        name=name
    )
