# src/splitter.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
from .config import settings
import re

def create_splitter() -> RecursiveCharacterTextSplitter:
    """
    Creates a text splitter for documents with hierarchical splitting.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", "? ", "! ", " "],
    )
    return splitter

def split_with_metadata(text: str, title: str):
    """
    Splits text into chunks with metadata, preserving code blocks and images.

    Args:
        text (str): Full document text
        title (str): Document title for metadata

    Returns:
        List[Document]: Chunks as Document objects with metadata
    """
    # Step 1: Protect code blocks and images by replacing them with placeholders
    code_blocks = re.findall(r'```.*?```', text, flags=re.DOTALL)
    images = re.findall(r'!\[.*?\]\(.*?\)', text)
    
    placeholders = {}
    for i, block in enumerate(code_blocks + images):
        placeholder = f"[[PLACEHOLDER_{i}]]"
        placeholders[placeholder] = block
        text = text.replace(block, placeholder)

    # Step 2: Split text into chunks
    splitter = create_splitter()
    chunks = splitter.split_text(text)

    # Step 3: Restore code blocks and images in chunks
    restored_chunks = []
    for chunk in chunks:
        for placeholder, content in placeholders.items():
            chunk = chunk.replace(placeholder, content)
        restored_chunks.append(chunk)

    # Step 4: Add metadata
    documents = []
    for i, chunk in enumerate(restored_chunks):
        documents.append(
            Document(
                page_content=chunk,
                metadata={
                    "title": title,
                    "chunk_id": f"{title}_{i}"
                }
            )
        )

    return documents
