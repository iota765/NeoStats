from langchain_core.prompts import ChatPromptTemplate

rewrite_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Rewrite the user question into a focused web search query composed of keywords.\n"
            "Rules:\n"
            "- Keep it short (6-14 words).\n"
            "- If the question implies recency, add the phrase (last 30 days).\n"
            "- Do NOT answer the question.\n"
            "- Respond ONLY with a valid JSON object of the form: {{\"query\": \"...\"}}.",
        ),
        ("human", "Question: {question}"),
    ]
)
