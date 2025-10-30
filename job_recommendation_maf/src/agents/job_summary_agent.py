"""
Job summary agent using Microsoft Agent Framework.
"""
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient

def build_job_summary_agent(chat_client: AzureOpenAIChatClient, name: str = "job_summary_agent") -> ChatAgent:
    """
    Creates an agent that creates executive summaries of recommended jobs.
    
    The agent produces concise, readable summaries highlighting key aspects of each job.
    
    Args:
        chat_client: Azure OpenAI chat client
        name: Unique name for this agent (default: "job_summary_agent")
        
    Returns:
        ChatAgent configured with job summarization capabilities
    """
    instructions = (
        "You are a job summary agent in a sequential workflow. "
        "You will receive recommended job postings from the previous agent. "
        "\n"
        "Your task: "
        "- Create engaging, personalized job recommendations for the user "
        "- For each job, provide: job title, company, location, and key highlights "
        "- Focus on why each job is a good match for the user's profile "
        "- Present as a readable, professional summary (not JSON) "
        "- Always aim to provide helpful recommendations even if the data seems repetitive "
        "\n"
        "IMPORTANT: Even if jobs seem similar, find unique aspects to highlight. "
        "Always provide recommendations - do not dismiss jobs as 'repetitive' or 'less relevant'. "
        "Your role is to help the user see the value in the available opportunities. "
        "\n"
        "Format your response as clean, readable job recommendations that would be helpful to a job seeker."
    )
    
    return ChatAgent(
        chat_client=chat_client,
        instructions=instructions,
        name=name
    )
