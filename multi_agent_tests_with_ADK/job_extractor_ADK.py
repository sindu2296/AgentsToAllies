import requests
import json
import time
import os
import collections

# --- ADK Core Components (Simplified) ---

class ADK_Environment:
    """
    A simplified ADK environment managing agents and message passing.
    """
    def __init__(self):
        self.agents = {} # Stores agent instances by ID
        self.message_queues = collections.defaultdict(list) # Stores messages for each agent

    def register_agent(self, agent_instance):
        """Registers an agent with the environment."""
        self.agents[agent_instance.id] = agent_instance
        print(f"Environment: Registered agent '{agent_instance.id}'")

    def send_message(self, sender_id, receiver_id, content):
        """Sends a message from one agent to another."""
        if receiver_id in self.agents:
            self.message_queues[receiver_id].append({'sender': sender_id, 'content': content})
            # print(f"Message: '{sender_id}' sent '{content['type']}' to '{receiver_id}'")
        else:
            print(f"Environment Error: Receiver agent '{receiver_id}' not found. Message from '{sender_id}' dropped.")

    def get_messages_for_agent(self, agent_id):
        """Retrieves messages for a given agent and clears its queue."""
        messages = self.message_queues[agent_id]
        self.message_queues[agent_id] = [] # Clear queue after retrieval
        return messages

    def run_simulation(self, steps=1):
        """Runs the simulation for a specified number of steps."""
        print("\n--- Starting ADK Simulation ---")
        for step in range(steps):
            print(f"\n--- Simulation Step {step + 1} ---")
            for agent_id, agent in list(self.agents.items()): # Iterate over a copy to prevent issues if agents modify agent list
                # Simulate agent's perceive-deliberate-act cycle
                agent.perceive(self.get_messages_for_agent(agent_id))
                agent.deliberate()
                agent.act(self) # Pass environment to allow sending messages
            time.sleep(1) # Small delay for demonstration purposes
        print("\n--- Simulation Finished ---")

class BaseAgent:
    """
    Base class for all agents, defining core behaviors.
    """
    def __init__(self, agent_id):
        self.id = agent_id
        self.beliefs = {} # Internal knowledge/state
        self.goals = [] # What the agent aims to achieve
        self.percepts = [] # Incoming messages or observations

    def perceive(self, messages):
        """Updates agent's perceptions based on incoming messages."""
        self.percepts.extend(messages)

    def deliberate(self):
        """Agent's reasoning logic to update beliefs and decide on actions."""
        # This method should be overridden by subclasses
        pass

    def act(self, env):
        """Agent's action execution, interacting with the environment."""
        # This method should be overridden by subclasses
        pass

# --- Specific Agents for Job Extraction and Analysis ---

class SerpApiJobsExtractorAgent(BaseAgent):
    """
    Agent responsible for extracting job data using SerpApi (Google Jobs).
    """
    def __init__(self, agent_id="SerpApiJobsExtractor"):
        super().__init__(agent_id)
        self.api_key = os.getenv("SERPAPI_API_KEY")
        if not self.api_key:
            raise ValueError("SERPAPI_API_KEY environment variable not set.")

        self.base_url = "https://serpapi.com/search"
        self.beliefs['last_extracted_jobs_count'] = 0
        self.goals = ["extract and deliver fresh job listings"]
        self.last_extraction_time = 0 # To control extraction frequency

    def deliberate(self):
        """
        Decides if it's time to perform a job extraction.
        Triggers extraction based on a schedule (e.g., every 12 hours).
        """
        # Clear previous percepts for this cycle
        self.percepts = []

        # Check if enough time has passed since last extraction
        if (time.time() - self.last_extraction_time) > (12 * 3600): # 12 hours for real-world or (5 * 60) for 5 minutes for demo
            print(f"[{self.id}]: Deciding to extract new jobs...")
            # Example query: You can make this dynamic or based on student profile later
            self.percepts.append({'type': 'trigger_extraction',
                                  'query': 'Software Engineer',
                                  'location': 'United States'}) # Using broader location for more results
            self.percepts.append({'type': 'trigger_extraction',
                                  'query': 'Data Scientist',
                                  'location': 'New York'})

    def act(self, env):
        """
        Executes the job extraction and sends data to the JobMarketAnalystAgent.
        """
        for percept in self.percepts:
            if percept['type'] == 'trigger_extraction':
                query = percept['query']
                location = percept['location']
                print(f"[{self.id}]: Acting on 'trigger_extraction' for '{query}' in '{location}'.")
                extracted_jobs = self._extract_jobs(query, location)
                if extracted_jobs:
                    self.beliefs['last_extracted_jobs_count'] = len(extracted_jobs)
                    print(f"[{self.id}]: Extracted {len(extracted_jobs)} jobs. Sending to JMAA_Global.")
                    # Send the extracted job data to the JobMarketAnalystAgent
                    env.send_message(self.id, "JMAA_Global",
                                     {'type': 'new_job_data', 'source': 'SerpApi_GoogleJobs', 'jobs': extracted_jobs})
                else:
                    print(f"[{self.id}]: No jobs extracted for '{query}' in '{location}'.")
                self.last_extraction_time = time.time() # Update last extraction time after attempt
                # Note: SerpApi free tier limits searches. Be mindful during testing.
                time.sleep(2) # Small delay between multiple search queries to avoid hitting rate limits too quickly

    def _extract_jobs(self, query, location, num_results=100):
        """
        Performs the actual API call to SerpApi.
        """
        params = {
            "api_key": self.api_key,
            "engine": "google_jobs",
            "q": query,
            "location": location,
            "gl": "us", # Country code
            "hl": "en", # Language code
            "output": "json"
        }
        # Iterate through pages to get more results, up to num_results
        all_jobs = []
        start_page = 0
        while len(all_jobs) < num_results:
            params["start"] = start_page # Offset for pagination
            try:
                print(f"[{self.id}]: Fetching page {start_page // 10} for '{query}'...")
                response = requests.get(self.base_url, params=params, timeout=30)
                response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
                data = response.json()

                if 'jobs_results' in data:
                    jobs_on_page = data['jobs_results']
                    if not jobs_on_page: # No more jobs on this page
                        break
                    for item in jobs_on_page:
                        # Extract relevant fields for your JMAA
                        job_info = {
                            'job_id': item.get('job_id'), # SerpApi's unique ID for the job
                            'title': item.get('title'),
                            'company_name': item.get('company_name'),
                            'location': item.get('location'),
                            'detected_extensions': item.get('detected_extensions'), # E.g., 'schedule_type', 'posted_at'
                            'link': item.get('link'), # Direct link to the job on Google Jobs or original source
                            'description_snippet': item.get('description'), # Short description
                            'salary': item.get('salary'), # Might not always be present
                            'posted_at': item.get('posted_at'),
                            'source': item.get('source') # E.g., LinkedIn, Indeed, Company website
                        }
                        all_jobs.append(job_info)
                    start_page += len(jobs_on_page) # Move to next page offset
                    if len(jobs_on_page) < 10: # Assuming 10 results per page, if less, it's likely the last page
                        break
                else:
                    print(f"[{self.id}]: No 'jobs_results' in API response for '{query}'.")
                    break # No job results found
            except requests.exceptions.HTTPError as e:
                print(f"[{self.id}]: HTTP Error during extraction for '{query}': {e.response.status_code} - {e.response.text}")
                break
            except requests.exceptions.ConnectionError as e:
                print(f"[{self.id}]: Connection Error during extraction for '{query}': {e}")
                break
            except requests.exceptions.Timeout:
                print(f"[{self.id}]: Timeout Error during extraction for '{query}'.")
                break
            except requests.exceptions.RequestException as e:
                print(f"[{self.id}]: General Request Error during extraction for '{query}': {e}")
                break
            except json.JSONDecodeError:
                print(f"[{self.id}]: JSON Decode Error: Could not parse response for '{query}'.")
                break
            except Exception as e:
                print(f"[{self.id}]: An unexpected error occurred during extraction for '{query}': {e}")
                break
            time.sleep(0.5) # Be polite to the API, small delay between page requests

        return all_jobs[:num_results] # Return up to the desired number of results

