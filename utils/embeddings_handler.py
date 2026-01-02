"""Embeddings generation and management."""

from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np
import streamlit as st

from config import EMBEDDING_MODEL


class EmbeddingsHandler:
    """Handle text embeddings using HuggingFace models."""

    def __init__(self):
        """Initialize the embeddings model."""
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Embed a list of texts.

        Args:
            texts: List of text strings

        Returns:
            NumPy array of embeddings
        """
        embeddings = self.model.encode(texts, show_progress_bar=False)
        return embeddings

    def embed_single(self, text: str) -> np.ndarray:
        """
        Embed a single text.

        Args:
            text: Text string

        Returns:
            NumPy array of embedding
        """
        embedding = self.model.encode(text, show_progress_bar=False)
        return embedding

    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embeddings."""
        return self.embedding_dim
