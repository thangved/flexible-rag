from langchain_core.language_models import FakeListChatModel
from langchain_core.messages import HumanMessage

from core.chat_llm import ChatLLM

chat_model = FakeListChatModel(
    responses=[
        "Hello, how can I help you today?",
    ],
)


def test_create_chat_llm():
    """
    Test create ChatLLM
    """
    chat_llm = ChatLLM(chat_model=chat_model)
    assert chat_llm is not None


def test_chat():
    """
    Test chat method
    """
    chat_llm = ChatLLM(chat_model=chat_model)
    messages = [
        HumanMessage(
            content="Hello",
        )
    ]
    response = chat_llm.chat(messages)
    assert response is not None
    assert response == chat_model.responses[0]
