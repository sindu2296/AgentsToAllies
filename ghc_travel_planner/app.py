"""
Streamlit App for GHC 2025 Travel Planner
Interactive UI for planning trips to Grace Hopper Conference
"""
import streamlit as st
import asyncio
import sys
from pathlib import Path
from datetime import date

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import build_chat_client
from orchestration.sequential_orchestrator import run_sequential_travel_workflow
from orchestration.concurrent_orchestrator import run_concurrent_travel_workflow
from utils.memory import reset_memory

# Page configuration
st.set_page_config(
    page_title="GHC 2025 Travel Planner",
    page_icon="✈️",
    layout="wide"
)

# Title and description
st.title("✈️ GHC 2025 Travel Planner")
st.markdown("""
Welcome to the **Grace Hopper Conference 2025 Travel Planner**! 

This AI-powered system helps you find the best flights and hotels for your trip to Chicago.
Our agents will search for options and create a personalized travel itinerary for you.

**Conference Details:**
- 📍 Venue: McCormick Place, Chicago
- 📅 Dates: November 4-7, 2025
""")

st.divider()

# Sidebar for preferences
with st.sidebar:
    st.header("🎯 Your Preferences")
    
    # Travel dates
    st.subheader("📅 Travel Dates")
    departure_date = st.date_input(
        "Departure Date",
        value=date(2025, 11, 4),
        min_value=date(2025, 11, 1),
        max_value=date(2025, 11, 30)
    )
    return_date = st.date_input(
        "Return Date",
        value=date(2025, 11, 7),
        min_value=date(2025, 11, 1),
        max_value=date(2025, 11, 30)
    )
    
    # Flight preferences
    st.subheader("✈️ Flight Preferences")
    flight_type = st.selectbox(
        "Flight Type",
        ["Direct flights only", "Direct flights preferred", "Open to connections"]
    )
    cabin_class = st.selectbox(
        "Cabin Class",
        ["Economy", "Premium Economy", "Business", "First"]
    )
    arrival_time = st.selectbox(
        "Preferred Arrival Time (Day 1)",
        ["Morning (before 12 PM)", "Afternoon (12-5 PM)", "Evening (after 5 PM)", "Flexible"]
    )
    
    # Hotel preferences
    st.subheader("🏨 Hotel Preferences")
    budget = st.selectbox(
        "Budget per Night",
        ["Under $150", "Under $200", "Under $250", "$250-$350", "Above $350", "No preference"]
    )
    proximity = st.selectbox(
        "Proximity to Venue",
        ["Walking distance (< 0.5 miles)", "Close (< 2 miles)", "Within Chicago", "No preference"]
    )
    
    # Workflow type
    st.divider()
    st.subheader("⚙️ Workflow Type")
    workflow_type = st.radio(
        "Select workflow:",
        ["Sequential (Step-by-step)", "Concurrent (Parallel search)"],
        help="Sequential processes one at a time. Concurrent runs flight and hotel searches in parallel for faster results."
    )
    
    # Plan button
    plan_button = st.button("🚀 Plan My Trip", type="primary", use_container_width=True)

# Main content area
if plan_button:
    # Build the query from user inputs
    travel_dates = f"{departure_date.strftime('%Y-%m-%d')} to {return_date.strftime('%Y-%m-%d')}"
    
    user_query = f"""
    I need help planning my trip to Grace Hopper Conference 2025 in Chicago.
    
    Travel Dates: {travel_dates}
    
    Flight Preferences:
    - Flying from Seattle (SEA)
    - Flight type: {flight_type}
    - Cabin class: {cabin_class}
    - Preferred arrival time on first day: {arrival_time}
    
    Hotel Preferences:
    - Budget: {budget}
    - Proximity preference: {proximity}
    - Close to McCormick Place
    
    Please find the best options for both flights and accommodation and create a complete travel itinerary!
    """
    
    # Reset memory
    reset_memory()
    
    # Show user query
    with st.expander("📝 View Your Request", expanded=False):
        st.text(user_query)
    
    # Progress indicator
    with st.spinner("🔍 Our AI agents are planning your trip..."):
        try:
            # Build chat client
            chat_client = build_chat_client()
            
            # Run the appropriate workflow
            if "Sequential" in workflow_type:
                result = asyncio.run(run_sequential_travel_workflow(chat_client, user_query))
            else:
                result = asyncio.run(run_concurrent_travel_workflow(chat_client, user_query))
            
            # Display results
            st.success("✅ Travel Planning Complete!")
            
            # Parse and display the conversation
            st.subheader("📋 Your Travel Itinerary")
            
            # Display the full result
            messages = result.split("--------------------------------------------------------------------------------")
            
            for message in messages:
                if message.strip():
                    # Check if it's a step header
                    if "Step" in message and "[" in message:
                        lines = message.strip().split("\n")
                        if len(lines) > 0:
                            header = lines[0]
                            content = "\n".join(lines[1:])
                            
                            # Determine agent type for icon
                            icon = "👤"
                            if "flight_agent" in message:
                                icon = "✈️"
                            elif "hotel_agent" in message:
                                icon = "🏨"
                            elif "summary_agent" in message:
                                icon = "📋"
                            
                            with st.expander(f"{icon} {header}", expanded=True):
                                st.markdown(content)
                    else:
                        st.markdown(message)
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.exception(e)

else:
    # Welcome message
    st.info("""
    👈 **Get Started:**
    1. Set your travel dates in the sidebar
    2. Choose your flight preferences (direct flights, arrival time, etc.)
    3. Set your hotel budget and proximity preferences
    4. Select Sequential or Concurrent workflow
    5. Click "Plan My Trip" to get your personalized itinerary!
    
    Our AI agents will:
    - ✈️ Search for the best flights from Seattle to Chicago
    - 🏨 Find hotels near McCormick Place within your budget
    - 📋 Create a complete travel itinerary with all details
    """)
    
    # Show example
    with st.expander("💡 See Example Results"):
        st.markdown("""
        **Flight Results:**
        - Option 1: Alaska Airlines AS 5678 - 10:30 AM departure, $295
        - Option 2: United Airlines UA 1234 - 8:00 AM departure, $320
        
        **Hotel Results:**
        - Hyatt Regency McCormick Place - $189/night, connected to venue
        - Hotel Chicago Downtown - $175/night, 4.2 miles from venue
        
        **Complete Itinerary:**
        Our summary agent will combine everything into a clear, actionable travel plan!
        """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Powered by Microsoft Agent Framework & Azure OpenAI</p>
    <p>Built for Grace Hopper Conference 2025 attendees</p>
</div>
""", unsafe_allow_html=True)
