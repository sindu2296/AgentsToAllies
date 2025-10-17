# https://ai.azure.com/build/deployments/aoai/connections/ai-myaihub247689594485_aoai/gpt-5-mini?wsid=/subscriptions/a6d87861-33e5-4578-8a0d-54be2196b868/resourceGroups/my-ai-resources/providers/Microsoft.MachineLearningServices/workspaces/my-ai-project&tid=bceb0489-2ee1-4115-abe4-ec10d29dbce1
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
model_name = os.getenv("MODEL_NAME")
deployment = model_name

subscription_key = os.getenv("AI_FOUNDRY_AZURE_OPENAI_API_KEY")
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key
)

response = client.chat.completions.create(
    # This sample demonstrates a basic call to the chat completion API. The call is synchronous.
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",  
        },
        {
            "role": "user",
            "content": "I am going to Paris, give me top 3 things to do?",
        }
    ],
    
    # This sample demonstrates a multi-turn conversation with the chat completion API. When using the model for a chat application,
    # you'll need to manage the history of that conversation and send the latest messages to the model.
    # messages=[
    #     {
    #         "role": "system",
    #         "content": "You are a helpful assistant.",
    #     },
    #     {
    #         "role": "user",
    #         "content": "I am going to Paris, what should I see?",
    #     },
    #     {
    #         "role": "assistant",
    #         "content": "Paris, the capital of France, is known for its stunning architecture, art museums, historical landmarks, and romantic atmosphere. Here are some of the top attractions to see in Paris:\n \n 1. The Eiffel Tower: The iconic Eiffel Tower is one of the most recognizable landmarks in the world and offers breathtaking views of the city.\n 2. The Louvre Museum: The Louvre is one of the world's largest and most famous museums, housing an impressive collection of art and artifacts, including the Mona Lisa.\n 3. Notre-Dame Cathedral: This beautiful cathedral is one of the most famous landmarks in Paris and is known for its Gothic architecture and stunning stained glass windows.\n \n These are just a few of the many attractions that Paris has to offer. With so much to see and do, it's no wonder that Paris is one of the most popular tourist destinations in the world.",
    #     },
    #     {
    #         "role": "user",
    #         "content": "What is so great about #1?",
    #     }
    # ],
    model=deployment
)

print(response.choices[0].message.content)