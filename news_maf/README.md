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

================================================================================
WORKFLOW EXECUTION
================================================================================
Query: Latest news on diversity and inclusion in tech companies
--------------------------------------------------------------------------------

INFO: [WORKFLOW] Starting news gathering workflow
INFO: [WORKFLOW] Query: Latest news on diversity and inclusion in tech companies
INFO: [QUERY_CLASSIFICATION] Analyzing user query
INFO: [QUERY_CLASSIFICATION] Calling Query Classifier Agent...
INFO: [QUERY_CLASSIFIER] Raw response: {"targets": ["technology", "business", "general"]}
INFO: [QUERY_CLASSIFIER] Parsed targets: ['technology', 'business', 'general']
INFO: [QUERY_CLASSIFIER] Filtered targets: ['technology', 'business', 'general']
INFO: [QUERY_CLASSIFICATION] Classification complete
INFO: [QUERY_CLASSIFICATION] Selected categories: ['technology', 'business', 'general']
INFO: [NEWS_GATHERING] Gathering news from selected categories
INFO: [NEWS_GATHERING] Categories: ['technology', 'business', 'general']
INFO: [NEWS_GATHERING] Executing 3 agents in parallel
INFO: [CONCURRENT_EXECUTION] Building concurrent workflow
INFO: Dead-end executors detected (no outgoing edges): ['aggregate_agent_results']. Verify these are intended as final nodes in the workflow.
INFO: [CONCURRENT_EXECUTION] Executing 3 News Gatherer Agents in parallel...
INFO: Yielding pre-loop events
INFO: Starting superstep 1
INFO: Function name: fetch_top_headlines
INFO: Function fetch_top_headlines succeeded.
INFO: Function name: fetch_top_headlines
INFO: Function fetch_top_headlines succeeded.
INFO: Function name: fetch_top_headlines
INFO: Function fetch_top_headlines succeeded.
INFO: Completed superstep 1
INFO: Starting superstep 2
INFO: [CONCURRENT_EXECUTION] Aggregating results from 3 agents
INFO: [TECHNOLOGY] Parsed 6 articles
INFO: [BUSINESS] Parsed 6 articles
INFO: [GENERAL] Parsed 6 articles
INFO: Completed superstep 2
INFO: Workflow completed after 2 supersteps
INFO: [CONCURRENT_EXECUTION] Concurrent execution complete
INFO: [NEWS_GATHERING] News gathering complete
INFO: [NEWS_GATHERING] Articles collected: 18

INFO: [DATA_CONSOLIDATION] Consolidating articles
INFO: [DATA_CONSOLIDATION] Processing 18 raw articles
INFO: [DATA_CONSOLIDATION] Consolidation complete
INFO: [DATA_CONSOLIDATION] Unique articles after deduplication: 16

INFO: [SUMMARY_GENERATION] Generating executive summary
INFO: [SUMMARY_GENERATION] Calling Summarizer Agent with 16 articles...
INFO: [SUMMARY_GENERATION] Summary generation complete

--------------------------------------------------------------------------------
WORKFLOW OUTPUT:
--------------------------------------------------------------------------------
**Categories analyzed (in parallel):** technology, business, general
*Workflow Statistics: 18 articles gathered, 16 unique articles, 3 categories*

### Executive Summary

1. **Technology Advancements in Gaming and AI**:
   - Nintendo released a new hardware bundle featuring "Pokémon Legends: Z-A" for Switch 2 users [Nintendo Life](https://www.nintendolife.com/news/2025/10/reminder-pokemon-legends-z-a-switch-2-hardware-bundle-now-available).
   - Anthropic enhanced its Claude AI chatbot with "Skills," improving its functionality for workplace tasks [The Verge](https://www.theverge.com/ai-artificial-intelligence/800868/anthropic-claude-skills-ai-agents).
   - A splinter group emerged in the GZDoom community after developers inserted AI-generated code, creating the UZDoom fork [Ars Technica](https://arstechnica.com/gaming/2025/10/civil-war-gzdoom-fan-developers-split-off-over-use-of-chatgpt-generated-code).

2. **Energy Infrastructure Upgrades**:
   - The Department of Energy approved a $1.6 billion loan guarantee to modernize transmission lines across five Midwest states, aimed at reducing fossil fuel dependency [Associated Press](https://apnews.com/article/trump-energy-loan-power-transmission-lines-midwest-df38cc75193e29317d706c2d7c03c1eb).

3. **Consumer Health Alert**:
   - A Consumer Reports investigation revealed lead contamination in certain protein powders, cautioning consumers about potential risks from high exposure [NPR](https://www.npr.org/2025/10/16/nx-s1-5576294/protein-powder-lead-consumer-reports).

4. **Market and Business Concerns**:
   - Stocks dropped as fears about regional banks' lending practices intensified, prompting market uncertainty [CNBC](https://www.cnbc.com/2025/10/15/stock-market-today-live-updates.html).
   - United Airlines and Delta warned that extended government shutdowns could significantly harm aviation bookings [CNBC](https://www.cnbc.com/2025/10/16/government-shutdown-united-airlines-ceo-scott-kirby.html).

5. **Obituaries and Political Updates**:
   - Susan Stamberg, a pioneering woman in U.S. broadcasting and NPR "founding mother," passed away [NPR](https://www.npr.org/2025/10/16/1184880448/susan-stamberg-obituary).
   - Senate Democrats blocked a military funding bill amidst budget disagreements over the ongoing shutdown [Politico](https://www.politico.com/live-updates/2025/10/16/congress/senate-democrats-military-funding-bill-00611606).
================================================================================