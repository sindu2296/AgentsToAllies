"""
Configuration for Microsoft Agent Framework news agents.
Uses Azure OpenAI with AzureCliCredential for authentication.
"""
import os
from dotenv import load_dotenv
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

load_dotenv()

# Azure OpenAI configuration
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("MODEL_NAME")

def build_chat_client() -> AzureOpenAIChatClient:
    """
    Creates an Azure OpenAI chat client for Agent Framework.
    
    Uses Azure CLI credentials for authentication.
    Ensure you're logged in with `az login` before running.
    """
    return AzureOpenAIChatClient(
        credential=AzureCliCredential(),
        endpoint=endpoint,
        model_id=deployment
    )
