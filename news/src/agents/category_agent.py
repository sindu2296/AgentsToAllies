from typing import Any, Dict, List, Optional

from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.functions import KernelArguments
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)


def build_category_agent(
    kernel: Kernel,
    name: str,
    category: str,
    memory: Optional[List[Dict[str, Any]]] = None,
) -> ChatCompletionAgent:
    """
    Creates an agent that fetches news for a specific category.
    
    The agent automatically calls the news.fetch_top_headlines function
    and returns the JSON result.
    """
    memory_hint = _build_memory_hint(memory)

    instructions = (
        f"You are a news fetcher for the '{category}' category. "
        f"Fetch news by calling news.fetch_top_headlines with category='{category}'. "
        "Return the JSON result exactly as received from the function."
    )
    if memory_hint:
        instructions += f" {memory_hint}"
    
    # Configure function-calling behavior explicitly for Azure Chat completions
    settings = AzureChatPromptExecutionSettings()
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    
    return ChatCompletionAgent(
        name=name,
        instructions=instructions,
        kernel=kernel,
        arguments=KernelArguments(settings=settings),
    )


def _build_memory_hint(memory: Optional[List[Dict[str, Any]]]) -> str:
    if not memory:
        return ""

    titles = []
    for article in memory:
        if not isinstance(article, dict):
            continue
        title = article.get("title") or article.get("headline")
        if title:
            titles.append(title)

    if not titles:
        return ""

    preview = " | ".join(titles[:3])
    return (
        "Previously surfaced headlines. Prefer fresh items or new angles: "
        f"{preview}"
    )
