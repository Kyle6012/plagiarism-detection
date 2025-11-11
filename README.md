# Plagiarism Detection System

A powerful plagiarism and AI-generated content detection system that helps identify potential plagiarism and detect AI-generated text in a variety of file formats. This project is a monorepo containing a React frontend and a FastAPI backend.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Local Development Setup](#local-development-setup)
- [Windows Local Deployment](#windows-local-deployment)
- [Usage](#usage)
- [Future Work](#future-work)

## Features

- **Text Plagiarism Detection**: Upload and analyze text files to detect similarities with previously uploaded documents.
- **Image Plagiarism Detection**: Upload image files to compare with stored image embeddings for similarity.
- **AI-Generated Text Detection**: Detect AI-generated content in text using advanced AI models.
- **Web Interface**: Simple and user-friendly web interface for easy interaction with the system.

## Technologies Used

- **FastAPI**: Web framework for building the backend API.
- **React**: JavaScript library for building the user interface.
- **PostgreSQL with pgvector**: Database for storing document and image embeddings and performing vector similarity searches.
- **Docker**: For containerizing and managing the development environment.

## Local Development Setup

To set up the plagiarism detection system locally, follow the steps below.

### Prerequisites

- Python 3.12+
- Poetry for Python package management
- Node.js 18+
- Docker and Docker Compose

### Step-by-Step Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Kyle6012/plagiarism-detection.git
    cd plagiarism-detection
    ```

2.  **Backend Setup**:
    - Navigate to the backend directory:
      ```bash
      cd backend
      ```
    - Install the required Python packages using Poetry:
      ```bash
      poetry install
      ```
    - Activate the virtual environment created by Poetry:
        ```bash
        poetry shell
        ```
    - Run the database migrations:
        ```bash
        alembic upgrade head
        ```

3.  **Frontend Setup**:
    - Navigate to the frontend directory:
      ```bash
      cd ../frontend
      ```
    - Install the required Node.js packages:
      ```bash
      npm install
      ```

4.  **Running the Application**:
    - **Start the Docker services** (PostgreSQL, Redis, etc.):
        In the root directory of the project, run:
        ```bash
        docker-compose -f infra/docker-compose.yml up -d
        ```
    - **Start the backend server**:
        In the `backend` directory, run:
        ```bash
        poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
        ```
    - **Start the frontend server**:
        In the `frontend` directory, run:
        ```bash
        npm run dev
        ```

5.  **Access the system**:
    Open your browser and go to http://localhost:5173.

## Windows Local Deployment

To deploy the application locally on Windows 10 or 11, you will need to use WSL (Windows Subsystem for Linux) and Docker Desktop.

### Prerequisites

1.  **WSL 2**: Ensure you have WSL 2 installed. You can install it by running the following command in a PowerShell with administrator privileges:
    ```powershell
    wsl --install
    ```
    This will install the default Ubuntu distribution.

2.  **Docker Desktop**: Download and install Docker Desktop for Windows. The installer can be found on the [Docker website](https://www.docker.com/products/docker-desktop/). During installation, make sure to select the "Use WSL 2 instead of Hyper-V" option.

### Step-by-Step Setup

1.  **Clone the repository in WSL**: Open your WSL terminal (e.g., Ubuntu) and clone the repository:
    ```bash
    git clone https://github.com/Kyle6012/plagiarism-detection.git
    cd plagiarism-detection
    ```

2.  **Run the application with Docker Compose**:
    ```bash
    docker-compose -f infra/docker-compose.yml up -d
    ```
    This will build and start all the services required for the application to run. The backend and frontend will be available at their respective ports.

## Usage

Once the application is running, you can access the web interface at `http://localhost:5173`. From there, you can upload files for plagiarism and AI-generated content detection.

## Future Work

The following features are planned for future releases but are not yet implemented:

-   **Batch Processing**: The system is designed to support batch processing of documents for large-scale analysis. The `batch_processing.py` service contains a placeholder for this functionality, which will be implemented to handle asynchronous processing of multiple files.
-   **User Authentication**: Implement user accounts and authentication to allow users to manage their own documents and view their history.
-   **Dashboard and Reporting**: A dashboard to provide users with a summary of their plagiarism and AI detection results, along with detailed reports.
-   **More File Formats**: Support for additional file formats, such as `.docx`, `.pdf`, and more.
