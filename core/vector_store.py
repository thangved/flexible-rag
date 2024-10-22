from typing import Annotated, Optional

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import FakeEmbeddings


class VectorStore:
    def __init__(
        self,
        collection_name: Annotated[
            Optional[str], "Collection name"
        ] = "default_collection",
    ) -> None:
        embeddings = FakeEmbeddings(size=4096)
        self.chroma = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
        )

    def add_documents(
        self, documents: Annotated[list[Document], "List of documents"]
    ) -> None:
        self.chroma.add_documents(documents=documents)

    def similarity_search(
        self,
        query: Annotated[str, "Query string"],
        reference_id: Annotated[Optional[str], "Reference ID"] = None,
        k: Annotated[int, "Number of result documents"] = 3,
    ) -> list[Document]:
        filter = {"reference_id": reference_id} if reference_id is not None else None
        docs_with_scores = self.chroma.similarity_search_with_score(
            query=query, k=k, filter=filter
        )
        return [doc[0] for doc in docs_with_scores]

    def delete_by_reference_id(
        self,
        reference_id: Annotated[str, "Reference ID"],
    ) -> None:
        docs = self.chroma.get(where={"reference_id": reference_id})
        self.chroma.delete(ids=docs["ids"])
