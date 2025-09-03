# src/config.py
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    provider: str = Field("groq", description="groq|gemini")
    model_name: str = Field("llama-3.1-8b-instant")
    embed_model: str = Field("all-MiniLM-L6-v2")
    vectorstore: str = Field("chroma", description="chroma|faiss")
    chunk_size: int = Field(1000)   # ~200 words per chunk
    chunk_overlap: int = Field(200) # Overlap to preserve context
    top_k: int = Field(10)
    temperature: float = Field(0.5)

    GROQ_API_KEY: str | None = None
    GOOGLE_API_KEY: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
