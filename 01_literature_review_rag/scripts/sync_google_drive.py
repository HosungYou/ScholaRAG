#!/usr/bin/env python3
"""
Google Drive Integration for ResearcherRAG
Download papers directly from Google Drive folder

Setup:
    1. pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
    2. Enable Google Drive API: https://console.cloud.google.com/
    3. Download credentials.json to scripts/ folder
    4. Run this script to authenticate

Usage:
    # First time: authenticate
    python scripts/sync_google_drive.py --setup

    # Download from specific folder
    python scripts/sync_google_drive.py --folder "Research Papers"

    # Auto-sync and ingest
    python scripts/sync_google_drive.py --folder "Research Papers" --ingest
"""
import sys
import os
import argparse
import pickle
from pathlib import Path

# Check if Google API libraries are installed
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload
except ImportError:
    print("\n❌ Google API libraries not installed!")
    print("\nPlease install:")
    print("  pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    print()
    sys.exit(1)

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.core.ingestion import ingest_documents
from backend.core.retrieval import get_retriever

# Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# File paths
SCRIPT_DIR = Path(__file__).parent
TOKEN_FILE = SCRIPT_DIR / 'token.pickle'
CREDENTIALS_FILE = SCRIPT_DIR / 'credentials.json'


def authenticate():
    """
    Authenticate with Google Drive API
    Opens browser for first-time authentication
    """
    creds = None

    # Load existing credentials
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing credentials...")
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print("\n❌ credentials.json not found!")
                print("\nSetup instructions:")
                print("1. Go to: https://console.cloud.google.com/")
                print("2. Create a project")
                print("3. Enable Google Drive API")
                print("4. Create OAuth 2.0 credentials")
                print("5. Download credentials.json")
                print(f"6. Save to: {CREDENTIALS_FILE}")
                print()
                return None

            print("🌐 Opening browser for authentication...")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save credentials
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

        print("✓ Authentication successful!")

    return creds


def find_folder(service, folder_name: str):
    """Find Google Drive folder by name"""
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"

    results = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name)'
    ).execute()

    folders = results.get('files', [])

    if not folders:
        return None

    if len(folders) > 1:
        print(f"\n⚠️  Found {len(folders)} folders named '{folder_name}':")
        for i, folder in enumerate(folders, 1):
            print(f"  {i}. {folder['name']} (ID: {folder['id']})")
        print("\nUsing the first one. Use --folder-id to specify exact folder.")

    return folders[0]


def list_pdfs_in_folder(service, folder_id: str):
    """List all PDF files in a folder"""
    query = f"'{folder_id}' in parents and mimeType='application/pdf' and trashed=false"

    results = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name, size, modifiedTime)',
        orderBy='name'
    ).execute()

    return results.get('files', [])


def download_file(service, file_id: str, destination: Path):
    """Download a file from Google Drive"""
    request = service.files().get_media(fileId=file_id)

    with open(destination, 'wb') as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()


