import os

import chromadb
from langchain_cohere import CohereEmbeddings

COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")

CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = os.getenv("CHROMA_PORT", 8080)


print(f"COHERE_API_KEY: {len(COHERE_API_KEY) * '*'}")

print(f"CHROMA_HOST: {CHROMA_HOST}")
print(f"CHROMA_PORT: {CHROMA_PORT}")


def chroma_client() -> chromadb.Client:
    """
    Creates a Chroma client to connect to the Chroma server.

    Returns:
        chromadb.Client: Chroma client
    """
    return chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)


def cohere_embeddings():
    """
    Creates a Cohere embeddings function.

    Returns:
        CohereEmbeddings: Cohere embeddings function
    """
    return CohereEmbeddings(
        cohere_api_key=COHERE_API_KEY,
        model="embed-multilingual-v3.0",
    )
