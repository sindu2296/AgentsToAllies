# Multi-Agent News Workflow

News gathering and summarization using Microsoft Agent Framework with direct agent calls.

---

## 🚀 Quick Start - Try the Streamlit UI

### Launch the Interactive Web UI
```bash
streamlit run app.py
```

**The easiest way to get started!** Open your browser at `http://localhost:8501` and:
1. Enter any news query (e.g., "Latest AI breakthroughs", "Tech industry updates")
2. Watch the agents and processes execute in real-time with visual indicators as a part of workflow pattern
3. Download results as text files

**No configuration needed** - Just run the command above!

---

## How It Works

- **Query Classifier Agent** analyzes your query and determines relevant news topics
- **News Gatherer Agents** fetch articles in parallel from your selected topics  
- **Data Consolidation** removes duplicate articles for cleaner data
- **Summarizer Agent** creates an executive summary of all findings

---

## Workflow Architecture

```
User Query
    ↓
Query Classifier Agent (analyzes query, determines categories)
    ↓
News Gatherer Agents (parallel execution for each category)
├── News Gatherer Agent 1 (Tech)
├── News Gatherer Agent 2 (Business)
└── News Gatherer Agent 3 (General)
    ↓
Data Consolidation (deduplication)
    ↓
Summarizer Agent (creates executive summary)
    ↓
Final Output
```

---

## References

- [Microsoft Agent Framework Documentation](https://learn.microsoft.com/en-us/agent-framework/)
- [ConcurrentBuilder Pattern](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/concurrent)

---

Sample input and output:

WORKFLOW EXECUTION
================================================================================
Query: What's new in AI and technology for women in computing?
--------------------------------------------------------------------------------

INFO: [WORKFLOW] Starting workflow: What's new in AI and technology for women in computing?
INFO: ================================================================================
INFO: Stage 1: Query Classifier Agent
INFO: ================================================================================
INFO: → LLM Call: Analyzing query to determine categories...
INFO: ✓ Selected categories: ['technology', 'science']
INFO: ================================================================================
INFO: Stage 2: News Gatherer Agents
INFO: ================================================================================
INFO: → Fetching [technology] category
INFO:   • LLM Call: Agent deciding to call fetch_top_headlines tool...
INFO:   • Tool Call: fetch_top_headlines(category='technology')
INFO:   • LLM Call: Agent processing tool results...
INFO: → Fetching [science] category
INFO:   • LLM Call: Agent deciding to call fetch_top_headlines tool...
INFO:   • Tool Call: fetch_top_headlines(category='science')
INFO:   • LLM Call: Agent processing tool results...
INFO: Dead-end executors detected (no outgoing edges): ['aggregate_agent_results']. Verify these are intended as final nodes in the workflow.
INFO: Yielding pre-loop events
INFO: Starting superstep 1
INFO: Function name: fetch_top_headlines
INFO: Function fetch_top_headlines succeeded.
INFO: Function name: fetch_top_headlines
INFO: Function fetch_top_headlines succeeded.
INFO: Completed superstep 1
INFO: Starting superstep 2
INFO: ✓ [technology] Fetched 6 articles
INFO: ✓ [science] Fetched 6 articles
INFO: Completed superstep 2
INFO: Workflow completed after 2 supersteps
INFO: ✓ Gathered 12 articles total
INFO: ================================================================================
INFO: Stage 3: Data Consolidation
INFO: ================================================================================
INFO: ✓ Removed 0 duplicates
INFO: ✓ Consolidated to 12 unique articles
INFO: ================================================================================
INFO: Stage 4: Summarizer Agent
INFO: ================================================================================
INFO: → LLM Call: Generating executive summary from articles...
INFO: ✓ Executive summary generated

--------------------------------------------------------------------------------
WORKFLOW OUTPUT:
--------------------------------------------------------------------------------
**Categories (parallel):** technology, science
**Statistics:** 12 articles gathered, 12 unique, 2 categories

1. Arc Raiders, the popular extraction shooter, has unveiled an ambitious 2025 roadmap including a new map, community events, and quests, signaling continued development and engagement-focused enhancements [Eurogamer](https://www.eurogamer.net/arc-raiders-has-an-impressive-2025-roadmap-and-its-bringing-a-new-map-new-events-and-other-game-changers).

2. Logitech’s Alto Keys K98M mechanical keyboard introduces enthusiast-grade features such as precise typing feedback and visually appealing design, broadening accessibility in the mechanical keyboard market [The Verge](https://www.theverge.com/tech/810124/logitech-alto-keys-k98m-mechanical-keyboard-price-specs-impressions).

3. Google Translate is adding an innovative model picker allowing users to choose between "Fast" or "Advanced" translation modes, improving accessibility and tailored usage for diverse needs [9to5Google](http://9to5google.com/2025/11/02/google-translate-model-picker/).

4. Researchers documented unique predatory behavior by orcas flipping great white sharks to access their livers, revealing sophisticated hunting techniques in marine species [NBC News](https://www.nbcnews.com/science/science-news/video-orcas-hunting-great-white-sharks-rcna240951).

5. Comet 3I/ATLAS demonstrated non-gravitational acceleration near the Sun and turned blue, providing scientists with intriguing insights into interstellar phenomena and cometary compositions [Fox Weather](https://www.foxweather.com/earth-space/latest-3i-atlas-comet-sun-earth-november-2025).
================================================================================