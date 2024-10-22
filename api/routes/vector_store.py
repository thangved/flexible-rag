from typing import Annotated, List, Optional

import chromadb
from fastapi import APIRouter, Depends, Response, status
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from pydantic import BaseModel, Field

from core.vector_store import VectorStore

from ..dependencies import get_chroma_client, get_cohere_embeddings

router = APIRouter(
    dependencies=[Depends(get_chroma_client), Depends(get_cohere_embeddings)],
)


class AddDocumentInput(BaseModel):
    """
    Add Document Input

    Attributes:
        content (str): Document content
        collection_name (str): Collection name
        reference_id (str): Reference ID
    """

    model_config = {
        "title": "Add Document Input",
        "strict": True,
    }
    content: str = Field(
        ...,
        description="Document content",
        title="Document content",
        examples=["Hoàng Sa và Trường Sa là của Việt Nam"],
    )
    collection_name: str = Field(
        ...,
        description="Collection name",
        title="Collection name",
        examples=["geography"],
    )
    reference_id: str = Field(
        ...,
        description="Reference ID",
        title="Reference ID",
        examples=["1"],
    )


class AddDocumentResponse(BaseModel):
    """
    Add Document Response

    Attributes:
        ids (list[str]): List of unique document IDs
    """

    model_config = {
        "title": "Add Document Response",
        "strict": True,
    }
    ids: list[str] = Field(
        ...,
        description="A list of unique document IDs",
        title="Stored document IDs",
        examples=["cab7e246-b777-4e8c-a88b-0ce9bd44e190"],
    )


class DocumentWithScoreMetadata(BaseModel):
    """
    Metadata for Document with Score

    Attributes:
        reference_id (str): Reference ID
    """

    model_config = {
        "title": "Document with Score Metadata",
        "strict": True,
    }
    reference_id: str = Field(
        ...,
        title="Reference ID",
        description="Reference ID",
        examples=["1"],
    )


class DocumentWithScore(BaseModel):
    """
    Document with Score

    Attributes:
        page_content (str): Page content
        metadata (DocumentWithScoreMetadata): Metadata
        score (float): Score
    """

    model_config = {
        "title": "Document with Score",
        "strict": True,
    }
    page_content: str = Field(
        ...,
        title="Page content",
        description="Page content",
        examples=["Hoang Sa and Truong Sa belong to Vietnam"],
    )
    metadata: DocumentWithScoreMetadata = Field(
        ...,
        title="Metadata",
        description="Metadata",
    )
    score: float = Field(
        ...,
        title="Score",
        description="Score",
        examples=[0.99],
    )


@router.post(
    "/",
    description="Add a document to the vector store",
    summary="Add a document to the vector store",
    name="Add Document",
    response_description="Document added",
)
def create_document(
    document: Annotated[AddDocumentInput, "Add Document Input"],
    chroma_client: Annotated[chromadb.Client, Depends(get_chroma_client)],
    cohere_embeddings: Annotated[Embeddings, Depends(get_cohere_embeddings)],
) -> Annotated[AddDocumentResponse, "Document added"]:
    """
    Add a document to the vector store

    Args:
        document (AddDocumentInput): Add Document Input
        chroma_client (chromadb.Client): Chroma client
        cohere_embeddings (Embeddings): Embeddings function

    Returns:
        AddDocumentResponse: Document added
    """
    vector_store = VectorStore(
        collection_name=document.collection_name,
        client=chroma_client,
        embeddings=cohere_embeddings,
    )
    ids = vector_store.add_documents(
        [Document(page_content=document.content)], reference_id=document.reference_id
    )
    return AddDocumentResponse(ids=ids)


@router.get(
    "/",
    name="Similarity Search",
    description="Search for similar documents",
    summary="Search for similar documents",
    response_description="List of similar documents",
)
def similarity_search(
    collection_name: Annotated[str, "Collection name"],
    chroma_client: Annotated[chromadb.Client, Depends(get_chroma_client)],
    cohere_embeddings: Annotated[Embeddings, Depends(get_cohere_embeddings)],
    query: Annotated[str, "Query string"] = "Hoàng Sa và Trường Sa là của ai?",
    k: Annotated[int, "Number of documents to return"] = 10,
    reference_id: Annotated[Optional[str], "Reference ID"] = None,
) -> Annotated[List[DocumentWithScore], "List of similar documents"]:
    """
    Search for similar documents

    Args:
        collection_name (str): Collection name
        chroma_client (chromadb.Client): Chroma client
        cohere_embeddings (Embeddings): Embeddings function
        query (str): Query string
        k (int): Number of documents to return
        reference_id (str): Reference ID

    Returns:
        List[DocumentWithScore]: List of similar documents
    """
    vector_store = VectorStore(
        collection_name=collection_name,
        client=chroma_client,
        embeddings=cohere_embeddings,
    )
    docs = vector_store.similarity_search(query=query, reference_id=reference_id, k=k)
    return [
        DocumentWithScore(
            page_content=doc[0].page_content,
            metadata=DocumentWithScoreMetadata(
                reference_id=doc[0].metadata["reference_id"]
            ),
            score=doc[1],
        )
        for doc in docs
    ]


@router.delete(
    "/{reference_id}",
    description="Delete documents by reference ID",
    summary="Delete documents by reference ID",
    response_description="No content",
)
def delete_documents_by_reference_id(
    reference_id: Annotated[str, "Reference ID"],
    collection_name: Annotated[str, "Collection name"],
    chroma_client: Annotated[chromadb.Client, Depends(get_chroma_client)],
) -> Annotated[None, "No content"]:
    """
    Delete documents by reference ID

    Args:
        reference_id (str): Reference ID
        collection_name (str): Collection name
        chroma_client (chromadb.Client): Chroma client

    Returns:
        None: No content
    """
    vector_store = VectorStore(
        collection_name=collection_name,
        client=chroma_client,
    )
    vector_store.delete_by_reference_id(reference_id=reference_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
