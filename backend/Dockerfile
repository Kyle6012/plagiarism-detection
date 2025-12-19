# Use single stage build for simplicity
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for OCR and PDF processing
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install --no-cache-dir poetry

# Copy dependency files
COPY backend/pyproject.toml backend/poetry.lock ./

# Install dependencies globally (no venv needed in container)
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main

# Install additional dependencies from requirements.txt (to ensure new packages are installed)
COPY backend/requirements.txt .
RUN pip install --default-timeout=1000 -r requirements.txt

# Copy application code
COPY backend/ .

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
