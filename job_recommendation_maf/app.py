import streamlit as st
import asyncio
import sys
import logging
from pathlib import Path
from io import StringIO
import contextlib

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import build_chat_client
from orchestration.sequential_orchestrator import run_sequential_job_workflow

# Keep clean logs - structured workflow logging is handled in the orchestrator

# Setup logging capture
class LogCapture(logging.Handler):
    def __init__(self):
        super().__init__()
        self.logs = []
    
    def emit(self, record):
        self.logs.append(self.format(record))
    
    def get_logs(self):
        return "\n".join(self.logs)
    
    def clear(self):
        self.logs = []

# Setup stdout capture for print statements
class PrintCapture:
    def __init__(self):
        self.logs = []
        self.terminal = sys.stdout
    
    def write(self, message):
        if message.strip():
            self.logs.append(message)
        self.terminal.write(message)
    
    def flush(self):
        self.terminal.flush()
    
    def get_logs(self):
        return "".join(self.logs)
    
    def clear(self):
        self.logs = []

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
    .metrics-container {
        display: flex;
        justify-content: space-around;
        padding: 20px;
        background-color: #f8f9fa;
        border-radius: 10px;
        margin: 20px 0;
    }
    .metric-item {
        text-align: center;
    }
    .metric-number {
        font-size: 24px;
        font-weight: bold;
        color: #28a745;
    }
    .metric-label {
        font-size: 12px;
        color: #6c757d;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("💼 Multi-AI Agent Job Recommendation Workflow")
st.markdown("""
    **Welcome!** Enter your professional profile and watch as multiple AI agents 
    collaborate to find and recommend the best job opportunities for you. 
    The workflow runs through sequential stages for thorough job analysis.
""")

# Initialize log capture in session state
if "log_capture" not in st.session_state:
    st.session_state.log_capture = LogCapture()
    st.session_state.print_capture = PrintCapture()
    
    # Setup logging to capture structured workflow information like news_maf
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    st.session_state.log_capture.setLevel(logging.INFO)  # Capture INFO level logs
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    st.session_state.log_capture.setFormatter(formatter)
    root_logger.addHandler(st.session_state.log_capture)

# Sidebar for workflow info
with st.sidebar:
    st.header("ℹ️ Workflow Information")
    st.markdown("""
        ### AI Workflow Stages:
        1. **Job Extractor Agent** - Uses SERP API to find relevant jobs
        2. **Job Recommendation Agent** - AI analysis with GPT-4o
        3. **Job Summary Agent** - Creates summary with GPT-4o
        4. **Top 5 Recommended Jobs** - Final curated job list
        
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
    
    # Clear previous logs
    st.session_state.log_capture.clear()
    st.session_state.print_capture.clear()
    
    # Placeholder containers for workflow stages
    stage_containers = {
        "stage1": st.container(),
        "stage2": st.container(), 
        "stage3": st.container(),
        "stage4": st.container(),
        "logs": st.container(),
        "results": st.container()
    }
    
    try:
        with st.spinner("🔄 Running job recommendation workflow..."):
            # Initialize chat client
            chat_client = build_chat_client()
            
            # Display workflow progress  
            with stage_containers["stage1"]:
                with st.spinner("Stage 1: Job Extractor Agent..."):
                    st.markdown(
                        '<div class="workflow-stage"><div class="stage-title">Stage 1: Job Extractor Agent</div>'
                        '<div class="stage-content">🔍 Using SERP API to search for jobs matching your profile...</div></div>',
                        unsafe_allow_html=True
                    )
            
            with stage_containers["stage2"]:
                with st.spinner("Stage 2: Job Recommendation Agent..."):
                    st.markdown(
                        '<div class="workflow-stage"><div class="stage-title">Stage 2: Job Recommendation Agent</div>'
                        '<div class="stage-content">🤖 GPT-4o analyzing and ranking job matches...</div></div>',
                        unsafe_allow_html=True
                    )
            
            with stage_containers["stage3"]:
                with st.spinner("Stage 3: Job Summary Agent..."):
                    st.markdown(
                        '<div class="workflow-stage"><div class="stage-title">Stage 3: Job Summary Agent</div>'
                        '<div class="stage-content">📝 GPT-4o creating personalized job summary...</div></div>',
                        unsafe_allow_html=True
                    )
            
            with stage_containers["stage4"]:
                with st.spinner("Stage 4: Top 5 Recommended Jobs..."):
                    st.markdown(
                        '<div class="workflow-stage"><div class="stage-title">Stage 4: Top 5 Recommended Jobs</div>'
                        '<div class="stage-content">⭐ Finalizing curated list of best job matches...</div></div>',
                        unsafe_allow_html=True
                    )
            
            # Capture stdout while executing workflow
            original_stdout = sys.stdout
            sys.stdout = st.session_state.print_capture
            
            try:
                # Execute workflow using sequential orchestrator
                result = asyncio.run(run_sequential_job_workflow(chat_client, user_profile))
            finally:
                sys.stdout = original_stdout
            
            # Display logs in expandable section - BEFORE results
            with stage_containers["logs"]:
                st.markdown("---")
                st.markdown("### 📜 Workflow Logs")
                
                with st.expander("✓ Click to View Detailed Execution Logs", expanded=False):
                    logs_content = st.session_state.log_capture.get_logs()
                    print_content = st.session_state.print_capture.get_logs()
                    
                    combined_logs = ""
                    if logs_content:
                        combined_logs += "=== LOGGING OUTPUT ===\n" + logs_content + "\n\n"
                    if print_content:
                        combined_logs += "=== PRINT OUTPUT ===\n" + print_content
                    
                    if combined_logs.strip():
                        st.code(combined_logs, language="log")
                    else:
                        st.info("ℹ️ No logs captured during execution. Logs may be handled directly by the workflow.")

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
        
        # Display logs even on error - BEFORE error details
        with stage_containers["logs"]:
            st.markdown("---")
            st.markdown("### 📜 Error Logs")
            
            with st.expander("✓ Click to View Logs (Debugging Info)", expanded=True):
                logs_content = st.session_state.log_capture.get_logs()
                print_content = st.session_state.print_capture.get_logs()
                
                combined_logs = ""
                if logs_content:
                    combined_logs += "=== LOGGING OUTPUT ===\n" + logs_content + "\n\n"
                if print_content:
                    combined_logs += "=== PRINT OUTPUT ===\n" + print_content
                
                if combined_logs.strip():
                    st.code(combined_logs, language="log")
                else:
                    st.info("ℹ️ No logs captured during execution.")
        
        st.markdown("""
            **Troubleshooting tips:**
            - Ensure your environment variables (Azure credentials, SerpAPI key) are set correctly
            - Check that the configuration is set in `src/config.py`
            - Try with a clearer profile description like "Software engineer with Python"
            - Verify your SerpAPI account has available credits for job searches
        """)

else:
    if not user_profile and run_button:
        st.warning("⚠️ Please enter your professional profile first!")
    else:
        st.info("👆 Enter your professional profile and click 'Find Jobs' to get started")
