# News Processing with Microsoft Agent Framework (MAF)

This project demonstrates news processing using **Microsoft Agent Framework** with proper workflow-based orchestration. It showcases both sequential and concurrent patterns using MAF's official workflow APIs.

## 🎯 Overview

The Microsoft Agent Framework implementation uses:
- **ChatAgent**: For creating AI agents with Azure OpenAI
- **Function Tools**: For agent capabilities (fetching news)
- **ConcurrentBuilder Workflow**: For official concurrent orchestration
- **Structured Logging**: For easy debugging and learning
- **Azure CLI Authentication**: For secure credential management

### Why Workflows?

MAF provides official workflow patterns for orchestration instead of manual `asyncio.gather()`:
- **ConcurrentBuilder**: Fan-out to multiple agents in parallel, then aggregate results
- **Type-safe**: Better error handling and state management
- **Maintainable**: Clear separation of concerns
- **Observable**: Built-in tracing and monitoring support

## 📁 Project Structure

```
news_maf/
├── src/
│   ├── agents/
│   │   ├── router_agent.py       # Determines news categories
│   │   ├── category_agent.py     # Fetches news for a category
│   │   └── summarizer_agent.py   # Creates executive summaries
│   ├── orchestration/
│   │   ├── sequential_orchestrator.py   # Simple one-by-one processing
│   │   └── concurrent_orchestrator.py   # Workflow-based parallel processing
│   ├── plugins/
│   │   └── news_plugin.py        # NewsAPI integration as function tool
│   ├── utils/
│   │   └── dedup.py              # Article deduplication
│   ├── config.py                 # Azure OpenAI client setup
│   ├── main_sequential.py        # Sequential demo
│   └── main_concurrent.py        # Concurrent workflow demo
└── README.md
```

## 🚀 Getting Started

### Prerequisites

