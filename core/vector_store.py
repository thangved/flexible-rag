from typing import Annotated, Optional, Tuple

import chromadb
import chromadb.api
import chromadb.api.client
import nanoid
from chromadb.utils import embedding_functions

from core.models.documents import Document


class VectorStore:
    """Vector store class"""

    def __init__(
        self,
        collection_name: Annotated[
            Optional[str],
            "Collection name",
        ] = "default_collection",
        client: Annotated[
            Optional[chromadb.api.client.Client],
            "Chroma client",
        ] = chromadb.Client(),
        embeddings: Annotated[
            Optional[chromadb.Embeddings],
            "Embeddings function",
        ] = embedding_functions.DefaultEmbeddingFunction(),
    ):
        """
        Initialize the vector store

        Args:
            collection_name (str): Collection name
        """
        self.collection = client.get_or_create_collection(
            name=collection_name,
            embedding_function=embeddings,
            metadata={"hnsw:space": "cosine"},
        )

    def add_documents(
        self,
        documents: Annotated[
            list[str],
            "List of documents",
        ],
        reference_id: Annotated[
            Optional[str],
            "Reference ID",
        ] = None,
    ) -> Annotated[
        list[str],
        "List of document IDs",
    ]:
        """
        Add documents to the vector store

        Args:
            documents (list[Document]): List of documents

        Returns:
            list[str]: List of document IDs
        """
        metadatas = (
            [
                {
                    "reference_id": reference_id,
                }
                for _ in range(len(documents))
            ]
            if reference_id is not None
            else [{} for _ in range(len(documents))]
        )
        ids = [nanoid.generate() for _ in range(len(documents))]
        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas,
        )
        return ids

    def similarity_search(
        self,
        query: Annotated[
            str,
            "Query string",
        ],
        reference_id: Annotated[
            Optional[str],
            "Reference ID",
        ] = None,
        k: Annotated[
            int,
            "Number of result documents",
        ] = 3,
    ) -> list[Tuple[Document, float]]:
        """
        Search for similar documents

        Args:
            query (str): Query string
            reference_id (str): Reference ID
            k (int): Number of result documents

        Returns:
            list[Tuple[Document, float]]: List of documents and their similarity scores
        """
        where = {"reference_id": reference_id} if reference_id is not None else None
        res = self.collection.query(
            query_texts=[query],
            n_results=k,
            where=where,
        )
        return [
            (
                Document(
                    page_content=res["documents"][0][i],
                    metadata=res["metadatas"][0][i],
                ),
                res["distances"][0][i] / 100,
            )
            for i in range(len(res["documents"][0]))
        ]

    def delete_by_reference_id(
        self,
        reference_id: Annotated[
            str,
            "Reference ID",
        ],
    ) -> None:
        """
        Delete documents by reference_id

        Args:
            reference_id (str): Reference ID

        Returns:
            None
        """
        self.collection.delete(where={"reference_id": reference_id})
