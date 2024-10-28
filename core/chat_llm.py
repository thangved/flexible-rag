from abc import ABC, abstractmethod
from typing import Annotated

from pydantic import BaseModel, Field

from core.models.chat import ChatMessage


class ChatInput(BaseModel):
    """
    Chat input

    Attributes:
        messages (list[ChatMessage]): Messages
    """

    messages: list[ChatMessage] = Field(
        ...,
        title="Messages",
        description="Messages",
    )


class ChatLLMModel(ABC):
    """Chat with a language model"""

    @abstractmethod
    def chat(self, chat_input: Annotated[ChatInput, "Chat Input"]) -> str:
        """
        Chat with the chat model

        Args:
            chat_input (ChatInput): Chat input

        Returns:
            str: Chat output
        """


class ChatLLM:
    """
    Chat with a language model

    Attributes:
        chat_model (BaseChatModel): A chat model
    """

    def __init__(
        self,
        chat_model: Annotated[ChatLLMModel, "A chat model"],
    ) -> None:
        """
        Create a ChatLLM

        Args:
            chat_model (BaseChatModel): A chat model
        """
        self.chat_model = chat_model

    def chat(self, chat_input: Annotated[ChatInput, "Chat Input"]) -> str:
        """
        Chat with the chat model

        Args:
            chat_input (LanguageModelInput): Chat input

        Returns:
            str: Chat output
        """
        return self.chat_model.chat(chat_input)
