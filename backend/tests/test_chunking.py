import pytest
import numpy as np
from app.services.embedding import EmbeddingService
from app.services.ai_detection import AIDetectionService
from unittest.mock import MagicMock, patch

def test_embedding_chunking():
    service = EmbeddingService()
    text = "This is a long text that should be chunked. " * 20
    chunks = service.chunk_text(text, chunk_size=100, overlap=20)
    assert len(chunks) > 1
    assert all(len(c) <= 100 for c in chunks)

@patch('app.services.embedding.HAS_MODEL', False)
def test_generate_text_embedding_with_chunking():
    service = EmbeddingService()
    mock_model = MagicMock()
    # Mock encode to return a 384-dim vector
    mock_model.encode.return_value = np.zeros(384)
    service.model = mock_model
    
    text = "This is a long text. " * 50
    embedding = service.generate_text_embedding(text)
    
    assert len(embedding) == 384
    assert mock_model.encode.call_count > 1

def test_ai_detection_chunking():
    service = AIDetectionService()
    mock_classifier = MagicMock()
    mock_classifier.return_value = [{'label': 'Fake', 'score': 0.9}]
    service.classifier = mock_classifier
    service.enabled = True
    
    text = "This is a long AI text. " * 100
    result = service.detect(text)
    
    assert result['is_ai'] is True
    assert "chunks analyzed" in result['message']
    assert mock_classifier.call_count > 1
