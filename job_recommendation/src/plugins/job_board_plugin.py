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
            "Search for jobs using SerpAPI for a given user profile. "
            "Returns a compact JSON string with title, company, location, url, description."
        ),
    )
    def search_jobs(self, user_profile: str, limit: int = 5) -> str:
        serpapi_key = os.getenv("SERPAPI_API_KEY")
        if not serpapi_key:
            raise ValueError("SERPAPI_API_KEY not set.")
        print("Searching jobs for query:", user_profile)
        url = "https://serpapi.com/search.json"
        params = {
            "api_key": serpapi_key,
            "engine": "google_jobs",
            "q": user_profile,
            "num": limit,
        }
        try:
            resp = requests.get(url, params=params, timeout=20)
            resp.raise_for_status()
            data = resp.json() or {}
            #print("SerpAPI raw response:", data)
            jobs_out = []
            for job in data.get("jobs_results", []):
                desc = job.get("description") or ""
                # Limit description to 100 words
                desc_words = desc.split()
                if len(desc_words) > 100:
                    desc = " ".join(desc_words[:100]) + "..."
                jobs_out.append({
                    "title": job.get("title"),
                    "company": job.get("company"),
                    "location": job.get("location"),
                    "description": desc,
                })
            #print("Extracted jobs:", jobs_out)
            return json.dumps(jobs_out)
        except Exception as e:
            return json.dumps({"error": str(e)})
