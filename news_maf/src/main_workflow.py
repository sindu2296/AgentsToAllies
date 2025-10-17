"""
News Workflow Demo - Workflow-Centric Approach

This demo showcases a true workflow pattern where:
- The workflow orchestrates a complete business process
- Agents are components within the workflow
- Clear stages with data flow between them
- Business logic and AI agents are separated
"""
import asyncio
import logging

from config import build_chat_client
from orchestration.news_workflow import NewsGatheringWorkflow

# Enable logging to see workflow stages
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s',
    force=True
)

# Suppress verbose HTTP request logs from Azure OpenAI client
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('openai').setLevel(logging.WARNING)
logging.getLogger('azure').setLevel(logging.WARNING)


async def main():
    """
    Demonstrates the News Gathering Workflow.
    
    Grace Hopper Conference & Workshop Demo:
    This workflow demonstrates how AI agents work together in a business process
    to gather and summarize news about technology, diversity, and innovation.
    """
    print("\n" + "="*80)
    print("MULTI-AGENT NEWS WORKFLOW - Grace Hopper Conference Workshop")
    print("="*80)
    print("\nWorkflow Demonstration:")
    print("  • Stage 1: Analyze user query → Select news categories")
    print("  • Stage 2: Fetch articles from multiple sources in parallel")
    print("  • Stage 3: Remove duplicate articles")
    print("  • Stage 4: Generate executive summary")
    print("\n" + "="*80 + "\n")
    
    # Initialize workflow
    chat_client = build_chat_client()
    workflow = NewsGatheringWorkflow(chat_client=chat_client)
    
    # Example queries for Grace Hopper Conference workshop
    queries = [
        "What's new in AI and technology for women in computing?",
        "Latest news on diversity and inclusion in tech companies",
        "Recent developments in cybersecurity and data privacy"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*80}")
        print(f"WORKFLOW EXECUTION {i}/{len(queries)}")
        print(f"{'='*80}")
        print(f"Query: {query}")
        print(f"{'-'*80}\n")
        
        # Execute the complete workflow
        result = await workflow.execute(query)
        
        print(f"\n{'-'*80}")
        print("WORKFLOW OUTPUT:")
        print(f"{'-'*80}")
        print(result)
        print(f"{'='*80}\n")


if __name__ == "__main__":
    asyncio.run(main())
