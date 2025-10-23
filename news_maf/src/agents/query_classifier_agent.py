"""
Query Classifier agent - determines relevant news categories.
"""
import logging
from typing import List
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient

logger = logging.getLogger(__name__)

CATEGORIES = ["technology", "sports", "business", "science", "health", "entertainment", "general"]

INSTRUCTIONS = """You are a query classifier. Analyze the user query and determine which news categories are most relevant.

Available categories: technology, sports, business, science, health, entertainment, general

Rules:
1. Select 1-3 most relevant categories
2. If no clear match, return ["general"]
3. Output ONLY a valid JSON array of category strings
4. NO markdown code blocks, NO explanations, NO extra text
5. Example output: ["technology", "business"]

Output format: ["category1", "category2"]"""


def build_query_classifier_agent(chat_client: AzureOpenAIChatClient) -> ChatAgent:
    """Create query classifier agent."""
    return ChatAgent(
        chat_client=chat_client,
        instructions=INSTRUCTIONS,
        name="query_classifier_agent"
    )


async def classify_query(classifier: ChatAgent, query: str) -> List[str]:
    """
    Classify query and return list of categories.
    
    Args:
        classifier: Query classifier agent
        query: User's news query
        
    Returns:
        List of category names (defaults to ["general"] on error)
    """
    try:
        result = await classifier.run(query)
        
        # Get response text
        response_text = result.text
        if not response_text:
            logger.warning("[CLASSIFIER] Empty response, using general")
            return ["general"]
        
        # Clean and parse
        response_text = response_text.strip()
        
        # Remove markdown fences if present
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            if lines[-1].strip() == "```":
                response_text = "\n".join(lines[1:-1]).strip()
            else:
                response_text = "\n".join(lines[1:]).strip()
        
        # Parse JSON
        import json
        categories = json.loads(response_text)
        
        if not isinstance(categories, list):
            logger.warning("[CLASSIFIER] Not a list, using general")
            return ["general"]
        
        # Filter to valid categories
        valid = [c.lower() for c in categories if isinstance(c, str) and c.lower() in CATEGORIES]
        return valid if valid else ["general"]
        
    except Exception as e:
        logger.error(f"[CLASSIFIER] Error: {e}, using general")
        return ["general"]
