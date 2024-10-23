from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
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


class Document(BaseModel):
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
    metadata: DocumentMetadata = Field(
        ...,
        title="Metadata",
        description="Metadata",
    )


class DocumentWithScore(Document):
    """
    Document with Score

    Attributes:
        score (float): Score
    """

    model_config = {
        "title": "Document with Score",
        "strict": True,
    }
    score: float = Field(
        ...,
        title="Score",
        description="Score",
        examples=[0.99],
    )
