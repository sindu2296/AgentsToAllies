from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel import Kernel

def build_category_agent(kernel: Kernel, name: str, category: str) -> ChatCompletionAgent:
    instructions = (
        f"You are a news retriever for the '{category}' category. "
        f"When asked for news, call the function news.fetch_top_headlines with category='{category}'. "
        "If the function returns JSON, pass it along verbatim unless asked to summarize."
    )
    return ChatCompletionAgent(
        name=name,
        instructions=instructions,
        kernel=kernel,
    )
