# Plagiarism Detection System

A powerful plagiarism and AI-generated content detection system that helps identify potential plagiarism and detect AI-generated text in a variety of file formats. This project is a monorepo containing a React frontend and a FastAPI backend.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Local Development Setup](#local-development-setup)
- [Windows 10/11 Local Deployment Guide](#windows-1011-local-deployment-guide)
    - [Why Use WSL? A Note for Windows Users](#why-use-wsl-a-note-for-windows-users)
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

This section is for users familiar with software development. For a more detailed guide for Windows, please see the next section.

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


## Windows 10/11 Local Deployment Guide

This guide provides detailed, step-by-step instructions to run the application locally on a Windows 10 or 11 machine.

### Why Use WSL? A Note for Windows Users

You might wonder why we are using the "Windows Subsystem for Linux" (WSL) instead of running the commands directly in Windows. This is a great question!

The simple answer is **reliability**. Modern web development tools, including those used in this project, are often designed and tested primarily for a Linux environment. By using WSL, we are creating a small, self-contained Linux environment directly on your Windows machine.

This approach helps to:
-   **Avoid Common Errors**: It prevents many common Windows-specific issues with file paths, command compatibility, and software installations.
-   **Ensure Consistency**: It guarantees that the development environment behaves the same for everyone, regardless of their operating system.
-   **Provide a Smoother Setup**: While it may seem like an extra step, using WSL is ultimately the most straightforward and reliable path to getting the application running successfully.

### Part 1: Initial Setup (WSL and Docker)

1.  **Install WSL 2**: Open PowerShell as an administrator and run:
    ```powershell
    wsl --install
    ```
    This will install the Windows Subsystem for Linux (WSL) with the default Ubuntu distribution. Restart your computer when prompted.

2.  **Install Docker Desktop**: Download and install Docker Desktop for Windows from the [official Docker website](https://www.docker.com/products/docker-desktop/). During installation, ensure the "Use WSL 2 instead of Hyper-V" option is selected.

### Part 2: Setting Up the Project

1.  **Open WSL Terminal**: Open your WSL terminal (you can find "Ubuntu" in your Start Menu). All the following commands will be run here.

2.  **Clone the Repository**:
    ```bash
    git clone https://github.com/Kyle6012/plagiarism-detection.git
    cd plagiarism-detection
    ```

3.  **Start Infrastructure Services**: Run the Docker containers. This command starts the database and other background services. It does **not** start the main application itself.
    ```bash
    docker-compose -f infra/docker-compose.yml up -d
    ```
    You can verify that the containers are running in Docker Desktop. You should see containers named `plagiarism_db`, `plagiarism_redis`, and `plagiarism_minio`.

### Part 3: Running the Backend

1.  **Install Python and Poetry**: We need to install the tools to run the backend.
    ```bash
    sudo apt-get update
    sudo apt-get install python3-pip python3.11-venv -y
    sudo apt-get install pipx -y
    pipx install poetry
    pipx ensurepath
    ```
    **Important:** You may need to close and reopen your WSL terminal at this point for the `poetry` command to be recognized.

2.  **Install Backend Dependencies**: Navigate to the `backend` directory and install the necessary packages.
    ```bash
    cd backend
    poetry install
    ```

3.  **Run Database Migrations**: This sets up the database schema.
    ```bash
    poetry run alembic upgrade head
    ```

4.  **Start the Backend Server**:
    ```bash
    poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```
    **Leave this terminal open.** The backend is now running.

### Part 4: Running the Frontend

1.  **Open a New WSL Terminal**: Open a second WSL terminal window. You'll have two terminals running side-by-side.

2.  **Install Node.js**: We need to install the tools to run the frontend.
    ```bash
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
    ```

3.  **Install Frontend Dependencies**: Navigate to the `frontend` directory in your **new** terminal.
    ```bash
    cd plagiarism-detection/frontend
    npm install
    ```

4.  **Start the Frontend Server**:
    ```bash
    npm run dev
    ```
    **Leave this terminal open.** The frontend is now running.

### Part 5: Access the Application

The application is now fully running. You can access the web interface by opening your browser and navigating to:
**http://localhost:5173**

## Usage

Once the application is running, you can access the web interface to upload files for plagiarism and AI-generated content detection.

## Future Work

-   **Batch Processing**: The system is designed to support batch processing of documents for large-scale analysis. The `batch_processing.py` service contains a placeholder for this functionality.
-   **User Authentication**: Implement user accounts and authentication.
-   **Dashboard and Reporting**: A dashboard to provide users with a summary of their results.
-   **More File Formats**: Support for additional file formats like `.docx` and `.pdf`.
