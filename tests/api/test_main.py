import chromadb
import pytest
from chromadb.utils import embedding_functions
from httpx import ASGITransport, AsyncClient

from api.dependencies import get_chroma_client, get_cohere_embeddings
from api.main import app

app.dependency_overrides[get_chroma_client] = chromadb.Client
app.dependency_overrides[get_cohere_embeddings] = embedding_functions.DefaultEmbeddingFunction


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
