import chromadb
import cohere
from chromadb import Documents, EmbeddingFunction, Embeddings

from core.chat_llm import ChatLLMModel
from core.models.chat import ChatMessage, ChatMessageRole

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


class CohereEmbeddingsFunction(EmbeddingFunction):
    """Cohere embeddings function."""

    def __call__(self, input: Documents) -> Embeddings:
        co = cohere.Client(api_key=COHERE_API_KEY)
        response = co.embed(
            texts=input, model="embed-multilingual-v2.0", input_type="search_document"
        )
        return response.embeddings


def get_embeddings_function() -> CohereEmbeddingsFunction:
    """
    Creates a Cohere embeddings function.

    Returns:
        CohereEmbeddings: Cohere embeddings function
    """
    return CohereEmbeddingsFunction(
        cohere_api_key=COHERE_API_KEY,
    )


def transform_chat_message(chat_message: ChatMessage) -> dict:
    """
    Transforms a chat message to a dictionary.

    Args:
        chat_message (ChatMessage): Chat message

    Returns:
        dict: Chat message dictionary
    """
    role = "user"
    if chat_message.role == ChatMessageRole.Ai:
        role = "assistant"
    if chat_message.role == ChatMessageRole.System:
        role = "system"
    return {
        "role": role,
        "content": chat_message.content,
    }


class CohereChatModel(ChatLLMModel):
    """Cohere chat model."""

    def chat(self, chat_input) -> str:
        co = cohere.ClientV2(api_key=COHERE_API_KEY)
        messages = [transform_chat_message(m) for m in chat_input.messages]
        res = co.chat(messages=messages, model="command-r-plus-08-2024")
        return res.message.content[0].text


def get_chat_model() -> CohereChatModel:
    """
    Creates a chat model.

    Returns:
        ChatCohere: Chat model
    """
    return CohereChatModel()
