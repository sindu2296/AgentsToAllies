from semantic_kernel.agents import ChatCompletionAgent
from ..config import build_kernel

def build_job_summary_agent(kernel=None) -> ChatCompletionAgent:
    kernel = kernel or build_kernel()
    instructions = (
        "You are a concise job description summarizer. You receive a job posting with fields such as title, company, location, and description. "
        "Produce a 5-bullet executive summary highlighting the key aspects, requirements, and benefits. If the job description is missing, say so. "
        "Return the summary as plain text."
    )
    return ChatCompletionAgent(
        name="job_summary_agent",
        instructions=instructions,
        kernel=kernel,
    )
