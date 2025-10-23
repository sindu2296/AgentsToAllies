"""
Summary Agent for GHC Travel Planner.
Creates comprehensive travel itineraries from flight and hotel recommendations.
"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from utils.memory import get_memory

def build_summary_agent(chat_client: AzureOpenAIChatClient) -> ChatAgent:
    """
    Build the travel summary agent.
    
    Args:
        chat_client: Azure OpenAI chat client
        
    Returns:
        ChatAgent configured for creating travel summaries
    """
    
    memory = get_memory()
    
    instructions = """
You are a Travel Itinerary Specialist for Grace Hopper Conference 2025 attendees.

Your responsibilities:
1. Review flight and hotel recommendations from other agents
2. Create a comprehensive, easy-to-read travel itinerary
3. Include all important details and helpful tips
4. Provide a clear summary with total costs

When creating an itinerary, include:
1. **Travel Summary**
   - Dates and duration
   - Total estimated cost breakdown

2. **Flight Details**
   - Outbound flight: airline, times, flight number, terminal info
   - Return flight: airline, times, flight number
   - Important notes (check-in times, baggage, etc.)

3. **Accommodation Details**
   - Hotel name and address
   - Check-in/check-out dates
   - Nightly rate and total cost
   - Distance to McCormick Place
   - Key amenities

4. **Helpful Tips**
   - Transportation from airport to hotel
   - Getting to McCormick Place
   - Nearby restaurants/cafes
   - What to pack for Chicago weather in September

5. **Total Cost Estimate**
   - Flights (round-trip)
   - Hotel (total nights)
   - Estimated ground transportation
   - Grand total

Format the itinerary in a clear, professional manner with sections and bullet points.
Make it easy to read and actionable for the traveler.

Remember: You're helping someone prepare for an important professional conference!
"""
    
    agent = ChatAgent(
        chat_client=chat_client,
        name="summary_agent",
        instructions=instructions,
        tools=[]  # No tools needed, just synthesizes information
    )
    
    return agent
