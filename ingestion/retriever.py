from ingestion.document_loader import load_documents
from ingestion.chunking import split_documents
from models.embeddings import get_embeddings
from langchain_community.vectorstores import FAISS


def build_retriever(file_path: str):
    print(f"[retriever] Building retriever for file: {file_path}")
    documents = load_documents(file_path)
    if not documents:
        print("No documents loaded. Exiting.")
        return None

    chunks = split_documents(documents)
    if not chunks:
        print("No chunks created from documents. Exiting.")
        return None

    embedding_model = get_embeddings()
    if not embedding_model:
        print("Embedding model could not be loaded. Exiting.")
        return None

    try:
        index = FAISS.from_documents(chunks, embedding_model)
        print("[retriever] FAISS index created successfully")
        return index
    except Exception as e:
        print(f"Error creating vector store index: {str(e)}")
        return None
