from models.llm import load_llm
from prompts.rag_generation_prompt import rag_generation_prompt
from config.state import State

llm = load_llm()


def generate_from_context(state: State):
    try:
        print("[generate_from_context] Starting context-based generation")
        if "relevant_docs" in state:
            docs = state.get("relevant_docs") or []
        else:
            docs = state.get("docs", []) or []

        print(f"[generate_from_context] Docs available: {len(docs)}")

        context = "\n\n-----\n\n".join([d.page_content for d in docs]).strip()
        print(f"[generate_from_context] Context length: {len(context)} characters")
        if not context:
            print("[generate_from_context] No context available")
            return {
                "answer": "I don't know based on the available information."
            }

        messages = rag_generation_prompt.format_messages(
            question=state["question"],
            context=context,
            response_mode=state.get("response_mode", "Concise"),
        )
        out = llm.invoke(messages)
        print("[generate_from_context] Answer generated from context")
        return {"answer": out.content}
    except Exception as e:
        print(f"Error generating answer from context: {str(e)}")
        return {"answer": "I don't know based on the available information."}
