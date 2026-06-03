import streamlit as st

st.title("Multi-Source Agentic AI System")
st.write("✅ App is starting... if you see this, dependencies are working!")

# Test imports one by one
try:
    from langchain.chat_models import ChatGroq
    st.success("✅ LangChain loaded")
except Exception as e:
    st.error(f"❌ LangChain error: {e}")

try:
    import chromadb
    st.success("✅ ChromaDB loaded")
except Exception as e:
    st.error(f"❌ ChromaDB error: {e}")

try:
    from sentence_transformers import SentenceTransformer
    st.success("✅ Sentence Transformers loaded")
except Exception as e:
    st.error(f"❌ Sentence Transformers error: {e}")

try:
    from groq import Groq
    st.success("✅ Groq loaded")
except Exception as e:
    st.error(f"❌ Groq error: {e}")

st.write("---")
st.write("If all packages loaded, main app should work!")
