import os
import asyncio
from dotenv import load_dotenv
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
 
load_dotenv()

model_name = os.getenv("MODEL_NAME")
deployment = model_name

async def main():
    client = AzureOpenAIChatClient(
        credential=AzureCliCredential(),
        deployment_name=deployment
    )

    agent = client.create_agent(
        instructions="You are good at telling jokes.",
        name="Joker"
    )
 
    result = await agent.run("Tell me a joke about a pirate.")
    print(result.text)
 
asyncio.run(main())