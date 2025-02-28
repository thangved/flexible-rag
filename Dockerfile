FROM python:3.10-slim-bookworm AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update -y
RUN apt-get install -y git

FROM base AS install

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --all-groups


FROM install AS test

COPY . .

RUN ["uv", "run", "pytest"]

FROM install AS development

CMD [ "uv", "run", "fastapi", "dev", "/app/api/main.py", "--host", "0.0.0.0", "--port", "8000" ]

FROM install AS production

COPY . .

CMD [ "uv", "run", "fastapi", "run", "/app/api/main.py", "--host", "0.0.0.0", "--port", "8000" ]
