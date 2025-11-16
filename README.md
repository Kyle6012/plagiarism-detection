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

### Plagiarism Detection

-   **`POST /api/v1/documents/upload`**: Upload a batch of documents for plagiarism detection. Requires authentication.

    **Example:**
    ```javascript
    const handleUpload = async (files) => {
        const formData = new FormData();
        files.forEach(file => {
            formData.append('files', file);
        });

        const token = localStorage.getItem('token');

        try {
            const response = await fetch('/api/v1/documents/upload', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Upload failed');
            }

            const data = await response.json();
            console.log('Upload successful:', data);
            // Returns: { status: "ok", data: { batch_id: "..." } }
        } catch (error) {
            console.error('Error uploading files:', error);
        }
    };
    ```

-   **`GET /api/v1/batch/{batch_id}`**: Get the status of a processing batch. Requires authentication.

    **Example:**
    ```javascript
    const checkBatchStatus = async (batchId) => {
        const token = localStorage.getItem('token');
        try {
            const response = await fetch(`/api/v1/batch/${batchId}`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });
            const data = await response.json();
            console.log('Batch status:', data);
        } catch (error) {
            console.error('Error fetching batch status:', error);
        }
    };
    ```

-   **`GET /api/v1/batch/{batch_id}/results`**: Get the plagiarism results for a batch. Requires authentication.

    **Example:**
    ```javascript
    const getBatchResults = async (batchId) => {
        const token = localStorage.getItem('token');
        try {
            const response = await fetch(`/api/v1/batch/${batchId}/results`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });
            const data = await response.json();
            console.log('Batch results:', data);
        } catch (error) {
            console.error('Error fetching batch results:', error);
        }
    };
    ```

-   **`GET /api/v1/document/{document_id}`**: Get details for a specific document. Requires authentication.

    **Example:**
    ```javascript
    const getDocument = async (documentId) => {
        const token = localStorage.getItem('token');
        try {
            const response = await fetch(`/api/v1/document/${documentId}`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });
            const data = await response.json();
            console.log('Document details:', data);
        } catch (error) {
            console.error('Error fetching document details:', error);
        }
    };
    ```

### Authentication

-   **`POST /api/v1/auth/register`**: Register a new user.

    **Example:**
    ```javascript
    const registerUser = async (email, password) => {
        try {
            const response = await fetch('/api/v1/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            if (response.ok) {
                console.log('Registration successful!');
                // Redirect to login page
            } else {
                const errorData = await response.json();
                console.error('Registration failed:', errorData.detail);
            }
        } catch (error) {
            console.error('Error during registration:', error);
        }
    };
    ```

-   **`POST /api/v1/auth/jwt/login`**: Log in a user and receive a JWT token.

    **Example:**
    ```javascript
    const loginUser = async (email, password) => {
        try {
            const response = await fetch('/api/v1/auth/jwt/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    username: email,
                    password: password,
                }),
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('token', data.access_token);
                console.log('Login successful!');
                // Redirect to dashboard
            } else {
                console.error('Login failed');
            }
        } catch (error) {
            console.error('Error during login:', error);
        }
    };
    ```

-   **`POST /api/v1/auth/forgot-password`**: Request a password reset for a user.

    **Example:**
    ```javascript
    const forgotPassword = async (email) => {
        try {
            const response = await fetch('/api/v1/auth/forgot-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email }),
            });

            if (response.ok) {
                console.log('Password reset email sent!');
            } else {
                console.error('Failed to send password reset email');
            }
        } catch (error) {
            console.error('Error during password reset request:', error);
        }
    };
    ```

-   **`POST /api/v1/auth/reset-password`**: Reset a user's password using a token.

    **Example:**
    ```javascript
    const resetPassword = async (token, password) => {
        try {
            const response = await fetch('/api/v1/auth/reset-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ token, password }),
            });

            if (response.ok) {
                console.log('Password reset successful!');
            } else {
                console.error('Password reset failed');
            }
        } catch (error) {
            console.error('Error during password reset:', error);
        }
    };
    ```

### User Management

-   **`GET /api/v1/users/me`**: Get the current user's profile. Requires authentication.

    **Example:**
    ```javascript
    const getUserProfile = async () => {
        const token = localStorage.getItem('token');
        try {
            const response = await fetch('/api/v1/users/me', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });
            const data = await response.json();
            console.log('User profile:', data);
        } catch (error) {
            console.error('Error fetching user profile:', error);
        }
    };
    ```

### Dashboard

-   **`GET /api/v1/users/me/dashboard`**: Get dashboard metrics for the current user. Requires authentication.

    **Example:**
    ```javascript
    const getDashboardMetrics = async () => {
        const token = localStorage.getItem('token');
        try {
            const response = await fetch('/api/v1/users/me/dashboard', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });
            const data = await response.json();
            console.log('Dashboard metrics:', data.data);
            // Returns: { num_batches: X, num_documents: Y }
        } catch (error) {
            console.error('Error fetching dashboard metrics:', error);
        }
    };
    ```

## Concurrency and Multi-User Support

The system is designed to handle multiple users and concurrent document processing efficiently. This is achieved through the following architectural choices:

-   **Asynchronous API**: The FastAPI backend is asynchronous, allowing it to handle a large number of concurrent HTTP requests without being blocked by I/O operations.
-   **Background Task Processing**: Heavy computations and file processing are offloaded to a distributed Celery task queue. This prevents API endpoints from being tied up and allows for scalable, parallel processing of documents from multiple users.
-   **Isolated Database Sessions**: Each API request is provided with an independent database session, ensuring that concurrent transactions are handled safely and without interfering with one another.
-   **Stateless Authentication**: The use of JWT for authentication ensures that the system is stateless, allowing it to be easily scaled horizontally across multiple instances.
