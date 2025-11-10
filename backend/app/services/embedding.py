from sentence_transformers import SentenceTransformer
import hashlib

class EmbeddingService:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def generate_text_embedding(self, text):
        return self.model.encode(text)

    @staticmethod
    def hash_content(content):
        return hashlib.sha256(content.encode()).hexdigest()
