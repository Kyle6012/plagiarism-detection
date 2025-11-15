# Stage 1: Build the application
FROM python:3.11-bullseye as builder

WORKDIR /app

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install poetry

COPY backend/pyproject.toml backend/poetry.lock ./
RUN poetry install --no-root --no-dev

# Stage 2: Create the final image
FROM python:3.11-bullseye

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

COPY --from=builder /app/.venv .venv
COPY backend/ .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
