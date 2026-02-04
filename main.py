"""
Secure RAG Researcher
A retrieval-augmented generation system for querying private documents
using vector embeddings and LLM integration.
"""

import os
import re
import sys
from pathlib import Path
from typing import Optional
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA


class SecureRAGResearcher:
    """Main class for document Q&A using RAG architecture."""
    
    def __init__(
        self,
        pdf_path: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        model_name: str = "gpt-4o",
        temperature: float = 0,
        vectorstore_path: Optional[str] = None,
        enable_pii_detection: bool = False
    ):
        """
        Initialize the RAG researcher.
        
        Args:
            pdf_path: Path to the PDF document
            chunk_size: Size of text chunks for splitting
            chunk_overlap: Overlap between chunks to preserve context
            model_name: OpenAI model to use
            temperature: LLM temperature (0 = deterministic)
            vectorstore_path: Optional path to save/load FAISS index
            enable_pii_detection: Enable PII pattern detection in responses
        """
        self.pdf_path = pdf_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.model_name = model_name
        self.temperature = temperature
        self.vectorstore_path = vectorstore_path or "./vectorstore"
        self.enable_pii_detection = enable_pii_detection
        
        self.vectorstore = None
        self.qa_chain = None
        
        self._validate_environment()
    
    def _validate_environment(self):
        """Validate required environment variables and files."""
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "OPENAI_API_KEY environment variable not set. "
                "Please set it before running."
            )
        
        if not Path(self.pdf_path).exists():
            raise FileNotFoundError(f"PDF file not found: {self.pdf_path}")
    
    def load_and_process_document(self) -> list:
        """
        Load PDF and split into chunks.
        
        Returns:
            List of document chunks
        """
        print(f"Loading document: {self.pdf_path}")
        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()
        
        print(f"Splitting into chunks (size={self.chunk_size}, overlap={self.chunk_overlap})")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        chunks = text_splitter.split_documents(documents)
        
        print(f"Created {len(chunks)} chunks from {len(documents)} pages")
        return chunks
    
    def create_vectorstore(self, chunks: list, force_recreate: bool = False):
        """
        Create or load FAISS vector store.
        
        Args:
            chunks: Document chunks to embed
            force_recreate: If True, recreate even if vectorstore exists
        """
        vectorstore_exists = Path(self.vectorstore_path).exists()
        
        if vectorstore_exists and not force_recreate:
            print(f"Loading existing vectorstore from {self.vectorstore_path}")
            embeddings = OpenAIEmbeddings()
            self.vectorstore = FAISS.load_local(
                self.vectorstore_path, 
                embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            print("Creating embeddings and building vector index...")
            embeddings = OpenAIEmbeddings()
            self.vectorstore = FAISS.from_documents(chunks, embeddings)
            
            print(f"Saving vectorstore to {self.vectorstore_path}")
            self.vectorstore.save_local(self.vectorstore_path)
        
        print("Vectorstore ready")
    
    def setup_qa_chain(self):
        """Initialize the retrieval QA chain."""
        if not self.vectorstore:
            raise ValueError("Vectorstore not initialized. Call create_vectorstore first.")
        
        print(f"Setting up QA chain with {self.model_name}")
        llm = ChatOpenAI(
            model_name=self.model_name,
            temperature=self.temperature
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 4}  # Retrieve top 4 most relevant chunks
            ),
            return_source_documents=True
        )
        
        print("QA chain ready")
    
    def scan_for_secrets(self, documents: list) -> list:
        """
        Scans retrieved document chunks for potential PII or secrets.
        
        This is an optional security feature that can detect common PII patterns
        in retrieved chunks. Useful for compliance logging and audit trails.
        
        Args:
            documents: List of LangChain Document objects
            
        Returns:
            List of security findings (unique alerts)
        """
        if not self.enable_pii_detection:
            return []
        
        findings = []
        
        # Common PII and secret patterns
        patterns = {
            "Email Address": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "SSN": r'\b\d{3}-\d{2}-\d{4}\b',
            "Credit Card": r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
            "API Key Pattern": r'(?:api[_-]?key|apikey|api[_-]?secret)[\s:="\']([a-zA-Z0-9_\-]{20,})',
            "AWS Access Key": r'\b(AKIA[0-9A-Z]{16})\b',
            "Phone Number": r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
            "IP Address": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        }
        
        for doc in documents:
            for label, pattern in patterns.items():
                matches = re.findall(pattern, doc.page_content, re.IGNORECASE)
                if matches:
                    # Only log the pattern type, not the actual data
                    findings.append(f"{label} pattern detected in source chunk")
        
        # Return unique findings only
        return list(set(findings))
    
    def query(self, question: str) -> dict:
        """
        Query the document with a question.
        
        Args:
            question: Natural language question
            
        Returns:
            Dictionary with 'result', 'source_documents', and optionally 'security_alerts'
        """
        if not self.qa_chain:
            raise ValueError("QA chain not initialized. Call setup_qa_chain first.")
        
        print(f"\nQuery: {question}")
        response = self.qa_chain.invoke({"query": question})
        
        # Optional PII detection
        if self.enable_pii_detection:
            security_findings = self.scan_for_secrets(response['source_documents'])
            if security_findings:
                response['security_alerts'] = security_findings
                print("\nSecurity Alerts:")
                for alert in security_findings:
                    print(f"   {alert}")
        
        return response
    
    def initialize(self, force_recreate: bool = False):
        """
        Full initialization pipeline.
        
        Args:
            force_recreate: If True, recreate vectorstore even if it exists
        """
        chunks = self.load_and_process_document()
        self.create_vectorstore(chunks, force_recreate=force_recreate)
        self.setup_qa_chain()
        print("\nSystem initialized and ready for queries!\n")


def main():
    """Main entry point for the application."""
    # Configuration
    PDF_PATH = "sample_security_policy.pdf"
    
    try:
        # Initialize the researcher
        researcher = SecureRAGResearcher(
            pdf_path=PDF_PATH,
            chunk_size=1000,
            chunk_overlap=200,
            model_name="gpt-4o",
            temperature=0,
            enable_pii_detection=False  # Set to True to enable PII detection
        )
        
        # Initialize the system (will reuse vectorstore if it exists)
        researcher.initialize(force_recreate=False)
        
        # Example queries
        queries = [
            "What are the specific PII handling requirements mentioned in section 4?",
            "What encryption standards are required for data at rest?",
            "How long should security logs be retained?"
        ]
        
        for query in queries:
            response = researcher.query(query)
            print(f"Answer: {response['result']}\n")
            print(f"Sources: {len(response['source_documents'])} relevant chunks found")
            
            # Show security alerts if PII detection is enabled
            if 'security_alerts' in response:
                print(f"Security: {len(response['security_alerts'])} alert(s)")
            
            print("-" * 80 + "\n")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
