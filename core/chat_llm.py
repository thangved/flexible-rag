from typing import Annotated

from langchain_core.language_models import BaseChatModel, LanguageModelInput


class ChatLLM:
    def __init__(
        self,
        chat_model: Annotated[BaseChatModel, "A chat model"],
    ) -> None:
        self.chat_model = chat_model

    def chat(self, chat_input: Annotated[LanguageModelInput, "Chat Input"]) -> str:
        res = self.chat_model.invoke(input=chat_input)
        if type(res.content) is str:
            return res.content
        return "\n".join([s for s in res.content if type(s) is str])
