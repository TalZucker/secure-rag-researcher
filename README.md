# 🔒 Secure RAG Researcher

A production-ready Retrieval-Augmented Generation (RAG) system for querying private documents using vector embeddings and GPT-4. Built with LangChain, FAISS, and OpenAI APIs.

## 🎯 Overview

This project demonstrates a complete RAG pipeline that:
- Loads and processes PDF documents
- Chunks text strategically to preserve context
- Creates vector embeddings for semantic search
- Stores embeddings in a local FAISS index
- Enables natural language Q&A over document content
- Returns answers grounded in source material

**Perfect for**: Internal documentation, security policies, research papers, technical whitepapers, and enterprise knowledge bases.

## 🏗️ Architecture

```
PDF Document → Text Chunking → Vector Embeddings → FAISS Index
                                                        ↓
User Query → Vector Search → Relevant Chunks → GPT-4 → Answer
```

**Key Components:**
- **Document Loader**: PyPDFLoader for PDF parsing
- **Text Splitter**: Recursive character splitting with overlap
- **Embeddings**: OpenAI's text-embedding-ada-002
- **Vector Store**: FAISS (Facebook AI Similarity Search) - runs locally
- **LLM**: GPT-4o for answer generation
- **Chain**: RetrievalQA with "stuff" strategy

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/secure-rag-researcher.git
cd secure-rag-researcher
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

5. **Add your document**
```bash
mkdir -p data
# Place your PDF in data/sample_security_policy.pdf
# Or use the provided sample document
```

### Usage

**Basic usage:**
```bash
python main.py
```

**Interactive usage:**
```python
from main import SecureRAGResearcher

# Initialize
researcher = SecureRAGResearcher(
    pdf_path="data/your_document.pdf",
    chunk_size=1000,
    chunk_overlap=200
)

# Setup (first time will create vectorstore, subsequent runs will load it)
researcher.initialize()

# Query
response = researcher.query("What are the PII handling requirements?")
print(response['result'])
```

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Chunking strategy
CHUNK_SIZE = 1000        # Size of each text chunk
CHUNK_OVERLAP = 200      # Overlap to preserve context

# Model settings
OPENAI_MODEL = "gpt-4o"  # Or "gpt-3.5-turbo" for cost savings
TEMPERATURE = 0          # 0 = deterministic, higher = creative
RETRIEVAL_TOP_K = 4      # Number of chunks to retrieve

# Security features
ENABLE_PII_DETECTION = False  # Enable PII pattern scanning
```

## 🔐 Security Features

- **Local Vector Storage**: FAISS runs entirely on your machine
- **No Data Leakage**: Documents are chunked and embedded locally
- **API Key Protection**: Environment variables kept out of version control
- **Optional PII Detection**: Scan responses for common PII patterns (emails, SSNs, credit cards, etc.)
- **Secure by Design**: Only query results sent to OpenAI, not full documents

**Note**: OpenAI API calls do send text chunks for embedding and LLM processing. For fully air-gapped operation, consider using local models (Ollama, LLaMA) instead.

### PII Detection

Enable optional PII pattern detection to scan retrieved document chunks:

```python
researcher = SecureRAGResearcher(
    pdf_path="data/your_document.pdf",
    enable_pii_detection=True  # Enables security scanning
)
```

When enabled, the system will detect and alert on patterns like:
- Email addresses
- Social Security Numbers
- Credit card numbers
- API keys
- Phone numbers
- IP addresses

This is useful for compliance logging and audit trails in regulated environments.

## 🧠 Key Engineering Decisions

- 200-token overlap prevents context loss at chunk boundaries
- FAISS persistence avoids re-embedding on every run
- "Stuff" chain type for simplicity (suitable for <4k tokens of context)
- Temperature=0 for consistent, factual responses

## 📝 License

MIT License - feel free to use for personal or commercial projects

## 🤝 Contributing

This is a portfolio project, but suggestions and improvements are welcome!

## 📧 Contact

Tal Zucker - talzucker99@gmail.com

Project Link: [https://github.com/TalZucker/secure-rag-researcher](https://github.com/yourusername/secure-rag-researcher)

---

**Built with**: LangChain • OpenAI • FAISS • Python
