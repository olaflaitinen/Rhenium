"""
ChromaDB Vector Store Implementation.
"""
import uuid
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings

from backend.semantic.interface import VectorStore
from backend.semantic.embeddings import EmbeddingService
from backend.config.settings import settings

class ChromaVectorStore(VectorStore):
    """ChromaDB implementation of VectorStore."""

    def __init__(self, collection_name: str = "schema_metadata"):
        self.client = chromadb.PersistentClient(path="./data/chroma_db")
        self.embedding_service = EmbeddingService()
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_texts(
        self, 
        texts: List[str], 
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """Add texts to ChromaDB."""
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in texts]
            
        # Generate embeddings
        embeddings = self.embedding_service.embed_documents(texts)
        
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        return ids

    def similarity_search(
        self, 
        query: str, 
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        query_embedding = self.embedding_service.embed_query(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where=filter
        )
        
        # Format results
        formatted_results = []
        if results['documents']:
            for i in range(len(results['documents'][0])):
                doc = results['documents'][0][i]
                meta = results['metadatas'][0][i] if results['metadatas'] else {}
                formatted_results.append({
                    "content": doc,
                    "metadata": meta
                })
                
        return formatted_results

    def delete(self, ids: List[str]) -> bool:
        """Delete documents."""
        self.collection.delete(ids=ids)
        return True
