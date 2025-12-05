"""
Embedding Service.

Handles generation of embeddings for text using Sentence Transformers
or OpenAI embeddings.
"""
from typing import List
from backend.config.settings import settings

class EmbeddingService:
    """Service to generate embeddings for text."""
    
    def __init__(self):
        self.provider = "sentence-transformers" # Default for local dev
        self._model = None

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query string."""
        return self.embed_documents([text])[0]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents."""
        if not self._model:
            self._load_model()
            
        if self.provider == "sentence-transformers":
            embeddings = self._model.encode(texts)
            return embeddings.tolist()
        
        return []

    def _load_model(self):
        """Lazy load the embedding model."""
        try:
            from sentence_transformers import SentenceTransformer
            # Use a small, fast model for default
            self._model = SentenceTransformer('all-MiniLM-L6-v2')
        except ImportError:
            raise ImportError(
                "sentence-transformers not installed. "
                "Install with `pip install sentence-transformers`"
            )
