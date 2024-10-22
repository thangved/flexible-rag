from langchain_core.documents import Document

from core.vector_store import VectorStore

collection_name = "test_collection"
vector_store = VectorStore(collection_name=collection_name)


def test_create_vector_store_instance():
    vector_store = VectorStore(collection_name=collection_name)
    assert vector_store.chroma._collection_name == collection_name


def test_add_documents():
    doc_1 = Document(page_content="test content 1")
    doc_2 = Document(page_content="test content 2")

    vector_store.add_documents([doc_1], reference_id="1")
    vector_store.add_documents([doc_2], reference_id="2")


def test_similarity_search():
    docs = vector_store.similarity_search(query="test content 1")
    docs_1 = vector_store.similarity_search(query="test content 1", reference_id="1")
    docs_2 = vector_store.similarity_search(query="test content 2", reference_id="2")

    assert len(docs) == 2

    for doc, score in docs:
        assert doc.metadata["reference_id"] in ["1", "2"]
        assert type(score) == float

    for doc, score in docs_1:
        assert doc.metadata["reference_id"] == "1"
        assert type(score) == float

    for doc, score in docs_2:
        assert doc.metadata["reference_id"] == "2"
        assert type(score) == float


def test_delete_by_reference_id():
    vector_store.delete_by_reference_id(reference_id="1")
    docs_1 = vector_store.similarity_search(query="test content 1", reference_id="1")
    assert len(docs_1) == 0
    docs_2 = vector_store.similarity_search(query="test content 2", reference_id="2")
    assert len(docs_2) == 1
