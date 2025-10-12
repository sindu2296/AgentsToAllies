from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.functions import KernelArguments
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)

def build_category_agent(kernel: Kernel, name: str, category: str) -> ChatCompletionAgent:
    """
    Creates an agent that fetches news for a specific category.
    
    The agent automatically calls the news.fetch_top_headlines function
    and returns the JSON result.
    """
    instructions = (
        f"You are a news fetcher for the '{category}' category. "
        f"Fetch news by calling news.fetch_top_headlines with category='{category}'. "
        "Return the JSON result exactly as received from the function."
    )
    
    # Configure function-calling behavior explicitly for Azure Chat completions
    settings = AzureChatPromptExecutionSettings()
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    
    return ChatCompletionAgent(
        name=name,
        instructions=instructions,
        kernel=kernel,
        arguments=KernelArguments(settings=settings),
    )
