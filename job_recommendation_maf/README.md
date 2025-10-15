# Job Recommendation with Microsoft Agent Framework

This project demonstrates how to build a modular job recommendation system using **Microsoft Agent Framework (MAF)** with multi-agent sequential orchestration.

## Overview

This implementation showcases:
- **Multi-Agent Architecture**: Specialized agents for extraction, recommendation, and summarization
- **Sequential Orchestration**: Jobs flow through agents in a predictable, ordered manner
- **Function Tools**: SerpAPI integration as a MAF function tool
- **Azure OpenAI**: Powered by Azure OpenAI with API key authentication

## Architecture

### Agents

1. **Job Extractor Agent**
   - Uses SerpAPI (Google Jobs) to search for jobs based on user profile
   - Returns job listings as JSON
   - Tool: `search_jobs` function

2. **Job Recommender Agent**
   - Analyzes jobs and matches them to user's skills/experience
   - Ranks jobs by relevance
   - Adds `match_reason` to explain why each job fits
   - Returns top 3-5 recommendations as JSON

3. **Job Summary Agent**
   - Creates executive summaries (5 bullets each) of recommended jobs
   - Highlights: responsibilities, qualifications, skills, benefits, match reason
   - Returns human-readable text

### Workflow

The orchestrator uses Microsoft Agent Framework's **`SequentialBuilder`** to create a pipeline where each agent processes the conversation in turn:

```python
from agent_framework import SequentialBuilder

# Build sequential workflow
workflow = (
    SequentialBuilder()
    .participants([extractor, recommender, summarizer])
    .build()
)

# Run the workflow
async for event in workflow.run_stream(user_profile):
    if isinstance(event, WorkflowCompletedEvent):
        completion = event
```

```
User Profile 
    ↓
[Job Extractor Agent] → Searches SerpAPI
    ↓
[Job Recommender Agent] → Ranks & filters
    ↓
[Job Summary Agent] → Creates summaries
    ↓
Final Output (Complete Conversation)
```

**Key Feature**: Each agent sees the full conversation history and adds their response, building a complete dialogue through the pipeline.

## Prerequisites

1. Python 3.9+ and pip installed
2. Required environment variables in a `.env` file:
   ```
   AZURE_OPENAI_ENDPOINT=your_azure_endpoint
   MODEL_NAME=your_model_name
   AI_FOUNDRY_AZURE_OPENAI_API_KEY=your_api_key
   SERPAPI_API_KEY=your_serpapi_key
   ```

## Setup

1. Ensure you have the virtual environment activated:
   ```powershell
   .\env\Scripts\activate  # Windows
   source env/bin/activate  # Unix/MacOS
   ```

2. Install dependencies (if not already installed):
   ```
   pip install -r requirements.txt
   ```

## Running the Example

Navigate to the job_recommendation_maf directory:
```powershell
cd job_recommendation_maf
```

Run the sequential orchestration:
```powershell
python -m src.main_sequential
```

## Project Structure

```
job_recommendation_maf/
├── src/
│   ├── agents/
│   │   ├── job_extractor_agent.py    # Searches for jobs via SerpAPI
│   │   ├── job_recommender_agent.py  # Ranks and recommends jobs
│   │   └── job_summary_agent.py      # Creates executive summaries
│   ├── orchestration/
│   │   └── sequential_orchestrator.py # Sequential workflow coordinator
│   ├── plugins/
│   │   └── job_board_plugin.py       # SerpAPI function tool
│   ├── utils/
│   │   └── dedup.py                  # Job deduplication utilities
│   ├── config.py                     # Azure OpenAI client setup
│   └── main_sequential.py            # Entry point for sequential demo
└── README.md
```

## Key Differences from Semantic Kernel Version

| Feature | Microsoft Agent Framework | Semantic Kernel |
|---------|---------------------------|-----------------|
| Agent Creation | `chat_client.create_agent()` | `ChatCompletionAgent(kernel, ...)` |
| Client | `AzureOpenAIChatClient` | `AsyncAzureOpenAI` + `AzureChatCompletion` |
| Tools/Plugins | Function tools (Python functions) | Kernel plugins with `@kernel_function` |
| Orchestration | `SequentialBuilder().participants([...]).build()` | `SequentialOrchestration` + `InProcessRuntime` |
| Execution | `workflow.run_stream()` → `WorkflowCompletedEvent` | `orchestration.invoke()` → `.get(timeout)` |
| Conversation | Full conversation history in result | Agent responses only |

## Example Output

```
================================================================================
USER PROFILE: software engineer 2 with Python and cloud experience
================================================================================

[ORCHESTRATOR] Building sequential workflow for: software engineer 2 with Python and cloud experience
[ORCHESTRATOR] Workflow built with 3 agents: extractor -> recommender -> summarizer
[ORCHESTRATOR] Running workflow...
[PLUGIN] Searching jobs for: software engineer 2 with Python and cloud experience
[PLUGIN] Found 5 jobs

[ORCHESTRATOR] Workflow completed successfully!
[ORCHESTRATOR] Total messages in conversation: 4

--------------------------------------------------------------------------------
FINAL RESULT:
--------------------------------------------------------------------------------
**Job Recommendations for:** software engineer 2 with Python and cloud experience

================================================================================
CONVERSATION FLOW
================================================================================

--------------------------------------------------------------------------------
Step 01 [user]
--------------------------------------------------------------------------------
Search for jobs matching this user profile: software engineer 2 with Python and cloud experience

--------------------------------------------------------------------------------
Step 02 [job_extractor_agent]
--------------------------------------------------------------------------------
[{"title": "Software Engineer II", "company": "Amazon", "location": "Austin, TX", ...}, ...]

--------------------------------------------------------------------------------
Step 03 [job_recommender_agent]
--------------------------------------------------------------------------------
[{"title": "Software Engineer II", "company": "Amazon", "match_reason": "Strong alignment with Python and AWS cloud experience", ...}, ...]

--------------------------------------------------------------------------------
Step 04 [job_summary_agent]
--------------------------------------------------------------------------------
### Software Engineer II - Amazon.com Services LLC - Austin, TX
• Build scalable distributed systems using Python, Java, and cloud technologies
• 3+ years of professional software development experience required
• Experience with AWS, microservices, and DevOps practices preferred
• Competitive compensation: $129K-$224K base + equity + benefits
• Strong match: Aligns with Python and cloud experience requirements

[... additional summaries ...]

================================================================================

**Total jobs found:** 5 | **Recommended:** 3
================================================================================
```

## Notes

- The Microsoft Agent Framework provides a streamlined, Pythonic approach to building agents
- Uses **`SequentialBuilder`** from MAF for pipeline orchestration (based on [official docs](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/sequential?pivots=programming-language-python))
- Function tools are simpler than Semantic Kernel plugins (just Python functions)
- Each agent sees the full conversation history and adds their response
- The workflow returns a `WorkflowCompletedEvent` with complete conversation flow
- Agents automatically handle tool/function calling when needed

## Comparison with Other Implementations

- **`job_recommendation/`** - Uses Semantic Kernel with `SequentialOrchestration` + `InProcessRuntime`
- **`job_recommendation_maf/`** (this folder) - Uses Microsoft Agent Framework with `SequentialBuilder`
- Both achieve the same goal with different frameworks and patterns

For more details on Microsoft Agent Framework, see the [official documentation](https://learn.microsoft.com/en-us/agent-framework/).
