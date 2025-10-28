# Job Recommendation with Semantic Kernel

This project demonstrates how to build a modular job recommendation system using Semantic Kernel agents, plugins, and orchestrators. The architecture and workflow are inspired by the news processing pipeline, with both sequential and concurrent orchestration options.

## Overview

### 1. Basic Job Recommendation
- Uses a job extractor agent to search for jobs based on a user profile (via SerpAPI)
- Demonstrates built-in and custom orchestration
- Simple pipeline for understanding Semantic Kernel agent/plugin integration

### 2. Sequential Processing
- Collects user profile data
- Extracts job listings using the job extractor agent (SerpAPI)
- Recommends jobs using the job recommender agent
- Summarizes jobs using the job summary agent
- Orchestration is performed step-by-step (sequentially)
- Good for understanding agent chaining and data flow

### 3. Concurrent/Parallel Processing
- Similar to sequential, but job recommendation and summarization can be performed in parallel for efficiency
- Useful for large job lists or more complex flows

## Prerequisites

1. Python 3.9+ and pip installed
2. Required environment variables in a `.env` file:
   ```
   AZURE_OPENAI_ENDPOINT=your_azure_endpoint
   MODEL_NAME=your_model_name
   AZURE_OPENAI_API_KEY=your_api_key
   SERPAPI_API_KEY=your_serpapi_key
   ```

## Setup

1. Create and activate a Python virtual environment:
   ```powershell
   python -m venv env
   .\env\Scripts\activate  # Windows
   source env/bin/activate  # Unix/MacOS
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Examples

First, navigate to the job_recommendation directory:
```powershell
cd job_recommendation
```

### Sequential Orchestration
Run the sequential pipeline:
```powershell
python -m src.orchestration.sequential_orchestrator
```

### Concurrent Orchestration
Run the concurrent pipeline (if implemented):
```powershell
python -m src.orchestration.concurrent_orchestrator
```

## Project Structure

- `src/agents/` — Agent definitions (job extractor, recommender, summary)
- `src/plugins/` — Plugins (e.g., SerpAPI job board)
- `src/orchestration/` — Orchestrators (sequential, concurrent)
- `src/utils/` — Utility functions
- `src/config.py` — Kernel and environment setup

## Notes
- Ensure your `.env` file is correctly configured with all required API keys.
- The job extractor agent uses SerpAPI to fetch job listings from Google Jobs.
- The pipeline is modular and can be extended with additional agents or plugins.

For more details, see the code and comments in each module.
