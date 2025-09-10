from google.adk.agents import Agent
# from google.adk.tools import Tool
from news_api import fetch_articles_from_newsapi

# Assuming you have fetch_articles_from_newsapi defined as above

class TechNewsAgent(Agent):
    def __init__(self, model_name: str):
        super().__init__(
            name="tech_news_agent",
            model=model_name,
            instruction="You are an expert in fetching and providing summaries of the latest technology news.",
        )             # tools=[lambda query: fetch_articles_from_newsapi(query=query, category="technology")]
    async def execute(self, query: str):
        # You can use the query if needed, or just ignore it and fetch tech news
        return fetch_articles_from_newsapi(category="technology")

class SportsNewsAgent(Agent):
    def __init__(self, model_name: str):
        super().__init__(
            name="sports_news_agent",
            model=model_name,
            instruction="You are an expert in fetching and providing summaries of the latest sports news."
            # tools=[lambda query: fetch_articles_from_newsapi(query=query, category="sports")]
            # tools=[
            #     Tool(
            #         name="fetch_sports_news",
            #         func=lambda query: fetch_articles_from_newsapi(query=query, category="sports"),
            #         description="Fetches recent sports news articles based on keywords."
            #     )
            # ]
        )
    async def execute(self, query: str):
        # You can use the query if needed, or just ignore it and fetch tech news
        return fetch_articles_from_newsapi(category="sports")

# ... create similar agents for other categories like World News, Business News, etc.