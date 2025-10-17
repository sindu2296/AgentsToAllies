"""
Sequential Job Recommendation Demo - Microsoft Agent Framework

This demonstrates processing job recommendations sequentially using MAF.
Flow: Extract jobs → Recommend top matches → Summarize results
"""
import asyncio
from config import build_chat_client
from orchestration.sequential_orchestrator import run_sequential_job_workflow

async def main():
    """
    Sequential Job Recommendation Orchestrator Demo using Microsoft Agent Framework
    
    This demonstrates processing jobs through extraction, recommendation, and summarization.
    """
    chat_client = build_chat_client()

    # Example user profiles
    user_profiles = [
        "software engineer with Python and Azure cloud experience",
        # "data scientist with machine learning and AI background",
        # "full stack developer with React and Node.js skills",
    ]

    for user_profile in user_profiles:
        print("\n" + "="*80)
        print(f"USER PROFILE: {user_profile}")
        print("="*80)
        
        result = await run_sequential_job_workflow(chat_client, user_profile)
        
        print(result)
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
