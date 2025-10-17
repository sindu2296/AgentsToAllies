from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel import Kernel

def build_summarizer_agent(kernel: Kernel) -> ChatCompletionAgent:
    """
    Creates an agent that summarizes news articles into an executive brief.
    
    This agent takes a JSON array of articles and produces a concise,
    well-formatted summary with inline source citations.
    """
    instructions = (
        "You are an executive news summarizer. "
        "You receive JSON arrays of news articles with title, author, source, url, and description fields. "
        "Create a concise 5-bullet executive summary that highlights the most important information. "
        "Include inline source citations with URLs in markdown format like [Source Name](url). "
        "If you receive an error key in the JSON, report it clearly. "
        "Be concise, professional, and actionable in your summaries."
    )
    return ChatCompletionAgent(
        name="summarizer_agent",
        instructions=instructions,
        kernel=kernel,
    )
