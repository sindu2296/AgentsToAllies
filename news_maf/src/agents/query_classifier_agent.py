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

Select 1-3 most relevant categories. If no clear match, use "general".
Just list the category names, separated by commas or spaces."""


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
        response_text = result.text
        
        if not response_text:
            logger.warning("[CLASSIFIER] Empty response, using general")
            return ["general"]
        
        # Extract category names from response (handles "technology, business" or "technology business")
        response_text = response_text.lower().strip()
        
        # Find all valid categories mentioned in the response
        found_categories = []
        for category in CATEGORIES:
            if category in response_text:
                found_categories.append(category)
        
        # Return found categories or default to general
        return found_categories if found_categories else ["general"]
        
    except Exception as e:
        logger.error(f"[CLASSIFIER] Error: {e}, using general")
        return ["general"]
