# Utility functions for job recommendation system

def deduplicate_jobs(jobs):
    # TODO: Implement deduplication logic
    return list({job['id']: job for job in jobs}.values())

def clean_job_data(job):
    # TODO: Implement job data cleaning
    return job
