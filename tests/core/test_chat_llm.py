from core.chat_llm import ChatLLM
from core.models.chat import ChatMessage, ChatMessageRole
from tests.fake.llm_chat import FakeLLMChatModel

chat_model = FakeLLMChatModel()


def test_create_chat_llm():
    """Test create ChatLLM"""
    chat_llm = ChatLLM(chat_model=chat_model)
    assert chat_llm is not None


def test_chat():
    """Test chat method"""
    chat_llm = ChatLLM(chat_model=chat_model)
    messages = [ChatMessage(role=ChatMessageRole.Human, content="Hello")]
    response = chat_llm.chat(messages)
    assert type(response) is str
