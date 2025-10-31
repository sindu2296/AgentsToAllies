# Framework Comparison: Semantic Kernel vs Microsoft Agent Framework

This document provides a detailed comparison between the Semantic Kernel (SK) and Microsoft Agent Framework (MAF) implementations of the same news aggregation system.

## 📊 Quick Comparison Table

| Aspect | Semantic Kernel | Microsoft Agent Framework |
|--------|-----------------|---------------------------|
| **Package** | `semantic_kernel` | `agent-framework` |
| **Agent Class** | `ChatCompletionAgent` | `ChatAgent` |
| **Setup Complexity** | Medium (kernel, services, plugins) | Low (client, agent) |
| **Function Integration** | `@kernel_function` decorator | Direct Python function |
| **Agent Invocation** | `async for msg in agent.invoke()` | `await agent.run()` |
| **Function Calling** | `FunctionChoiceBehavior.Auto()` | Automatic with `tools=[...]` |
| **Orchestration** | Built-in patterns (Concurrent, Sequential) | Manual with asyncio |
| **Authentication** | `AsyncAzureOpenAI` client | `AzureCliCredential` |
| **Learning Curve** | Steeper | Gentler |
| **Best For** | Complex orchestrations, enterprise | Quick prototypes, simplicity |

## 🏗️ Architecture Comparison

### Semantic Kernel Structure
```
Kernel → Service → Plugin → Agent → Orchestration
```

### MAF Structure
```
ChatClient → Agent → asyncio orchestration
```

## 💻 Code Comparison

### 1. Setup & Configuration

**Semantic Kernel:**
```python
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from openai import AsyncAzureOpenAI

client = AsyncAzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key
)

chat_completion = AzureChatCompletion(
    deployment_name=deployment,
    async_client=client,
)

kernel = Kernel()
kernel.add_service(chat_completion)
```

**Microsoft Agent Framework:**
```python
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

chat_client = AzureOpenAIChatClient(
    credential=AzureCliCredential(),
    endpoint=endpoint,
    model_id=deployment
)
```

**Winner:** MAF (simpler, fewer concepts)

### 2. Function/Plugin Definition

**Semantic Kernel:**
```python
from semantic_kernel.functions import kernel_function

class NewsPlugin:
    @kernel_function(
        name="fetch_top_headlines",
        description="Fetch top headlines from NewsAPI for a given category."
    )
    def fetch_top_headlines(self, category: str, limit: int = 6) -> str:
        # Implementation
        return json.dumps(articles)

# Must add to kernel
kernel.add_plugin(NewsPlugin(), plugin_name="news")
```

**Microsoft Agent Framework:**
```python
def fetch_top_headlines(category: str, limit: int = 6) -> str:
    """
    Fetch top headlines from NewsAPI for a given category.
    """
    # Implementation
    return json.dumps(articles)

# No registration needed, pass directly to agent
```

**Winner:** MAF (no decorators, direct functions)

### 3. Agent Creation

**Semantic Kernel:**
```python
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.functions import KernelArguments

settings = kernel.get_prompt_execution_settings_from_service_id()
settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

agent = ChatCompletionAgent(
    name="category_agent",
    instructions=f"Fetch news for {category}",
    kernel=kernel,
    arguments=KernelArguments(settings=settings)
)
```

**Microsoft Agent Framework:**
```python
from agent_framework import ChatAgent

agent = ChatAgent(
    chat_client=chat_client,
    instructions=f"Fetch news for {category}",
    name="category_agent",
    tools=[fetch_top_headlines]
)
```

**Winner:** MAF (significantly simpler)

### 4. Agent Invocation

**Semantic Kernel:**
```python
response = ""
async for msg in agent.invoke(messages="Fetch news"):
    response += msg.content.content
```

**Microsoft Agent Framework:**
```python
result = await agent.run("Fetch news")
response = result.text
```

**Winner:** MAF (more intuitive)

### 5. Concurrent Execution

**Semantic Kernel:**
```python
from semantic_kernel.agents import ConcurrentOrchestration
from semantic_kernel.agents.runtime import InProcessRuntime

runtime = InProcessRuntime()
runtime.start()

concurrent_orch = ConcurrentOrchestration(members=agents)
orchestration_result = await concurrent_orch.invoke(
    task="Fetch news",
    runtime=runtime
)

results = await orchestration_result.get()

await runtime.stop_when_idle()
```

**Microsoft Agent Framework:**
```python
import asyncio

results = await asyncio.gather(*[
    agent.run("Fetch news") 
    for agent in agents
])
```

**Winner:** SK (built-in pattern with runtime management) vs MAF (simpler code but manual)

## 📈 Feature Comparison

