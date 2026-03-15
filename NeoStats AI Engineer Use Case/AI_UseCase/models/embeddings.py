from langchain_community.embeddings import HuggingFaceEmbeddings
from config.config import EMBEDDING_MODEL

def get_embeddings():
    try:
        return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    except Exception as e:
        print("Error loading embeddings model:", e)
        return None