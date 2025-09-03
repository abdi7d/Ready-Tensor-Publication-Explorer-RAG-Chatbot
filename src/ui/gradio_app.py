from ..config import settings
from ..rag_chain import build_rag_chain
import gradio as gr
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def build_and_launch(persist_directory: str = "VectorStore", demo_port: int = 7860):
    qa = build_rag_chain(persist_directory=persist_directory)

    def answer_question(message, chat_history):
        """
        message: user question (string)
        chat_history: list of dicts {"role": ..., "content": ...}
        """
        if chat_history is None:
            chat_history = []

        # --- Simple small talk handling ---
        lower_msg = message.strip().lower()
        if lower_msg in ["hi", "hello", "hey", "how are you", "what's up","how are you doing?"]:
            # reply = "Hello 👋 How can I help you with the documents?"
            reply = "Hello 👋 How can I help you with Ready Tensor Publications?"
            chat_history.append({"role": "user", "content": message})
            chat_history.append({"role": "assistant", "content": reply})
            return "", chat_history

        # --- RAG query (only pass the question) ---
        out = qa.invoke({"query": message})
        answer = out.get("result") or out.get("answer") or "No answer."
        docs = out.get("source_documents", [])

        # Append sources (optional)
        sources = []
        for d in docs:
            meta = getattr(d, "metadata", {})
            src = meta.get("source", "unknown")
            preview = d.page_content[:200].replace("\n", " ")
            sources.append(f"[{src}] {preview}")
        combined_sources = "\n".join(sources)

        final_answer = answer
        if combined_sources:
            final_answer += f"\n\n**Sources:**\n{combined_sources}"

        # Update chat history
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": final_answer})
        return "", chat_history

    # Document preview
    doc_preview = ""
    p = Path("data/project_1_publication.json")
    if p.exists():
        try:
            doc_preview = p.read_text(encoding="utf-8")
        except Exception:
            doc_preview = "[preview not available]"

    with gr.Blocks(theme="Origin") as demo:
        with gr.Row():
            gr.Image(
                value="assets/ready_tensor_logo.jpg"
                if Path("assets/ready_tensor_logo.jpg").exists()
                else None,
                width=160,
                height=40,
            )
            gr.Markdown("#  🤖 RAG Assistant — Ready Tensor Explorer")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📄 Document preview")
                with open("data/project_1_publications.json", "r", encoding="utf-8") as f:
                    doc_preview = f.read()
                gr.Textbox(value=doc_preview, lines=20, interactive=False)

            with gr.Column(scale=2):
                chatbot = gr.Chatbot(
                    type="messages",
                    label="Conversation",
                    avatar_images=(
                        "https://cdn-icons-png.flaticon.com/512/2922/2922510.png",
                        "https://cdn-icons-png.flaticon.com/512/4712/4712027.png",
                    ),
                    show_copy_button=True,
                )

                txt = gr.Textbox(
                    label="Ask a question",
                    placeholder="Type your question here..."
                )
                submit = gr.Button("Send")

                # Wire up inputs/outputs
                submit.click(
                    fn=answer_question,
                    inputs=[txt, chatbot],
                    outputs=[txt, chatbot],
                )
                txt.submit(
                    fn=answer_question,
                    inputs=[txt, chatbot],
                    outputs=[txt, chatbot],
                )

        gr.Markdown("**Tips:** Keep questions short and specific for best results.")

    demo.launch(server_port=demo_port)
