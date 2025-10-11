# News Processing with Semantic Kernel

This project demonstrates two different approaches to processing news using Semantic Kernel agents: sequential and pro (parallel) processing.

## Overview

### 1. Basic Processing (`main_basic.py`)
The simplest implementation using Sequential Orchestration:
- Uses a single category agent (technology)
- Demonstrates built-in `SequentialOrchestration` class
- Simple pipeline with predefined flow
- Perfect for understanding basic Semantic Kernel concepts
- Shows how to use `SequentialOrchestration` with `InProcessRuntime`

### 2. Sequential Processing (`main_sequential.py`)
Demonstrates custom orchestration with sequential execution:
- Uses a router agent to determine relevant categories
- Custom orchestration logic using async/await
- Processes multiple categories sequentially (one after another)
- Shows how to implement complex flows without built-in orchestrators
- Simpler architecture but takes longer for multiple categories

### 3. Concurrent Processing (`main_concurrent.py`)
In this scenario, the news processing happens in parallel:
- Uses a router agent to determine relevant categories
- Multiple category agents work in parallel
- More efficient for multi-category queries
- Includes deduplication and better summarization

## Prerequisites

1. Python 3.9+ and pip installed
2. Required environment variables in a `.env` file:
   ```
   AZURE_OPENAI_ENDPOINT=your_azure_endpoint
   MODEL_NAME=your_model_name
   AI_FOUNDRY_AZURE_OPENAI_API_KEY=your_api_key
   NEWSAPI_API_KEY=your_newsapi_key
   ```

## Setup

1. Create and activate a Python virtual environment:
   ```powershell
   python -m venv env
   .\env\Scripts\activate  # Windows
   source env/bin/activate # Unix/MacOS
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Examples

First, navigate to the news directory:
```powershell
cd news
```

### Basic Processing
```powershell
python .\src\main_basic.py
```
This demonstrates the simplest form of agent orchestration with a single tech news agent.

### Sequential Processing
```powershell
python .\src\main_sequential.py
```
This will demonstrate:
- Smart category routing based on user queries
- Processing multiple categories sequentially (one at a time)
- Deduplication and summarization of articles

### Concurrent Processing
```powershell
python .\src\main_concurrent.py
```
This will demonstrate:
- Smart category routing based on user queries
- Parallel news fetching across multiple categories
- Deduplication of articles
- Enhanced summarization

## Sample Queries

Try these example queries with the concurrent version:
1. "Round up AI chip and cloud infra news"
2. "What happened in sports and health this morning?"
3. "Give me business and tech headlines about big tech"

## Orchestration Patterns

This project demonstrates two key orchestration patterns from [Semantic Kernel Agent Orchestration](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/?pivots=programming-language-python):

### Sequential Orchestration
Demonstrated in two ways:
- `main_basic.py`: Uses the built-in `SequentialOrchestration` class with a predefined pipeline
- `main_sequential.py`: Implements custom sequential orchestration with multiple agents

### Concurrent Orchestration (`main_concurrent.py`)
Uses Semantic Kernel's `ConcurrentOrchestration` for concurrent execution of multiple agents, allowing parallel processing of different news categories.

## Implementation Architecture

### Sequential Version
Components:
- Router Agent: Determines relevant categories
- Category Agents: Fetch news for each category (one at a time)
- Summarizer Agent: Creates concise summaries
- Deduplication: Removes duplicate articles

### Concurrent Version
Components:
- Router Agent: Determines relevant news categories
- Category Agents: Fetch news for specific categories
- Summarizer Agent: Creates concise summaries
- Deduplication: Removes duplicate articles across categories