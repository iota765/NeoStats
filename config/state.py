from typing import TypedDict, List, Any
from langchain_core.documents import Document


class State(TypedDict, total=False):
    question: str
    response_mode: str
    need_retrieval: bool
    docs: List[Document]
    relevant_docs: List[Document]
    context: str
    answer: str
    web_query: str
    web_attempts: int
    retriever: Any

