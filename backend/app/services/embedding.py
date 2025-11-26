import os
import hashlib

try:
    from sentence_transformers import SentenceTransformer
    HAS_MODEL = True
except ImportError:
    HAS_MODEL = False

class EmbeddingService:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        if HAS_MODEL and not os.getenv("VERCEL"):
            self.model = SentenceTransformer(model_name)
        else:
            self.model = None

    def generate_text_embedding(self, text):
        if self.model:
            return self.model.encode(text)
        # Fallback for Vercel or when model is missing: return empty list or zeros
        # This effectively disables semantic search but allows the app to boot
        return []

    @staticmethod
    def hash_content(content):
        return hashlib.sha256(content.encode()).hexdigest()
