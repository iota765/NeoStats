from langchain_core.prompts import ChatPromptTemplate

decide_retrieval_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You decide whether document retrieval is needed before answering.\n"
            "Respond with JSON matching: {'should_retrieve': boolean}.\n\n"
            "Guidelines:\n"
            "- should_retrieve = true when the question asks about specific entities, companies, people, dates, metrics, or any factual details.\n"
            "- should_retrieve = true when the answer likely depends on documents or external data (like company profiles, financials, roadmaps).\n"
            "- should_retrieve = false only for generic, timeless explanations that any model can answer from general knowledge.\n"
            "- If you are uncertain, set should_retrieve = true.",
        ),
        ("human", "Question: {question}"),
    ]
)

