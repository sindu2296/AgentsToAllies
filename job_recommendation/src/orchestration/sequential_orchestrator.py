
# Copyright (c) Microsoft. All rights reserved.
import asyncio
from ..config import build_kernel
from semantic_kernel.agents import ChatCompletionAgent, SequentialOrchestration
from semantic_kernel import Kernel
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.contents import ChatMessageContent
from ..agents.job_extractor_agent import build_job_extractor_agent
from ..agents.job_recommender_agent import build_job_recommender_agent
from ..agents.job_summary_agent import build_job_summary_agent
from ..utils.dedup_utils import deduplicate_jobs
from ..utils.job_cleaner_utils import clean_job_data

def get_agents(kernel: Kernel) -> list[ChatCompletionAgent]:
    """Return a list of agents for sequential orchestration."""
    extractor = build_job_extractor_agent(kernel)
    #recommender = build_job_recommender_agent(kernel)
    summarizer = build_job_summary_agent(kernel)
    return [extractor, summarizer]

def agent_response_callback(message: ChatMessageContent) -> None:
    print(f"# {message.name}\n{message.content}")

async def main():
    kernel = build_kernel()
    agents = get_agents(kernel)
    sequential_orchestration = SequentialOrchestration(
        members=agents,
        agent_response_callback=agent_response_callback,
    )
    runtime = InProcessRuntime()
    runtime.start()

    user_profile = "software engineer 2"
    orchestration_result = await sequential_orchestration.invoke(
        task=user_profile,
        runtime=runtime,
    )
    value = await orchestration_result.get(timeout=30)
    print(f"***** Final Result *****\n{value}")
    await runtime.stop_when_idle()

if __name__ == "__main__":
    asyncio.run(main())
