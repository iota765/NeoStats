import os
from typing import Optional

from langchain_groq import ChatGroq
from config.config import LLM_MODEL, GROQ_API_KEY

_groq_llm = None
_openai_llm = None
_gemini_llm = None


def get_chatgroq_model() -> ChatGroq:
    """Singleton Groq chat model using config values."""
    global _groq_llm
    if _groq_llm is None:
        print("[llm] Loading Groq model")
        _groq_llm = ChatGroq(model=LLM_MODEL, api_key=GROQ_API_KEY)
        print("[llm] Groq LLM loaded successfully")
    return _groq_llm


def get_openai_model() -> Optional[object]:
    """Return an OpenAI chat model if OPENAI_API_KEY is set, otherwise None."""
    from langchain_openai import ChatOpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    print("[llm] Loading OpenAI model")
    return ChatOpenAI(api_key=api_key, model="gpt-4o-mini")


def get_gemini_model() -> Optional[object]:
    """Return a Gemini chat model if GOOGLE_API_KEY/GEMINI_API_KEY is set, otherwise None."""
    from langchain_google_genai import ChatGoogleGenerativeAI

    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    print("[llm] Loading Gemini model")
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=api_key)


def load_llm() -> object:
    """Return the first configured chat model, preferring Groq for this project."""
    print("[llm] Selecting LLM provider")
    if GROQ_API_KEY:
        return get_chatgroq_model()

    openai_model = get_openai_model()
    if openai_model is not None:
        return openai_model

    gemini_model = get_gemini_model()
    if gemini_model is not None:
        return gemini_model

    raise ValueError(
        "No LLM is configured. Set GROQ_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY/GEMINI_API_KEY."
    )
