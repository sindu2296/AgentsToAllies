# GHC 2025 Travel Planner

AI-powered multi-agent system for planning trips to **Grace Hopper Conference 2025** in Chicago using **Microsoft Agent Framework**.

## 🎯 Overview

This system helps GHC attendees find the best flights from Seattle to Chicago and hotels near McCormick Place, then creates a comprehensive travel itinerary.

**Conference Dates: November 4-7, 2025**

### Architecture

**Three Specialized Agents:**
1. **✈️ Flight Agent** - Searches for flights from Seattle (SEA) to Chicago (ORD/MDW)
2. **🏨 Hotel Agent** - Finds accommodation near McCormick Place within budget
3. **📋 Summary Agent** - Creates comprehensive travel itineraries

**Two Workflow Patterns:**
- **Sequential**: Flight → Hotel → Summary (step-by-step processing)
- **Concurrent**: (Flight || Hotel) → Summary (parallel processing for speed)

**Memory System:**
- Stores user preferences (dates, budget, flight preferences)
- Shared across agents in a session
- Enables personalized recommendations

## 📋 Features

✅ Flight search with preferences (direct flights, timing, cabin class)  
✅ Hotel search near GHC venue with budget filtering  
✅ User preference memory across agent interactions  
✅ Sequential and concurrent workflow patterns  
✅ Interactive Streamlit UI  
✅ Mock data fallback when API keys unavailable  

## 🚀 Quick Start

### Prerequisites

1. Python 3.13.9
2. Azure OpenAI API credentials
3. (Optional) SerpAPI key for real flight/hotel data

### Installation

```bash
# Navigate to the project folder
cd ghc_travel_planner

# Install dependencies (from root requirements.txt)
pip install -r ../requirements.txt
```

### Configuration

Ensure your `.env` file (in the root folder) has:

```bash
# Required
AI_FOUNDRY_AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=your_deployment_name

# Optional (for real flight/hotel data)
SERPAPI_API_KEY=your_serpapi_key
```

> **Note:** Without `SERPAPI_API_KEY`, the system uses realistic mock data.

## 🎮 Usage

### Option 1: Streamlit Web App (Recommended)

```bash
cd ghc_travel_planner
streamlit run app.py
```

Then:
1. Set your travel dates
2. Choose flight preferences (direct flights, arrival time)
3. Set hotel budget and proximity preferences
4. Select workflow type (Sequential or Concurrent)
5. Click "Plan My Trip"

### Option 2: Sequential Workflow (Command Line)

```bash
cd ghc_travel_planner
python src/main_sequential.py
```

This runs the sequential workflow: Flight Agent → Hotel Agent → Summary Agent

### Option 3: Concurrent Workflow (Command Line)

```bash
cd ghc_travel_planner
python src/main_concurrent.py
```

This runs the concurrent workflow: (Flight Agent || Hotel Agent) → Summary Agent

## 📁 Project Structure

```
ghc_travel_planner/
├── app.py                          # Streamlit web interface
├── README.md                       # This file
└── src/
    ├── config.py                   # Azure OpenAI client setup
    ├── main_sequential.py          # Sequential workflow runner
    ├── main_concurrent.py          # Concurrent workflow runner
    ├── agents/
    │   ├── flight_agent.py         # Flight search agent with memory
    │   ├── hotel_agent.py          # Hotel search agent with memory
    │   └── summary_agent.py        # Itinerary summary agent
    ├── orchestration/
    │   ├── sequential_orchestrator.py   # Sequential workflow
    │   └── concurrent_orchestrator.py   # Concurrent workflow
    ├── plugins/
    │   ├── flight_search_plugin.py # Flight search tool (SerpAPI)
    │   └── hotel_search_plugin.py  # Hotel search tool (SerpAPI)
    └── utils/
        └── memory.py               # User preference storage
```

## 🧠 Agent Details

### Flight Agent

**Responsibilities:**
- Search flights from Seattle to Chicago
- Filter based on user preferences (direct flights, timing)
- Store travel dates and flight preferences in memory
- Recommend best 2-3 options

**Tools:**
- `search_flights(travel_dates, preferences)` - Uses SerpAPI Google Flights

