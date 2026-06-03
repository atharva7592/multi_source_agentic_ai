"""
Streamlit configuration initialization for both local and cloud deployment.
Handles vector store caching and session state management.
"""
import os
import streamlit as st
from pathlib import Path


def initialize_vectorstore():
    """Initialize vectorstore - recreate if needed (handles cloud deployments)"""
    try:
        from rag_setup import vectordb
        return vectordb
    except Exception as e:
        st.error(f"❌ Error initializing vector database: {str(e)}")
        st.stop()


def setup_streamlit_cache():
    """Configure Streamlit caching directories"""
    streamlit_dir = Path.home() / ".streamlit"
    streamlit_dir.mkdir(exist_ok=True)
    
    # Configure cache settings
    cache_dir = streamlit_dir / "cache"
    cache_dir.mkdir(exist_ok=True)
    
    return cache_dir


def get_data_path():
    """Get the path to company documents"""
    base_path = Path(__file__).parent
    data_path = base_path / "data" / "company_docs"
    
    if not data_path.exists():
        raise FileNotFoundError(f"Data directory not found at {data_path}")
    
    return data_path


def verify_dependencies():
    """Verify all required dependencies are installed"""
    required_packages = {
        "streamlit": "Streamlit",
        "langchain": "LangChain",
        "langgraph": "LangGraph",
        "chromadb": "ChromaDB",
        "groq": "Groq",
    }
    
    missing = []
    for package, name in required_packages.items():
        try:
            __import__(package)
        except ImportError:
            missing.append(name)
    
    if missing:
        st.error(f"❌ Missing dependencies: {', '.join(missing)}")
        st.info("Run: pip install -r requirements.txt")
        st.stop()


def setup_logging():
    """Configure logging for debugging"""
    import logging
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    return logging.getLogger(__name__)


if __name__ == "__main__":
    setup_streamlit_cache()
    verify_dependencies()
    setup_logging()
    print("✅ Streamlit configuration initialized")
