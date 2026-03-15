from langchain_community.document_loaders import PyPDFLoader, TextLoader


def load_documents(file_path):
    """Load documents from a file"""

    try:
        print(f"[document_loader] Loading file: {file_path}")
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            print("[document_loader] Using PyPDFLoader")

        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path)
            print("[document_loader] Using TextLoader")

        else:
            raise ValueError("Unsupported file type")

        documents = loader.load()
        print(f"[document_loader] Documents loaded successfully: {len(documents)}")
        return documents

    except Exception as e:
        print(f"Error loading documents: {str(e)}")
        return []
