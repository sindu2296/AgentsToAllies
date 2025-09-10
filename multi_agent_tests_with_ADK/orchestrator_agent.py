from google.adk.agents import Agent, BaseAgent
from typing import List, Dict

class NewsOrchestratorAgent(Agent):
    news_agents: Dict[str, BaseAgent]  # Declare as class attribute
    summarizer_agent: BaseAgent        # Declare as class attribute

    def __init__(self, model_name: str, news_agents: List[BaseAgent], summarizer_agent: BaseAgent):
        super().__init__(
            name="news_orchestrator",
            model=model_name,
            instruction="You are a comprehensive news aggregator. Your goal is to understand the user's news request, fetch relevant news from various sources, and provide a concise summary. You can delegate tasks to specialized news agents and a summarizer agent.",
            sub_agents=news_agents + [summarizer_agent] # Make sub-agents available
        )
        self.news_agents = {agent.name: agent for agent in news_agents}
        self.summarizer_agent = summarizer_agent

    async def execute(self, user_query: str) -> str:
        # 1. Intent Recognition and Delegation (LLM's core role)
        # The LLM will decide which news agent(s) to use based on the user_query
        # You can prompt it to output a specific JSON format or just rely on its tool calling.

        # Example: Dynamic tool calling based on LLM reasoning
        # For simplicity, let's hardcode a basic delegation based on keywords.
        # In a real scenario, the LLM would reason about this.

        if "tech" in user_query.lower():
            target_agent = self.news_agents.get("tech_news_agent") # Corrected key
            query_for_agent = user_query.replace("tech", "").strip()
        elif "sports" in user_query.lower():
            target_agent = self.news_agents.get("sports_news_agent") # Corrected key
            query_for_agent = user_query.replace("sports", "").strip()
        else:
            # Default to a general news search or use another specialized agent
            target_agent = self.news_agents.get("world_news_agent") # Assuming you have one
            query_for_agent = user_query

        if not target_agent:
            return "Sorry, I can't find a specialized agent for that news category."

        # 2. Fetch News (by calling the delegated agent)
        print(f"Orchestrator delegating to {target_agent.name} with query: '{query_for_agent}'")
        # ADK handles the A2A communication when you call sub-agent methods
        raw_articles = await target_agent.execute(query=query_for_agent) # Assuming execute expects a 'query'

        if not raw_articles:
            return f"No news found for '{user_query}' from {target_agent.name}."

        # 3. Summarize (using the summarizer agent)
        full_news_text = "\n\n".join([f"Title: {a['title']}\nSource: {a['source']}\nURL: {a['url']}\nDescription: {a['description']}" for a in raw_articles])
        print("Orchestrator sending articles for summarization...")
        summarized_news = await self.summarizer_agent.execute(text_to_summarize=full_news_text)

        # 4. Present the results
        return f"Here's your news:\n\n{summarized_news}"