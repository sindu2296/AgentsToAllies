"""
Configuration for GHC Travel Planner using Microsoft Agent Framework.
Sets up Azure OpenAI chat client for agent communication.
"""
import os
from dotenv import load_dotenv
from agent_framework.azure import AzureOpenAIChatClient

# Load environment variables
load_dotenv()

def build_chat_client() -> AzureOpenAIChatClient:
    """
    Build and return an Azure OpenAI chat client for agent interactions.
    
    Returns:
        AzureOpenAIChatClient configured with Azure OpenAI credentials
    """
    # Get credentials from environment
    api_key = os.getenv("AI_FOUNDRY_AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("MODEL_NAME") or os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
    
    if not all([api_key, endpoint, deployment_name]):
        raise ValueError(
            "Missing required environment variables. Please set:\n"
            "- AI_FOUNDRY_AZURE_OPENAI_API_KEY\n"
            "- AZURE_OPENAI_ENDPOINT\n"
            "- MODEL_NAME or AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"
        )
    
    # Create Azure OpenAI chat client
    chat_client = AzureOpenAIChatClient(
        api_key=api_key,
        endpoint=endpoint,
        deployment_name=deployment_name
    )
    
    return chat_client
