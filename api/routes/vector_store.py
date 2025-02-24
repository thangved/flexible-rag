from typing import Annotated, Optional, Tuple

import chromadb
import httpx
from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, Field

from core.models.documents import Document, DocumentWithScore
from core.vector_store import VectorStore

from ..dependencies import (
    CohereEmbeddingsFunction,
    get_chroma_client,
    get_embeddings_function,
    logger,
)

router = APIRouter(
    dependencies=[
        Depends(get_chroma_client),
        Depends(get_embeddings_function),
    ],
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


class DocumentWithReference(DocumentWithScore):
    """Document with reference"""

    reference: dict = Field(description="Reference", title="Reference", default=None)


class SimilaritySearchResponse(BaseModel):
    """
    Similarity Search Response

    Attributes:
        documents (list[DocumentWithReference]): List of documents
    """

    model_config = {
        "title": "Similarity Search Response",
        "strict": True,
    }
    documents: list[DocumentWithReference] = Field(
        ...,
        description="List of documents",
        title="List of documents",
    )
    query: str = Field(
        ...,
        description="Query string",
        title="Query string",
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
        examples=["Uj9uY4N41cpSZb0MHBY_w"],
    )


@router.post(
    "",
    description="Add a document to the vector store",
    summary="Add a document to the vector store",
    name="Add Document",
    response_description="Document added",
)
def create_document(
    document: Annotated[
        AddDocumentInput,
        "Add Document Input",
    ],
    chroma_client: Annotated[
        chromadb.Client,
        Depends(get_chroma_client),
    ],
    cohere_embeddings: Annotated[
        CohereEmbeddingsFunction,
        Depends(get_embeddings_function),
    ],
) -> Annotated[
    AddDocumentResponse,
    "Document added",
]:
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
        [document.content],
        reference_id=document.reference_id,
    )
    return AddDocumentResponse(ids=ids)


@router.get(
    "",
    name="Similarity Search",
    description="Search for similar documents",
    summary="Search for similar documents",
    response_description="List of similar documents",
)
def similarity_search(
    collection_name: Annotated[
        str,
        "Collection name",
    ],
    chroma_client: Annotated[
        chromadb.Client,
        Depends(get_chroma_client),
    ],
    cohere_embeddings: Annotated[
        CohereEmbeddingsFunction,
        Depends(get_embeddings_function),
    ],
    query: Annotated[
        str,
        "Query string",
    ],
    k: Annotated[
        int,
        "Number of documents to return",
    ] = 10,
    reference_id: Annotated[
        Optional[str],
        "Reference ID",
    ] = None,
    reference_callback: Annotated[Optional[str], "Reference callback"] = None,
) -> Annotated[
    SimilaritySearchResponse,
    "Similarity Search Response",
]:
    """
    Search for similar documents

    Args:
        collection_name (str): Collection name
        chroma_client (chromadb.Client): Chroma client
        cohere_embeddings (CohereEmbeddingsFunction): Embeddings function
        query (str): Query string
        k (int): Number of documents to return
        reference_id (str): Reference ID
        reference_callback (str): Reference callback url

    Returns:
        SimilaritySearchResponse: Similarity Search Response
    """
    vector_store = VectorStore(
        collection_name=collection_name,
        client=chroma_client,
        embeddings=cohere_embeddings,
    )
    result_documents = vector_store.similarity_search(
        query=query,
        reference_id=reference_id,
        k=k,
    )

    def map_documents(doc: Tuple[Document, float]):
        """
        Map foreach document and return the result

        Args:
            doc (Tuple[Document, float]): A tuple contain document and score

        Returns:
            DocumentWithReference: Mapped document
        """
        mapped_document = DocumentWithReference(
            page_content=doc[0].page_content,
            metadata=doc[0].metadata,
            score=doc[1],
        )
        if reference_callback is not None:
            try:
                mapped_document.reference = httpx.get(
                    url=reference_callback.format(
                        reference_id=doc[0].metadata.reference_id
                    ),
                    timeout=1,
                ).json()
            except BaseException as e:
                logger.warning("Call reference_callback error: %s", e)
                mapped_document.reference = {"id": doc[0].metadata.reference_id}
        return mapped_document

    documents = list(map(map_documents, result_documents))
    return SimilaritySearchResponse(
        documents=documents,
        query=query,
    )


@router.delete(
    "/{reference_id}",
    description="Delete documents by reference ID",
    summary="Delete documents by reference ID",
    response_description="No content",
)
def delete_documents_by_reference_id(
    reference_id: Annotated[
        str,
        "Reference ID",
    ],
    collection_name: Annotated[
        str,
        "Collection name",
    ],
    chroma_client: Annotated[
        chromadb.Client,
        Depends(get_chroma_client),
    ],
) -> Annotated[
    None,
    "No content",
]:
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
