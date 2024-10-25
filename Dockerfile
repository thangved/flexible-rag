FROM python:3.9 AS base

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

CMD [ "poetry", "run", "fastapi", "run", "/app/api/main.py", "--host", "0.0.0.0", "--port", "8000" ]
