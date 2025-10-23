"""
Flight Agent for GHC Travel Planner.
Searches for best flight options from Seattle to Chicago and stores user preferences.
"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from plugins.flight_search_plugin import search_flights
from utils.memory import get_memory

def build_flight_agent(chat_client: AzureOpenAIChatClient) -> ChatAgent:
    """
    Build the flight search agent with memory capabilities.
    
    Args:
        chat_client: Azure OpenAI chat client
        
    Returns:
        ChatAgent configured for flight search
    """
    
    memory = get_memory()
    
    instructions = """
You are a Flight Search Specialist for Grace Hopper Conference 2025 attendees.

Your responsibilities:
1. Search for flights from Seattle (SEA) to Chicago (ORD/MDW)
2. Analyze flight options based on user preferences (direct flights, timing, price)
3. Store user preferences in memory for future reference
4. Recommend the best 2-3 flight options

Key Information:
- GHC 2025 is at McCormick Place in Chicago
- Most attendees prefer direct flights
- ORD (O'Hare) is closer to the venue than MDW (Midway)
- Consider arrival times - conference typically starts morning sessions

When you receive a query:
1. Extract travel dates and preferences
2. Store them in memory using the context
3. Call the search_flights tool
4. Analyze results and recommend best options
5. Explain why each flight is suitable

Always be helpful and consider the user's schedule and budget constraints.
"""
    
    agent = ChatAgent(
        chat_client=chat_client,
        name="flight_agent",
        instructions=instructions,
        tools=[search_flights]
    )
    
    return agent
