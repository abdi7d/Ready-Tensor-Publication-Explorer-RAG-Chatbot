# src/embeddings.py
from .config import settings
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
except Exception:
    GoogleGenerativeAIEmbeddings = None

def get_embedder():
    """ 
    Returns an embeddings object based on settings.
    Default: HuggingFace sentence-transformers/all-MiniLM-L6-v2
    If provider = gemini and Google embeddings available, use that.
    """
    if settings.provider.lower() == "gemini" and GoogleGenerativeAIEmbeddings is not None:
        # Using a Google-hosted embeddings model (if available)
        return GoogleGenerativeAIEmbeddings(model=settings.embed_model)
    # Default to HF/embedder
    return HuggingFaceEmbeddings(model_name=settings.embed_model)
