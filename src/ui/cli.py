# src/ui/cli.py
from ..rag_chain import build_rag_chain
from dotenv import load_dotenv
load_dotenv()

def run_cli(persist_directory: str = "VectorStore"):
    qa = build_rag_chain(persist_directory=persist_directory)
    print("[cli] RAG assistant ready. Type 'exit' or 'quit' to stop.")
    while True:
        q = input("\nQuestion> ").strip()
        if q.lower() in {"exit", "quit"}:
            break
        res = qa({"query": q})
        answer = res.get("result") or res.get("answer")
        docs = res.get("source_documents", [])
        print("\n=== Answer ===\n")
        print(answer)
        if docs:
            print("\n--- Sources ---")
            for i, d in enumerate(docs, 1):
                meta = d.metadata if hasattr(d, "metadata") else {}
                src = meta.get("source", "unknown")
                print(f"[{i}] source: {src} | preview: {d.page_content[:250].replace('\\n',' ')}")
