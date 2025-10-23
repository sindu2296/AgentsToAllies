"""
Hotel search plugin for GHC Travel Planner.
Searches for hotels near Grace Hopper Conference venue in Chicago.
"""
import os
import json
import requests
from typing import Annotated
from dotenv import load_dotenv

load_dotenv()

# GHC 2025 venue information
GHC_VENUE = "McCormick Place, Chicago"
GHC_ADDRESS = "2301 S Dr Martin Luther King Jr Dr, Chicago, IL 60616"

def search_hotels(
    travel_dates: Annotated[str, "Check-in and check-out dates in format 'YYYY-MM-DD to YYYY-MM-DD'"],
    budget: Annotated[str, "Budget preference like 'under $200/night', 'mid-range', 'luxury'"]
) -> str:
    """
    Search for hotels near GHC 2025 venue in Chicago.
    
    Args:
        travel_dates: Stay dates (e.g., "2025-11-04 to 2025-11-07")
        budget: Budget preference (e.g., "under $200 per night")
        
    Returns:
        JSON string with hotel options near McCormick Place
    """
    
    print(f"[HOTEL PLUGIN] Searching hotels for: {travel_dates}")
    print(f"[HOTEL PLUGIN] Budget: {budget}")
    print(f"[HOTEL PLUGIN] Near: {GHC_VENUE}")
    
    # Parse dates
    try:
        checkin_date, checkout_date = travel_dates.split(" to ")
    except:
        checkin_date = "2025-11-04"
        checkout_date = "2025-11-07"
    
    # Check for SerpAPI key
    api_key = os.getenv("SERPAPI_API_KEY")
    
    if not api_key:
        # Return mock data if no API key
        print("[HOTEL PLUGIN] No SERPAPI_API_KEY found, using mock data")
        mock_hotels = [
            {
                "name": "Hyatt Regency McCormick Place",
                "address": "2233 S Dr Martin Luther King Jr Dr, Chicago, IL 60616",
                "distance_to_venue": "0.2 miles (5 min walk)",
                "rating": "4.3",
                "reviews": "2,847 reviews",
                "price_per_night": "$189",
                "total_price": "$756 (4 nights)",
                "amenities": ["Free WiFi", "Gym", "Restaurant", "Connected to convention center"],
                "description": "Connected directly to McCormick Place via skybridge. Perfect for GHC attendees."
            },
            {
                "name": "Hotel Chicago Downtown, Autograph Collection",
                "address": "1 W Washington St, Chicago, IL 60602",
                "distance_to_venue": "4.2 miles (12 min drive)",
                "rating": "4.5",
                "reviews": "1,234 reviews",
                "price_per_night": "$175",
                "total_price": "$700 (4 nights)",
                "amenities": ["Free WiFi", "Gym", "Rooftop bar", "Downtown location"],
                "description": "Stylish downtown hotel with easy access to Loop and McCormick Place via transit."
            },
            {
                "name": "Fairfield Inn & Suites Chicago Downtown/River North",
                "address": "216 E Ontario St, Chicago, IL 60611",
                "distance_to_venue": "5.1 miles (15 min drive)",
                "rating": "4.2",
                "reviews": "956 reviews",
                "price_per_night": "$149",
                "total_price": "$596 (4 nights)",
                "amenities": ["Free breakfast", "Free WiFi", "Gym", "Near Magnificent Mile"],
                "description": "Budget-friendly option in River North with complimentary breakfast."
            },
            {
                "name": "Residence Inn Chicago Downtown/Loop",
                "address": "11 S LaSalle St, Chicago, IL 60603",
                "distance_to_venue": "4.5 miles (13 min drive)",
                "rating": "4.4",
                "reviews": "1,567 reviews",
                "price_per_night": "$195",
                "total_price": "$780 (4 nights)",
                "amenities": ["Free breakfast", "Kitchenette", "Free WiFi", "Gym"],
                "description": "Extended-stay hotel in the Loop with full kitchens in rooms."
            }
        ]
        
        print(f"[HOTEL PLUGIN] Found {len(mock_hotels)} mock hotels")
        return json.dumps(mock_hotels)
    
    # Real SerpAPI search using requests
    url = "https://serpapi.com/search.json"
    params = {
        "api_key": api_key,
        "engine": "google_hotels",
        "q": "hotels near McCormick Place Chicago",
        "check_in_date": checkin_date,
        "check_out_date": checkout_date,
        "adults": "1",
        "currency": "USD",
        "gl": "us",
        "hl": "en"
    }
    
    try:
        resp = requests.get(url, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json() or {}
        
        hotels = []
        if "properties" in data:
            for hotel in data["properties"][:4]:  # Top 4 hotels
                hotels.append({
                    "name": hotel.get("name", "Unknown Hotel"),
                    "address": hotel.get("link", ""),
                    "distance_to_venue": hotel.get("nearby_places", [{}])[0].get("distance", "N/A"),
                    "rating": str(hotel.get("overall_rating", "N/A")),
                    "reviews": f"{hotel.get('reviews', 0)} reviews",
                    "price_per_night": f"${hotel.get('rate_per_night', {}).get('lowest', 'N/A')}",
                    "total_price": f"${hotel.get('total_rate', {}).get('lowest', 'N/A')}",
                    "amenities": hotel.get("amenities", [])[:4],
                    "description": hotel.get("description", "")[:150] + "..."
                })
        
        print(f"[HOTEL PLUGIN] Found {len(hotels)} hotels from SerpAPI")
        return json.dumps(hotels if hotels else mock_hotels)
        
    except requests.RequestException as e:
        error_msg = f"SerpAPI error: {e}, using mock data"
        print(f"[HOTEL PLUGIN ERROR] {error_msg}")
        return json.dumps(mock_hotels)
