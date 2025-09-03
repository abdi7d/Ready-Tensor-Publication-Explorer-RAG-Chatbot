# ingest.py
import argparse
from pathlib import Path
from src.loaders import load_documents_from_folder
from src.splitter import split_with_metadata
from src.vectordb import PersistedVectorStore

def main(data_dir: str, persist_dir: str):
    # 1️. Load documents from folder
    docs = load_documents_from_folder(data_dir)
    print(f"[ingest] documents found: {len(docs)}")

    # 2️. Split documents into chunks with metadata
    split_docs = []
    for doc in docs:
        # Use document title from metadata if available
        title = doc.metadata.get("title", "Untitled")

        # Split document text and get Document objects with metadata
        chunks = split_with_metadata(doc.page_content, title)

        # Add source information from original document
        for chunk in chunks:
            chunk.metadata["source"] = doc.metadata.get("source", "")
            split_docs.append(chunk)

    print(f"[ingest] chunks created: {len(split_docs)}")

    # 3️. Persist chunks to vector store
    store = PersistedVectorStore(persist_directory=persist_dir)
    store.create_or_update(split_docs)
    print("[ingest] done. persisted to:", persist_dir)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/raw", help="folder with raw docs (pdf, md, txt, json)")
    ap.add_argument("--persist_dir", default="VectorStore", help="where to persist vector db")
    args = ap.parse_args()

    # Ensure the persist directory exists
    Path(args.persist_dir).mkdir(parents=True, exist_ok=True)

    main(args.data, args.persist_dir)
