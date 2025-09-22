# Example plugin for job data source integration
import os
import json
import requests
from dotenv import load_dotenv
from semantic_kernel.functions import kernel_function

load_dotenv()

class JobBoardPlugin:
    """Native plugin exposing SerpAPI as a callable SK function for job search."""

    @kernel_function(
        name="search_jobs",
        description=(
            "Search for jobs using SerpAPI for a given query (keywords, location, etc). "
            "Returns a compact JSON string with title, company, location, url, description."
        ),
    )
    def search_jobs(self, query: str, limit: int = 10) -> str:
        serpapi_key = os.getenv("SERPAPI_API_KEY")
        if not serpapi_key:
            raise ValueError("SERPAPI_API_KEY not set.")

        url = "https://serpapi.com/search.json"
        params = {
            "api_key": serpapi_key,
            "engine": "google_jobs",
            "q": query,
            "num": limit,
        }
        try:
            resp = requests.get(url, params=params, timeout=20)
            resp.raise_for_status()
            data = resp.json() or {}
            jobs_out = []
            for job in data.get("jobs_results", []):
                jobs_out.append({
                    "title": job.get("title"),
                    "company": job.get("company_name"),
                    "location": job.get("location"),
                    "url": job.get("job_id"),
                    "description": job.get("description"),
                })
            return json.dumps(jobs_out)
        except Exception as e:
            return json.dumps({"error": str(e)})
