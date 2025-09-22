from ..config import build_kernel

class JobRecommenderAgent:
    """Recommends jobs based on user profile and extracted jobs."""
    def __init__(self, kernel=None):
        self.kernel = kernel or build_kernel()

    def run(self, user_profile, jobs):
        """
        Uses Semantic Kernel to recommend jobs based on user profile.
        """
        # Example: Use kernel to rank jobs by relevance to user_profile
        if not jobs:
            return []
from semantic_kernel.agents import ChatCompletionAgent
from ..config import build_kernel

def build_job_recommender_agent(kernel=None) -> ChatCompletionAgent:
    kernel = kernel or build_kernel()
    instructions = (
        "You are a job recommender agent. You receive a user profile and a list of job postings. "
        "Match jobs to the user's skills, experience, and preferences. Return the top recommendations as a JSON array. "
        "Call the tool resume_parser_plugin.parse_resume if resume text is provided to extract structured profile information."
    )
    return ChatCompletionAgent(
        name="job_recommender_agent",
        instructions=instructions,
        kernel=kernel,
    )