### Semantic Kernel Advantages

✅ **Built-in Orchestration Patterns**
- ConcurrentOrchestration
- SequentialOrchestration  
- HandoffOrchestration
- GroupChatOrchestration
- MagenticOrchestration

✅ **Rich Plugin Ecosystem**
- Standardized plugin format
- Easy plugin sharing and reuse
- Strong typing with decorators

✅ **Advanced Features**
- Memory management
- Planning capabilities
- Semantic functions
- Prompt templates

✅ **Enterprise Ready**
- Mature framework
- Extensive documentation
- Production-tested patterns

### Microsoft Agent Framework Advantages

✅ **Simplicity**
- Fewer concepts to learn
- Direct Python functions as tools
- No kernel abstraction

✅ **Quick Setup**
- Azure CLI authentication
- Minimal configuration
- Fast prototyping

✅ **Intuitive API**
- Simple `agent.run()` pattern
- Direct result access
- Less boilerplate

✅ **Flexibility**
- Easy integration with any chat client
- Standard Python async patterns
- Minimal framework lock-in

## 🎯 When to Use Each

### Choose Semantic Kernel When:

1. **Complex Multi-Agent Systems**
   - Need sophisticated orchestration
   - Multiple coordination patterns
   - Enterprise-scale deployments

2. **Rich Plugin Ecosystem**
   - Want to leverage existing plugins
   - Need standardized tool format
   - Building reusable components

3. **Advanced AI Features**
   - Semantic memory
   - AI planning
   - Prompt engineering

4. **Long-term Projects**
   - Need stability and maturity
   - Want comprehensive documentation
   - Require production support

### Choose Microsoft Agent Framework When:

1. **Quick Prototypes**
   - Need fast iteration
   - Building proof-of-concepts
   - Testing agent ideas

2. **Simple Agent Applications**
   - Straightforward workflows
   - Minimal orchestration needs
   - Direct function calling

3. **Learning Agent Development**
   - New to agent frameworks
   - Want gentle learning curve
   - Prefer minimal abstractions

4. **Custom Integrations**
   - Need flexibility
   - Building custom chat clients
   - Want minimal framework overhead

## 📝 Real-World Example Comparison

### Scenario: Fetch and summarize news from 3 categories

**Lines of Code:**
- Semantic Kernel: ~150 lines
- MAF: ~100 lines

**Concepts to Learn:**
- Semantic Kernel: Kernel, Service, Plugin, Agent, Orchestration, Runtime, FunctionChoiceBehavior
- MAF: ChatClient, Agent, tools

**Setup Time:**
- Semantic Kernel: ~10 minutes
- MAF: ~3 minutes

**Debugging Complexity:**
- Semantic Kernel: Medium (multiple layers)
- MAF: Low (fewer abstractions)

## 🔄 Migration Between Frameworks

### SK to MAF Migration
Relatively straightforward:
1. Replace Kernel setup with ChatClient
2. Convert plugins to functions
3. Replace agent invocation pattern
4. Replace orchestration with asyncio

### MAF to SK Migration
More involved:
1. Add Kernel setup
2. Wrap functions in plugins
3. Add FunctionChoiceBehavior configuration
4. Use built-in orchestration patterns

## 🎓 Learning Resources

### Semantic Kernel
- [Official Docs](https://learn.microsoft.com/en-us/semantic-kernel/)
- [GitHub Repository](https://github.com/microsoft/semantic-kernel)
- [Sample Applications](https://github.com/microsoft/semantic-kernel/tree/main/python/samples)

### Microsoft Agent Framework
- [Official Docs](https://learn.microsoft.com/en-us/agent-framework/)
- [GitHub Repository](https://github.com/microsoft/agent-framework)
- [Quick Start Guide](https://learn.microsoft.com/en-us/agent-framework/tutorials/quick-start)

## 💡 Recommendations

### For This Project
Both implementations are provided so you can:
1. **Compare** the approaches side-by-side
2. **Learn** different agent patterns
3. **Choose** the right tool for your use case

### Getting Started
1. Start with **MAF** (`news_maf/`) if you're new to agents
2. Move to **SK** (`news/`) when you need advanced features
3. Run both implementations to see the differences

### Production Deployment
- **Simple applications:** MAF is sufficient
- **Complex systems:** SK provides better structure
- **Hybrid approach:** Use both for different parts of your system

## 🔍 Summary

Both frameworks are excellent choices, each with their strengths:

- **Semantic Kernel** = Power, structure, enterprise-ready
- **Microsoft Agent Framework** = Simplicity, speed, flexibility

Choose based on your project's complexity, your team's experience, and your long-term goals. The news aggregation samples in this repository let you explore both approaches hands-on!
