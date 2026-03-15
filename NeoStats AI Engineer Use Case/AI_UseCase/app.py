import os
import sys

import streamlit as st

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.rag_helpers import build_uploaded_retriever
from utils.web_helpers import capture_pipeline_run
from workflow.graph_builder import app as rag_app


def init_session_state() -> None:
    defaults = {
        "messages": [],
        "retriever": None,
        "uploaded_file_names": [],
        "uploaded_doc_count": 0,
        "uploaded_chunk_count": 0,
        "processed_upload_signature": None,
        "uploader_key": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_document_state() -> None:
    st.session_state.retriever = None
    st.session_state.uploaded_file_names = []
    st.session_state.uploaded_doc_count = 0
    st.session_state.uploaded_chunk_count = 0
    st.session_state.processed_upload_signature = None


def get_upload_signature(uploaded_files) -> tuple:
    return tuple((uploaded_file.name, uploaded_file.size) for uploaded_file in uploaded_files)


def process_documents(uploaded_files) -> None:
    print("[app] Processing uploaded documents")
    retriever, doc_count, chunk_count = build_uploaded_retriever(uploaded_files)

    st.session_state.retriever = retriever
    st.session_state.uploaded_file_names = [uploaded_file.name for uploaded_file in uploaded_files]
    st.session_state.uploaded_doc_count = doc_count
    st.session_state.uploaded_chunk_count = chunk_count
    st.session_state.processed_upload_signature = get_upload_signature(uploaded_files)
    print("[app] Documents processed successfully")


def ask_question(question: str, response_mode: str) -> str:
    print("[app] Starting new question")
    print(f"[app] Question: {question}")
    print(f"[app] Response mode: {response_mode}")
    state = {
        "question": question,
        "response_mode": response_mode,
        "docs": [],
        "relevant_docs": [],
        "context": "",
        "answer": "",
        "web_query": "",
        "web_attempts": 0,
    }

    if st.session_state.retriever is not None:
        state["retriever"] = st.session_state.retriever

    result = capture_pipeline_run(rag_app, state)
    print("[app] Final answer generated")
    return result.get("answer", "No answer generated.")


def render_sidebar() -> str:
    with st.sidebar:
        st.header("Settings")
        response_mode = st.radio("Response style", ["Concise", "Detailed"], index=0)

        uploaded_files = st.file_uploader(
            "Upload files",
            type=["pdf", "txt"],
            accept_multiple_files=True,
            key=f"uploaded_files_{st.session_state.uploader_key}",
        )

        if uploaded_files:
            current_signature = get_upload_signature(uploaded_files)
            if current_signature != st.session_state.processed_upload_signature:
                with st.spinner("Processing documents..."):
                    try:
                        process_documents(uploaded_files)
                        st.success("Documents ready.")
                    except Exception as exc:
                        reset_document_state()
                        st.error(str(exc))
        elif st.session_state.processed_upload_signature is not None:
            print("[app] Uploaded files removed. Clearing document state")
            reset_document_state()

        if st.button("Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        if st.button("Remove documents", use_container_width=True):
            print("[app] Removing document retriever from session")
            reset_document_state()
            st.session_state.uploader_key += 1
            st.rerun()

    return response_mode


def main() -> None:
    st.set_page_config(page_title="NeoStats Chatbot", layout="centered")
    init_session_state()
    response_mode = render_sidebar()

    st.title("NeoStats Chatbot")
    st.write("Ask questions, with or without uploaded documents.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask a question")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    answer = ask_question(prompt, response_mode)
                except Exception as exc:
                    answer = f"Error: {exc}"
                st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()
