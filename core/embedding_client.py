from typing import List
from sentence_transformers import SentenceTransformer


class EmbeddingClient:
    def __init__(self, model: str = "all-MiniLM-L6-v2"):
        print("Loading embedding model...")
        self.model = SentenceTransformer(model)
        print("Embedding model loaded.")

    def embed_text(self, text: str) -> List[float]:
        if not text.strip():
            raise ValueError("Input text cannot be empty.")
        return self.model.encode(text).tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            raise ValueError("Text list cannot be empty.")
        return self.model.encode(texts).tolist()