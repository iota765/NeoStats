from config.state import State
from ingestion.retriever import build_retriever


def retrieve(state: State):
    try:
        print("[retrieve] Starting retrieval step")
        retriever = state.get("retriever")
        if retriever is None:
            file_path = state.get("file_path")
            if not file_path:
                print("Retrieve node: no retriever or file_path; returning empty docs.")
                return {"docs": []}
            retriever = build_retriever(file_path)

        if retriever is None:
            print("Failed to build retriever.")
            return {"docs": []}

        if hasattr(retriever, "invoke"):
            print("[retrieve] Using retriever.invoke")
            docs = retriever.invoke(state["question"])
        elif hasattr(retriever, "get_relevant_documents"):
            print("[retrieve] Using get_relevant_documents")
            docs = retriever.get_relevant_documents(state["question"])
        elif hasattr(retriever, "similarity_search"):
            print("[retrieve] Using similarity_search")
            docs = retriever.similarity_search(state["question"])
        else:
            print("Retriever object does not support invoke, get_relevant_documents, or similarity_search.")
            return {"docs": []}

        print(f"Retrieved {len(docs)} documents.")
        if docs:
            print(f"[retrieve] First document preview: {docs[0].page_content[:200]}")
        return {"docs": docs}
    except Exception as e:
        print(f"Error occurred while retrieving documents: {str(e)}")
        return {"docs": []}
