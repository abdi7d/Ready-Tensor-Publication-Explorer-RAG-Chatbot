# src/llm.py
import os
from .config import settings
from langchain_core.language_models import BaseChatModel

# Try to import provider wrappers; if missing, raise descriptive error when used
try:
    from langchain_groq import ChatGroq
except Exception:
    ChatGroq = None

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except Exception:
    ChatGoogleGenerativeAI = None

def get_chat_llm() -> BaseChatModel:
    provider = settings.provider.lower()
    if provider == "groq":
        if ChatGroq is None:
            raise RuntimeError("langchain_groq not installed or available.")
        api_key = os.getenv("GROQ_API_KEY", settings.GROQ_API_KEY)
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not set. Put it in .env or env variables.")
        return ChatGroq(groq_api_key=api_key, model_name=settings.model_name, temperature=settings.temperature)
    elif provider == "gemini":
        if ChatGoogleGenerativeAI is None:
            raise RuntimeError("langchain_google_genai not installed or available.")
        api_key = os.getenv("GOOGLE_API_KEY", settings.GOOGLE_API_KEY)
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY is not set. Put it in .env or env variables.")
        return ChatGoogleGenerativeAI(model=settings.model_name, temperature=settings.temperature)
    else:
        raise ValueError("Unsupported provider: " + settings.provider)
