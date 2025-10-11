from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.functions import KernelArguments

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
    
    # Configure the agent to automatically invoke functions
    settings = kernel.get_prompt_execution_settings_from_service_id()
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    
    return ChatCompletionAgent(
        name=name,
        instructions=instructions,
        kernel=kernel,
        arguments=KernelArguments(settings=settings),
    )
