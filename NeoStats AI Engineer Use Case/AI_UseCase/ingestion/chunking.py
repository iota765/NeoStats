from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(docs):
    try:
        print(f"[chunking] Starting chunking for {len(docs)} documents")
        splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=150)
        chunks = splitter.split_documents(docs)
        print(f"[chunking] Documents split into chunks successfully: {len(chunks)}")
        return chunks
    except Exception as e:
        print(f"Error splitting documents: {str(e)}")
        return []
