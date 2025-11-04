# News Processing with Semantic Kernel

This project demonstrates two ways to orchestrate news agents with Semantic Kernel: a clear, step-by-step sequential flow and a high-throughput concurrent flow.

## Story At A Glance

Use these talking points for executive briefings or demos:

1. **Router decides who should help.** The router agent analyses the user prompt and selects the most relevant news categories.
2. **Category specialists gather intel.** Dedicated agents call the News plugin to pull JSON headlines for each assigned category.
3. **Summarizer condenses the feed.** We deduplicate the combined headlines and produce a five-bullet executive summary with inline citations.
4. **Orchestration pattern is the lever.** Sequential mode uses Semantic Kernel's `SequentialOrchestration` for deterministic control flow; concurrent mode showcases `ConcurrentOrchestration` for speed.
5. **Session memory keeps content fresh.** The concurrent orchestrator hangs on to a short list of recent headlines per category, nudging agents to avoid repeats during the same run.

## Overview

### 1. Sequential Processing (`main_sequential.py`)

Sequential orchestration using Semantic Kernel's `SequentialOrchestration`:

- Router agent chooses 1–3 relevant categories
- Each category agent runs in turn (no overlap) using `SequentialOrchestration` to keep behaviour predictable
- Deduplication and summarization run after all categories finish
- Demonstrates how to use `SequentialOrchestration` for multi-step workflows

### 2. Concurrent Processing (`main_concurrent.py`)

Parallel orchestration using `ConcurrentOrchestration`:

- Router agent selects categories, then multiple category agents run simultaneously
- A lightweight memory cache keeps the last five headlines per category to minimise duplicates between successive queries in the same session
- Deduplication ensures merged results stay clean
- Summarizer agent delivers the finished executive brief

## Prerequisites

1. Install Python 3.9 or later (for example: `winget install Python.Python.3.13`).
2. Optional but recommended: install Visual Studio Code from <https://code.visualstudio.com/>.
3. Configure the following environment variables in a `.env` file at the repo root:

   ```bash
   AZURE_OPENAI_ENDPOINT=your_endpoint
   AZURE_OPENAI_API_KEY=your_key
   MODEL_NAME=your_model_name
   NEWSAPI_API_KEY=your_newsapi_key
   ```

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv env
   .\env\Scripts\activate  # Windows
   # source env/bin/activate  # macOS / Linux
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

## Running the Examples

Move into the `news` folder before running the samples:

```powershell
cd news
```

### Sequential Processing

```powershell
python .\src\main_sequential.py
```

### Concurrent Processing

```powershell
python .\src\main_concurrent.py
```

Suggested demo queries (run sequentially to showcase memory and deduplication):

1. `Round up AI chip and cloud infra news`
2. `What happened in sports and health this morning?`
3. `Give me business and tech headlines about big tech`

## Orchestration Patterns

This repo mirrors the patterns described in [Semantic Kernel's orchestration documentation](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/?pivots=programming-language-python).

### Sequential Orchestration

- `src/main_sequential.py`: Uses Semantic Kernel's `SequentialOrchestration` to process categories one at a time, with each agent wrapped in its own sequential pipeline for consistent orchestration patterns.

### Concurrent Orchestration

- `src/main_concurrent.py`: Uses `ConcurrentOrchestration` for parallel agent execution.
- **Memory Implementation**: `ConcurrentNewsOrchestrator` maintains a `_category_memory` dictionary (in `concurrent_orchestrator.py`, line 32) that stores the last 5 headlines per category. This memory is passed to category agents via the `build_category_agent()` function, which converts it into a text hint (in `category_agent.py`, `_build_memory_hint()`) that's injected into agent instructions. This helps agents avoid repeating the same headlines across multiple queries in the same session.
- Memory persists only for the orchestrator instance lifetime—restarting the process clears the cache.

## Architecture Snapshot

```text
┌─────────────┐    ┌────────────────┐    ┌─────────────────┐    ┌────────────────────┐
│ User Query  │ -> │ Router Agent   │ -> │ Category Agents  │ -> │ Dedup + Summarizer  │
└─────────────┘    │ agents/router  │    │ agents/category │    │ agents/summarizer   │
                   └────────────────┘    └─────────────────┘    └────────────────────┘
                           │                     │                       │
                           │ category list       │ JSON articles         │ Markdown brief
                           │                     │ cached per category   │ (with sources)
```

Component quick reference:

- **Router agent** – `news/src/agents/router_agent.py`
- **Category agents & memory hint** – `news/src/agents/category_agent.py`
- **Summarizer agent** – `news/src/agents/summarizer_agent.py`
- **Orchestrators** – `news/src/orchestration/*.py`
- **News plugin** – `news/src/plugins/news_plugin.py`
- **Deduplication helper** – `news/src/utils/dedup.py`

## FAQ

- **How long does the memory last?** For the lifetime of the orchestrator instance. Restarting the process resets the cache so demos stay predictable.
- **What happens if a category appears again later?** The memory hint is injected into the agent instructions, steering the model toward fresh coverage or new angles.
- **Can this scale to long-term memory?** Yes—swap the in-memory dictionary for a persistent store (table, Redis, vector DB) and merge that context before each agent call.
