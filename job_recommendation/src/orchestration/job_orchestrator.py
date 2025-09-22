import json
import logging
from semantic_kernel import Kernel
from ..agents.job_extractor_agent import build_job_extractor_agent
from ..agents.job_recommender_agent import build_job_recommender_agent
from ..agents.job_summary_agent import build_job_summary_agent
from ..plugins.job_board_plugin import JobBoardPlugin
from ..plugins.resume_parser_plugin import ResumeParserPlugin
from ..utils.dedup_utils import deduplicate_jobs
from ..utils.job_cleaner_utils import clean_job_data

class JobProOrchestrator:
    def __init__(self, kernel: Kernel):
        self.kernel = kernel
        self.extractor = build_job_extractor_agent(kernel)
        self.recommender = build_job_recommender_agent(kernel)
        self.summarizer = build_job_summary_agent(kernel)
        self.job_plugin = JobBoardPlugin()
        self.resume_plugin = ResumeParserPlugin()

    async def run(self, user_profile: str, resume_text: str = None) -> str:
        logging.info(f"[JOB] Processing user profile: {user_profile}")
        # Optionally parse resume
        parsed_resume = None
        if resume_text:
            async for msg in self.resume_plugin.parse_resume(resume_text):
                parsed_resume = msg.content.content
            logging.info(f"[JOB] Parsed resume: {parsed_resume}")

        # Step 1: Extract jobs using profile keywords
        jobs = []
        async for msg in self.extractor.invoke(user_profile):
            try:
                jobs.extend(json.loads(msg.content.content))
            except Exception:
                continue
        jobs = [clean_job_data(j) for j in jobs]
        jobs = deduplicate_jobs(jobs)
        logging.info(f"[JOB] Extracted {len(jobs)} jobs.")

        # Step 2: Recommend jobs
        recommended = []
        async for msg in self.recommender.invoke(json.dumps({"user_profile": user_profile, "jobs": jobs})):
            try:
                recommended.extend(json.loads(msg.content.content))
            except Exception:
                continue
        recommended = [clean_job_data(j) for j in recommended]
        recommended = deduplicate_jobs(recommended)
        logging.info(f"[JOB] Recommended {len(recommended)} jobs.")

        # Step 3: Summarize recommended jobs
        summaries = []
        for job in recommended:
            async for msg in self.summarizer.invoke(json.dumps(job)):
                summaries.append(msg.content.content)

        if not summaries:
            return "No job recommendations found."

        header = f"Job recommendations for: {user_profile}"
        return f"{header}\n\n" + "\n\n".join(summaries)
