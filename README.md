# Plagiarism Detection System

A powerful plagiarism and AI-generated content detection system that helps identify potential plagiarism and detect AI-generated text in a variety of file formats. This project is a monorepo containing a React frontend and a FastAPI backend.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Local Development Setup](#local-development-setup)
- [Docker Setup (Under Development)](#docker-setup-under-development)
- [API Endpoints](#api-endpoints)
- [Future Work](#future-work)

## Features

- **Text Plagiarism Detection**: Upload and analyze text files to detect similarities with previously uploaded documents.
- **Image Plagiarism Detection**: Upload image files to compare with stored image embeddings for similarity.
- **AI-Generated Text Detection**: Detect AI-generated content in text using advanced AI models.
- **Web Interface**: Simple and user-friendly web interface for easy interaction with the system.
- **Asynchronous Processing**: Celery and Redis are used for background processing of large files.
- **Scalable Storage**: MinIO is used for S3-compatible object storage.

## Technologies Used

- **FastAPI**: Web framework for building the backend API.
- **React**: JavaScript library for building the user interface.
- **PostgreSQL with pgvector**: Database for storing document and image embeddings and performing vector similarity searches.
- **Celery and Redis**: For asynchronous task management.
- **MinIO**: For S3-compatible object storage.
- **Docker**: For containerizing and managing the development environment.
- **Alembic**: For database migrations.

## Project Structure

The project is organized as a monorepo with the following structure:

- `backend/`: The FastAPI backend application.
- `frontend/`: The React frontend application.
- `infra/`: Docker Compose configuration for the infrastructure services.

## Local Development Setup

### Prerequisites

- Python 3.12+
- Poetry for Python package management
- Node.js 18+
- Docker and Docker Compose

### Step-by-Step Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/plagiarism-detection.git
    cd plagiarism-detection
    ```

2.  **Start Infrastructure Services**:
    ```bash
    docker-compose -f infra/docker-compose.yml up -d
    ```

3.  **Backend Setup**:
    ```bash
    cd backend
    poetry install
    poetry shell
    alembic upgrade head
    poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

4.  **Frontend Setup**:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

5.  **Access the system**:
    Open your browser and go to http://localhost:5173.

## Docker Setup (Under Development)

The Docker setup is still under development and may not be fully functional.

To build and run the entire application with Docker, use the following command:

```bash
sudo docker compose -f infra/docker-compose.yml up -d --build
```

## API Endpoints

The backend API provides the following endpoints:

- `POST /api/v1/documents/upload`: Upload documents for plagiarism detection.

## Future Work

-   **User Authentication**: Implement user accounts and authentication.
-   **Dashboard and Reporting**: A dashboard to provide users with a summary of their results.
-   **More File Formats**: Support for additional file formats like `.docx` and `.pdf`.
-   **Full API Implementation**: Complete the implementation of all API endpoints.
-   **Testing**: Write a comprehensive test suite for the backend and frontend.
