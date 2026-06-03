"""
Minimal test app - just Streamlit and Groq, nothing else
"""
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.title("🤖 Minimal Test")
st.write("If you see this, Streamlit Cloud is working!")

groq_key = os.getenv("GROQ_API_KEY")
if groq_key:
    st.success("✅ GROQ_API_KEY found!")
else:
    st.error("❌ GROQ_API_KEY missing - add to Streamlit Secrets")

try:
    from groq import Groq
    st.success("✅ Groq library loads")
except Exception as e:
    st.error(f"❌ Groq error: {e}")

st.write("---")
st.write("If all checks passed, basic deployment works!")
