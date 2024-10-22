import chromadb
from langchain_cohere import CohereEmbeddings

from .config import CHROMA_HOST, CHROMA_PORT, COHERE_API_KEY

print(f"COHERE_API_KEY: {len(COHERE_API_KEY) * '*'}")

print(f"CHROMA_HOST: {CHROMA_HOST}")
print(f"CHROMA_PORT: {CHROMA_PORT}")


def get_chroma_client() -> chromadb.Client:
    """
    Creates a Chroma client to connect to the Chroma server.

    Returns:
        chromadb.Client: Chroma client
    """
    return chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)


def get_cohere_embeddings():
    """
    Creates a Cohere embeddings function.

    Returns:
        CohereEmbeddings: Cohere embeddings function
    """
    return CohereEmbeddings(
        cohere_api_key=COHERE_API_KEY,
        model="embed-multilingual-v3.0",
    )
