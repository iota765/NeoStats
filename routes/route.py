from typing import Literal
from config.state import State
from utils.query_analysis import requires_external_lookup


def route_after_decide(state: State) -> Literal["retrieve", "generate_direct"]:
    if state.get("retriever") is not None:
        print("Routing after decide: using 'retrieve' (retriever present in state).")
        return "retrieve"
    if state.get("need_retrieval"):
        print("Routing after decide: using 'retrieve' (model decided retrieval needed).")
        return "retrieve"
    print("Routing after decide: using 'generate_direct' (no retrieval).")
    return "generate_direct"


def route_after_direct(state: State) -> Literal["end", "rewrite_query"]:
    answer = (state.get("answer") or "").strip().lower()
    question = state.get("question", "")

    if requires_external_lookup(question):
        print("Routing after direct generation: factual/entity question should be verified. Trying web search.")
        return "rewrite_query"

    if "i don't know" in answer or "i do not know" in answer:
        print("Routing after direct generation: model did not know the answer. Trying web search.")
        return "rewrite_query"

    print("Routing after direct generation: final answer available without web search.")
    return "end"


def route_after_relevance(state: State) -> Literal["generate_from_context", "rewrite_query"]:
    if state.get("relevant_docs") and len(state["relevant_docs"]) > 0:
        print("Routing after relevance: using 'generate_from_context' (relevant docs found).")
        return "generate_from_context"

    if state.get("web_attempts", 0) >= 1:
        print(
            "Routing after relevance: stopping with 'I don't know' because web search did not provide proper context."
        )
        return "generate_from_context"

    if state.get("retriever") is not None:
        print(
            "Routing after relevance: no proper context found in uploaded documents. Trying web search once."
        )
    else:
        print("Routing after relevance: using 'rewrite_query' (trying one web search for context).")
    return "rewrite_query"
