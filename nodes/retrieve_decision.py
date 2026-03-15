import json

from models.llm import load_llm
from prompts.decide_retrieval_prompt import decide_retrieval_prompt
from config.state import State
from utils.query_analysis import requires_external_lookup

llm = load_llm()


def decide_retrieval(state: State):
    try:
        print("[decide_retrieval] Starting retrieval decision")
        print(f"[decide_retrieval] Question: {state['question']}")
        heuristic_lookup = requires_external_lookup(state["question"])
        print(f"[decide_retrieval] heuristic_requires_lookup={heuristic_lookup}")

        if heuristic_lookup:
            print("[decide_retrieval] Forcing retrieval/web lookup for factual or entity-based question")
            return {"need_retrieval": True}

        out = llm.invoke(decide_retrieval_prompt.format_messages(question=state["question"]))
        content = str(getattr(out, "content", out)).strip()
        print(f"[decide_retrieval] Raw model output: {content}")

        try:
            payload = json.loads(content)
            need_retrieval = bool(payload.get("should_retrieve", True))
        except json.JSONDecodeError:
            lowered = content.lower()
            need_retrieval = "true" in lowered and "false" not in lowered

        print(f"[decide_retrieval] need_retrieval={need_retrieval}")
        return {"need_retrieval": need_retrieval}
    except Exception as e:
        print(f"Error deciding retrieval: {str(e)}")
        return {"need_retrieval": True}
