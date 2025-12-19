import asyncio
import io
from fastapi import UploadFile
from app.services.parsing import extract_text_from_file
from PIL import Image, ImageDraw, ImageFont

async def test_ocr():
    # Create a dummy image with text
    img = Image.new('RGB', (400, 200), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((10, 10), "Hello OCR World", fill=(0, 0, 0))
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    # Mock UploadFile
    mock_file = UploadFile(
        filename="test_image.png",
        file=img_byte_arr
    )
    
    # Read content as the service expects
    content = img_byte_arr.getvalue()
    
    print("Testing OCR extraction...")
    # We need to mock the content reading in extract_text_from_file or just call it
    # Since extract_text_from_file calls await file.read(), we need to ensure it works
    
    # Actually, let's just test the logic inside parsing.py if possible or mock the file object
    text = await extract_text_from_file(mock_file)
    print(f"Extracted Text: '{text.strip()}'")
    
    if "Hello OCR World" in text:
        print("✅ OCR Test Passed!")
    else:
        print("❌ OCR Test Failed!")

if __name__ == "__main__":
    asyncio.run(test_ocr())
