from logging import getLogger

import chromadb
import cohere
from chromadb import Documents, EmbeddingFunction, Embeddings

from core.chat_llm import ChatLLMModel
from core.models.chat import ChatMessage, ChatMessageRole
from core.rerank import RerankModel

from .config import CHROMA_HOST, CHROMA_PORT, COHERE_API_KEY

logger = getLogger(__name__)

logger.info("===== DEPENDENCIES.PY =====")

logger.info("COHERE_API_KEY: %s", len(COHERE_API_KEY) * "*")

logger.info("CHROMA_HOST: %s", CHROMA_HOST)
logger.info("CHROMA_PORT: %s", CHROMA_PORT)

logger.info("===== DEPENDENCIES.PY =====")

co = cohere.ClientV2(api_key=COHERE_API_KEY)


class CohereEmbeddingsFunction(EmbeddingFunction):
    """Cohere embeddings function."""

    # skipcq: PYL-W0622
    def __call__(self, input: Documents) -> Embeddings:
        response = co.embed(
            texts=input,
            model="embed-multilingual-v2.0",
            input_type="search_document",
            embedding_types=["float"],
        )
        return response.embeddings.float_


class CohereChatModel(ChatLLMModel):
    """Cohere chat model."""

    def chat(self, chat_input) -> str:
        """
        Chat with the model.

        Args:
            chat_input: Chat input

        Returns:
            str: Chat response
        """
        messages = [transform_chat_message(m) for m in chat_input.messages]
        res = co.chat(messages=messages, model="command-r-plus-08-2024")
        return res.message.content[0].text


class CohereRerankModel(RerankModel):
    """Cohere rerank model."""

    def rerank_documents(self, query, docs):
        """
        Rerank the documents based on the query.

        Args:
            query: The query use to rerank
            docs: List of documents

        Returns:
            List[float]: List of relevance scores
        """
        res = co.rerank(documents=docs, query=query, model="rerank-multilingual-v2.0")
        sorted_index = sorted(res.results, key=lambda x: x.index)
        return [el.relevance_score for el in sorted_index]


def get_chroma_client() -> chromadb.Client:
    """
    Creates a Chroma client to connect to the Chroma server.

    Returns:
        chromadb.Client: Chroma client
    """
    try:
        return chromadb.HttpClient(
            host=CHROMA_HOST,
            port=CHROMA_PORT,
        )
    except BaseException as e:
        logger.error("Error creating Chroma client: %s", e)
        return chromadb.Client()


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


def get_chat_model() -> CohereChatModel:
    """
    Creates a chat model.

    Returns:
        ChatCohere: Chat model
    """
    return CohereChatModel()


def get_rerank_model() -> CohereRerankModel:
    """
    Creates a rerank model.

    Returns:
        CohereRerankModel: Rerank model
    """
    return CohereRerankModel()
