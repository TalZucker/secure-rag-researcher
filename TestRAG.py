"""
Unit tests for Secure RAG Researcher
Demonstrates testing practices and code quality.
"""

import unittest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from main import SecureRAGResearcher


class TestSecureRAGResearcher(unittest.TestCase):
    """Test cases for SecureRAGResearcher class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_pdf_path = "data/sample_security_policy.pdf"
        os.environ['OPENAI_API_KEY'] = 'test-key-12345'  # Mock API key
    
    def test_initialization_requires_api_key(self):
        """Test that initialization fails without API key."""
        del os.environ['OPENAI_API_KEY']
        
        with self.assertRaises(ValueError) as context:
            SecureRAGResearcher(pdf_path=self.test_pdf_path)
        
        self.assertIn("OPENAI_API_KEY", str(context.exception))
        
        # Restore for other tests
        os.environ['OPENAI_API_KEY'] = 'test-key-12345'
    
    def test_initialization_requires_existing_pdf(self):
        """Test that initialization fails with non-existent PDF."""
        with self.assertRaises(FileNotFoundError):
            SecureRAGResearcher(pdf_path="nonexistent.pdf")
    
    def test_default_parameters(self):
        """Test default parameter values."""
        if Path(self.test_pdf_path).exists():
            researcher = SecureRAGResearcher(pdf_path=self.test_pdf_path)
            
            self.assertEqual(researcher.chunk_size, 1000)
            self.assertEqual(researcher.chunk_overlap, 200)
            self.assertEqual(researcher.model_name, "gpt-4o")
            self.assertEqual(researcher.temperature, 0)
    
    def test_custom_parameters(self):
        """Test custom parameter configuration."""
        if Path(self.test_pdf_path).exists():
            researcher = SecureRAGResearcher(
                pdf_path=self.test_pdf_path,
                chunk_size=500,
                chunk_overlap=100,
                model_name="gpt-3.5-turbo",
                temperature=0.7
            )
            
            self.assertEqual(researcher.chunk_size, 500)
            self.assertEqual(researcher.chunk_overlap, 100)
            self.assertEqual(researcher.model_name, "gpt-3.5-turbo")
            self.assertEqual(researcher.temperature, 0.7)
    
    @patch('main.PyPDFLoader')
    def test_load_and_process_document(self, mock_loader):
        """Test document loading and chunking."""
        # Mock PDF loader
        mock_doc = MagicMock()
        mock_doc.page_content = "Test content " * 100
        mock_loader.return_value.load.return_value = [mock_doc]
        
        if Path(self.test_pdf_path).exists():
            researcher = SecureRAGResearcher(pdf_path=self.test_pdf_path)
            chunks = researcher.load_and_process_document()
            
            self.assertIsInstance(chunks, list)
            self.assertGreater(len(chunks), 0)
    
    def test_qa_chain_requires_vectorstore(self):
        """Test that QA chain setup requires vectorstore."""
        if Path(self.test_pdf_path).exists():
            researcher = SecureRAGResearcher(pdf_path=self.test_pdf_path)
            
            with self.assertRaises(ValueError):
                researcher.setup_qa_chain()
    
    def test_query_requires_qa_chain(self):
        """Test that querying requires initialized QA chain."""
        if Path(self.test_pdf_path).exists():
            researcher = SecureRAGResearcher(pdf_path=self.test_pdf_path)
            
            with self.assertRaises(ValueError):
                researcher.query("test question")
    
    def test_pii_detection_disabled_by_default(self):
        """Test that PII detection is disabled by default."""
        if Path(self.test_pdf_path).exists():
            researcher = SecureRAGResearcher(pdf_path=self.test_pdf_path)
            self.assertEqual(researcher.enable_pii_detection, False)
    
    def test_pii_detection_can_be_enabled(self):
        """Test that PII detection can be enabled."""
        if Path(self.test_pdf_path).exists():
            researcher = SecureRAGResearcher(
                pdf_path=self.test_pdf_path,
                enable_pii_detection=True
            )
            self.assertEqual(researcher.enable_pii_detection, True)
    
    @patch('main.PyPDFLoader')
    def test_scan_for_secrets_detects_email(self, mock_loader):
        """Test that PII scanner detects email patterns."""
        from unittest.mock import MagicMock
        
        if Path(self.test_pdf_path).exists():
            researcher = SecureRAGResearcher(
                pdf_path=self.test_pdf_path,
                enable_pii_detection=True
            )
            
            # Create mock document with email
            mock_doc = MagicMock()
            mock_doc.page_content = "Contact us at support@example.com for help"
            
            findings = researcher.scan_for_secrets([mock_doc])
            
            self.assertIsInstance(findings, list)
            # Should detect email pattern
            email_alerts = [f for f in findings if "Email" in f]
            self.assertGreater(len(email_alerts), 0)
    
    @patch('main.PyPDFLoader')
    def test_scan_for_secrets_returns_empty_when_disabled(self, mock_loader):
        """Test that PII scanner returns empty list when disabled."""
        from unittest.mock import MagicMock
        
        if Path(self.test_pdf_path).exists():
            researcher = SecureRAGResearcher(
                pdf_path=self.test_pdf_path,
                enable_pii_detection=False  # Disabled
            )
            
            # Create mock document with email
            mock_doc = MagicMock()
            mock_doc.page_content = "Contact us at support@example.com for help"
            
            findings = researcher.scan_for_secrets([mock_doc])
            
            self.assertEqual(findings, [])


class TestConfiguration(unittest.TestCase):
    """Test configuration and environment setup."""
    
    def test_config_imports(self):
        """Test that configuration file is importable."""
        try:
            import config
            self.assertTrue(hasattr(config, 'CHUNK_SIZE'))
            self.assertTrue(hasattr(config, 'CHUNK_OVERLAP'))
            self.assertTrue(hasattr(config, 'OPENAI_MODEL'))
        except ImportError:
            self.fail("config.py should be importable")
    
    def test_data_directory_exists(self):
        """Test that data directory exists."""
        data_dir = Path("data")
        self.assertTrue(data_dir.exists(), "data/ directory should exist")


def run_tests():
    """Run all tests with verbose output."""
    print("\n" + "=" * 70)
    print("🧪 Running Secure RAG Researcher Test Suite")
    print("=" * 70 + "\n")
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 70)
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed.")
    print("=" * 70 + "\n")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
