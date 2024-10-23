import chromadb
import cohere
from chromadb import Documents, EmbeddingFunction, Embeddings
from langchain_cohere import ChatCohere

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
    return chromadb.HttpClient(
        host=CHROMA_HOST,
        port=CHROMA_PORT,
    )


class CohereEmbeddings(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        co = cohere.Client(api_key=COHERE_API_KEY)
        response = co.embed(
            texts=input, model="embed-multilingual-v2.0", input_type="search_document"
        )
        return response.embeddings


def get_cohere_embeddings() -> CohereEmbeddings:
    """
    Creates a Cohere embeddings function.

    Returns:
        CohereEmbeddings: Cohere embeddings function
    """
    return CohereEmbeddings(
        cohere_api_key=COHERE_API_KEY,
    )


def get_chat_model() -> ChatCohere:
    """
    Creates a chat model.

    Returns:
        ChatCohere: Chat model
    """
    return ChatCohere()
