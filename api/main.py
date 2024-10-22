from fastapi import FastAPI

from .routes import chat_llm, vector_store

app = FastAPI(
    root_path="/api/v1",
    contact={
        "name": "Kim Minh Thang",
        "email": "root@thangved.com",
        "url": "https://thangved.com",
    },
    description=(
        "Implemented a RAG (Retrieval-Augmented Generation) with common APIs, without"
        " any specific task in mind. This is a flexible RAG that can be used for any"
        " task with a simple configuration."
    ),
    title="Flexible RAG API",
    summary="Flexible RAG API",
    version="0.1.0",
)


app.include_router(
    router=vector_store.router,
    prefix="/vector_store",
    tags=["Vector Store"],
)

app.include_router(
    router=chat_llm.router,
    prefix="/chat_llm",
    tags=["Chat LLM"],
)
