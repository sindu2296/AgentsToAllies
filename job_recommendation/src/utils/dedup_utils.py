# Utility functions for deduplication

def deduplicate_jobs(jobs):
    """
    Deduplicate jobs by unique job id and title.
    """
    seen = set()
    deduped = []
    for job in jobs:
        key = (job.get('id'), job.get('title'))
        if key not in seen:
            seen.add(key)
            deduped.append(job)
    return deduped
