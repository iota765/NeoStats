from typing import Dict


def capture_pipeline_run(graph_app, state: Dict) -> Dict:
    print("[app] Invoking RAG graph")
    print(f"[app] Question: {state.get('question', '')}")
    result = graph_app.invoke(state)
    print("[app] Graph execution completed")
    return result
