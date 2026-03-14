"""
Streamlit web interface for the Multi-Source Agentic Q&A Assistant.
Run with: streamlit run streamlit_app.py
"""
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Check if API key is set FIRST
groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    st.error("❌ GROQ_API_KEY not configured. Please add it to Streamlit Secrets.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Agentic Q&A Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import modules AFTER checking API key
try:
    from supervisor_graph import build_graph, format_answer_with_sources
    from conversation_memory import create_memory
except Exception as e:
    st.error(f"❌ Error loading modules: {str(e)}")
    st.stop()

# CSS Styling
st.markdown("""
<style>
    .main {
        max-width: 1000px;
    }
    .stMessage {
        padding: 10px;
        border-radius: 5px;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196F3;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "memory" not in st.session_state:
    st.session_state.memory = create_memory(max_history=100)

if "graph" not in st.session_state:
    st.session_state.graph = build_graph()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("📊 Assistant Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear History"):
            st.session_state.memory.clear()
            st.session_state.messages = []
            st.success("History cleared!")
    
    with col2:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    # Statistics
    st.markdown("---")
    st.subheader("📈 Statistics")
    
    stats = st.session_state.memory.get_agent_stats()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("SQL Queries", stats.get("SQL", 0))
    
    with col2:
        st.metric("RAG Queries", stats.get("RAG", 0))
    
    with col3:
        st.metric("Total Messages", len(st.session_state.memory))
    
    # Conversation history
    st.markdown("---")
    st.subheader("💬 Conversation History")
    
    if len(st.session_state.memory) > 0:
        for msg in st.session_state.memory.messages[:10]:  # Last 10
            role_icon = "👤" if msg.get("role") == "user" else "🤖"
            agent_info = f" ({msg.get('agent', '')})" if msg.get('agent') else ""
            st.write(f"{role_icon} {msg['content'][:50]}...{agent_info}")
    else:
        st.info("No conversation yet. Start by asking a question!")

# Main content
st.title("🤖 Multi-Source Agentic Q&A Assistant")
st.markdown("""
This assistant intelligently answers questions by:
- 📊 Querying structured databases (SQL Agent)
- 📄 Retrieving from documents (RAG Agent)
- ✅ Validating questions for relevance
- 📋 Maintaining conversation history
- 🔗 Showing sources for answers
""")

st.markdown("---")

# Chat interface
st.subheader("💬 Chat")

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.write(msg["content"])
            
            # Show sources if available
            if "sources" in msg and msg["sources"]:
                with st.expander(f"📎 Sources ({msg.get('agent', 'Unknown')})"):
                    for i, source in enumerate(msg["sources"], 1):
                        st.write(f"**{i}. {source}**")

# Input area
user_input = st.chat_input("Ask me anything business-related...")

if user_input:
    # Add user message to display
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Add to memory
    st.session_state.memory.add_user_message(user_input)
    
    # Process query
    with st.spinner("🔄 Processing your question..."):
        try:
            result = st.session_state.graph.invoke({"question": user_input})
            
            answer = result.get("answer", "No answer")
            sources = result.get("sources", [])
            agent = result.get("agent", "Unknown")
            
            # Add to memory
            st.session_state.memory.add_assistant_message(answer, agent=agent, sources=sources)
            
            # Display answer
            with st.chat_message("assistant"):
                st.write(answer)
                
                # Show sources
                if sources:
                    with st.expander(f"📎 Sources ({agent})"):
                        for i, source in enumerate(sources, 1):
                            st.write(f"**{i}. {source}**")
                
                st.caption(f"🤖 Answered by: **{agent}**")
            
            # Add to message history
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources,
                "agent": agent
            })
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            
            with st.chat_message("assistant"):
                st.write(f"Sorry, I encountered an error: {str(e)}")

# Footer
st.markdown("---")
st.caption("💡 Examples: 'List first 5 products' | 'How many customers?' | 'Show orders from 1996'")
