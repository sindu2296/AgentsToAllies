"""
Flight search plugin for GHC Travel Planner.
Searches for flights from Seattle to Chicago using SerpAPI Google Flights.
"""
import os
import json
import requests
from typing import Annotated
from dotenv import load_dotenv

load_dotenv()

def search_flights(
    travel_dates: Annotated[str, "Travel dates in format 'YYYY-MM-DD to YYYY-MM-DD'"],
    preferences: Annotated[str, "Flight preferences like 'direct flights only', 'budget airline', etc."]
) -> str:
    """
    Search for flights from Seattle to Chicago for GHC 2025.
    
    Args:
        travel_dates: Travel dates (e.g., "2025-11-04 to 2025-11-07")
        preferences: Flight preferences (e.g., "direct flights, economy class")
        
    Returns:
        JSON string with flight options
    """
    
    print(f"[FLIGHT PLUGIN] Searching flights for: {travel_dates}")
    print(f"[FLIGHT PLUGIN] Preferences: {preferences}")
    
    # Parse dates
    try:
        departure_date, return_date = travel_dates.split(" to ")
    except:
        departure_date = "2025-11-04"
        return_date = "2025-11-07"
    
    # Check for SerpAPI key
    api_key = os.getenv("SERPAPI_API_KEY")
    
    if not api_key:
        # Return mock data if no API key
        print("[FLIGHT PLUGIN] No SERPAPI_API_KEY found, using mock data")
        mock_flights = [
            {
                "airline": "United Airlines",
                "flight_number": "UA 1234",
                "departure_time": f"{departure_date} 08:00 AM",
                "arrival_time": f"{departure_date} 02:15 PM",
                "duration": "4h 15m",
                "stops": "Direct",
                "price": "$320",
                "departure_airport": "SEA (Seattle)",
                "arrival_airport": "ORD (Chicago)",
                "cabin_class": "Economy"
            },
            {
                "airline": "Alaska Airlines",
                "flight_number": "AS 5678",
                "departure_time": f"{departure_date} 10:30 AM",
                "arrival_time": f"{departure_date} 04:45 PM",
                "duration": "4h 15m",
                "stops": "Direct",
                "price": "$295",
                "departure_airport": "SEA (Seattle)",
                "arrival_airport": "ORD (Chicago)",
                "cabin_class": "Economy"
            },
            {
                "airline": "Southwest Airlines",
                "flight_number": "WN 9012",
                "departure_time": f"{departure_date} 06:00 AM",
                "arrival_time": f"{departure_date} 12:15 PM",
                "duration": "4h 15m",
                "stops": "Direct",
                "price": "$275",
                "departure_airport": "SEA (Seattle)",
                "arrival_airport": "MDW (Chicago Midway)",
                "cabin_class": "Economy"
            }
        ]
        
        print(f"[FLIGHT PLUGIN] Found {len(mock_flights)} mock flights")
        return json.dumps(mock_flights)
    
    # Real SerpAPI search using requests
    url = "https://serpapi.com/search.json"
    params = {
        "api_key": api_key,
        "engine": "google_flights",
        "departure_id": "SEA",
        "arrival_id": "ORD",
        "outbound_date": departure_date,
        "return_date": return_date,
        "currency": "USD",
        "hl": "en"
    }
    
    try:
        resp = requests.get(url, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json() or {}
        
        flights = []
        if "best_flights" in data:
            for flight in data["best_flights"][:3]:  # Top 3 flights
                flights.append({
                    "airline": flight.get("flights", [{}])[0].get("airline", "Unknown"),
                    "flight_number": flight.get("flights", [{}])[0].get("flight_number", "N/A"),
                    "departure_time": flight.get("flights", [{}])[0].get("departure_airport", {}).get("time", "N/A"),
                    "arrival_time": flight.get("flights", [{}])[0].get("arrival_airport", {}).get("time", "N/A"),
                    "duration": flight.get("total_duration", "N/A"),
                    "stops": "Direct" if len(flight.get("flights", [])) == 1 else f"{len(flight.get('flights', [])) - 1} stop(s)",
                    "price": f"${flight.get('price', 0)}",
                    "departure_airport": "SEA (Seattle)",
                    "arrival_airport": "ORD (Chicago)",
                    "cabin_class": "Economy"
                })
        
        print(f"[FLIGHT PLUGIN] Found {len(flights)} flights from SerpAPI")
        return json.dumps(flights if flights else mock_flights[:2])
        
    except requests.RequestException as e:
        error_msg = f"SerpAPI error: {e}, using mock data"
        print(f"[FLIGHT PLUGIN ERROR] {error_msg}")
        return json.dumps(mock_flights[:2])
