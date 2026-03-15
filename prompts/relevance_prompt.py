from langchain_core.prompts import ChatPromptTemplate

is_relevant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You judge whether a document helps answer a question.\n"
            "Respond with a SINGLE WORD: either 'true' or 'false'.\n"
            "Do not include any other text.",
        ),
        (
            "human",
            "Question:\n{question}\n\nDocument:\n{doc_content}",
        ),
    ]
)


