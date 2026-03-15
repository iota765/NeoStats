from models.llm import load_llm
from prompts.direct_generation_prompt import direct_generation_prompt
from config.state import State

llm = load_llm()

def generate_direct(state: State):
    try:
        print("[generate_direct] Starting direct answer generation")
        messages = direct_generation_prompt.format_messages(
            question=state["question"],
            response_mode=state.get("response_mode", "Concise"),
        )
        response = llm.invoke(messages)
        print("[generate_direct] Direct answer generated successfully")
        return {"answer": response.content}
    except Exception as e:
        print(f"Error in direct generation: {str(e)}")
        return {"answer": "Error generating response."}
