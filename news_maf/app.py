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
    page_title="News Extraction AI Workflow",
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
st.title("📰 News Extraction AI Workflow")
st.markdown("""
    **Welcome!** This workflow helps you discover and summarize **news by category** 
    (e.g., technology, health, business). 
    
    ⚠️ **Note:** This is designed for category-based queries, not specific news items. 
    For example:
    - ✅ "What's new in technology and health?"
    - ✅ "Give me top headlines in entertainment and sports"
    - ❌ "What did Trump say about X?" (too specific)
    
    Multiple AI agents work in parallel to gather, deduplicate, and summarize articles efficiently.
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
        ### Multi-Agent Workflow:
        
        **🤖Agents:**
        - **Query Classifier Agent** - Analyzes your query
        - **News Gatherer Agents** - Fetch articles by category (parallel)
        - **Summarizer Agent** - Creates executive summary

        **⚙️Processes:**
        - **Data Consolidation** - Removes duplicates
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
            
            # ========================================================================
            # STAGE 1: [query_classification] - Query Classifier Agent
            # ========================================================================
            with stage_containers["stage1"]:
                with st.spinner("Stage 1: Query classification..."):
                    st.markdown(
                        '<div class="workflow-stage">'
                        '<div class="stage-title">🔍 STAGE 1: Query Classifier Agent</div>'
                        '<div class="stage-content">Analyzing your query to determine relevant news categories...</div>'
                        '</div>',
                        unsafe_allow_html=True
                    )
            
            # ========================================================================
            # STAGE 2: [news_gathering] - News Gatherer Agents (Parallel)
            # ========================================================================
            with stage_containers["stage2"]:
                with st.spinner("Stage 2: News gathering..."):
                    st.markdown(
                        '<div class="workflow-stage">'
                        '<div class="stage-title">📡 STAGE 2: News Gatherer Agents</div>'
                        '<div class="stage-content">Multiple gatherer agents fetching articles in parallel (one per category)...</div>'
                        '</div>',
                        unsafe_allow_html=True
                    )
            
            # ========================================================================
            # STAGE 3: [data_consolidation] - Data Processing
            # ========================================================================
            with stage_containers["stage3"]:
                with st.spinner("Stage 3: Data consolidation..."):
                    st.markdown(
                        '<div class="workflow-stage">'
                        '<div class="stage-title">🧹 STAGE 3: Data Consolidation</div>'
                        '<div class="stage-content">Removing duplicate articles and consolidating results...</div>'
                        '</div>',
                        unsafe_allow_html=True
                    )
            
            # ========================================================================
            # STAGE 4: [summary_generation] - Summarizer Agent
            # ========================================================================
            with stage_containers["stage4"]:
                with st.spinner("Stage 4: Summary generation..."):
                    st.markdown(
                        '<div class="workflow-stage">'
                        '<div class="stage-title">✍️ STAGE 4: Summarizer Agent</div>'
                        '<div class="stage-content">Creating executive summary from consolidated articles...</div>'
                        '</div>',
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
