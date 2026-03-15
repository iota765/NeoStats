from langchain_core.prompts import ChatPromptTemplate

is_relevant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You judge whether a document contains direct evidence needed to answer a question.\n"
            "Return true only if the document explicitly supports the answer.\n"
            "Return false if the document is only loosely related, incomplete, ambiguous, or missing the exact fact asked.\n"
            "Respond with a SINGLE WORD: either 'true' or 'false'.\n"
            "Do not include any other text.",
        ),
        (
            "human",
            "Question:\n{question}\n\nDocument:\n{doc_content}",
        ),
    ]
)


