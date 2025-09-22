from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel import Kernel

def build_summarizer_agent(kernel: Kernel) -> ChatCompletionAgent:
    instructions = (
        "You are a concise news summarizer. You receive a JSON array of articles with "
        "title, author, source, url, and description. Produce a 5-bullet executive summary "
        "with source names and include the URLs inline. If there's an error key, report it."
    )
    return ChatCompletionAgent(
        name="summarizer_agent",
        instructions=instructions,
        kernel=kernel,
    )
