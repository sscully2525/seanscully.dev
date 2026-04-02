"""
Streamlit UI for Multi-Agent Orchestrator
Interactive interface for the agent system.
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.orchestrator import AgentOrchestrator
from src.memory.conversation import ConversationMemory
import uuid

# Page config
st.set_page_config(
    page_title="Multi-Agent Orchestrator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .agent-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .execution-path {
        background-color: #e8f4f8;
        border-left: 4px solid #1f77b4;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = AgentOrchestrator()
if 'memory' not in st.session_state:
    st.session_state.memory = ConversationMemory()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Sidebar
with st.sidebar:
    st.title("⚙️ Configuration")
    
    st.subheader("Session")
    st.code(st.session_state.session_id[:8], language="text")
    
    if st.button("🔄 New Session"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.chat_history = []
        st.rerun()
    
    st.divider()
    
    st.subheader("Available Agents")
    agents = {
        "🔍 Research": "Web search and information gathering",
        "💻 Code": "Programming and technical tasks",
        "📊 Analysis": "Data analysis and insights",
        "🧮 Math": "Calculations and numerical reasoning",
        "✨ Creative": "Writing and content generation"
    }
    for agent, desc in agents.items():
        st.markdown(f"**{agent}**  
{desc}")
    
    st.divider()
    
    st.subheader("About")
    st.markdown("""
    This multi-agent system uses LangGraph to coordinate 
    specialized AI agents for complex tasks.
    
    **Architecture:**
    - Router → Agents → Synthesizer
    - Redis-backed memory
    - Streaming execution
    """)

# Main content
st.markdown('<p class="main-header">🤖 Multi-Agent Orchestrator</p>', unsafe_allow_html=True)
st.markdown("*Intelligent task routing with specialized AI agents*")

# Example queries
st.subheader("💡 Try these examples:")
col1, col2, col3 = st.columns(3)

example_queries = [
    "Explain quantum computing and write a Python simulation",
    "Analyze Tesla stock trends and create a visualization script",
    "Research renewable energy trends with data analysis"
]

for i, col in enumerate([col1, col2, col3]):
    with col:
        if st.button(example_queries[i], key=f"example_{i}"):
            st.session_state.current_query = example_queries[i]
            st.rerun()

# Query input
st.divider()
query = st.text_area(
    "Enter your query:",
    value=st.session_state.get('current_query', ''),
    placeholder="Ask anything... The system will route to the right agent(s)",
    height=100
)

# Execute button
col1, col2 = st.columns([1, 5])
with col1:
    execute = st.button("🚀 Execute", type="primary", use_container_width=True)

# Process query
if execute and query:
    with st.spinner("🤔 Thinking..."):
        # Save user message
        st.session_state.memory.save_message(
            st.session_state.session_id,
            "user",
            query
        )
        
        # Execute orchestrator
        result = st.session_state.orchestrator.invoke(
            query,
            st.session_state.session_id
        )
        
        # Save assistant message
        st.session_state.memory.save_message(
            st.session_state.session_id,
            "assistant",
            result["response"]
        )
        
        # Add to chat history
        st.session_state.chat_history.append({
            "query": query,
            "response": result["response"],
            "execution_path": result["execution_path"],
            "agent_outputs": result["agent_outputs"]
        })

# Display results
if st.session_state.chat_history:
    st.divider()
    
    # Show latest result
    latest = st.session_state.chat_history[-1]
    
    # Execution path
    st.subheader("📍 Execution Path")
    path_html = " → ".join([f"**{agent}**" for agent in latest["execution_path"]])
    st.markdown(f'<div class="execution-path">{path_html}</div>', unsafe_allow_html=True)
    
    # Response
    st.subheader("💬 Response")
    st.markdown(latest["response"])
    
    # Agent outputs (expandable)
    with st.expander("🔍 View Agent Outputs"):
        tabs = st.tabs(["Research", "Code", "Analysis"])
        
        with tabs[0]:
            research = latest["agent_outputs"]["research"]
            if research:
                st.json(research)
            else:
                st.info("No research agent invoked")
        
        with tabs[1]:
            code = latest["agent_outputs"]["code"]
            if code:
                if "code_blocks" in code:
                    for block in code["code_blocks"]:
                        st.code(block["code"], language=block.get("language", "python"))
                st.json(code)
            else:
                st.info("No code agent invoked")
        
        with tabs[2]:
            analysis = latest["agent_outputs"]["analysis"]
            if analysis:
                st.json(analysis)
            else:
                st.info("No analysis agent invoked")

# Chat history
if len(st.session_state.chat_history) > 1:
    st.divider()
    st.subheader("📜 Conversation History")
    
    for i, chat in enumerate(reversed(st.session_state.chat_history[:-1])):
        with st.expander(f"Q: {chat['query'][:50]}..."):
            st.markdown(f"**Path:** {' → '.join(chat['execution_path'])}")
            st.markdown(chat['response'][:500] + "...")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666;">
    <small>Built with LangGraph, Streamlit, and ❤️ | 
    <a href="https://github.com/sscully2525/seanscully.dev">View on GitHub</a></small>
</div>
""", unsafe_allow_html=True)
