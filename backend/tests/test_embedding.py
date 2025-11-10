from app.services.embedding import EmbeddingService

def test_generate_text_embedding():
    service = EmbeddingService()
    embedding = service.generate_text_embedding("This is a test sentence.")
    assert embedding.shape == (384,)

def test_hash_content():
    content = "This is a test sentence."
    hashed_content = EmbeddingService.hash_content(content)
    assert isinstance(hashed_content, str)
    assert len(hashed_content) == 64
