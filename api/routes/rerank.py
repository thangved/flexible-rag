from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from api.dependencies import get_rerank_model
from core.models.documents import Document, DocumentWithScore
from core.rerank import Rerank, RerankModel

router = APIRouter(dependencies=[Depends(get_rerank_model)])


class RerankInput(BaseModel):
    model_config = {
        "title": "Rerank Input",
        "strict": True,
    }
    query: str = Field(
        ...,
        title="Query",
        description="Query",
        examples=["Hoang Sa and Truong Sa belong to Vietnam"],
    )
    documents: list[Document] = Field(
        ...,
        title="Documents",
        description="List of documents",
        examples=[
            [
                {
                    "page_content": "Document 1",
                    "metadata": {
                        "reference_id": "1",
                    },
                },
                {
                    "page_content": "Document 2",
                    "metadata": {
                        "reference_id": "2",
                    },
                },
            ]
        ],
    )


class RerankOutput(BaseModel):
    model_config = {
        "title": "Rerank Output",
        "strict": True,
    }
    query: str = Field(
        ...,
        title="Query",
        description="Query",
        examples=["Hoang Sa and Truong Sa belong to Vietnam"],
    )
    documents: list[DocumentWithScore] = Field(
        ...,
        title="Documents",
        description="List of documents",
        examples=[
            [
                {
                    "page_content": "Document 1",
                    "metadata": {
                        "reference_id": "1",
                    },
                    "score": 0.9,
                },
                {
                    "page_content": "Document 2",
                    "metadata": {
                        "reference_id": "2",
                    },
                    "score": 0.8,
                },
            ]
        ],
    )


@router.post(
    "",
    description="Rerank the documents based on the query",
    summary="Rerank the documents",
    response_description="List of documents with ranked score and sorted by score",
)
def rerank_documents(
    rerank_input: RerankInput,
    rerank_model: Annotated[RerankModel, Depends(get_rerank_model)],
) -> RerankOutput:
    rerank = Rerank(model=rerank_model)
    reranked_documents = rerank.rerank_documents(
        rerank_input.query, rerank_input.documents
    )
    return RerankOutput(query=rerank_input.query, documents=reranked_documents)
