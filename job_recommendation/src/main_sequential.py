"""
Sequential job recommendation workflow.
Demonstrates sequential orchestration using SequentialOrchestration:
- Extract jobs based on user profile
- Summarize jobs
Uses the built-in SequentialOrchestration class with InProcessRuntime.
"""
import asyncio

from config import build_kernel
from semantic_kernel.agents import SequentialOrchestration
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.contents import ChatMessageContent
from agents.job_extractor_agent import build_job_extractor_agent
from agents.job_summary_agent import build_job_summary_agent
from agents.job_recommender_agent import build_job_recommender_agent


def agent_response_callback(message: ChatMessageContent) -> None:
    """Callback to print agent responses during orchestration."""
    print(f"\n# {message.name}")
    print(f"{message.content}")


async def main():
    """Main sequential orchestration workflow using SequentialOrchestration."""
    kernel = build_kernel()
    
    # Build agents for sequential processing
    # Start with just extractor and summarizer for simpler workflow
    extractor = build_job_extractor_agent(kernel)
    recommender = build_job_recommender_agent(kernel)
    summarizer = build_job_summary_agent(kernel)
    
    # Create sequential orchestration with agents
    # Using just 2 agents to avoid timeout issues
    sequential_orchestration = SequentialOrchestration(
        members=[extractor, recommender, summarizer],
        agent_response_callback=agent_response_callback,
    )
    
    # Create and start the runtime
    runtime = InProcessRuntime()
    runtime.start()
    
    # Example user profiles
    user_profiles = [
        "software engineer 2 with Python experience",
        #"data scientist with machine learning background",
    ]
    
    try:
        for user_profile in user_profiles:
            print("\n" + "="*80)
            print(f"USER PROFILE: {user_profile}")
            print("="*80)
            
            # Invoke the sequential orchestration
            orchestration_result = await sequential_orchestration.invoke(
                task=user_profile,
                runtime=runtime,
            )
            
            # Get the final result with timeout
            value = await orchestration_result.get(timeout=60)
            
            print("\n" + "-"*80)
            print("***** FINAL RESULT *****")
            print("-"*80)
            print(value)
            print("\n")
    
    except Exception as e:
        print(f"\n!!! Error occurred: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Stop the runtime when done
        await runtime.stop_when_idle()


if __name__ == "__main__":
    asyncio.run(main())
