# Example for a hypothetical NewsAPI tool
import requests
import os
from dotenv import load_dotenv

def fetch_articles_from_newsapi(category: str, limit: int = 6) -> list:
    """
    Fetches news articles from NewsAPI based on a query and optional category.
    """
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("NEWSAPI_API_KEY")
    if not api_key:
        raise ValueError("NEWSAPI_API_KEY not set in environment variables.")

    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "pageSize": limit,
        "country": "us",
        "category": category
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raise an exception for HTTP errors
        data = response.json()
        articles = []
        for article in data.get("articles", []):
            articles.append({
                "title": article.get("title"),
                "author": article.get("author"),
                "source": article.get("source", {}).get("name"),
                "url": article.get("url"),
                "description": article.get("description")
            })
        return articles
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news from NewsAPI: {e}")
        return []

if __name__=="__main__":
    # Example usage
    category = "technology"
    articles = fetch_articles_from_newsapi(category=category)
    print(f"Fetched {len(articles)} articles for category '{category}':")
    for article in articles:
        print(f"- {article['title']} {[article['author']]} ({article['source']}) - {article['url']}")
        if article['description']:
            print(f"  Description: {article['description']}")
        else:
            print("  No description available.")
        print("----------------------------------------")
# You'd define similar functions for other news APIs (e.g., GNews API, Alpha Vantage, etc.)