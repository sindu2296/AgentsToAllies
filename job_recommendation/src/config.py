import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from openai import AsyncAzureOpenAI
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from plugins.job_board_plugin import JobBoardPlugin

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
model_name = os.getenv("MODEL_NAME")
deployment = model_name
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = "2024-12-01-preview"

def build_kernel() -> Kernel:
    # Initialize the kernel
    kernel = Kernel()

    # Initialize Azure OpenAI client
    client = AsyncAzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key
    )

    # Configure chat completion
    chat_completion = AzureChatCompletion(
        deployment_name=deployment,
        async_client=client,
    )

    # Add the service to the kernel
    kernel.add_service(chat_completion)

    # Register SerpAPI plugin (JobBoardPlugin)
    kernel.add_plugin(JobBoardPlugin(), plugin_name="job_board_plugin")

    return kernel
