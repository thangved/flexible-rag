from core.chat_llm import ChatLLMModel


class FakeLLMChatModel(ChatLLMModel):
    """A fake chat model."""

    def chat(self, chat_input) -> str:
        """
        Chat with the model.

        Args:
            chat_input: Chat input (not used)

        Returns:
            str: A fake chat response
        """
        return "Hello, how can I help you today?"
