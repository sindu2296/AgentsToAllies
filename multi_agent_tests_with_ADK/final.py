import os
from dotenv import load_dotenv
from news_source_agents import SportsNewsAgent,TechNewsAgent
from summarizer_agent import SummarizerAgent
from orchestrator_agent import NewsOrchestratorAgent

load_dotenv() # Load environment variables from .env file

# Choose your LLM model
# For Google's Gemini, use something like "gemini-1.5-flash" or "gemini-1.5-pro"
# Make sure to set GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION if using Vertex AI
# Or just GOOGLE_API_KEY if using Google AI Studio.
LLM_MODEL = "gemini-2.0-flash" # Or "gpt-4o" if using OpenAI, etc.

# Initialize your news agents
tech_agent = TechNewsAgent(model_name=LLM_MODEL)
sports_agent = SportsNewsAgent(model_name=LLM_MODEL)
# Add more specialized news agents as needed
# world_agent = WorldNewsAgent(model_name=LLM_MODEL)

# Initialize the summarizer agent
summarizer = SummarizerAgent(model_name=LLM_MODEL)

# Create the orchestrator with its sub-agents
orchestrator = NewsOrchestratorAgent(
    model_name=LLM_MODEL,
    news_agents=[tech_agent, sports_agent], # Add all your news source agents
    summarizer_agent=summarizer
)

# Run the system via ADK's web UI (great for testing)
# In your terminal, navigate to the directory containing your main script and run:
# adk web

# Or, programmatically interact with it:
async def main():
    while True:
        user_input = input("What news are you interested in? (e.g., 'latest tech news', 'sports news') or 'quit': ")
        if user_input.lower() == 'quit':
            break
        response = await orchestrator.execute(user_query=user_input)
        print("\n------------------------------")
        print(response)
        print("------------------------------\n")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())