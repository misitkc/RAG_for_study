"""FAISS vector store management."""

import os
import json
from typing import List, Dict, Tuple
import numpy as np
import faiss

from utils.embeddings_handler import EmbeddingsHandler
from config import VECTOR_STORE_PATH, METADATA_PATH


class VectorStore:
    """Manage FAISS vector store with metadata."""

    def __init__(self):
        """Initialize vector store handler."""
        self.embeddings_handler = EmbeddingsHandler()
        self.index = None
        self.metadata = []
        self.index_path = VECTOR_STORE_PATH
        self.metadata_path = METADATA_PATH
        self._load_existing_index()

    def _load_existing_index(self):
        """Load existing FAISS index and metadata if they exist."""
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)

        if os.path.exists(self.index_path):
            try:
                self.index = faiss.read_index(self.index_path)
                if os.path.exists(self.metadata_path):
                    with open(self.metadata_path, "r") as f:
                        self.metadata = json.load(f)
            except Exception as e:
                print(f"Error loading existing index: {e}")
                self.index = None
                self.metadata = []

    def add_chunks(self, chunks: List[Dict]) -> None:
        """
        Add document chunks to the vector store.

        Args:
            chunks: List of chunk dictionaries with 'text' key
        """
        if not chunks:
            return

        # Extract texts
        texts = [chunk["text"] for chunk in chunks]

        # Generate embeddings
        embeddings = self.embeddings_handler.embed_texts(texts)

        # Convert to float32 for FAISS
        embeddings = embeddings.astype(np.float32)

        # Initialize or add to index
        if self.index is None:
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)

        self.index.add(embeddings)

        # Store metadata
        self.metadata.extend(chunks)

        # Save index and metadata
        self._save_index()

    def search(self, query: str, top_k: int = 4) -> List[Dict]:
        """
        Search for relevant chunks.

        Args:
            query: Query text
            top_k: Number of results to return

        Returns:
            List of relevant chunks with metadata
        """
        if self.index is None or not self.metadata:
            return []

        # Embed query
        query_embedding = self.embeddings_handler.embed_single(query)
        query_embedding = query_embedding.astype(np.float32).reshape(1, -1)

        # Search
        distances, indices = self.index.search(query_embedding, min(top_k, len(self.metadata)))

        # Retrieve metadata
        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                chunk = self.metadata[int(idx)].copy()
                results.append(chunk)

        return results

    def clear_index(self) -> None:
        """Clear the vector store."""
        self.index = None
        self.metadata = []
        self._save_index()

    def _save_index(self) -> None:
        """Save index and metadata to disk."""
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)

        if self.index is not None:
            faiss.write_index(self.index, self.index_path)

        with open(self.metadata_path, "w") as f:
            json.dump(self.metadata, f)

    def get_total_chunks(self) -> int:
        """Get total number of chunks in the store."""
        return len(self.metadata) if self.metadata else 0

    def get_documents_info(self) -> Dict[str, int]:
        """Get information about documents in the store."""
        docs = {}
        for chunk in self.metadata:
            source = chunk.get("source", "Unknown")
            docs[source] = docs.get(source, 0) + 1
        return docs
