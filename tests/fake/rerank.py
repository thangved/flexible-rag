from typing import List

from core.rerank import RerankModel


class FakeRerankModel(RerankModel):
    """Fake Rerank Model"""

    def rerank(
        self,
        query: str,
        docs: List[str],
    ) -> List[float]:
        """
        Rerank the documents based on the query
        Args:
            query (str): The query use to rerank
            docs (List[str]): List of documents

            Returns:
                List[float]: List of relevance scores ([0.2, 0.1, 0.4, 0.3] => [3, 4, 1, 2])
        """
        return [
            0.2,
            0.1,
            0.4,
            0.3,
        ]  # => [3, 4, 1, 2]
