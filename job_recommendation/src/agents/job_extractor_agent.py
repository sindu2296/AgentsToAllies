from semantic_kernel.agents import ChatCompletionAgent
from config import build_kernel

def build_job_extractor_agent(kernel=None) -> ChatCompletionAgent:
    kernel = kernel or build_kernel()
    instructions = (
        "You are a job extractor agent in a sequential workflow. "
        "When given a user profile (skills, experience, job title), call the job_board_plugin-search_jobs function with that profile. "
        "The function will return job postings as JSON. "
        "Return ONLY the JSON output from the function - do not add commentary or ask questions. "
        "Pass the JSON directly to the next agent."
    )
    return ChatCompletionAgent(
        name="job_extractor_agent",
        instructions=instructions,
        kernel=kernel,
    )
