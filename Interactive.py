#!/usr/bin/env python3
"""
Interactive CLI for Secure RAG Researcher
Run queries against your documents from the command line.
"""

import sys
from pathlib import Path
from main import SecureRAGResearcher


def print_banner():
    """Print welcome banner."""
    print("\n" + "=" * 70)
    print("🔒 SECURE RAG RESEARCHER - Interactive Mode")
    print("=" * 70)
    print("Ask questions about your documents in natural language.")
    print("Type 'quit' or 'exit' to end the session.\n")


def main():
    """Run interactive CLI."""
    
    # Check if PDF exists
    pdf_path = "data/sample_security_policy.pdf"
    if not Path(pdf_path).exists():
        print(f"❌ Error: PDF not found at {pdf_path}")
        print("Run 'python generate_sample_pdf.py' first to create a sample document.")
        sys.exit(1)
    
    print_banner()
    
    # Optional: Enable PII detection
    enable_pii = input("Enable PII detection? (y/n): ").lower() == 'y'
    if enable_pii:
        print("🔒 PII detection enabled\n")
    
    try:
        # Initialize researcher
        print("🔧 Initializing system...")
        researcher = SecureRAGResearcher(
            pdf_path=pdf_path,
            chunk_size=1000,
            chunk_overlap=200,
            model_name="gpt-4o",
            temperature=0,
            enable_pii_detection=enable_pii
        )
        
        researcher.initialize(force_recreate=False)
        
        # Interactive loop
        while True:
            try:
                query = input("\n❓ Your question: ").strip()
                
                if not query:
                    continue
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!\n")
                    break
                
                # Process query
                response = researcher.query(query)
                
                print(f"\n💡 Answer:")
                print(f"{response['result']}\n")
                
                # Show sources
                num_sources = len(response['source_documents'])
                print(f"📚 Based on {num_sources} source chunk(s)")
                
                # Optional: show source preview
                if input("\nShow source excerpts? (y/n): ").lower() == 'y':
                    for i, doc in enumerate(response['source_documents'], 1):
                        print(f"\n--- Source {i} ---")
                        print(doc.page_content[:200] + "...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!\n")
                break
            except Exception as e:
                print(f"\n❌ Error processing query: {e}\n")
    
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
