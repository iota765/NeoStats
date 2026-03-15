from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from PyPDF2 import PdfReader


def _load_pdf_with_pypdf2(file_path):
    print("[document_loader] Falling back to PyPDF2 PDF reader")
    reader = PdfReader(file_path)
    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            documents.append(
                Document(
                    page_content=text,
                    metadata={"source": file_path, "page": page_number},
                )
            )

    print(f"[document_loader] PyPDF2 fallback extracted {len(documents)} pages")
    return documents


def load_documents(file_path):
    """Load documents from a file"""

    try:
        print(f"[document_loader] Loading file: {file_path}")
        lower_path = file_path.lower()

        if lower_path.endswith(".pdf"):
            try:
                loader = PyPDFLoader(file_path)
                print("[document_loader] Using PyPDFLoader")
                documents = loader.load()
            except Exception as pdf_error:
                print(f"[document_loader] PyPDFLoader failed: {pdf_error}")
                documents = _load_pdf_with_pypdf2(file_path)

            if not documents:
                documents = _load_pdf_with_pypdf2(file_path)

            print(f"[document_loader] Documents loaded successfully: {len(documents)}")
            return documents

        elif lower_path.endswith(".txt"):
            loader = TextLoader(file_path, autodetect_encoding=True)
            print("[document_loader] Using TextLoader")

        else:
            raise ValueError("Unsupported file type")

        documents = loader.load()
        print(f"[document_loader] Documents loaded successfully: {len(documents)}")
        return documents

    except Exception as e:
        print(f"Error loading documents: {str(e)}")
        return []
