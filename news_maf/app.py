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
from orchestration.news_workflow import NewsGatheringWorkflow

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
    page_title="Multi-AI News Workflow",
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
        border-left: 5px solid #0066cc;
        background-color: #f0f7ff;
    }
    .stage-title {
        font-size: 18px;
        font-weight: bold;
        color: #0066cc;
    }
    .stage-content {
        font-size: 14px;
        color: #333;
        margin-top: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("📰 Multi-AI Agent News Workflow")
st.markdown("""
    **Welcome!** Enter any query and watch as multiple AI agents collaborate to gather, 
    analyze, and summarize news across different categories. The workflow runs in parallel 
    stages for maximum efficiency.
""")

# Initialize log capture in session state
if "log_capture" not in st.session_state:
    st.session_state.log_capture = LogCapture()
    st.session_state.print_capture = PrintCapture()
    
    # Setup root logger to capture all logs (INFO level only - no DEBUG messages)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    st.session_state.log_capture.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    st.session_state.log_capture.setFormatter(formatter)
    root_logger.addHandler(st.session_state.log_capture)

# Sidebar for workflow info
with st.sidebar:
    st.header("ℹ️ Workflow Information")
    st.markdown("""
        ### Workflow Stages:
        1. **Query Analysis** - Router agent analyzes your query
        2. **Parallel Fetching** - Category agents fetch news in parallel
        3. **Data Consolidation** - Duplicate removal and quality filtering
        4. **Summary Generation** - Summarizer creates executive brief
    """)

# Main input area
st.markdown("### 🔍 Enter Your Query")
query = st.text_input(
    "What would you like to know about?",
    placeholder="e.g., 'What's new in AI and technology?'",
    label_visibility="collapsed"
)

col1, col2 = st.columns([3, 1])
with col2:
    run_button = st.button("🚀 Run Workflow", type="primary", use_container_width=True)

if run_button and query:
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
        with st.spinner("🔄 Running multi-agent workflow..."):
            # Initialize workflow
            chat_client = build_chat_client()
            workflow = NewsGatheringWorkflow(chat_client=chat_client)
            
            # Display workflow progress
            with stage_containers["stage1"]:
                with st.spinner("Stage 1: Analyzing query..."):
                    st.markdown(
                        '<div class="workflow-stage"><div class="stage-title">Stage 1: Query Analysis</div>'
                        '<div class="stage-content">🔍 Router agent analyzing your query...</div></div>',
                        unsafe_allow_html=True
                    )
            
            with stage_containers["stage2"]:
                with st.spinner("Stage 2: Fetching news..."):
                    st.markdown(
                        '<div class="workflow-stage"><div class="stage-title">Stage 2: Parallel News Gathering</div>'
                        '<div class="stage-content">📡 Fetching articles from multiple categories in parallel...</div></div>',
                        unsafe_allow_html=True
                    )
            
            with stage_containers["stage3"]:
                with st.spinner("Stage 3: Processing data..."):
                    st.markdown(
                        '<div class="workflow-stage"><div class="stage-title">Stage 3: Data Consolidation</div>'
                        '<div class="stage-content">🧹 Removing duplicates and filtering data...</div></div>',
                        unsafe_allow_html=True
                    )
            
            with stage_containers["stage4"]:
                with st.spinner("Stage 4: Generating summary..."):
                    st.markdown(
                        '<div class="workflow-stage"><div class="stage-title">Stage 4: Summary Generation</div>'
                        '<div class="stage-content">✍️ Summarizer agent creating executive brief...</div></div>',
                        unsafe_allow_html=True
                    )
            
            # Capture stdout while executing workflow
            original_stdout = sys.stdout
            sys.stdout = st.session_state.print_capture
            
            try:
                # Execute workflow
                result = asyncio.run(workflow.execute(query))
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
                st.markdown("### 📋 Results")
                st.markdown(result)
                
                # Option to download results
                st.download_button(
                    label="📥 Download Results",
                    data=result,
                    file_name="news_workflow_results.txt",
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
            - Ensure your environment variables (Azure credentials) are set correctly
            - Check that the news API keys are configured in `src/config.py`
            - Try a simpler query like "technology news"
        """)

else:
    if not query and run_button:
        st.warning("⚠️ Please enter a query first!")
    else:
        st.info("👆 Enter a query and click 'Run Workflow' to get started")
