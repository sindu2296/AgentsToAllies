# Utility functions for job data cleaning

def clean_job_data(job):
    """
    Clean and normalize job data fields.
    """
    job = job.copy()
    job['title'] = job.get('title', '').strip().title()
    job['company'] = job.get('company', '').strip()
    job['location'] = job.get('location', '').strip()
    job['description'] = job.get('description', '').strip()
    return job
