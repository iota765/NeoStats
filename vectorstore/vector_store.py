from langchain_community.vectorstores import FAISS


def create_vector_store(chunks, embeddings):
    try:
        print(f"[vector_store] Creating FAISS store from {len(chunks)} chunks")
        faiss_store = FAISS.from_documents(chunks, embeddings)
        print("[vector_store] FAISS store created successfully")
        return faiss_store
    except Exception as e:
        print(f"Error creating vector store: {str(e)}")
        return None

