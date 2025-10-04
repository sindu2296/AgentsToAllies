from semantic_kernel.agents import ChatCompletionAgent
from ..config import build_kernel

def build_job_recommender_agent(kernel=None) -> ChatCompletionAgent:
    kernel = kernel or build_kernel()
    instructions = (
        "You are a job recommender agent. You receive a user profile and a list of job postings. "
        "Match jobs to the user's skills, experience, and preferences. Return the top recommendations as a JSON array. "
        "Call the tool resume_parser_plugin.parse_resume if resume text is provided to extract structured profile information."
    )
    return ChatCompletionAgent(
        name="job_recommender_agent",
        instructions=instructions,
        kernel=kernel,
    )
