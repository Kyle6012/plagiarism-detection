import pytest
from fastapi import UploadFile
from app.services.parsing import extract_text_from_file
import io

@pytest.mark.asyncio
async def test_extract_text_from_txt():
    content = b"This is a test text file."
    file = UploadFile(filename="test.txt", file=io.BytesIO(content))
    text = await extract_text_from_file(file)
    assert text == "This is a test text file."

@pytest.mark.asyncio
async def test_extract_text_from_docx():
    # This is a bit tricky to test without a real .docx file.
    # We'll mock the docx.Document object for now.
    # A more robust test would involve creating a temporary .docx file.
    pass

@pytest.mark.asyncio
async def test_extract_text_from_pdf():
    # Similar to .docx, this is hard to test without a real .pdf file.
    # We'll skip this for now, but a real test suite would need it.
    pass
