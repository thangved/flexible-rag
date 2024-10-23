from abc import ABC, abstractmethod
from typing import Annotated, List

from core.models.documents import DocumentWithScore
from core.vector_store import Document


class RerankModel(ABC):
    @abstractmethod
    def rerank(
        self,
        query: Annotated[str, "The query use to rerank"],
        docs: Annotated[List[str], "List of documents"],
    ) -> Annotated[List[float], "List of scores for each document"]:
        """
        Rerank the documents based on the query
        Args:
            query (str): The query use to rerank
            docs (List[str]): List of documents

            Returns:
                List[float]: List of relevance scores
        """


class Rerank:
    def __init__(self, model: Annotated[RerankModel, "Rerank model"]) -> None:
        self.model = model

    def rerank(
        self,
        query: Annotated[str, "The query use to rerank"],
        docs: Annotated[List[Document], "List of documents"],
    ) -> Annotated[
        List[DocumentWithScore],
        "List of documents with ranked score and sorted by score",
    ]:
        """
        Rerank the documents based on the query
        Args:
            query (str): The query use to rerank
            docs (List[Document]): List of documents

        Returns:
            List[DocumentWithScore]: List of documents with ranked score and sorted by score
        """
        scores = self.model.rerank(query, [doc.page_content for doc in docs])
        mapped_documents = [
            DocumentWithScore(
                page_content=doc.page_content,
                metadata=doc.metadata,
                score=score,
            )
            for doc, score in zip(docs, scores)
        ]
        sorted_documents = sorted(mapped_documents, key=lambda x: x.score, reverse=True)
        return sorted_documents
