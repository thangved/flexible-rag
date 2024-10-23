from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from core.chat_llm import ChatInput, ChatLLM

from ..dependencies import get_chat_model

router = APIRouter(dependencies=[Depends(get_chat_model)])


class ChatOutput(BaseModel):
    """
    Chat output

    Attributes:
        content (str): Content of the message
    """

    content: str = Field(
        ...,
        title="Content of the message",
        description="Content of the message",
        examples=["Hello, how can I help you today?"],
    )


@router.post(
    "",
    description="Chat with the chat model",
    summary="Chat with the chat model",
    response_description="Response of the model",
)
def chat(
    chat_input: Annotated[ChatInput, "Chat Input"], chat_model=Depends(get_chat_model)
) -> Annotated[ChatOutput, "Chat Output"]:
    """
    Chat with the chat model

    Args:
        chat_input (ChatInput): Chat input
        chat_model (BaseChatModel): Chat model

    Returns:
        ChatOutput: Chat output
    """
    chat_llm = ChatLLM(chat_model=chat_model)
    res = chat_llm.chat(chat_input=chat_input)
    return ChatOutput(content=res)
