#!/usr/bin/env python3
"""
Flexible batch ingestion script that works on any computer
Supports custom directories and Google Drive sync folders

Usage:
    # Use default directory (data/raw_pdfs)
    python scripts/batch_ingest_flexible.py

    # Use custom directory
    python scripts/batch_ingest_flexible.py --dir /path/to/your/papers

    # Use Google Drive sync folder
    python scripts/batch_ingest_flexible.py --dir ~/GoogleDrive/Research/Papers
"""
import sys
import argparse
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.core.ingestion import ingest_documents
from backend.core.retrieval import get_retriever
from backend.core.config import settings


def find_pdf_directory():
    """
    Intelligently find PDF directory across different systems
    Checks multiple common locations
    """
    project_root = Path(__file__).parent.parent

    # Priority order of directories to check
    possible_dirs = [
        # 1. Default project directory
        project_root / "data" / "raw_pdfs",

        # 2. Google Drive sync folders (common locations)
        Path.home() / "Google Drive" / "Research" / "Papers",
        Path.home() / "GoogleDrive" / "Research" / "Papers",
        Path.home() / "My Drive" / "Research" / "Papers",

        # 3. Dropbox
        Path.home() / "Dropbox" / "Research" / "Papers",

        # 4. OneDrive
        Path.home() / "OneDrive" / "Research" / "Papers",

        # 5. Desktop
        Path.home() / "Desktop" / "Research_Papers",

        # 6. Documents
        Path.home() / "Documents" / "Research" / "Papers",
    ]

    # Find first existing directory with PDFs
    for dir_path in possible_dirs:
        if dir_path.exists():
            pdf_files = list(dir_path.glob("*.pdf"))
            if pdf_files:
                return dir_path

    # Return default even if empty
    return project_root / "data" / "raw_pdfs"


def scan_for_pdfs(directory: Path, recursive: bool = False):
    """
    Scan directory for PDF files

    Args:
        directory: Directory to scan
        recursive: If True, scan subdirectories too

    Returns:
        List of PDF file paths
    """
    if recursive:
        pdf_files = list(directory.rglob("*.pdf"))
    else:
        pdf_files = list(directory.glob("*.pdf"))

    # Sort by name for consistent ordering
    pdf_files.sort(key=lambda p: p.name)

    return pdf_files


def display_file_summary(pdf_files: list, max_display: int = 10):
    """Display summary of files to process"""
    print("\n" + "="*70)
    print(f"📁 Found {len(pdf_files)} PDF files")
    print("="*70)
    print()

    if not pdf_files:
        return

    print("Files to process:")
    for i, pdf in enumerate(pdf_files[:max_display], 1):
        # Show relative path from home for privacy
        try:
            rel_path = pdf.relative_to(Path.home())
            display_path = f"~/{rel_path}"
        except ValueError:
            display_path = str(pdf)

        print(f"  {i:2d}. {pdf.name}")
        print(f"      ({display_path})")

    if len(pdf_files) > max_display:
        print(f"  ... and {len(pdf_files) - max_display} more files")
    print()


def main():
    """Main ingestion function"""

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Batch ingest PDF papers into ResearcherRAG",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use auto-detected directory
  python scripts/batch_ingest_flexible.py

  # Use specific directory
  python scripts/batch_ingest_flexible.py --dir ~/Documents/Papers

  # Use Google Drive
  python scripts/batch_ingest_flexible.py --dir ~/GoogleDrive/Research/Papers

  # Scan subdirectories recursively
  python scripts/batch_ingest_flexible.py --recursive
        """
    )

    parser.add_argument(
        '--dir',
        type=str,
        help='Directory containing PDF files (default: auto-detect)',
        default=None
    )

    parser.add_argument(
        '--recursive',
        action='store_true',
        help='Scan subdirectories recursively'
    )

    parser.add_argument(
        '--yes', '-y',
        action='store_true',
        help='Skip confirmation prompt'
    )

    args = parser.parse_args()

    # Header
    print("\n" + "="*70)
    print("ResearcherRAG - Flexible Batch Paper Ingestion")
    print("="*70)

    # Determine directory
    if args.dir:
        pdf_dir = Path(args.dir).expanduser().resolve()
        print(f"\n📂 Using specified directory: {pdf_dir}")
    else:
        pdf_dir = find_pdf_directory()
        print(f"\n📂 Auto-detected directory: {pdf_dir}")

    # Check directory exists
    if not pdf_dir.exists():
        print(f"\n❌ Error: Directory does not exist!")
        print(f"   Path: {pdf_dir}")
        print("\nPlease:")
        print("  1. Create the directory, OR")
        print("  2. Specify a different directory with --dir")
        print("\nExample:")
        print(f"  python {Path(__file__).name} --dir ~/Documents/Papers")
        return 1

    # Scan for PDFs
    print(f"\n🔍 Scanning for PDF files...")
    if args.recursive:
        print("   (including subdirectories)")

    pdf_files = scan_for_pdfs(pdf_dir, recursive=args.recursive)

    # Display summary
    display_file_summary(pdf_files)

    if not pdf_files:
        print("❌ No PDF files found!")
        print("\nTips:")
        print("  • Make sure PDF files are in the directory")
        print("  • Use --recursive to scan subdirectories")
        print("  • Use --dir to specify a different directory")
        print("\nExamples:")
        print("  python scripts/batch_ingest_flexible.py --dir ~/Downloads")
        print("  python scripts/batch_ingest_flexible.py --recursive")
        return 1

    # Confirm
    if not args.yes:
        response = input("Process these files? (y/n): ")
        if response.lower() != 'y':
            print("\n❌ Cancelled.")
            return 0

    print("\n" + "="*70)
    print("📝 Processing papers...")
    print("="*70)
    print("\n⏳ This may take a few minutes...")
    print("   (~20 seconds per paper)\n")

    # Ingest documents
    try:
        documents = ingest_documents(
            str(pdf_dir),
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )

        if not documents:
            print("\n❌ No documents could be processed")
            print("   Check if PDFs are valid (not scanned images)")
            return 1

        print(f"\n✓ Created {len(documents)} text chunks from {len(pdf_files)} papers")

        # Add to vector store
        print("\n🔄 Adding to vector database...")
        retriever = get_retriever()
        retriever.add_documents(documents)

        # Get stats
        stats = retriever.get_collection_stats()

        # Success!
        print("\n" + "="*70)
        print("✅ Ingestion Complete!")
        print("="*70)
        print()
        print("📊 Statistics:")
        print(f"   Papers processed: {len(pdf_files)}")
        print(f"   Text chunks created: {len(documents)}")
        print(f"   Total in database: {stats.get('count', 0)}")
        print(f"   Source directory: {pdf_dir}")
        print()
        print("🚀 Next steps:")
        print("   1. Run: python app.py")
        print("   2. Open: http://localhost:7860")
        print("   3. Go to 'Ask Questions' tab")
        print("   4. Start querying your papers!")
        print()

        return 0

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
