from core.chat_llm import ChatLLMModel


class FakeLLMChatModel(ChatLLMModel):
    def chat(self, chat_input) -> str:
        return "Hello, how can I help you today?"
