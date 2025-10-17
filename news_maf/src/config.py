"""
Configuration for Microsoft Agent Framework news agents.
Uses Azure OpenAI with API key authentication.
"""
import os
from dotenv import load_dotenv
from agent_framework.azure import AzureOpenAIChatClient

load_dotenv()

# Azure OpenAI configuration
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("MODEL_NAME")

def build_chat_client() -> AzureOpenAIChatClient:
    """
    Creates an Azure OpenAI chat client for Agent Framework.
    
    Uses API key from environment variables for authentication.
    """
    return AzureOpenAIChatClient(
        api_key=api_key,
        endpoint=endpoint,
        deployment_name=deployment
    )
