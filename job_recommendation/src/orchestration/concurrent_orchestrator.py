# Copyright (c) Microsoft. All rights reserved.
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent, ConcurrentOrchestration
from semantic_kernel.agents.runtime import InProcessRuntime
from agents.job_extractor_agent import build_job_extractor_agent
from agents.job_recommender_agent import build_job_recommender_agent
from agents.job_summary_agent import build_job_summary_agent

def get_agents(kernel: Kernel) -> list[ChatCompletionAgent]:
    """Return a list of agents for concurrent orchestration."""
    extractor = build_job_extractor_agent(kernel)
    recommender = build_job_recommender_agent(kernel)
    summarizer = build_job_summary_agent(kernel)
    return [extractor, recommender, summarizer]

async def main():
    kernel = Kernel()
    agents = get_agents(kernel)
    concurrent_orchestration = ConcurrentOrchestration(members=agents)
    runtime = InProcessRuntime()
    runtime.start()

    user_profile = "Experienced Python developer seeking remote AI/ML jobs in Europe."
    orchestration_result = await concurrent_orchestration.invoke(
        task=user_profile,
        runtime=runtime,
    )
    value = await orchestration_result.get(timeout=30)
    for item in value:
        print(f"# {item.name}: {item.content}")
    await runtime.stop_when_idle()

if __name__ == "__main__":
    asyncio.run(main())
