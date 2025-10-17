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
        "You will receive recommended job postings in JSON format from the previous agent. "
        "\n"
        "Your task: "
        "- For each job posting, create a concise 5-bullet executive summary "
        "- Highlight: key responsibilities, required qualifications, nice-to-have skills, compensation/benefits, and why it's a good match "
        "- Format the output as clear, readable text (not JSON) "
        "- Include the job title, company, and location at the start of each summary "
        "- Separate each job summary with a line break "
        "\n"
        "If the input contains job data in JSON format, parse it and create summaries. "
        "Do NOT ask for more information - work with the job data you receive from the previous agent. "
        "If no jobs are provided or the JSON is empty, simply state 'No job recommendations to summarize.'"
    )
    
    return ChatAgent(
        chat_client=chat_client,
        instructions=instructions,
        name=name
    )
