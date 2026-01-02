"""Configuration settings for the RAG application."""

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Embeddings Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # HuggingFace model

# Vector Store Configuration
VECTOR_STORE_PATH = "data/faiss_index"
METADATA_PATH = "data/metadata.json"

# Document Processing Configuration
CHUNK_SIZE = 1000  # Characters per chunk
CHUNK_OVERLAP = 200  # Overlap between chunks
MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50MB max file size

# RAG Configuration
TOP_K_RESULTS = 4  # Number of chunks to retrieve
TEMPERATURE = 0.3  # Lower for more consistent answers

# UI Configuration
PAGE_TITLE = "Study RAG Assistant"
PAGE_ICON = "📚"

# Validate configuration
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please create a .env file.")
