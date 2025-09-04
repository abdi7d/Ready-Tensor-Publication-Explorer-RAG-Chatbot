# src/vectordb.py
from .config import settings
from .embeddings import get_embedder
from pathlib import Path
from typing import List
from langchain.schema import Document
from langchain_chroma import Chroma


# choose imports lazily to avoid import errors
try:
    from langchain_chroma import Chroma
except Exception:
    Chroma = None
try:
    from langchain_community.vectorstores import FAISS
    from faiss import Index  # type: ignore
except Exception:
    FAISS = None

class PersistedVectorStore:
    def __init__(self, persist_directory: str = "VectorStore"):
        self.persist_directory = persist_directory
        self.emb = get_embedder()
        self.store = None

    def create_or_update(self, documents: List[Document]):
        """
        Create or update a vector store from a list of langchain Documents.
        """
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
        if settings.vectorstore.lower() == "chroma":
            if Chroma is None:
                raise RuntimeError("Chroma is not available in this environment.")
            # self.store = Chroma.from_documents(documents, embedding=self.emb, persist_directory=self.persist_directory)
            self.store = Chroma.from_documents(documents, embedding=self.emb, persist_directory=self.persist_directory)
            # self.store.persist()
        elif settings.vectorstore.lower() == "faiss":
            if FAISS is None:
                raise RuntimeError("FAISS not available.")
            self.store = FAISS.from_documents(documents, embedding=self.emb)
            self.store.save_local(self.persist_directory)
        else:
            raise ValueError("Unsupported vectorstore: " + settings.vectorstore)

    def load(self):
        """
        Load an existing vector store.
        """
        if settings.vectorstore.lower() == "chroma":
            if Chroma is None:
                raise RuntimeError("Chroma not available.")
            # Chroma will look at persist_directory automatically
            self.store = Chroma(persist_directory=self.persist_directory, embedding_function=self.emb)
            return self.store
        elif settings.vectorstore.lower() == "faiss":
            if FAISS is None:
                raise RuntimeError("FAISS not available.")
            return FAISS.load_local(self.persist_directory, self.emb)
        raise RuntimeError("Unsupported vectorstore")

    def as_retriever(self, **kwargs):
        if self.store is None:
            self.load()
        return self.store.as_retriever(**kwargs)
