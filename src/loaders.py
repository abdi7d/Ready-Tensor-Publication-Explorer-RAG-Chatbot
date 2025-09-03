# src/loaders.py

from pathlib import Path
from typing import List
import json
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader
)
from langchain.schema import Document


def load_documents_from_folder(folder: str) -> List[Document]:
    folder = Path(folder)
    docs = []

    if not folder.exists():
        print(f"[loaders] folder {folder} not found — returning empty list")
        return docs

    for p in folder.rglob("*"):
        if p.is_dir():
            continue

        suffix = p.suffix.lower()

        try:
            if suffix == ".pdf":
                docs += PyPDFLoader(str(p)).load()

            elif suffix in {".md", ".markdown"}:
                docs += UnstructuredMarkdownLoader(str(p)).load()

            elif suffix == ".txt":
                docs += TextLoader(str(p), encoding="utf-8").load()

            elif suffix == ".json":
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if isinstance(data, list):
                    for item in data:
                        content = item.get("publication_description", "")
                        metadata = {
                            "id": item.get("id"),
                            "title": item.get("title"),
                            "username": item.get("username"),
                            "license": item.get("license"),
                            "source": str(p)
                        }
                        if content:
                            docs.append(Document(page_content=content, metadata=metadata))
                else:
                    docs.append(
                        Document(
                            page_content=json.dumps(data, ensure_ascii=False),
                            metadata={"source": str(p)}
                        )
                    )

            else:
                text = p.read_text(encoding="utf-8", errors="ignore")
                docs.append(Document(page_content=text, metadata={"source": str(p)}))

        except Exception as e:
            print(f"[loaders] failed to load {p}: {e}")

    return docs
