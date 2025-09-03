# src/rag_chain.py
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from .llm import get_chat_llm
from .retriever import get_retriever
from .prompts import QA_SYSTEM
# from .config import settings

PROMPT_TEMPLATE = QA_SYSTEM + "\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"
prompt = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["context", "question"])

def build_rag_chain(persist_directory: str = "VectorStore"):
    llm = get_chat_llm()
    retriever = get_retriever(persist_directory=persist_directory)
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False,
        chain_type_kwargs={"prompt": prompt}
    )
    return qa
