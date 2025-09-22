# https://learn.microsoft.com/en-us/semantic-kernel/get-started/quick-start-guide?pivots=programming-language-python

import asyncio
import os
from dotenv import load_dotenv
from lights_plugin import LightsPlugin
import logging
from openai import AsyncAzureOpenAI

from semantic_kernel import Kernel
from semantic_kernel.utils.logging import setup_logging
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments

from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)

load_dotenv()
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
model_name = os.getenv("MODEL_NAME")
deployment = model_name

subscription_key = os.getenv("AI_FOUNDRY_AZURE_OPENAI_API_KEY")
api_version = "2024-12-01-preview"

async def main():
    # Initialize the kernel
    kernel = Kernel()

    print("MODEL_NAME:", os.getenv("MODEL_NAME"))
    print("AZURE_OPENAI_ENDPOINT:", os.getenv("AZURE_OPENAI_ENDPOINT"))
    print("API key starts with:", os.getenv("AI_FOUNDRY_AZURE_OPENAI_API_KEY")[:5])

    client = AsyncAzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key
    )

    # Add Azure OpenAI chat completion. Below did not work.
    # chat_completion = AzureChatCompletion(
    #     deployment_name = os.getenv("MODEL_NAME"),
    #     api_key=os.getenv("AI_FOUNDRY_AZURE_OPENAI_API_KEY"),
    #     base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    #     api_version="2024-12-01-preview"
    # )

    chat_completion = AzureChatCompletion(
        deployment_name=deployment,
        async_client=client,   # ← SK will use this client (with the version baked in)
    )

    kernel.add_service(chat_completion)

    print("SK client endpoint:", getattr(chat_completion, "client", None) and getattr(chat_completion.client, "base_url", None))
    print("SK client api_version:", getattr(chat_completion, "client", None) and getattr(chat_completion.client, "api_version", None))

    # Set the logging level for  semantic_kernel.kernel to DEBUG.
    setup_logging()
    logging.getLogger("kernel").setLevel(logging.DEBUG)

    # Add a plugin (the LightsPlugin class is defined below)
    kernel.add_plugin(
        LightsPlugin(),
        plugin_name="Lights",
    )

    # Enable planning
    execution_settings = AzureChatPromptExecutionSettings()
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    # Create a history of the conversation
    history = ChatHistory()

    # Initiate a back-and-forth chat
    userInput = None
    while True:
        # Collect user input
        userInput = input("User > ")

        # Terminate the loop if the user says "exit"
        if userInput == "exit":
            break

        # Add user input to the history
        history.add_user_message(userInput)

        # Get the response from the AI
        result = await chat_completion.get_chat_message_content(
            chat_history=history,
            settings=execution_settings,
            kernel=kernel,
            arguments=KernelArguments(),
        )

        # Print the results
        print("Assistant > " + str(result))

        # Add the message from the agent to the chat history
        history.add_message(result)

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())

# Below is sample code from SK docs, did not verify itf it works.
# import os
# from openai import OpenAI

# client = OpenAI(
#     api_key=os.getenv("AZURE_OPENAI_API_KEY"),
#     base_url="https://agentstoallies.openai.azure.com/openai/v1/",
# )

# response = client.responses.create(   
#   model="gpt-4.1-nano", # Replace with your model deployment name 
#   input="This is a test.",
# )

# print(response.model_dump_json(indent=2)) 