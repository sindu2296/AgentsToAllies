from semantic_kernel.agents import ChatCompletionAgent
from ..config import build_kernel

def build_job_extractor_agent(kernel=None) -> ChatCompletionAgent:
    kernel = kernel or build_kernel()
    instructions = (
        "You are a job extractor agent. When given a user profile or keywords, call the tool job_board_plugin.search_jobs with the query. "
        "Return the job postings as JSON. If the function returns JSON, pass it along verbatim unless asked to summarize."
    )
    return ChatCompletionAgent(
        name="job_extractor_agent",
        instructions=instructions,
        kernel=kernel,
    )
