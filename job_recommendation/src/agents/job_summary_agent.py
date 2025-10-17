from semantic_kernel.agents import ChatCompletionAgent
from config import build_kernel

def build_job_summary_agent(kernel=None) -> ChatCompletionAgent:
    kernel = kernel or build_kernel()
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
    return ChatCompletionAgent(
        name="job_summary_agent",
        instructions=instructions,
        kernel=kernel,
    )
