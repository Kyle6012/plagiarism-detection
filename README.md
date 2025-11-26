https://github.com/Kyle6012/plagiarism-detection.git# Plagiarism Detection System

A powerful plagiarism and AI-generated content detection system featuring a premium, modern UI and flexible deployment options. This project is a monorepo containing a React frontend and a FastAPI backend.

## Features

- **Premium UI**: Modern, responsive interface with glassmorphism, dark mode, and smooth animations.
- **Text Plagiarism Detection**: Upload and analyze text files to detect similarities using semantic embeddings.
- **AI-Generated Text Detection**: Detect AI-generated content using local HuggingFace models or optional external APIs (OpenAI).
- **Archive Support**: Automatically extract and analyze files from `.zip`, `.tar`, `.tar.gz`, and other compressed formats.
- **Flexible Analysis Options**: Choose plagiarism detection, AI detection, or both for each batch.
- **Folder Upload**: Upload entire directories for batch processing.
- **Dual Deployment**:
    - **Full Mode (Docker)**: Complete feature set with local ML models, Celery workers, and Redis.
    - **Lite Mode (Vercel)**: Lightweight deployment for serverless environments (ML models disabled).
- **Scalable Architecture**: Asynchronous processing with Celery, Redis, and MinIO storage.
- **Optional External APIs**: Configure OpenAI or other services for enhanced AI detection accuracy.

## 🚀 Getting Started (Beginner's Guide)

Follow these steps to set up the project from scratch on your operating system.

### 1. Install Prerequisites

#### 🪟 Windows
1.  **Install WSL2 (Recommended)**:
    - Open PowerShell as Administrator and run: `wsl --install`
    - Restart your computer.
    - Open "Ubuntu" from the Start menu to set up your Linux username and password.
2.  **Install Docker Desktop**:
    - Download from [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/).
    - During install, ensure "Use WSL 2 instead of Hyper-V" is checked.
    - Open Docker Desktop settings -> Resources -> WSL Integration -> Enable for your Ubuntu distro.
3.  **Install Git**:
    - Download from [Git for Windows](https://git-scm.com/download/win).
    - Install with default settings.
4.  **Install Node.js**:
    - Download the "LTS" version from [Node.js Website](https://nodejs.org/).

#### 🍎 macOS
1.  **Install Docker Desktop**:
    - Download from [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/).
    - Drag to Applications and run it.
2.  **Install Git & Node.js (via Homebrew)**:
    - Open Terminal (Command + Space, type "Terminal").
    - Install Homebrew:
      ```bash
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
      ```
    - Install tools:
      ```bash
      brew install git node
      ```

#### 🐧 Linux (Ubuntu/Debian)
1.  **Install Docker**:
    ```bash
    # Add Docker's official GPG key:
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update

    # Install Docker packages:
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```
2.  **Install Git & Node.js**:
    ```bash
    sudo apt update
    sudo apt install git nodejs npm
    ```

### 2. Clone and Run

Now that you have the tools, let's run the app!

1.  **Open your Terminal** (PowerShell/Ubuntu on Windows, Terminal on Mac/Linux).
2.  **Clone the Project**:
    ```bash
    git clone https://github.com/Kyle6012/plagiarism-detection.git
    cd plagiarism-detection
    ```
3.  **Start the System**:
    ```bash
    # Windows / Mac
    docker-compose up --build -d

    # Linux (if permission denied)
    sudo docker-compose up --build -d
    ```
    *This will take a few minutes the first time as it downloads all dependencies.*

4.  **Verify it's running**:
    - Run `docker ps` to see the running containers.
    - Open your browser to the links below.

### 3. Access the Application
- **Frontend (The App)**: [http://localhost:80](http://localhost:80)
- **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **MinIO Storage Console**: [http://localhost:9001](http://localhost:9001)
    - **Username**: `minioadmin`
    - **Password**: `minioadmin`

## Deployment Options

### 1. Containerized (Docker) - Recommended
Runs the complete system with all services (Frontend, Backend, Postgres, Redis, MinIO, Celery Worker).
- **Config**: `docker-compose.yml` in the root.
- **Env**: Uses `backend/.env.docker` automatically.

### 2. Vercel (Lite Mode)
Deploys the Frontend and a lightweight Backend to Vercel's serverless platform.
- **Limitation**: Local ML models (Sentence Transformers) are disabled due to serverless bundle size limits.
- **Config**: `vercel.json`.
- **Setup**: Install Vercel CLI (`npm i -g vercel`) and run `vercel` in the root.

## Project Structure

- `backend/`: FastAPI application, database models, and ML logic.
- `frontend/`: React application with Vite and Tailwind CSS.
- `docker-compose.yml`: Root Docker configuration.
- `vercel.json`: Vercel deployment configuration.

## Technologies Used

- **Frontend**: React, Vite, Tailwind CSS (Premium Design System)
- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Database**: PostgreSQL with pgvector
- **Async Processing**: Celery, Redis
- **Storage**: MinIO (S3 compatible)
- **ML**: Sentence Transformers, PyTorch (Docker mode only)

## Optional Configuration

### External AI Detection APIs
To use external APIs for more accurate AI detection, edit `backend/.env.docker`:

```bash
# Enable external AI detection
USE_EXTERNAL_AI_DETECTION=true

# Add your OpenAI API key
OPENAI_API_KEY=sk-your-api-key-here
```

**Benefits of External APIs:**
- Higher accuracy for AI detection
- Support for latest AI models
- No need to download large model files

### Archive Support
The system automatically detects and extracts these formats:
- `.zip` - Standard ZIP archives
- `.tar` - TAR archives  
- `.tar.gz`, `.tgz` - Gzip-compressed TAR
- `.tar.bz2`, `.tbz2` - Bzip2-compressed TAR

Simply upload archives, and all text files inside will be extracted and analyzed.

## API Documentation

Once running, visit `http://localhost:8000/docs` for the interactive Swagger UI documentation.

### Key Endpoints
- `POST /api/v1/documents/upload?analysis_type=plagiarism|ai|both`: Upload documents or archives for analysis.
- `GET /api/v1/batch/{id}/results`: Get analysis results.
- `POST /api/v1/auth/register`: Create a new account.
- `POST /api/v1/ai-check`: Check text for AI-generated content.
