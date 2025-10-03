#!/usr/bin/env python3
"""
Batch ingestion script for processing papers directly from folder
Usage: python scripts/batch_ingest.py
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.core.ingestion import ingest_documents
from backend.core.retrieval import get_retriever
from backend.core.config import settings

def main():
    """Process all PDFs in raw_pdfs directory"""

    print("="*60)
    print("Batch Paper Ingestion")
    print("="*60)
    print()

    # Check for PDFs
    pdf_dir = Path(settings.raw_pdfs_path)
    pdf_files = list(pdf_dir.glob("*.pdf"))

    if not pdf_files:
        print(f"❌ No PDF files found in: {pdf_dir}")
        print()
        print("Please add PDF files to:")
        print(f"  {pdf_dir}")
        print()
        print("Or use the web interface:")
        print("  python app.py")
        return

    print(f"📁 Found {len(pdf_files)} PDF files in: {pdf_dir}")
    print()

    # Show files
    print("Files to process:")
    for i, pdf in enumerate(pdf_files[:10], 1):
        print(f"  {i}. {pdf.name}")
    if len(pdf_files) > 10:
        print(f"  ... and {len(pdf_files) - 10} more")
    print()

    # Confirm
    response = input("Process these files? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        return

    print()
    print("Processing papers...")
    print("(This may take a few minutes...)")
    print()

    # Ingest documents
    try:
        documents = ingest_documents(str(pdf_dir))

        if not documents:
            print("❌ No documents could be processed")
            return

        print()
        print(f"✓ Created {len(documents)} text chunks")
        print()

        # Add to vector store
        print("Adding to vector database...")
        retriever = get_retriever()
        retriever.add_documents(documents)

        # Get stats
        stats = retriever.get_collection_stats()

        print()
        print("="*60)
        print("✅ Ingestion Complete!")
        print("="*60)
        print()
        print(f"📊 Statistics:")
        print(f"  Papers processed: {len(pdf_files)}")
        print(f"  Text chunks: {len(documents)}")
        print(f"  Total in database: {stats.get('count', 0)}")
        print()
        print("You can now query your papers:")
        print("  python app.py")
        print()

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