1. Python 3.10 or later
2. Azure OpenAI service with a deployed model
3. NewsAPI key (get free key at https://newsapi.org/)
4. Azure CLI installed and authenticated (`az login`)

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables (.env file)
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
MODEL_NAME=your_model_deployment_name
AI_FOUNDRY_AZURE_OPENAI_API_KEY=your_api_key  # Optional with Azure CLI auth
NEWSAPI_API_KEY=your_newsapi_key
```

### Enable Logging (Highly Recommended)

To see detailed logs of what's happening, add this to the top of `main_sequential.py` or `main_concurrent.py`:

```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

This will show you:
- `[ROUTING]` - Which categories were selected
- `[FETCHING]` - Progress fetching from each category
- `[DEDUP]` - Deduplication results
- `[SUMMARIZING]` - Summary generation
- `[WORKFLOW]` - Workflow execution steps (concurrent mode)

### Running the Examples

**Sequential Processing:**
```bash
cd news_maf/src
python main_sequential.py
```

**Concurrent Processing (with Workflows):**
```bash
cd news_maf/src
python main_concurrent.py
```

## 🏗️ Architecture

### Workflow Flow (Concurrent Mode)

```text
User Query
    ↓
┌─────────────────┐
│  Router Agent   │  ← Determines categories
└─────────────────┘
    ↓
┌──────────────────────────────────────┐
│   ConcurrentBuilder Workflow         │
│   ┌────────────────────────────┐     │
│   │  Dispatcher (auto-created) │     │
│   └────────────────────────────┘     │
│              ↓                        │
│   ┌─────────────────────────────┐    │
│   │  Fan-out to Participants    │    │
│   │  • technology_agent         │    │
│   │  • sports_agent (parallel)  │    │
│   │  • business_agent           │    │
│   └─────────────────────────────┘    │
│              ↓                        │
│   ┌─────────────────────────────┐    │
│   │  Aggregator Function        │    │
│   │  • Collect all results      │    │
│   │  • Deduplicate articles     │    │
│   │  • Call summarizer          │    │
│   └─────────────────────────────┘    │
└──────────────────────────────────────┘
    ↓
Final Summary
```

### Key Components

#### 1. **ConcurrentBuilder Workflow (Concurrent Mode)**

The official MAF pattern for parallel execution:

```python
from agent_framework import ConcurrentBuilder

# Define aggregator function
async def aggregate_results(results):
    # Process results from all agents
    return final_output

# Build workflow
workflow = (
    ConcurrentBuilder()
    .participants([agent1, agent2, agent3])  # Agents to run in parallel
    .with_aggregator(aggregate_results)       # How to combine results
    .build()
)

# Run workflow
result = await workflow.run(input_message)
```

**Why use workflows?**

- ✅ Official MAF pattern (not manual asyncio)
- ✅ Better error handling and state management
- ✅ Built-in observability and tracing
- ✅ Type-safe aggregation of results
- ✅ Easier to test and maintain

#### 2. **ChatAgent (agent_framework)**

The core agent type in MAF that provides:

- Instructions-based behavior
- Function tool integration
- Async run() method for execution
- Built-in conversation management

#### 3. **Function Tools**

MAF agents use Python functions directly as tools:

```python
def fetch_top_headlines(category: str, limit: int = 6) -> str:
    """Fetch news from NewsAPI"""
    # Implementation

agent = ChatAgent(
    chat_client=client,
    instructions="...",
    tools=[fetch_top_headlines]  # Direct function reference
)
```

#### 4. **Logging for Learning**

Both orchestrators use Python's logging module:

```python
import logging
logger = logging.getLogger(__name__)

# Throughout the code
logger.info("[ROUTING] Processing query: {user_query}")
logger.info(f"[FETCHING] Category: {category}")
logger.info(f"[DEDUP] {count} unique articles")
```

Enable it in your main file to follow execution:

```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 🆚 MAF vs Semantic Kernel Comparison

| Feature | Microsoft Agent Framework | Semantic Kernel |
|---------|---------------------------|-----------------|
| **Agent Type** | `ChatAgent` | `ChatCompletionAgent` |
| **Function Tools** | Direct Python functions | `@kernel_function` decorators |
| **Invocation** | `await agent.run(prompt)` | `async for msg in agent.invoke(messages)` |
| **Orchestration** | `ConcurrentBuilder` workflows | Built-in orchestrator helpers |
| **Setup Complexity** | Simpler - fewer concepts | More concepts (kernel, plugins, etc.) |
| **Function Calling** | Automatic with `tools=[...]` | Requires `FunctionChoiceBehavior.Auto()` |
| **Authentication** | `AzureCliCredential` | `AsyncAzureOpenAI` client |
| **Learning Curve** | Gentler for beginners | Steeper but more powerful |
| **Modularity** | Methods and functions | Kernel + plugin architecture |

### Code Comparison: Concurrent Execution

**MAF (Workflow-based):**

```python
from agent_framework import ConcurrentBuilder

# Define how to combine results
async def aggregate(results):
    return combine_all(results)

# Build and run workflow
workflow = (
    ConcurrentBuilder()
    .participants([agent1, agent2, agent3])
    .with_aggregator(aggregate)
    .build()
)
result = await workflow.run("query")
```

**Semantic Kernel:**

```python
from semantic_kernel.agents.group_chat import ConcurrentOrchestrator

orchestrator = ConcurrentOrchestrator(
    agents=[agent1, agent2, agent3]
)

async for message in orchestrator.invoke("query"):
    print(message.content)
```

**Key Difference:** MAF uses explicit workflow builders with clear aggregation logic, while SK provides higher-level orchestrator classes. Both are official patterns (not manual asyncio).

## 📚 Understanding the Code Structure

### Modular Design Principles

Both orchestrators follow these principles for beginners:

1. **Small, focused methods** - Each method does one thing
   - `_route_query()` - Just routing
   - `_fetch_articles_sequentially()` - Just fetching
   - `_create_summary()` - Just summarizing

2. **Descriptive names** - Method names explain what they do
   - Not: `process()`
   - But: `_aggregate_and_summarize()`

3. **Logging at every step** - Follow execution in real-time
   - `logger.info("[ROUTING] ...")`
   - `logger.info("[FETCHING] ...")`
   - `logger.error("[ERROR] ...")`

4. **Type hints** - Know what goes in and out
   ```python
   async def _route_query(self, user_query: str) -> list[str]:
   ```

5. **Docstrings** - Understand purpose and usage
   ```python
   """
   Use router agent to determine which news categories to fetch.
   
   Args:
       user_query: User's natural language query
       
   Returns:
       List of category names
   """
   ```

## 📊 Example Queries

Try these with either sequential or concurrent orchestrators:

1. **Multi-category queries:**
   - "What's happening in tech and business today?"
   - "Show me sports and health news updates"
   - "Give me science and tech innovation news"

2. **Specific topic queries:**
   - "Round up AI chip and cloud infra news"
   - "What happened in sports this morning?"
   - "Business headlines about big tech"

## 🔧 Customization Guide

### Add a New Category

1. No code changes needed! Just use a different category name:

```python
orchestrator = ConcurrentNewsOrchestrator(chat_client)
result = await orchestrator.run("What's new in cryptocurrency?")
```

The router agent will detect "cryptocurrency" and fetch accordingly.

### Modify Summary Style

Edit `agents/summarizer_agent.py`:

```python
instructions = (
    "You are an executive news summarizer. "
    "Create a 3-bullet summary..."  # Change to your preference
)
```

### Add Error Recovery

Both orchestrators already handle errors gracefully:

- Empty responses logged and skipped
- JSON parse errors caught and logged
- Category failures don't stop other categories
- Summarizer failures return error messages

### Extend Logging

Add more detail by increasing log level:

```python
logging.basicConfig(level=logging.DEBUG)  # More verbose
```

Or customize format:

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
```

## 🐛 Troubleshooting

**"ModuleNotFoundError: No module named 'agent_framework'"**

- Install: `pip install agent-framework azure-identity`
- Verify correct virtual environment is active

**"Authentication error" or 401/403**

- Run `az login` to authenticate
- Check `az account show` for current subscription
- Verify AZURE_OPENAI_ENDPOINT in .env

**"No articles found" or empty results**

- Verify NEWSAPI_API_KEY in .env
- Check NewsAPI rate limits (500 requests/day free tier)
- Enable logging to see which categories failed

**Logging not showing**

- Add this at the start of main file:
  ```python
  import logging
  logging.basicConfig(level=logging.INFO)
  ```

**Workflow errors**

- Check agent names are unique (e.g., "tech_agent", "sports_agent")
- Verify all agents return proper AgentRunResponse objects
- Enable DEBUG logging to see workflow internals

## 📚 Learn More

### Official Documentation

- [Microsoft Agent Framework Docs](https://learn.microsoft.com/en-us/agent-framework/)
- [Concurrent Workflows Guide](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/concurrent)
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/)

### Code Structure

- `agents/` - Individual agent builders (router, category, summarizer)
- `orchestration/` - Coordination logic (sequential vs concurrent)
- `plugins/` - External integrations (NewsAPI)
- `utils/` - Shared utilities (deduplication)

### Key Learnings

1. **Workflows over asyncio.gather()** - Use official patterns for better maintainability
2. **Logging is essential** - Makes debugging and learning much easier
3. **Small methods** - Easier to understand, test, and modify
4. **Type hints** - Documents expectations and catches errors early
5. **Docstrings** - Explain the "why" not just the "what"

## 🎯 Next Steps

1. ✅ Enable logging and run both demos
2. ✅ Read through orchestrator code with logging output side-by-side
3. ✅ Try modifying agent instructions
4. ✅ Experiment with different news categories
5. ✅ Compare execution flow between sequential and concurrent modes
6. ✅ Explore the workflow pattern in `concurrent_orchestrator.py`

---

**Tip for Beginners:** Start with `sequential_orchestrator.py` - it's simpler and easier to follow. Once you understand that, the concurrent workflow pattern will make more sense!
