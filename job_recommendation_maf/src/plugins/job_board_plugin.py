"""
Job board plugin for Agent Framework.
Provides a function tool for fetching jobs from SerpAPI (Google Jobs).
"""
import os
import json
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

def search_jobs(user_profile: str, limit: int = 5) -> str:
    """
    Search for jobs using SerpAPI (Google Jobs) based on a user profile.
    
    Args:
        user_profile: User profile description (e.g., "software engineer 2 with Python experience")
        limit: Maximum number of jobs to return (default: 5)
    
    Returns:
        JSON string containing array of jobs with title, company, location, description
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return json.dumps({"error": "SERPAPI_API_KEY not set"})
    
    print(f"[PLUGIN] Searching jobs for: {user_profile}")
    
    url = "https://serpapi.com/search.json"
    params = {
        "api_key": api_key,
        "engine": "google_jobs",
        "q": user_profile,
        "num": limit,
    }
    
    try:
        resp = requests.get(url, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json() or {}
        
        jobs_out: List[Dict[str, Any]] = []
        
        for job in data.get("jobs_results", []):
            desc = job.get("description") or ""
            
            # Limit description to 100 words
            desc_words = desc.split()
            if len(desc_words) > 100:
                desc = " ".join(desc_words[:100]) + "..."
            
            jobs_out.append({
                "title": job.get("title"),
                "company": job.get("company_name") or job.get("company"),
                "location": job.get("location"),
                "description": desc,
            })
        
        print(f"[PLUGIN] Found {len(jobs_out)} jobs")
        return json.dumps(jobs_out)
        
    except requests.RequestException as e:
        error_msg = f"SerpAPI error: {e}"
        print(f"[PLUGIN ERROR] {error_msg}")
        return json.dumps({"error": error_msg})
