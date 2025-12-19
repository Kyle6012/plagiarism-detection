from fastapi import UploadFile
from pdfminer.high_level import extract_text
import docx
import io
import os
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import tempfile

async def extract_text_from_file(file: UploadFile) -> str:
    """
    Extracts text from a file, supporting .txt, .docx, .pdf, and image formats (.png, .jpg, .jpeg).
    """
    content = await file.read()
    filename = file.filename.lower()

    if filename.endswith(".docx"):
        doc = docx.Document(io.BytesIO(content))
        return " ".join([para.text for para in doc.paragraphs])
    
    elif filename.endswith(".pdf"):
        # Try standard extraction first
        text = extract_text(io.BytesIO(content))
        if len(text.strip()) < 10:  # Likely a scanned PDF
            # Use OCR for scanned PDFs
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp.write(content)
                tmp_path = tmp.name
            
            try:
                images = convert_from_path(tmp_path)
                ocr_text = ""
                for img in images:
                    ocr_text += pytesseract.image_to_string(img)
                return ocr_text
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        return text

    elif filename.endswith((".png", ".jpg", ".jpeg")):
        # Direct OCR for images
        image = Image.open(io.BytesIO(content))
        return pytesseract.image_to_string(image)

    elif filename.endswith(".txt"):
        return content.decode("utf-8")
    
    else:
        # For other file types, attempt to decode as utf-8
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            return ""
