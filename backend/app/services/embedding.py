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

    def chunk_text(self, text, chunk_size=500, overlap=50):
        """Split text into overlapping chunks"""
        if not text:
            return []
        chunks = []
        for i in range(0, len(text), chunk_size - overlap):
            chunks.append(text[i:i + chunk_size])
            if i + chunk_size >= len(text):
                break
        return chunks

    def generate_text_embedding(self, text):
        if not self.model:
            return []
        
        # For long texts, we chunk and average the embeddings
        # This is a simplified approach for a single document embedding
        chunks = self.chunk_text(text)
        if not chunks:
            return []
            
        import numpy as np
        embeddings = [self.model.encode(chunk) for chunk in chunks]
        avg_embedding = np.mean(embeddings, axis=0)
        return avg_embedding.tolist()

    @staticmethod
    def hash_content(content):
        return hashlib.sha256(content.encode()).hexdigest()
