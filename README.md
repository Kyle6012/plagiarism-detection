# Plagiarism Detection System

A powerful plagiarism and AI-generated content detection system that helps identify potential plagiarism and detect AI-generated text in a variety of file formats, including text documents and images. Built using Flask, SQLite, and advanced AI models, this tool provides a simple and efficient way to ensure the integrity of written content.

## Features

- **Text Plagiarism Detection**: Upload and analyze text files (.txt, .docx, .pdf) to detect similarities with previously uploaded documents.
- **Image Plagiarism Detection**: Upload image files (.jpeg, .png, .jpg) to compare with stored image embeddings for similarity.
- **AI-Generated Text Detection**: Detect AI-generated content in text using advanced AI models.
- **Web Interface**: Simple and user-friendly web interface for easy interaction with the system.
- **SQLite Database**: Stores document and image embeddings for comparison and similarity detection.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [License](#license)

## Technologies Used

- **Flask**: Web framework for building the backend API and front-end views.
- **SQLite**: Lightweight relational database for storing document and image embeddings.
- **NumPy**: Used for handling image and document embeddings.
- **AI Models**: Pre-trained models for detecting AI-generated content.
- **Jinja2**: Templating engine for rendering HTML pages.

## Installation

To set up the plagiarism detection system locally, follow the steps below.

### Prerequisites

- Python 3.12+
- Virtual Environment (recommended)
- SQLite3 (already included with Python)

### Step-by-Step Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Kyle6012/plagiarism-detection.git
   cd plagiarism-detection

2. **Set up a virtual environment**:
    ```
    python3 -m venv venv
    source venv/bin/activate
    venv\Scripts\activate # On Windows 
    ```
    
3. **Install dependencies**:
    ```
    pip install -r requirements.txt
    ```

4. **Create the SQLite database(if not already created): The database will automatically be created when the appliaction runs for the first time , but you can manually set any other database:
```
sqlite3 plagiarism_detection.db < schema.sql
```
5. **Run application**:
    ```
    flask run 
    # or 
    python3 app.py
    ```

6. **Access the system**:
    Open your browser and go to http://localhost:5000.
    
## Usage
Once the application is running you can interact with the following features:

1. *Home Page*: Welcome message and a button to get started.
2. *File Upload*: Upload text or image files to be processed for plagiarism detection.
        . **Text Files**: Supported formats: ``.txt``, ``.docx``, ``.pdf``
        . **Image Files**: Supported formats: ``.jpeg``, ``png``, ``jpg``
3. *Compare Files*: Upload a file and compare it against a dataset to calculate           similarity scores.
4. *AI Detection*: The uploaded files runs through ai detection to detect if content is ai generated.

## API Endpoints
### 1. POST /upload
**Purpose**: Upload a filefor processing.
**Request**:
    ``file``: The file to be uploaded (txt,jpg, etc).
**Response**
    . Success: ``{"message": "Text file processed and saved."}`` or ``{"message": "Image file processed and saved."}``.
    . Error: ``{"error": "Unsupported Format."}``.
    
### 2. POST /compare
**Purpose**: Upload a file to compare against stored documents/images.
**Request**:
    . ``file`` to be compared.
**Response**:
    . Similarity results for text or image comparison:
        ```
        {
            "simalarities": [0.92,0.87,0.70],
            "labels": ["Document 1", "Document 2","Document 3", "Document 3"]
        }
        ```

### 3. POST /detect-ai
**Purpose**: Submit text to detect AI-generated content.
**Request**:
    . ``text``: The text to analyze.
**Response**:
    . AI-generated probability score
        ```
        {
            "ai_generated_probability": 0.78
        }
        ```


