"""
Sequential GHC Travel Planner Demo - Microsoft Agent Framework

Demonstrates sequential processing of travel planning for Grace Hopper Conference 2025.
Flow: Flight Search → Hotel Search → Travel Summary
"""
import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import build_chat_client
from orchestration.sequential_orchestrator import run_sequential_travel_workflow
from utils.memory import reset_memory

async def main():
    """
    Sequential GHC Travel Planner Demo using Microsoft Agent Framework
    
    Processes travel planning sequentially: flights first, then hotels, then summary.
    """
    chat_client = build_chat_client()

    # Example user queries for GHC 2025
    user_queries = [
        """
        I need help planning my trip to Grace Hopper Conference 2025 in Chicago.
        
        Travel Dates: November 4-7, 2025
        
        Flight Preferences:
        - Flying from Seattle
        - Prefer direct flights
        - Would like to arrive by early afternoon on Nov 4
        - Economy class is fine
        
        Hotel Preferences:
        - Budget: under $200 per night
        - Close to McCormick Place (walking distance preferred)
        - Need WiFi for work
        
        Please find the best options for both flights and accommodation!
        """,
        
        # Uncomment for more examples:
        # """
        # Planning GHC 2025 trip from Seattle to Chicago.
        # Dates: Nov 3-8, 2025 (arriving day before conference)
        # Flight: Direct flights only, flexible on timing, economy
        # Hotel: Budget around $150/night, prefer connected to venue or very close
        # """
    ]

    for i, user_query in enumerate(user_queries, start=1):
        print("\n" + "="*80)
        print(f"TRAVEL PLANNING REQUEST #{i}")
        print("="*80)
        print(user_query.strip())
        print("="*80)
        
        # Reset memory for each new query
        reset_memory()
        
        result = await run_sequential_travel_workflow(chat_client, user_query)
        
        print(result)
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
