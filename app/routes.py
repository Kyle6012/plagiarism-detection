from flask import request, jsonify, render_template, Blueprint
import os
import sqlite3
import numpy as np
import chardet
from modules.db_operations import insert_document, insert_image
from modules.nlp_module import TextSimilarityAnalyzer
from modules.cv_module import ImageAnalyzer  # Updated import for new image analysis class
from modules.ai_detection import load_ai_detection_model, detect_ai_generated_text
from modules.utils import hash_text_content, plot_similarity
from modules.db_operations import initialize_database


bp = Blueprint('main', __name__)

UPLOAD_FOLDER = "uploads"
TOKENIZER, MODEL = load_ai_detection_model()

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Instantiate the text similarity and image analyzer once
similarity_analyzer = TextSimilarityAnalyzer()
image_analyzer = ImageAnalyzer()
initialize_database()
def read_file_content(file_path):
    with open(file_path, "rb") as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding'] if result['encoding'] else 'utf-8'
    return raw_data.decode(encoding, errors='ignore')

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "GET":
        return render_template("upload.html")

    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    similarities = []
    labels = []
    ai_score = None

    # Handling text files
    if file.filename.endswith((".txt", ".docx", ".pdf")):
        content = read_file_content(file_path)
        embedding = hash_text_content(content)
        insert_document(content, embedding)

        # Analyze similarity against existing documents
        with sqlite3.connect("plagiarism_detection.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT content FROM documents")
            documents = cursor.fetchall()

            for i, doc in enumerate(documents):
                similarity = similarity_analyzer.analyze_text_similarity(content, doc[0])
                similarities.append(float(similarity))  # Convert to Python float
                labels.append(f"Document {i + 1}")

        # Run AI detection
        ai_score = detect_ai_generated_text(content, TOKENIZER, MODEL)

        response = {
            "message": "Text file processed and saved.",
            "similarities": similarities,
            "labels": labels,
            "ai_generated_probability": float(ai_score) if isinstance(ai_score, np.float32) else ai_score,
        }

    # Handling image files
    elif file.filename.endswith((".jpeg", ".png", ".jpg")):
        image_hash = image_analyzer.get_image_hash(file_path)
        embedding = image_analyzer.extract_image_features(file_path)
        insert_image(image_hash, embedding.tobytes())

        # Calculate similarities against existing images
        with sqlite3.connect("plagiarism_detection.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT embedding FROM images")
            images = cursor.fetchall()

            for i, img in enumerate(images):
                stored_embedding = np.frombuffer(img[0], dtype=np.float32)
                similarity = 1 - np.linalg.norm(stored_embedding - embedding)
                similarities.append(float(similarity))  # Convert to Python float
                labels.append(f"Image {i + 1}")

        # Placeholder for AI detection applicability on images
        ai_score = detect_ai_generated_text("Image AI analysis placeholder", TOKENIZER, MODEL)
        response = {
            "message": "Image file processed and saved.",
            "similarities": similarities,
            "labels": labels,
            "ai_generated_probability": float(ai_score) if isinstance(ai_score, np.float32) else ai_score,
        }

    else:
        response = {"error": "Unsupported file format."}

    return jsonify(response)

@bp.route("/compare", methods=["POST"])
def compare():
    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    similarities = []
    labels = []

    # Handling text files comparison
    if file.filename.endswith((".txt", ".docx", ".pdf")):
        content = read_file_content(file_path)

        with sqlite3.connect("plagiarism_detection.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT content FROM documents")
            documents = cursor.fetchall()

            for i, doc in enumerate(documents):
                similarity = similarity_analyzer.analyze_text_similarity(content, doc[0])
                similarities.append(similarity)
                labels.append(f"Document {i + 1}")

    # Handling image files comparison
    elif file.filename.endswith((".jpeg", ".png", ".jpg")):
        embedding = image_analyzer.extract_image_features(file_path)
        with sqlite3.connect("plagiarism_detection.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT embedding FROM images")
            images = cursor.fetchall()

            for i, img in enumerate(images):
                stored_embedding = np.frombuffer(img[0], dtype=np.float32)
                similarity = 1 - np.linalg.norm(stored_embedding - embedding)
                similarities.append(similarity)
                labels.append(f"Image {i + 1}")

    else:
        return jsonify({"error": "Unsupported file format."})

    # Optionally plot and return similarities
    plot_similarity(similarities, labels)
    return jsonify({"similarities": similarities})

@bp.route("/detect-ai", methods=["POST"])
def detect_ai_text():
    text = request.form["text"]
    score = detect_ai_generated_text(text, TOKENIZER, MODEL)
    return jsonify({"ai_generated_probability": score})