import os
import json
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv
from semantic_kernel.functions import kernel_function

load_dotenv()  # Load environment variables from .env file

class NewsPlugin:
    """Native plugin exposing NewsAPI as a callable SK function."""

    @kernel_function(
        name="fetch_top_headlines",
        description=(
            "Fetch top headlines from NewsAPI for a given category. "
            "Returns a compact JSON string with title, author, source, url, description."
        ),
    )
    def fetch_top_headlines(self, category: str, limit: int = 6) -> str:
        load_dotenv()
        api_key = os.getenv("NEWSAPI_API_KEY")
        if not api_key:
            raise ValueError("NEWSAPI_API_KEY not set.")

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
                articles_out.append(
                    {
                        "title": a.get("title"),
                        "author": a.get("author"),
                        "source": (a.get("source") or {}).get("name"),
                        "url": a.get("url"),
                        "description": a.get("description"),
                    }
                )
            return json.dumps(articles_out[:limit])
        except requests.RequestException as e:
            return json.dumps({"error": f"NewsAPI error: {e}"})