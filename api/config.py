import os

COHERE_API_KEY = os.getenv(
    "COHERE_API_KEY",
    "",
)

CHROMA_HOST = os.getenv(
    "CHROMA_HOST",
    "localhost",
)
CHROMA_PORT = os.getenv(
    "CHROMA_PORT",
    "8080",
)
