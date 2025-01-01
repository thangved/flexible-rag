FROM python:3.14.0a3-slim-bookworm AS base

RUN pip install poetry

FROM base AS install

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --without docs

FROM install AS test

COPY . .

RUN poetry run pytest

FROM install AS development

CMD [ "poetry", "run", "fastapi", "dev", "/app/api/main.py", "--host", "0.0.0.0", "--port", "8000" ]

FROM install AS production

COPY . .

CMD [ "poetry", "run", "fastapi", "run", "/app/api/main.py", "--host", "0.0.0.0", "--port", "8000" ]
