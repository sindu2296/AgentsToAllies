import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
 
async def main():
    agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
        instructions="You are good at telling jokes.",
        name="Joker"
    )
 
    result = await agent.run("Tell me a joke about a pirate.")
    print(result.text)
 
asyncio.run(main())