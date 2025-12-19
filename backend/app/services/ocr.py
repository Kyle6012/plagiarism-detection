import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os
from typing import List

class OCRService:
    """Service for Optical Character Recognition (OCR)"""

    @staticmethod
    def extract_text_from_image(image_path: str) -> str:
        """
        Extract text from an image file using Tesseract OCR.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Extracted text string
        """
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"Error extracting text from image {image_path}: {e}")
            return ""

    @staticmethod
    def extract_text_from_scanned_pdf(pdf_path: str) -> str:
        """
        Extract text from a scanned PDF by converting pages to images and running OCR.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text string from all pages
        """
        try:
            # Convert PDF pages to images
            images = convert_from_path(pdf_path)
            
            full_text = []
            for i, image in enumerate(images):
                text = pytesseract.image_to_string(image)
                full_text.append(text)
                
            return "\n\n".join(full_text)
        except Exception as e:
            print(f"Error extracting text from scanned PDF {pdf_path}: {e}")
            return ""

    @staticmethod
    def is_image(filename: str) -> bool:
        """Check if file is a supported image format"""
        ext = os.path.splitext(filename)[1].lower()
        return ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']
