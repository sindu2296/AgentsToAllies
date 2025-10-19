# Multi-Agent News Workflow

News gathering and summarization using Microsoft Agent Framework.

---
## How It Works

- Router agent analyzes your query and selects news categories
- Category agents fetch articles in parallel
- Deduplication removes duplicates
- Summarizer agent creates the final summary

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
INFO: [STAGE 1] Query Analysis - Starting
INFO: [STAGE 1] Calling Router Agent to analyze query...
INFO: [ROUTER] Raw response: {"targets": ["technology", "business", "general"]}
INFO: [ROUTER] Parsed targets: ['technology', 'business', 'general']
INFO: [ROUTER] Filtered targets: ['technology', 'business', 'general']
INFO: [STAGE 1] Query Analysis - Complete
INFO: [STAGE 1] Selected categories: ['technology', 'business', 'general']
INFO: [STAGE 2] News Gathering - Starting
INFO: [STAGE 2] Fetching from 3 categories in parallel
INFO: [CONCURRENT] Building MAF concurrent workflow
INFO: Dead-end executors detected (no outgoing edges): ['aggregate_agent_results']. Verify these are intended as final nodes in the workflow.
INFO: [CONCURRENT] Executing workflow to fetch news from 3 category agents in parallel...
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
INFO: [CONCURRENT] Aggregating results from 3 agents
INFO: [TECHNOLOGY] Parsed 6 articles
INFO: [BUSINESS] Parsed 6 articles
INFO: [GENERAL] Parsed 6 articles
INFO: Completed superstep 2
INFO: Workflow completed after 2 supersteps
INFO: [CONCURRENT] Workflow execution complete
INFO: [STAGE 2] News Gathering - Complete
INFO: [STAGE 2] Fetched 18 articles
INFO: [STAGE 3] Data Consolidation - Starting
INFO: [STAGE 3] Processing 18 raw articles
INFO: [STAGE 3] Data Consolidation - Complete
INFO: [STAGE 3] 16 unique articles after deduplication
INFO: [STAGE 4] Summary Generation - Starting
INFO: [STAGE 4] Calling Summarizer Agent to create executive brief from 16 articles...
INFO: [STAGE 4] Summary Generation - Complete

--------------------------------------------------------------------------------
WORKFLOW OUTPUT:
--------------------------------------------------------------------------------
**Categories analyzed (in parallel):** technology, business, general
*Workflow Statistics: 18 articles fetched, 16 unique articles, 3 categories*

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