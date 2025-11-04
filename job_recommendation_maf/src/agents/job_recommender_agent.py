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
        "- Analyze ALL job postings and match them to the user's profile "
        "- Rank ALL jobs by relevance and fit score "
        "- Select and return EXACTLY the TOP 5 highest-scoring jobs ONLY "
        "- Include job title, company, location, and key details for each "
        "- Add a brief explanation of why each job matches the user's profile "
        "\n"
        "CRITICAL REQUIREMENTS: "
        "- Return EXACTLY 5 job recommendations, no more, no less "
        "- Even if there are 50+ jobs available, select only the TOP 5 matches "
        "- Number your recommendations 1-5 for clarity "
        "- If fewer than 5 jobs are available, return all available jobs but clearly indicate the count "
        "\n"
        "IMPORTANT: Do not filter out jobs as 'repetitive' or 'less detailed'. "
        "Find the positive aspects of each job opportunity. "
        "Always provide the top recommendations - your role is to help users find the best opportunities. "
        "Present the jobs in a format that the summary agent can easily work with."
    )
    
    return ChatAgent(
        chat_client=chat_client,
        instructions=instructions,
        name=name
    )
