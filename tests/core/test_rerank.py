from core.models.documents import Document, DocumentMetadata
from core.rerank import Rerank
from tests.fake.rerank import FakeRerankModel


def test_create_rerank():
    rerank = Rerank(model=FakeRerankModel())
    assert isinstance(rerank, Rerank)


def test_rerank_1():
    rerank = Rerank(model=FakeRerankModel())
    documents = []
    reranked_documents = rerank.rerank("query", documents)
    assert type(reranked_documents) is list
    assert len(reranked_documents) == 0


def test_rerank_2():
    rerank = Rerank(model=FakeRerankModel())
    documents = [
        Document(
            page_content="Document 1",
            metadata=DocumentMetadata(reference_id="1"),
        ),
        Document(
            page_content="Document 2",
            metadata=DocumentMetadata(reference_id="2"),
        ),
        Document(
            page_content="Document 3",
            metadata=DocumentMetadata(reference_id="3"),
        ),
        Document(
            page_content="Document 4",
            metadata=DocumentMetadata(reference_id="4"),
        ),
    ]
    reranked_documents = rerank.rerank("query", documents)
    assert type(reranked_documents) is list
    assert len(reranked_documents) == 4
    assert reranked_documents[0].metadata.reference_id == "3"
    assert reranked_documents[1].metadata.reference_id == "4"
    assert reranked_documents[2].metadata.reference_id == "1"
    assert reranked_documents[3].metadata.reference_id == "2"
