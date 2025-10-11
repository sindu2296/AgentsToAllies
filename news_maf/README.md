# News Processing with Microsoft Agent Framework (MAF)

This project demonstrates news processing using **Microsoft Agent Framework** alongside the Semantic Kernel implementation. Both frameworks implement the same news aggregation system, allowing for direct comparison.

## 🎯 Overview

The Microsoft Agent Framework implementation uses:
- **ChatAgent**: For creating AI agents with Azure OpenAI
- **Function Tools**: For agent capabilities (fetching news)
- **asyncio.gather()**: For concurrent execution
- **Azure CLI Authentication**: For secure credential management

## 📁 Project Structure

```
news_maf/
├── src/
│   ├── agents/
│   │   ├── router_agent.py       # Determines news categories
│   │   ├── category_agent.py     # Fetches news for a category
│   │   └── summarizer_agent.py   # Creates executive summaries
│   ├── orchestration/
│   │   ├── sequential_orchestrator.py   # Sequential processing
│   │   └── concurrent_orchestrator.py   # Parallel processing
│   ├── plugins/
│   │   └── news_plugin.py        # NewsAPI integration as function tool
│   ├── utils/
│   │   └── dedup.py              # Article deduplication
│   ├── config.py                 # Azure OpenAI client setup
│   ├── main_sequential.py        # Sequential demo
│   └── main_concurrent.py        # Concurrent demo
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

### Running the Examples

**Sequential Processing:**
```bash
cd news_maf/src
python main_sequential.py
```

**Concurrent Processing:**
```bash
cd news_maf/src
python main_concurrent.py
```

## 🏗️ Architecture

### Agent Flow

```
User Query
    ↓
┌─────────────────┐
│  Router Agent   │  ← ChatAgent determines categories
└─────────────────┘
    ↓
┌──────────────────────────────────────┐
│  Sequential or Concurrent Strategy   │
└──────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  Category Agents (ChatAgent + tools)    │
│  • technology_agent                     │
│  • sports_agent                         │
│  • business_agent                       │
└─────────────────────────────────────────┘
    ↓
┌─────────────────┐
│  Deduplication  │
└─────────────────┘
    ↓
┌─────────────────┐
│ Summarizer Agent│  ← ChatAgent creates executive brief
└─────────────────┘
    ↓
Final Summary
```

### Key Components

#### 1. **ChatAgent (agent_framework)**
The core agent type in MAF that provides:
- Instructions-based behavior
- Function tool integration
- Async run() method for execution
- Built-in conversation management

#### 2. **Function Tools**
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

#### 3. **AzureOpenAIChatClient**
Client for connecting to Azure OpenAI:
```python
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

client = AzureOpenAIChatClient(
    credential=AzureCliCredential(),
    endpoint=endpoint,
    model_id=deployment
)
```

#### 4. **Agent Invocation**
Simple async pattern:
```python
result = await agent.run("Your prompt here")
response_text = result.text
```

## 🆚 MAF vs Semantic Kernel Comparison

| Feature | Microsoft Agent Framework | Semantic Kernel |
|---------|---------------------------|-----------------|
| **Agent Type** | `ChatAgent` | `ChatCompletionAgent` |
| **Function Tools** | Direct Python functions | `@kernel_function` decorators |
| **Invocation** | `await agent.run(prompt)` | `async for msg in agent.invoke(messages)` |
| **Orchestration** | Manual with `asyncio.gather()` | Built-in `ConcurrentOrchestration` |
| **Setup Complexity** | Simpler - fewer concepts | More concepts (kernel, plugins, etc.) |
| **Function Calling** | Automatic with `tools=[...]` | Requires `FunctionChoiceBehavior.Auto()` |
| **Authentication** | `AzureCliCredential` | `AsyncAzureOpenAI` client |
| **Learning Curve** | Gentler for beginners | Steeper but more powerful |

### Code Comparison

**MAF:**
```python
# Simple and direct
agent = ChatAgent(
    chat_client=client,
    instructions="Fetch tech news",
    tools=[fetch_news_function]
)
result = await agent.run("Go")
print(result.text)
```

**Semantic Kernel:**
```python
# More structured but more setup
kernel = Kernel()
kernel.add_service(chat_completion)
kernel.add_plugin(NewsPlugin(), "news")

settings = kernel.get_prompt_execution_settings_from_service_id()
settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

agent = ChatCompletionAgent(
    instructions="Fetch tech news",
    kernel=kernel,
    arguments=KernelArguments(settings=settings)
)

async for msg in agent.invoke(messages="Go"):
    print(msg.content)
```

## ✨ MAF Features Used

### 1. **Simple Agent Creation**
```python
agent = ChatAgent(
    chat_client=client,
    instructions="You are a helpful assistant",
    name="helper",
    tools=[my_function]  # Optional function tools
)
```

### 2. **Straightforward Execution**
```python
result = await agent.run("Tell me a joke")
print(result.text)  # Direct access to response
```

### 3. **Function Tools Integration**
```python
def get_weather(city: str) -> str:
    """Get weather for a city"""
    return f"Sunny in {city}"

agent = ChatAgent(
    chat_client=client,
    instructions="You can check weather",
    tools=[get_weather]
)

result = await agent.run("What's the weather in Seattle?")
# Agent automatically calls get_weather("Seattle")
```

### 4. **Concurrent Execution**
```python
# Parallel agent execution using asyncio
agents = [agent1, agent2, agent3]
results = await asyncio.gather(*[agent.run(query) for agent in agents])
```

## 🎓 When to Use MAF vs SK

### Use Microsoft Agent Framework When:
- ✅ You want simpler, more direct agent code
- ✅ You're building straightforward agentic applications
- ✅ You prefer minimal abstractions
- ✅ You're new to agent frameworks
- ✅ You need quick prototypes

### Use Semantic Kernel When:
- ✅ You need complex multi-agent orchestration patterns
- ✅ You want built-in orchestration (Sequential, Concurrent, Handoff, etc.)
- ✅ You're building enterprise-scale agentic systems
- ✅ You need advanced plugin ecosystems
- ✅ You want fine-grained control over agent behavior

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

## 🔧 Customization

### Add a New Category Agent
```python
new_agent = build_category_agent(chat_client, "crypto_agent", "cryptocurrency")
```

### Change Summary Format
Edit `summarizer_agent.py`:
```python
instructions = "Create a 3-bullet summary with..."
```

### Add Error Handling
```python
try:
    result = await agent.run(query)
except Exception as e:
    print(f"Error: {e}")
```

## 🐛 Troubleshooting

**Import errors for agent_framework:**
- Run: `pip install agent-framework azure-identity`
- Ensure you're in the correct virtual environment

**Authentication errors:**
- Run `az login` to authenticate with Azure CLI
- Verify you have access to the Azure OpenAI resource

**No articles found:**
- Check NEWSAPI_API_KEY in .env
- Free tier has rate limits

## 📚 Learn More

- [Microsoft Agent Framework Documentation](https://learn.microsoft.com/en-us/agent-framework/)
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Agent Framework GitHub](https://github.com/microsoft/agent-framework)

## 🎯 Next Steps

1. ✅ Run both sequential and concurrent demos
2. ✅ Compare with Semantic Kernel implementation
3. ✅ Modify agent instructions
4. ✅ Add custom function tools
5. ✅ Experiment with different orchestration patterns
