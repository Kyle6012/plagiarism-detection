from fastapi import UploadFile
from pdfminer.high_level import extract_text
import docx
import io

async def extract_text_from_file(file: UploadFile) -> str:
    """
    Extracts text from a file, supporting .txt, .docx, and .pdf formats.
    """
    content = await file.read()

    if file.filename.endswith(".docx"):
        doc = docx.Document(io.BytesIO(content))
        return " ".join([para.text for para in doc.paragraphs])
    elif file.filename.endswith(".pdf"):
        return extract_text(io.BytesIO(content))
    elif file.filename.endswith(".txt"):
        return content.decode("utf-8")
    else:
        # For other file types, attempt to decode as utf-8, but this may fail
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            return ""
