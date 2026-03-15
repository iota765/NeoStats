🚀 NeoStats

NeoStats is an Adaptive Retrieval-Augmented Generation (RAG) chatbot built using Streamlit, LangGraph, FAISS, and Tavily.

It intelligently decides when to retrieve documents, search the web, or answer directly using the LLM, enabling reliable responses while reducing hallucinations.

✨ Features

📄 Document Q&A with uploaded PDF and TXT files

🔍 Adaptive retrieval routing based on query intent

🌐 Web search fallback when document context is insufficient

🧠 Relevance filtering for retrieved document chunks

⚡ Multi-LLM support: Groq, OpenAI, Gemini

🧪 Terminal-first debugging with detailed pipeline logs

🛑 Hallucination control via abstaining responses

🧠 Architecture

NeoStats uses an adaptive routing workflow instead of a fixed RAG pipeline.

## Graph View
![RAG Graph](./NeoStats%20AI%20Engineer%20Use%20Case/AI_UseCase/rag_graph.png)

Pipeline Flow

The graph decides whether retrieval is needed.

If required, it searches uploaded documents.

Retrieved chunks are graded for relevance.

If relevant context exists → generate answer using context.

If context is insufficient → rewrite query and perform web search.

If web results still lack context → return an abstaining response instead of guessing.

User Question
      │
      ▼
   Router
      │
 ┌────┴─────┐
 ▼          ▼
Direct LLM  Retrieval
             │
             ▼
       Relevance Filter
             │
             ▼
      Answer Generation
             │
             ▼
       Web Search Fallback
📊 Graph View

🛠 Tech Stack
Component	Technology
UI	Streamlit
Workflow	LangGraph
LLM Integration	LangChain
Vector Search	FAISS
Embeddings	HuggingFace Sentence Transformers
Web Search	Tavily
LLM Providers	Groq, OpenAI, Gemini
📂 Project Structure
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
⚙️ Key Modules

app.py
Streamlit entry point and UI logic.

workflow/graph_builder.py
Defines the LangGraph workflow pipeline.

models/llm.py
Loads supported LLM providers.

models/embeddings.py
Embedding model configuration.

utils/rag_helpers.py
Handles document processing and retriever creation.

utils/web_helpers.py
Utility for invoking web search.

nodes/
Core pipeline nodes including:

retrieval

relevance grading

generation

web search fallback

routes/route.py
Handles adaptive routing decisions.

📄 Pipeline Behavior
Document Processing

User uploads PDF or TXT files

Documents are loaded and split into chunks

Chunks are embedded and stored in FAISS

Retriever uses MMR search for diverse context

Answer Generation

If the model can answer directly → use LLM knowledge

Otherwise → retrieve relevant document chunks

If context is still insufficient → perform web search

If no reliable context is found → return:

I don't know based on the available information.

This prevents hallucinated responses.

⚡ Setup

Install dependencies:

pip install -r "NeoStats AI Engineer Use Case/AI_UseCase/requirements.txt"
🔑 Environment Variables

Create a .env file in:

NeoStats AI Engineer Use Case/AI_UseCase/

Example keys:

GROQ_API_KEY=
TAVILY_API_KEY=
OPENAI_API_KEY=optional
GEMINI_API_KEY=optional
▶️ Run the App

Navigate to the application folder:

cd "NeoStats AI Engineer Use Case/AI_UseCase"

Run the Streamlit app:

streamlit run app.py
🧪 Debugging

The system prints pipeline steps directly in the terminal, including:

LLM loading

retrieval decisions

document chunk retrieval

relevance filtering

query rewriting

web search attempts

answer generation

This helps debug routing and hallucination behavior.

🎯 Example Use Cases

NeoStats can act as a document-aware assistant for:

company research

financial report analysis

policy and documentation lookup

study material Q&A

internal knowledge-base assistants

🛡 Notes

Local documents are prioritized when valid context exists.

Web search is only used as a fallback.

The system intentionally avoids answering when context is weak to reduce hallucinations.