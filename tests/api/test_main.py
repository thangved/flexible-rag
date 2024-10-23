import chromadb
import pytest
from chromadb.utils import embedding_functions
from httpx import ASGITransport, AsyncClient

from api.dependencies import get_chat_model, get_chroma_client, get_embeddings_function
from api.main import app
from tests.fake.llm_chat import FakeLLMChatModel


def get_chroma_client_override():
    return chromadb.Client()


def get_embeddings_function_override():
    return embedding_functions.DefaultEmbeddingFunction()


def get_chat_model_override():
    return FakeLLMChatModel()


app.dependency_overrides[get_chroma_client] = get_chroma_client_override
app.dependency_overrides[get_embeddings_function] = get_embeddings_function_override
app.dependency_overrides[get_chat_model] = get_chat_model_override


@pytest.mark.anyio
async def test_add_document():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/vector_store",
            json={
                "content": "Hoàng Sa và Trường Sa là của Việt Nam",
                "collection_name": "geography",
                "reference_id": "1",
            },
        )
        assert response.status_code == 200
        assert type(response.json()["ids"]) is list


@pytest.mark.anyio
async def test_similarity_search():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get(
            "/vector_store",
            params={"query": "Hoàng Sa", "collection_name": "geography"},
        )
        assert response.status_code == 200
        res_json = response.json()
        assert type(res_json) is list
        assert len(res_json) > 0
        for doc in res_json:
            assert type(doc["score"]) is float
            assert type(doc["page_content"]) is str
            assert type(doc["metadata"]) is dict
            assert type(doc["metadata"]["reference_id"]) is str


@pytest.mark.anyio
async def test_delete_documents():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.delete(
            "/vector_store/1",
            params={"collection_name": "geography"},
        )
        assert response.status_code == 204


@pytest.mark.anyio
async def test_chat():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/chat_llm",
            json={
                "messages": [
                    {
                        "role": "human",
                        "content": "What is the capital of France?",
                    }
                ]
            },
        )
        assert response.status_code == 200
        assert type(response.json()["content"]) is str