**Key Considerations:**
- ORD (O'Hare) is closer to McCormick Place than MDW (Midway)
- Direct flights preferred for convenience
- Arrival time affects conference schedule

### Hotel Agent

**Responsibilities:**
- Search hotels near McCormick Place
- Filter by budget and distance
- Store budget preferences in memory
- Recommend best 2-3 options

**Tools:**
- `search_hotels(travel_dates, budget)` - Uses SerpAPI Google Hotels

**Key Considerations:**
- Hyatt Regency McCormick Place is connected to venue
- Walking distance (<0.5 miles) highly valued
- Budget-friendly options important for students

### Summary Agent

**Responsibilities:**
- Review flight and hotel recommendations
- Create comprehensive travel itinerary
- Include costs, timings, helpful tips
- Provide actionable travel plan

**Output Includes:**
- Travel summary with dates and costs (Nov 4-7, 2025)
- Flight details (outbound/return)
- Hotel information
- Transportation tips
- Total cost estimate

## 🔄 Workflows

### Sequential Workflow

```
User Query
    ↓
Flight Agent (searches flights + stores preferences)
    ↓
Hotel Agent (searches hotels + stores budget)
    ↓
Summary Agent (creates itinerary)
    ↓
Complete Travel Plan
```

**Advantages:**
- Predictable order of operations
- Each agent builds on previous results
- Clear step-by-step processing

**Use When:**
- Order matters
- Need to see each step
- Debugging or understanding flow

### Concurrent Workflow

```
User Query
    ↓
    ├─> Flight Agent (parallel) ─┐
    │                             ├─> Summary Agent
    └─> Hotel Agent (parallel) ──┘
                ↓
        Complete Travel Plan
```

**Advantages:**
- Faster execution (parallel processing)
- Efficient resource utilization
- Same quality results

**Use When:**
- Speed is important
- Operations are independent
- Scalability matters

## 💾 Memory System

The memory system stores user preferences across agent interactions:

```python
from utils.memory import get_memory

memory = get_memory()

# Store preferences
memory.store_preference("travel_dates", "2025-09-23 to 2025-09-27")
memory.store_preference("budget", "under $200/night")
memory.store_preference("flight_preference", "direct flights")

# Retrieve preferences
dates = memory.get_preference("travel_dates")
budget = memory.get_preference("budget")

# Get all preferences
all_prefs = memory.get_all_preferences()

# Clear memory for new session
memory.clear()
```

**Features:**
- In-memory storage (session-based)
- Shared across all agents
- Easy to extend to persistent storage (database, Redis, etc.)

## 🎨 Customization

### Adding New Agents

1. Create agent file in `src/agents/`
2. Define instructions and tools
3. Add to orchestrator workflow

### Adding New Tools

1. Create tool function in `src/plugins/`
2. Add type annotations for parameters
3. Register with agent's `tools` list

### Extending Memory

Modify `src/utils/memory.py` to:
- Add persistent storage (database, file, Redis)
- Track conversation history
- Implement user profiles

## 🧪 Example Output

```
================================================================================
GHC 2025 Travel Planner - Sequential Workflow
================================================================================
✓ Created 3 agents: flight_agent → hotel_agent → summary_agent
✓ Workflow built successfully

Processing request: I need help planning my trip to Grace Hopper Conference...
--------------------------------------------------------------------------------

[FLIGHT PLUGIN] Searching flights for: 2025-11-04 to 2025-11-07
[FLIGHT PLUGIN] Found 3 flights

Step 01 [user]
--------------------------------------------------------------------------------
I need help planning my trip to Grace Hopper Conference 2025 in Chicago...

Step 02 [flight_agent]
--------------------------------------------------------------------------------
Based on your preferences, I found 3 excellent direct flight options from Seattle to Chicago:

1. Alaska Airlines AS 5678 - $295
   - Departure: 10:30 AM, Arrival: 4:45 PM
   - Direct flight, 4h 15m

... (complete conversation flow)
```

## 🛠️ Troubleshooting

**Import Errors:**
- Ensure you're running from the correct directory
- Check `sys.path` modifications in files

**No API Key Warnings:**
- System will use mock data automatically
- Add `SERPAPI_API_KEY` to `.env` for real data

**Azure OpenAI Errors:**
- Verify API key and endpoint in `.env`
- Check deployment name matches your Azure resource

## 📚 Learn More

- [Microsoft Agent Framework Documentation](https://github.com/microsoft/agent-framework)
- [Grace Hopper Conference](https://ghc.anitab.org/)
- [SerpAPI Google Flights API](https://serpapi.com/google-flights-api)
- [SerpAPI Google Hotels API](https://serpapi.com/google-hotels-api)

## 🤝 Contributing

This is a sample project for the "From Agents to Allies" session. Feel free to:
- Add new agents (restaurant recommendations, event planning, etc.)
- Implement persistent memory
- Add more travel preferences
- Create additional workflows

---

**Built with ❤️ for GHC 2025 attendees using Microsoft Agent Framework**