class JobMarketAnalystAgent(BaseAgent):
    """
    A simplified agent that receives job data and "analyzes" it (prints it for demo).
    In a real system, this would store, process, and identify trends.
    """
    def __init__(self, agent_id="JMAA_Global"):
        super().__init__(agent_id)
        self.beliefs['total_jobs_processed'] = 0
        self.beliefs['jobs_by_source'] = collections.defaultdict(int)
        self.goals = ["process and analyze job market data"]

    def deliberate(self):
        """
        Processes incoming job data messages.
        """
        for percept in self.percepts:
            if percept['type'] == 'new_job_data':
                source = percept['content']['source']
                jobs = percept['content']['jobs']
                num_jobs = len(jobs)

                print(f"[{self.id}]: Received {num_jobs} new jobs from '{source}'.")
                self.beliefs['total_jobs_processed'] += num_jobs
                self.beliefs['jobs_by_source'][source] += num_jobs

                # In a real JMAA, you'd perform complex analysis here:
                # - Store jobs in a database
                # - Extract skills using NLP
                # - Analyze salary trends
                # - Identify most in-demand roles
                # - Update internal models for other agents (e.g., SkillGapRecommender)

                # For demonstration, just print a few details
                if jobs:
                    print(f"[{self.id}]: First 3 jobs received:")
                    for i, job in enumerate(jobs[:3]):
                        print(f"    - Title: {job.get('title', 'N/A')}")
                        print(f"      Company: {job.get('company_name', 'N/A')}")
                        print(f"      Location: {job.get('location', 'N/A')}")
                        print(f"      Link: {job.get('link', 'N/A')}")
                        print(f"      Source: {job.get('source', 'N/A')}")
                        print("-" * 30)
                print(f"[{self.id}]: Total jobs processed so far: {self.beliefs['total_jobs_processed']}")
                print(f"[{self.id}]: Jobs by source: {dict(self.beliefs['jobs_by_source'])}")

        self.percepts = [] # Clear percepts after processing

    def act(self, env):
        """
        JMAA typically acts by updating its internal beliefs or sending derived insights
        to other agents, but for this demo, it's primarily a receiver.
        """
        pass # No specific action to trigger externally in this simplified version

# --- Main Simulation Execution ---
if __name__ == "__main__":
    env = ADK_Environment()

    # Create and register agents
    job_extractor_agent = SerpApiJobsExtractorAgent()
    job_market_analyst_agent = JobMarketAnalystAgent()

    env.register_agent(job_extractor_agent)
    env.register_agent(job_market_analyst_agent)

    # Run the simulation for a few steps
    # The SerpApiJobsExtractorAgent will try to extract jobs once per simulation run
    # (controlled by its internal `last_extraction_time` logic).
    # You might want to run for 1 or 2 steps to see the initial extraction.
    env.run_simulation(steps=2) # Run for 2 steps to show initial extraction and a subsequent check