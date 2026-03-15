# NeoStats

An adaptive RAG chatbot built with Streamlit, LangGraph, FAISS, and Tavily.

This project supports:
- local document question answering with retrieval-augmented generation
- live web search fallback when document or model context is insufficient
- concise and detailed response modes
- terminal-first debugging with step-by-step pipeline prints

## Architecture

The chatbot uses an adaptive routing flow instead of a single fixed pipeline.

1. The graph first decides whether retrieval is needed.
2. If retrieval is needed, it searches uploaded documents.
3. Retrieved chunks are filtered for relevance.
4. If relevant context is found, the answer is generated only from that context.
5. If context is not sufficient, the system rewrites the query and performs one web search attempt.
6. If web results still do not provide proper context, the chatbot stops and returns an abstaining answer instead of guessing.

## Graph View

![RAG Graph](./NeoStats%20AI%20Engineer%20Use%20Case/AI_UseCase/rag_graph.png)

## Tech Stack

- Streamlit for the user interface
- LangGraph for workflow orchestration
- LangChain for prompts, document processing, and tool integration
- FAISS for vector search
- HuggingFace sentence-transformer embeddings
- Groq / OpenAI / Gemini model support
- Tavily for live web search

## Project Structure

```text
NeoStats AI Engineer Use Case/
└── AI_UseCase/
    ├── app.py
    ├── config/
    ├── ingestion/
    ├── models/
    ├── nodes/
    ├── prompts/
    ├── routes/
    ├── utils/
    ├── vectorstore/
    └── workflow/
```

## Key Modules

- `app.py`: Streamlit entrypoint and UI flow
- `workflow/graph_builder.py`: LangGraph workflow definition
- `models/llm.py`: model loading for Groq, OpenAI, and Gemini
- `models/embeddings.py`: embedding model configuration
- `utils/rag_helpers.py`: uploaded document processing and retriever creation
- `utils/web_helpers.py`: graph invocation helper
- `nodes/`: retrieval, relevance checking, generation, and web fallback nodes
- `routes/route.py`: graph routing logic

## Pipeline Behavior

### Document Flow

- User uploads `pdf` or `txt` files
- Documents are loaded and split into chunks
- Chunks are embedded and stored in a FAISS vector index
- The retriever uses MMR-based search to improve chunk diversity

### Answer Flow

- If the model can answer directly, it uses general knowledge
- If it cannot answer confidently, it routes to retrieval or web search
- If relevant context is missing, it returns:

```text
I don't know based on the available information.
```

This is intentional to reduce hallucinations.

## Setup

Install dependencies:

```bash
pip install -r "NeoStats AI Engineer Use Case/AI_UseCase/requirements.txt"
```

Set environment variables in:

```text
NeoStats AI Engineer Use Case/AI_UseCase/.env
```

Example keys used by the project:

- `GROQ_API_KEY`
- `TAVILY_API_KEY`
- `OPENAI_API_KEY` (optional)
- `GOOGLE_API_KEY` or `GEMINI_API_KEY` (optional)

## Run the App

From the project app folder:

```bash
cd "NeoStats AI Engineer Use Case/AI_UseCase"
python -m streamlit run app.py
```

## Debugging

The app is designed to print pipeline steps directly in the terminal, including:

- LLM loading
- retrieval decisions
- chunk retrieval
- relevance filtering
- query rewriting
- web search attempts
- final answer generation

This makes it easier to debug routing and hallucination issues while testing.

## Example Use Case

This chatbot can be used as a document-aware assistant for:

- company research
- financial or business Q&A
- policy and report lookup
- study material Q&A
- knowledge-base style internal assistants

## Notes

- Uploaded local documents are preferred when they provide valid context.
- Web search is used as a fallback, not the first source.
- The system is intentionally conservative and avoids answering when context is weak.
