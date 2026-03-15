import os
from dotenv import load_dotenv

load_dotenv()


def _get_config_value(name: str):
    value = os.getenv(name)
    if value:
        return value

    try:
        import streamlit as st

        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass

    return None


GROQ_API_KEY = _get_config_value("GROQ_API_KEY")
TAVILY_API_KEY = _get_config_value("TAVILY_API_KEY")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "openai/gpt-oss-20b"

if GROQ_API_KEY and not os.getenv("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY

if TAVILY_API_KEY and not os.getenv("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
