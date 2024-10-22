from typing import Annotated, Optional

import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings, FakeEmbeddings


class VectorStore:
    """
    Vector store class

    Attributes:
        chroma (Chroma): Chroma instance
    """

    def __init__(
        self,
        collection_name: Annotated[
            Optional[str],
            "Collection name",
        ] = "default_collection",
        client: Annotated[
            Optional[chromadb.Client],
            "Chroma client",
        ] = None,
        embeddings: Annotated[
            Optional[Embeddings],
            "Embeddings function",
        ] = FakeEmbeddings(size=768),
    ):
        """
        Initialize the vector store

        Args:
            collection_name (str): Collection name
        """
        self.chroma = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            client=client,
            collection_metadata={"hnsw:space": "cosine"},
        )

    def add_documents(
        self,
        documents: Annotated[
            list[Document],
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
        if reference_id is not None:
            for doc in documents:
                doc.metadata["reference_id"] = reference_id

        return self.chroma.add_documents(documents=documents)

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
    ) -> list[Document]:
        """
        Search for similar documents

        Args:
            query (str): Query string
            reference_id (str): Reference ID
            k (int): Number of result documents

        Returns:
            list[Document]: List of similar documents
        """
        query_filter = (
            {"reference_id": reference_id} if reference_id is not None else None
        )
        docs_with_scores = self.chroma.similarity_search_with_score(
            query=query,
            k=k,
            filter=query_filter,
        )
        return docs_with_scores

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
        docs = self.chroma.get(where={"reference_id": reference_id})
        ids = docs["ids"]
        if len(ids) > 0:
            self.chroma.delete(ids=docs["ids"])
