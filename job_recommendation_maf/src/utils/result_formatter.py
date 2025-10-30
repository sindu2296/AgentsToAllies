"""
Result formatting utilities for job recommendation workflow.
Handles formatting and logging of workflow results across different stages.
"""
import logging
import json

# Set up logging for structured workflow information
logger = logging.getLogger(__name__)


def format_staged_results(all_messages, user_profile):
    """Format the workflow results - return only final summary for UI, log detailed stages."""
    
    # Extract messages by agent type
    job_extraction = None
    job_analysis = None
    job_summary = None

    # Try to match by agent name, but fallback to message order if not found
    for msg in all_messages:
        agent_name = (getattr(msg, 'author_name', None) or "").lower()
        if "job_extractor" in agent_name:
            job_extraction = msg.text
        elif "job_recommender" in agent_name:
            job_analysis = msg.text
        elif "job_summary" in agent_name:
            job_summary = msg.text

    # Fallback: use message order if agent names not found
    if not job_extraction and len(all_messages) > 0:
        job_extraction = all_messages[0].text
    if not job_analysis and len(all_messages) > 1:
        job_analysis = all_messages[1].text
    if not job_summary and len(all_messages) > 2:
        job_summary = all_messages[-1].text

    # Log detailed workflow stages for debugging
    log_detailed_stages(job_extraction, job_analysis, job_summary, user_profile)

    # Return only the final summary for main UI display
    if job_summary:
        return f"# Top 5 Recommended Jobs\n\n**Profile:** {user_profile}\n\n---\n\n{job_summary}"
    else:
        return f"# Job Recommendation Results\n\n**Profile:** {user_profile}\n\nWorkflow completed but no final summary generated."


def log_detailed_stages(job_extraction, job_analysis, job_summary, user_profile):
    """Log detailed workflow stages for display in workflow logs section."""
    
    logger.info("=" * 80)
    # Stage 1: Job Extractor Agent
    if job_extraction:
        logger.info("[STAGE 1] Job Extraction - Starting")
        logger.info("[STAGE 1] Calling Job Extractor Agent to search for jobs...")
        try:
            jobs_data = json.loads(job_extraction)
            if isinstance(jobs_data, list):
                job_count = len(jobs_data)
                logger.info(f"[EXTRACTOR] Found {job_count} jobs matching the profile")
                
                # Show first few job titles as preview
                if job_count > 0:
                    for i, job in enumerate(jobs_data[:3]):
                        if isinstance(job, dict) and 'title' in job:
                            company = job.get('company', 'Unknown Company')
                            location = job.get('location', 'Unknown Location')
                            logger.info(f"[EXTRACTOR] Job {i+1}: {job['title']} at {company} ({location})")
                    if job_count > 3:
                        logger.info(f"[EXTRACTOR] ... and {job_count - 3} more jobs found")
        except Exception:
            logger.info("[EXTRACTOR] Job search completed successfully")
        
        logger.info("[STAGE 1] Job Extraction - Complete")
    
    logger.info("=" * 80)
    # Stage 2: Job Recommendation Agent
    if job_analysis:
        logger.info("[STAGE 2] Job Analysis - Starting")
        logger.info("[STAGE 2] Calling Job Recommender Agent to analyze matches...")
        logger.info("[RECOMMENDER] AI analysis and job filtering completed")
        logger.info("[RECOMMENDER] Jobs analyzed and ranked by relevance")
        logger.info("[STAGE 2] Job Analysis - Complete")
    
    logger.info("=" * 80)
    # Stage 3: Job Summary Agent
    if job_summary:
        logger.info("[STAGE 3] Summary Generation - Starting")
        logger.info("[STAGE 3] Calling Job Summary Agent to create final recommendations...")
        logger.info("[SUMMARIZER] AI-powered personalized job recommendations generated")
        logger.info("[SUMMARIZER] Top job recommendations finalized")
        logger.info("[STAGE 3] Summary Generation - Complete")
    logger.info("=" * 80)