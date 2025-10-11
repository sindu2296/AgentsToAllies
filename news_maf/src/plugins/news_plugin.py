"""
News plugin for Agent Framework.
Provides a function tool for fetching news from NewsAPI.
"""
import os
import json
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

def fetch_top_headlines(category: str, limit: int = 6) -> str:
    """
    Fetch top headlines from NewsAPI for a given category.
    
    Args:
        category: News category (technology, sports, business, science, health, entertainment, general)
        limit: Maximum number of articles to return (default: 6)
    
    Returns:
        JSON string containing array of articles with title, author, source, url, description
    """
    api_key = os.getenv("NEWSAPI_API_KEY")
    if not api_key:
        return json.dumps({"error": "NEWSAPI_API_KEY not set"})

    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "pageSize": limit,
        "country": "us",
        "category": category,
    }
    
    try:
        resp = requests.get(url, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json() or {}
        articles_out: List[Dict[str, Any]] = []
        
        for a in data.get("articles", []):
            articles_out.append({
                "title": a.get("title"),
                "author": a.get("author"),
                "source": (a.get("source") or {}).get("name"),
                "url": a.get("url"),
                "description": a.get("description"),
            })
        
        return json.dumps(articles_out[:limit])
    except requests.RequestException as e:
        return json.dumps({"error": f"NewsAPI error: {e}"})
