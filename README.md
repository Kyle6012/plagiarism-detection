# Plagiarism Detection System

A powerful plagiarism and AI-generated content detection system that helps identify potential plagiarism and detect AI-generated text in a variety of file formats. This project is a monorepo containing a React frontend and a FastAPI backend.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)

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

## Installation

To set up the plagiarism detection system locally, follow the steps below.

### Prerequisites

- Python 3.12+
- Node.js 18+
- Docker and Docker Compose

### Step-by-Step Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Kyle6012/plagiarism-detection.git
   cd plagiarism-detection
   ```

2. **Backend Setup**:
   ```bash
   cd backend
   poetry install
   ```

3. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   ```

## Usage

### Running the Application

1. **Start the backend server**:
   ```bash
   cd backend
   poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

2. **Start the frontend server**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the system**:
   Open your browser and go to http://localhost:5173.
