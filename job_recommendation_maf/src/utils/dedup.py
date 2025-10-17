"""
Utility functions for deduplicating jobs.
"""
from typing import List, Dict, Any

def deduplicate_jobs(jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Deduplicate jobs by unique combination of title and company.
    
    Args:
        jobs: List of job dictionaries
        
    Returns:
        List of unique jobs
    """
    seen = set()
    deduped = []
    
    for job in jobs:
        # Create a unique key from title and company
        title = job.get("title", "").lower().strip()
        company = job.get("company", "").lower().strip()
        key = (title, company)
        
        if key not in seen and title and company:
            seen.add(key)
            deduped.append(job)
    
    return deduped
