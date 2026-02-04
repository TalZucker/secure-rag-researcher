"""
Configuration settings for Secure RAG Researcher
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"

# Document settings
PDF_PATH = DATA_DIR / "sample_security_policy.pdf"

# Chunking strategy
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Model settings
OPENAI_MODEL = "gpt-4o"
TEMPERATURE = 0  # 0 for deterministic, higher for creative
RETRIEVAL_TOP_K = 4  # Number of chunks to retrieve per query

# OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Vectorstore settings
VECTORSTORE_TYPE = "FAISS"  # Local vector database
SAVE_VECTORSTORE = True
VECTORSTORE_PATH = str(VECTORSTORE_DIR)

# Security features
ENABLE_PII_DETECTION = False  # Set to True to scan for PII patterns in responses

# Alternative: Use local embeddings for fully air-gapped operation
# Uncomment to use sentence-transformers instead of OpenAI embeddings
# USE_LOCAL_EMBEDDINGS = True
# LOCAL_EMBEDDING_MODEL = "all-MiniLM-L6-v2"
