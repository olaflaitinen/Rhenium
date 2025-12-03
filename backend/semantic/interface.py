"""
Vector Store Interface.

Abstract base class for vector store implementations to support
semantic search over database schema and historical queries.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class VectorStore(ABC):
    """Abstract interface for vector database operations."""

    @abstractmethod
    def add_texts(
        self, 
        texts: List[str], 
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """Add texts to the vector store."""
        pass

    @abstractmethod
    def similarity_search(
        self, 
        query: str, 
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Return documents most similar to the query."""
        pass

    @abstractmethod
    def delete(self, ids: List[str]) -> bool:
        """Delete documents by ID."""
        pass
