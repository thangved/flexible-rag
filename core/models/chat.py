from enum import Enum

from pydantic import BaseModel, Field


class ChatMessageRole(str, Enum):
    """
    Role of the message

    Attributes:
        Human (str): Human role
        Ai (str): AI role
        System (str): System role
    """

    Human = "human"
    Ai = "ai"
    System = "system"


class ChatMessage(BaseModel):
    """
    Chat message

    Attributes:
        role (ChatMessageRole): Role of the message
        content (str): Content of the message
    """

    role: ChatMessageRole = Field(
        ...,
        title="Role of the message",
        description="Role of the message",
    )
    content: str = Field(
        ...,
        title="Content of the message",
        description="Content of the message",
        examples=["Hello, how can I help you today?"],
    )
