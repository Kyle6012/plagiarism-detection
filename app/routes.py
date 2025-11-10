from flask import request, jsonify, render_template, Blueprint
import os
import sqlite3
import numpy as np
import chardet
import docx
from PyPDF2 import PdfReader
from modules.db_operations import insert_document, insert_image, initialize_database
from modules.nlp_module import TextSimilarityAnalyzer
from modules.cv_module import ImageAnalyzer
from modules.ai_detection import load_ai_detection_model, detect_ai_generated_text

bp = Blueprint('main', __name__)

UPLOAD_FOLDER = "uploads"
TOKENIZER, MODEL = load_ai_detection_model()

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

similarity_analyzer = TextSimilarityAnalyzer()
image_analyzer = ImageAnalyzer()
initialize_database()

def read_file_content(file_path):
    if file_path.endswith(".pdf"):
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            return "".join(page.extract_text() for page in reader.pages)
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        with open(file_path, "rb") as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding'] if result['encoding'] else 'utf-8'
        return raw_data.decode(encoding, errors='ignore')

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/analyze", methods=["GET", "POST"])
def analyze_file():
    if request.method == "GET":
        return render_template("upload.html")

    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file provided."}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    response_data = {}

    if file.filename.endswith((".txt", ".docx", ".pdf")):
        content = read_file_content(file_path)

        # Insert document into database
        embedding = similarity_analyzer.get_embedding(content).numpy().tobytes()
        insert_document(content, embedding)

        # Analyze similarity against existing documents
        with sqlite3.connect("plagiarism_detection.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT content FROM documents")
            documents = [doc[0] for doc in cursor.fetchall()]

        similarities = [similarity_analyzer.analyze_text_similarity(content, doc) for doc in documents]
        labels = [f"Document {i+1}" for i in range(len(documents))]

        # Detect AI-generated text
        ai_score = detect_ai_generated_text(content, TOKENIZER, MODEL)

        response_data = {
            "message": "Text file processed.",
            "similarities": similarities,
            "labels": labels,
            "ai_generated_probability": float(ai_score),
        }

    elif file.filename.endswith((".jpeg", ".png", ".jpg")):
        embedding = image_analyzer.extract_image_features(file_path)
        insert_image(file.filename, embedding.tobytes())

        # Compare against existing images
        with sqlite3.connect("plagiarism_detection.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT embedding FROM images")
            images = [np.frombuffer(row[0], dtype=np.float32) for row in cursor.fetchall()]

        similarities = [1 - np.linalg.norm(embedding - img) for img in images]
        labels = [f"Image {i+1}" for i in range(len(images))]

        response_data = {
            "message": "Image file processed.",
            "similarities": similarities,
            "labels": labels,
        }

    else:
        return jsonify({"error": "Unsupported file format."}), 400

    return jsonify(response_data)
