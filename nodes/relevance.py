from typing import List
from langchain_core.documents import Document
from models.llm import load_llm
from prompts.relevance_prompt import is_relevant_prompt
from config.state import State


llm = load_llm()


def is_relevant(state: State):
    print("[relevance] Starting relevance filtering")
    docs = state.get("docs", []) or []
    print(f"[relevance] Retrieved docs count: {len(docs)}")
    relevant_docs: List[Document] = []

    for idx, doc in enumerate(docs, start=1):
        print(f"[relevance] Checking doc #{idx}")
        out = llm.invoke(
            is_relevant_prompt.format_messages(
                question=state["question"], doc_content=doc.page_content
            )
        )
        answer = str(getattr(out, "content", out)).strip().lower()
        is_rel = "true" in answer and "false" not in answer
        print(f"[relevance] Doc #{idx} verdict: {answer}")

        if is_rel:
            relevant_docs.append(doc)

    print(f"[relevance] Relevant docs count: {len(relevant_docs)}")
    return {"relevant_docs": relevant_docs}


