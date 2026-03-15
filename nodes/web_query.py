import json
from typing import List
from langchain_core.documents import Document
from models.llm import load_llm
from prompts.rewrite_prompt import rewrite_prompt
from config.state import State
from langchain_community.tools.tavily_search import TavilySearchResults


llm = load_llm()
rewrite_chain = rewrite_prompt | llm


def rewrite_query(state: State):
    try:
        print("[rewrite_query] Starting query rewrite")
        out = rewrite_chain.invoke({"question": state["question"]})
        raw_content = getattr(out, "content", str(out))
        print(f"[rewrite_query] Raw model output: {raw_content}")

        try:
            data = json.loads(raw_content)
            query = data.get("query") if isinstance(data, dict) else None
        except Exception:
            query = None

        if not query:
            query = state["question"]

        print(f"Rewritten query: {query}")
        return {"web_query": query}
    except Exception as e:
        print(f"Error rewriting query: {str(e)}")
        return {"web_query": state["question"]}


tavily = TavilySearchResults(max_results=5)


def web_search_node(state: State):
    try:
        attempts = state.get("web_attempts", 0)
        print(f"[web_search] Starting web search attempt {attempts + 1}")
        if attempts >= 5:
            print("Web search limit reached (5 attempts). Skipping further web calls.")
            return {"docs": [], "web_attempts": attempts}

        q = state.get("web_query") or state["question"]
        print(f"[web_search] Performing web search attempt {attempts + 1} with query: {q}")
        results = tavily.invoke({"query": q})
        print(f"[web_search] Raw result count: {len(results or [])}")
    except Exception as e:
        print(f"Error performing web search: {str(e)}")
        results = []

    docs: List[Document] = []
    existing_docs = state.get("docs", []) or []

    for r in results or []:
        if not isinstance(r, dict):
            continue

        title = r.get("title", "")
        url = r.get("url", "")
        content = r.get("content", "") or r.get("snippet", "")

        text = f"TITLE: {title}\nURL: {url}\nCONTENT:\n{content}"

        docs.append(
            Document(
                page_content=text,
                metadata={"source": "web", "url": url, "title": title},
            )
        )

    combined_docs: List[Document] = []
    seen_contents = set()

    for doc in list(existing_docs) + docs:
        content = getattr(doc, "page_content", "")
        if content in seen_contents:
            continue
        seen_contents.add(content)
        combined_docs.append(doc)

    print(
        f"[web_search] Attempt {attempts + 1} converted results to {len(docs)} web documents"
    )
    print(f"[web_search] Total docs available after merge: {len(combined_docs)}")
    return {"docs": combined_docs, "web_attempts": attempts + 1}

