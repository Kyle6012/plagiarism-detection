# 🛡️ Plagiarism & AI Detection System

A powerful, open-source plagiarism and AI-generated content detection system featuring a premium, modern UI and flexible deployment options. Designed for both coders and non-coders to use on any platform.

---

## 🌟 Features

- **Premium UI**: Modern, responsive interface with glassmorphism, dark mode, and smooth animations.
- **Semantic Plagiarism Detection**: Uses `pgvector` and `sentence-transformers` to detect similarities based on meaning, not just exact word matches.
- **AI-Generated Text Detection**: Detects content from GPT-3, GPT-4, and other models using local HuggingFace models, OpenAI's API, or **Together API**.
- **Smart Text Chunking**: Automatically splits long documents into overlapping chunks to ensure accurate analysis of large files.
- **Archive & Folder Support**: Upload `.zip`, `.tar`, or entire folders. The system extracts and filters relevant text files automatically.
- **Multi-Platform Support**: Runs anywhere Docker is available (Windows, macOS, Linux).
- **Lite Mode**: Optimized for Vercel/Serverless deployments (ML models disabled).

---

## 🚀 Quick Start Guide (For Everyone)

This guide is designed to get you up and running in minutes, regardless of your technical background.

### 1. Install Docker (One-time setup)
Docker is the engine that runs the application. Think of it like a "virtual machine" that contains everything the app needs.

- **Windows**: Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/). Ensure "WSL 2" is enabled during installation.
- **macOS**: Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
- **Linux**: Follow the [official Docker installation guide](https://docs.docker.com/engine/install/).

### 2. Get the Code
- **Coders**: `git clone https://github.com/Kyle6012/plagiarism-detection.git`
- **Non-Coders**: Click the green **"Code"** button at the top of this page and select **"Download ZIP"**. Extract the ZIP file to a folder on your computer.

### 3. Launch the App
1.  Open your terminal (Command Prompt/PowerShell on Windows, Terminal on Mac/Linux).
2.  Navigate to the project folder: `cd plagiarism-detection`
3.  Run the magic command:
    ```bash
    docker-compose up --build -d
    ```
4.  Wait a few minutes for the first-time setup. Once finished, open your browser to:
    👉 **[http://localhost:80](http://localhost:80)**

---

## 📊 Project Implementation Status

| Feature | Status | Notes |
| :--- | :--- | :--- |
| **Semantic Search** | ✅ Implemented | Uses `pgvector` with Cosine Similarity. |
| **AI Detection (Local)** | ✅ Implemented | Uses `roberta-base-openai-detector`. |
| **AI Detection (OpenAI/Together)** | ✅ Implemented | Optional; requires `OPENAI_API_KEY` or `TOGETHER_API_KEY`. |
| **Text Chunking** | ✅ Implemented | Handles long documents via overlapping chunks. |
| **Archive Extraction** | ✅ Implemented | Supports `.zip`, `.tar`, `.tar.gz`, `.tar.bz2`. |
| **File Parsing** | ✅ Implemented | Supports `.txt`, `.pdf`, `.docx`. |
| **User Auth** | ✅ Implemented | JWT-based authentication with registration. |
| **Dashboard** | ✅ Implemented | Basic stats for user batches and documents. |
| **Premium UI** | ✅ Implemented | Glassmorphism design with progress bars. |
| **OCR Support** | ✅ Implemented | Uses Tesseract for images and scanned PDFs. |
| **Export Results** | ✅ Implemented | PDF and CSV export of analysis. |
| **Admin Panel** | ✅ Implemented | System stats and management. |

## 🔮 Future Features

- **OCR Support**: Analyze text from images and scanned PDFs using Tesseract.
- **Export Results**: Download analysis reports in PDF or CSV format.
- **Admin Panel**: Manage users, view system stats, and configure settings.
- **Advanced Analytics**: Deeper insights into plagiarism trends and AI usage.
- **Multi-Language Support**: Expanded support for non-English languages.

---

## 🛠️ Developer Guide

### Tech Stack
- **Frontend**: React 18, Vite, Vanilla CSS (Custom Design System)
- **Backend**: FastAPI (Python 3.11+), SQLAlchemy 2.0
- **Database**: PostgreSQL 15 + `pgvector`
- **Task Queue**: Celery + Redis
- **Storage**: MinIO (S3 Compatible)

### Environment Variables
Edit `backend/.env.docker` to customize your installation:
- `USE_EXTERNAL_AI_DETECTION`: Set to `true` to use OpenAI or Together API.
- `OPENAI_API_KEY`: Your OpenAI key for enhanced detection.
- `TOGETHER_API_KEY`: Your Together API key (alternative to OpenAI).
- `S3_BUCKET_NAME`: Name of the storage bucket.

### Running Tests
```bash
# Backend tests
docker-compose exec api pytest backend/tests
```

---

## 📄 License

This project is open-source and available under the MIT License. Use it, modify it, and share it!

---

*Need help? Open an issue on GitHub or check the [API Documentation](http://localhost:8000/docs) when the app is running.*
