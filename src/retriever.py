# src/retriever.py
from .vectordb import PersistedVectorStore
from .config import settings

def get_retriever(persist_directory: str = "VectorStore"):
    store = PersistedVectorStore(persist_directory=persist_directory)
    store.load()
    # default search kwargs
    search_kwargs = {"k": settings.top_k,}
    retriever = store.as_retriever(search_kwargs=search_kwargs)
    return retriever
