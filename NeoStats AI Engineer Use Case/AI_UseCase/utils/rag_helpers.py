import os
import tempfile
from typing import List, Tuple

from langchain_core.documents import Document

from ingestion.chunking import split_documents
from ingestion.document_loader import load_documents
from models.embeddings import get_embeddings
from vectorstore.vector_store import create_vector_store


def load_uploaded_files(uploaded_files) -> List[Document]:
    all_docs: List[Document] = []

    for uploaded_file in uploaded_files:
        suffix = os.path.splitext(uploaded_file.name)[1] or ".pdf"
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            print(f"[upload] Temporary file created for {uploaded_file.name}: {tmp_path}")
            docs = load_documents(tmp_path)
            print(f"[upload] Loaded {len(docs)} pages from {uploaded_file.name}")
            all_docs.extend(docs)
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)
                print(f"[upload] Removed temporary file: {tmp_path}")

    print(f"[upload] Total documents loaded: {len(all_docs)}")
    return all_docs


def build_uploaded_retriever(uploaded_files) -> Tuple[object, int, int]:
    docs = load_uploaded_files(uploaded_files)
    if not docs:
        raise ValueError("No documents could be loaded from the uploaded files.")

    chunks = split_documents(docs)
    print(f"[upload] Total chunks created: {len(chunks)}")
    if not chunks:
        raise ValueError("No chunks were created from the uploaded documents.")

    embeddings = get_embeddings()
    if embeddings is None:
        raise ValueError("Embeddings model could not be loaded.")

    vector_store = create_vector_store(chunks, embeddings)
    if vector_store is None:
        raise ValueError("Vector store creation failed.")

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 8, "fetch_k": 20},
    )
    print("[upload] Retriever created successfully.")
    return retriever, len(docs), len(chunks)
