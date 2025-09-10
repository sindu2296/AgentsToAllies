import requests
import os
import json
import time
from dotenv import load_dotenv

class SerpApiJobExtractor:
    """
    A simple class to extract job listings for 'software engineer' using SerpApi's Google Jobs API.
    """
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        self.api_key = os.getenv("SERPAPI_API_KEY")
        if not self.api_key:
            raise ValueError("SERPAPI_API_KEY environment variable not set. Please set it or hardcode for testing.")

        self.base_url = "https://serpapi.com/search"
        print("SerpApiJobExtractor initialized.")

    def get_software_engineer_jobs(self, location="United States", num_results=10):
        """
        Fetches 'software engineer' jobs from SerpApi's Google Jobs API.

        Args:
            location (str): The geographical location to search for jobs (e.g., "Seattle, WA", "California", "United States").
            num_results (int): The maximum number of job results to fetch. SerpApi typically returns 10-20 per page.
                               This function will try to fetch multiple pages up to this limit.

        Returns:
            list: A list of dictionaries, where each dictionary represents a job.
                  Returns an empty list if an error occurs or no jobs are found.
        """
        all_jobs = []
        next_page_token = None # Initialize next_page_token for first request
        
        print(f"Fetching up to '{num_results}' 'software engineer' jobs in '{location}'...")

        while len(all_jobs) < num_results:
            params = {
                "api_key": self.api_key,
                "engine": "google_jobs",
                "q": "software engineer", # Filter for software engineer jobs
                "location": location,
                "gl": "us", # Target country (United States)
                "hl": "en", # Language (English)
                "output": "json", # Output format
            }
            if next_page_token:
                params["next_page_token"] = next_page_token # Use token for subsequent requests

            try:
                print(f"Fetching jobs (token: {next_page_token if next_page_token else 'initial'})...")
                response = requests.get(self.base_url, params=params, timeout=15)
                response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
                data = response.json()

                if 'jobs_results' in data:
                    current_page_jobs = data['jobs_results']
                    if not current_page_jobs:
                        # No more jobs on this page, or no jobs found at all
                        print("No more job results found on current page. Ending pagination.")
                        break

                    for job_item in current_page_jobs:
                        if len(all_jobs) < num_results: # Ensure we don't exceed desired num_results
                            # Extract relevant details. You can add more fields if needed.
                            job_details = {
                                'job_id': job_item.get('job_id'),
                                'title': job_item.get('title'),
                                'company_name': job_item.get('company_name'),
                                'location': job_item.get('location'),
                                'link': job_item.get('link'),
                                'description_snippet': job_item.get('description'),
                                'salary': job_item.get('salary'),
                                'posted_at': job_item.get('posted_at'),
                                'source': job_item.get('source')
                            }
                            all_jobs.append(job_details)
                        else:
                            break # Reached desired number of results

                    # Check for next_page_token for pagination
                    next_page_token = data.get('serpapi_pagination', {}).get('next_page_token')
                    if not next_page_token or len(all_jobs) >= num_results:
                        print("No 'next_page_token' found or target results reached. Ending pagination.")
                        break # No more pages or desired number of results fetched
                else:
                    print("No 'jobs_results' key found in the API response. Possible error or no jobs.")
                    # print(f"Full response (truncated to 500 chars): {json.dumps(data, indent=2)[:500]}...")
                    break # Exit loop if no job results

            except requests.exceptions.HTTPError as e:
                print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
                print(f"Error details: {e.response.json().get('error', 'No specific error message provided.')}")
                break
            except requests.exceptions.ConnectionError as e:
                print(f"Connection Error: {e}")
                break
            except requests.exceptions.Timeout:
                print("Request timed out.")
                break
            except requests.exceptions.RequestException as e:
                print(f"An error occurred during the API request: {e}")
                break
            except json.JSONDecodeError:
                print("Error decoding JSON from API response.")
                # print(f"Raw response (truncated to 500 chars): {response.text[:500]}...")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break
            
            # Be polite and avoid hitting rate limits too quickly, especially on free tiers.
            if next_page_token and len(all_jobs) < num_results: # Only sleep if more results are needed and token exists
                time.sleep(0.5) # Small delay between page requests

        return all_jobs[:num_results] # Return up to the requested number of results

# --- How to use the class ---
if __name__ == "__main__":
    extractor = SerpApiJobExtractor()

    # Get 50 software engineer jobs in the United States
    # Remember SerpApi free tier limits, so num_results might be capped by your plan.
    jobs = extractor.get_software_engineer_jobs(location="United States", num_results=50)

    if jobs:
        print(f"\n--- Found {len(jobs)} Software Engineer Jobs ---")
        for i, job in enumerate(jobs):
            print(f"\nJob {i+1}:")
            print(f"  Title: {job.get('title', 'N/A')}")
            print(f"  Company: {job.get('company_name', 'N/A')}")
            print(f"  Location: {job.get('location', 'N/A')}")
            print(f"  Posted: {job.get('posted_at', 'N/A')}")
            print(f"  Source: {job.get('source', 'N/A')}")
            print(f"  Salary: {job.get('salary', 'N/A')}")
            print(f"  Link: {job.get('link', 'N/A')}")
            print(f"  Snippet: {job.get('description_snippet', 'N/A')[:150]}...") # Truncate snippet
    else:
        print("\nNo jobs found or an error occurred. Check your API key and internet connection.")
        print("If using a free SerpApi tier, you might have hit your search limit or there are no more jobs.")