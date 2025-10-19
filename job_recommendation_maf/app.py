import streamlit as st
import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import build_chat_client
from orchestration.sequential_orchestrator import run_sequential_job_workflow

st.set_page_config(
    page_title="Job Recommendation Workflow",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .workflow-stage {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #28a745;
        background-color: #f0f9f5;
    }
    .stage-title {
        font-size: 18px;
        font-weight: bold;
        color: #28a745;
    }
    .stage-content {
        font-size: 14px;
        color: #333;
        margin-top: 8px;
    }
    .job-card {
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border: 1px solid #e0e0e0;
        background-color: #f9f9f9;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("💼 Job Recommendation Workflow")
st.markdown("""
    **Welcome!** Enter your professional profile and watch as multiple AI agents 
    collaborate to find and recommend the best job opportunities for you. 
    The workflow extracts jobs, analyzes matches, and summarizes results.
""")

# Sidebar for workflow info
with st.sidebar:
    st.header("ℹ️ Workflow Information")
    st.markdown("""
        ### Workflow Stages:
        1. **Job Extraction** - Searches for jobs matching your profile
        2. **Job Recommendation** - Ranks and filters best matches
        3. **Summary Generation** - Creates detailed job summaries
        
        ### Input Example:
        "Software engineer with Python and Azure cloud experience"
    """)

# Main input area
st.markdown("### 👤 Your Professional Profile")
user_profile = st.text_area(
    "Describe your role, skills, and experience",
    placeholder="e.g., 'Software engineer with 5+ years of Python and AWS cloud experience'",
    height=100,
    label_visibility="collapsed"
)

col1, col2 = st.columns([3, 1])
with col2:
    run_button = st.button("🚀 Find Jobs", type="primary", use_container_width=True)

if run_button and user_profile:
    st.markdown("---")
    st.markdown("### 📊 Workflow Execution")
    
    # Placeholder containers for workflow stages
    stage_containers = {
        "stage1": st.container(),
        "stage2": st.container(),
        "stage3": st.container(),
        "results": st.container()
    }
    
    try:
        with st.spinner("🔄 Running job recommendation workflow..."):
            # Initialize workflow
            chat_client = build_chat_client()
            
            # Display workflow progress
            with stage_containers["stage1"]:
                with st.spinner("Stage 1: Extracting jobs..."):
                    st.markdown(
                        '<div class="workflow-stage"><div class="stage-title">Stage 1: Job Extraction</div>'
                        '<div class="stage-content">🔍 Searching for jobs matching your profile...</div></div>',
                        unsafe_allow_html=True
                    )
            
            with stage_containers["stage2"]:
                with st.spinner("Stage 2: Analyzing matches..."):
                    st.markdown(
                        '<div class="workflow-stage"><div class="stage-title">Stage 2: Job Recommendation</div>'
                        '<div class="stage-content">⭐ Ranking jobs by relevance to your skills...</div></div>',
                        unsafe_allow_html=True
                    )
            
            with stage_containers["stage3"]:
                with st.spinner("Stage 3: Generating summaries..."):
                    st.markdown(
                        '<div class="workflow-stage"><div class="stage-title">Stage 3: Summary Generation</div>'
                        '<div class="stage-content">📝 Creating detailed job summaries...</div></div>',
                        unsafe_allow_html=True
                    )
            
            # Execute workflow
            result = asyncio.run(run_sequential_job_workflow(chat_client, user_profile))
            
            # Display results
            with stage_containers["results"]:
                st.markdown("---")
                st.success("✅ Workflow completed successfully!")
                st.markdown("### 💼 Job Recommendations")
                st.markdown(result)
                
                # Option to download results
                st.download_button(
                    label="📥 Download Recommendations",
                    data=result,
                    file_name="job_recommendations.txt",
                    mime="text/plain"
                )
    
    except Exception as e:
        st.error(f"❌ Error executing workflow: {e}")
        st.markdown("""
            **Troubleshooting tips:**
            - Ensure your environment variables (Azure credentials, SerpAPI key) are set correctly
            - Check that the configuration is set in `src/config.py`
            - Try with a clearer profile description like "Software engineer with Python"
        """)

else:
    if not user_profile and run_button:
        st.warning("⚠️ Please enter your professional profile first!")
    else:
        st.info("👆 Enter your professional profile and click 'Find Jobs' to get started")
