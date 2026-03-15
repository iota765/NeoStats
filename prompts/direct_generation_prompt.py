from langchain_core.prompts import ChatPromptTemplate

direct_generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer the question using only your general knowledge.\n"
            "Response mode: {response_mode}.\n"
            "If response mode is Concise, keep the answer short and clear.\n"
            "If response mode is Detailed, give a fuller explanation with key details.\n"
            "Do not guess, infer missing facts, or make up details.\n"
            "If you do not know the answer with high confidence, reply exactly with:\n"
            "\"I don't know based on my general knowledge.\"",
        ),
        ("human", "{question}"),
    ]
)