def sync_papers(
    service,
    folder_name: str = None,
    folder_id: str = None,
    output_dir: Path = None
):
    """
    Sync papers from Google Drive to local directory

    Args:
        service: Google Drive service
        folder_name: Name of folder to sync
        folder_id: Direct folder ID (overrides folder_name)
        output_dir: Local directory to download to

    Returns:
        List of downloaded file paths
    """
    # Find folder
    if folder_id:
        folder = {'id': folder_id, 'name': 'Specified Folder'}
    elif folder_name:
        print(f"\n🔍 Searching for folder: '{folder_name}'...")
        folder = find_folder(service, folder_name)
        if not folder:
            print(f"❌ Folder '{folder_name}' not found!")
            return []
        print(f"✓ Found folder: {folder['name']}")
    else:
        print("❌ Please specify --folder or --folder-id")
        return []

    # List PDFs
    print(f"\n📄 Listing PDF files...")
    pdf_files = list_pdfs_in_folder(service, folder['id'])

    if not pdf_files:
        print(f"❌ No PDF files found in folder '{folder['name']}'")
        return []

    print(f"✓ Found {len(pdf_files)} PDF files")
    print()

    # Create output directory
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "data" / "raw_pdfs" / "google_drive_sync"

    output_dir.mkdir(parents=True, exist_ok=True)

    # Download files
    downloaded_files = []
    skipped_files = []

    print("📥 Downloading files...")
    print()

    for i, file_info in enumerate(pdf_files, 1):
        file_name = file_info['name']
        destination = output_dir / file_name

        # Check if already exists and same size
        if destination.exists():
            local_size = destination.stat().st_size
            remote_size = int(file_info.get('size', 0))

            if local_size == remote_size:
                print(f"  [{i:2d}/{len(pdf_files)}] ⊘ Skip: {file_name} (already exists)")
                skipped_files.append(destination)
                continue

        print(f"  [{i:2d}/{len(pdf_files)}] ⬇️  {file_name}...", end='', flush=True)

        try:
            download_file(service, file_info['id'], destination)
            downloaded_files.append(destination)
            print(" ✓")
        except Exception as e:
            print(f" ✗ Error: {e}")

    print()
    print("="*70)
    print("📊 Download Summary")
    print("="*70)
    print(f"  Downloaded: {len(downloaded_files)} files")
    print(f"  Skipped: {len(skipped_files)} files (already exist)")
    print(f"  Total: {len(pdf_files)} files")
    print(f"  Location: {output_dir}")
    print()

    return downloaded_files + skipped_files


def main():
    """Main function"""

    parser = argparse.ArgumentParser(
        description="Sync papers from Google Drive to ResearcherRAG",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--setup',
        action='store_true',
        help='Run authentication setup'
    )

    parser.add_argument(
        '--folder',
        type=str,
        help='Name of Google Drive folder to sync'
    )

    parser.add_argument(
        '--folder-id',
        type=str,
        help='Direct Google Drive folder ID'
    )

    parser.add_argument(
        '--output',
        type=str,
        help='Local directory to download to',
        default=None
    )

    parser.add_argument(
        '--ingest',
        action='store_true',
        help='Automatically ingest downloaded papers into RAG system'
    )

    args = parser.parse_args()

    # Header
    print("\n" + "="*70)
    print("ResearcherRAG - Google Drive Sync")
    print("="*70)

    # Authenticate
    print("\n🔐 Authenticating with Google Drive...")
    creds = authenticate()

    if not creds:
        return 1

    service = build('drive', 'v3', credentials=creds)

    if args.setup:
        print("\n✅ Setup complete!")
        print("\nYou can now sync folders:")
        print('  python scripts/sync_google_drive.py --folder "Research Papers"')
        return 0

    if not args.folder and not args.folder_id:
        print("\n❌ Please specify --folder or --folder-id")
        print("\nExample:")
        print('  python scripts/sync_google_drive.py --folder "Research Papers"')
        return 1

    # Sync papers
    output_dir = Path(args.output) if args.output else None
    files = sync_papers(
        service,
        folder_name=args.folder,
        folder_id=args.folder_id,
        output_dir=output_dir
    )

    if not files:
        return 1

    # Ingest if requested
    if args.ingest:
        print("\n" + "="*70)
        print("📝 Ingesting papers into RAG system...")
        print("="*70)

        try:
            folder_path = files[0].parent
            documents = ingest_documents(str(folder_path))

            print(f"\n✓ Created {len(documents)} text chunks")

            # Add to vector store
            print("\n🔄 Adding to vector database...")
            retriever = get_retriever()
            retriever.add_documents(documents)

            # Get stats
            stats = retriever.get_collection_stats()

            print("\n✅ Ingestion complete!")
            print(f"   Total in database: {stats.get('count', 0)}")

        except Exception as e:
            print(f"\n❌ Ingestion failed: {e}")
            return 1

    print("\n🚀 Done! You can now query your papers:")
    print("   python app.py")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
