# Use single stage build for simplicity
FROM python:3.11-slim

WORKDIR /app

# Install poetry
RUN pip install --no-cache-dir poetry

# Copy dependency files
COPY backend/pyproject.toml backend/poetry.lock ./

# Install dependencies globally (no venv needed in container)
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main

# Copy application code
COPY backend/ .

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
