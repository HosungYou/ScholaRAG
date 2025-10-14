#!/usr/bin/env python3
"""
Stage 4: PDF Download with Retry Logic

Downloads PDFs for relevant papers with proper error handling,
retry logic, and progress tracking.

Usage:
    python scripts/04_download_pdfs.py --project <project_path>

Example:
    python scripts/04_download_pdfs.py --project projects/2025-10-13_AI-Chatbots
"""

import argparse
import pandas as pd
import sys
import os
import requests
import time
from pathlib import Path
from typing import Dict, Optional
from urllib.parse import urlparse
import hashlib


class PDFDownloader:
    """Download PDFs with retry logic and progress tracking"""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.input_dir = self.project_path / "data" / "02_screening"
        self.output_dir = self.project_path / "data" / "03_pdfs"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Download settings
        self.max_retries = 3
        self.timeout = 30
        self.delay_between_downloads = 2  # seconds

    def load_relevant_papers(self) -> pd.DataFrame:
        """
        Load papers that passed screening

        Returns:
            DataFrame with relevant papers
        """
        print("\n📂 Loading relevant papers...")

        relevant_file = self.input_dir / "relevant_papers.csv"
        if not relevant_file.exists():
            print(f"❌ Error: Relevant papers file not found: {relevant_file}")
            print("   Run screening first: python scripts/03_screen_papers.py")
            sys.exit(1)

        df = pd.read_csv(relevant_file)
        print(f"   ✓ Loaded {len(df)} relevant papers")

        # Filter papers with PDF URLs
        df_with_pdf = df[df['pdf_url'].notna()].copy()
        print(f"   ✓ {len(df_with_pdf)} papers have PDF URLs ({len(df_with_pdf)/len(df)*100:.1f}%)")

        return df_with_pdf

    def generate_filename(self, title: str, index: int) -> str:
        """
        Generate safe filename from paper title

        Args:
            title: Paper title
            index: Paper index for uniqueness

        Returns:
            Safe filename
        """
        # Remove special characters
        safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in title)

        # Limit length
        safe_title = safe_title[:100]

        # Remove extra whitespace
        safe_title = '_'.join(safe_title.split())

        # Add index for uniqueness
        filename = f"{index:04d}_{safe_title}.pdf"

        return filename

    def download_pdf(
        self,
        url: str,
        output_path: Path,
        retries: int = 0
    ) -> Dict[str, any]:
        """
        Download a single PDF with retry logic

        Args:
            url: PDF URL
            output_path: Where to save the PDF
            retries: Current retry attempt

        Returns:
            Dictionary with download status
        """
        try:
            # Send GET request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }

            response = requests.get(
                url,
                headers=headers,
                timeout=self.timeout,
                allow_redirects=True,
                stream=True
            )
            response.raise_for_status()

            # Check if response is actually a PDF
            content_type = response.headers.get('Content-Type', '')
            if 'application/pdf' not in content_type and not url.endswith('.pdf'):
                return {
                    'success': False,
                    'error': f'Not a PDF file (Content-Type: {content_type})'
                }

            # Save PDF
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # Verify file size
            file_size = output_path.stat().st_size
            if file_size < 1000:  # Less than 1KB is suspicious
                output_path.unlink()
                return {
                    'success': False,
                    'error': f'File too small ({file_size} bytes)'
                }

            return {
                'success': True,
                'file_size': file_size
            }

        except requests.exceptions.Timeout:
            if retries < self.max_retries:
                time.sleep(2 ** retries)  # Exponential backoff
                return self.download_pdf(url, output_path, retries + 1)
            return {
                'success': False,
                'error': 'Timeout after retries'
            }

        except requests.exceptions.HTTPError as e:
            return {
                'success': False,
                'error': f'HTTP {e.response.status_code}'
            }

        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }

    def download_all_pdfs(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Download all PDFs with progress tracking

        Args:
            df: DataFrame with papers and PDF URLs

        Returns:
            DataFrame with download results
        """
        print("\n" + "="*60)
        print("📥 PDF DOWNLOAD")
        print("="*60)
        print(f"\nTotal PDFs to download: {len(df)}")
        print(f"Estimated time: {len(df) * self.delay_between_downloads / 60:.1f} minutes")

        # Check for existing progress
        progress_file = self.output_dir / "download_log.csv"
        if progress_file.exists():
            print(f"\n✓ Found existing download log")
            df_progress = pd.read_csv(progress_file)
            print(f"  Already downloaded: {len(df_progress[df_progress['downloaded']])} PDFs")

            # Merge with current dataframe
            df = df.merge(
                df_progress[['title', 'downloaded', 'local_path', 'error']],
                on='title',
                how='left',
                suffixes=('', '_prev')
            )

            df_to_download = df[df['downloaded'].isna() | (df['downloaded'] == False)]
            already_downloaded = len(df) - len(df_to_download)
        else:
            df['downloaded'] = False
            df['local_path'] = None
            df['error'] = None
            df_to_download = df.copy()
            already_downloaded = 0

        if len(df_to_download) == 0:
            print("\n✓ All PDFs already downloaded!")
            return df

        print(f"\n⏳ Starting downloads...")

        # Download each PDF
        download_results = []
        for idx, row in df_to_download.iterrows():
            paper_idx = idx + 1
            filename = self.generate_filename(row['title'], paper_idx)
            output_path = self.output_dir / filename

            print(f"\n[{paper_idx}/{len(df)}] {row['title'][:60]}...")

            # Download PDF
            result = self.download_pdf(row['pdf_url'], output_path)

            if result['success']:
                print(f"   ✓ Downloaded ({result['file_size'] / 1024:.1f} KB)")
                download_results.append({
                    'title': row['title'],
                    'downloaded': True,
                    'local_path': str(output_path),
                    'error': None
                })
            else:
                print(f"   ✗ Failed: {result['error']}")
                download_results.append({
                    'title': row['title'],
                    'downloaded': False,
                    'local_path': None,
                    'error': result['error']
                })

            # Rate limiting
            time.sleep(self.delay_between_downloads)

            # Save progress every 10 downloads
            if len(download_results) % 10 == 0:
                df_temp = pd.DataFrame(download_results)
                if already_downloaded > 0:
                    df_existing = pd.read_csv(progress_file)
                    df_temp = pd.concat([df_existing, df_temp], ignore_index=True)
                df_temp.to_csv(progress_file, index=False)
                print(f"   💾 Progress saved")

        # Save final results
        df_results = pd.DataFrame(download_results)
        if already_downloaded > 0:
            df_existing = pd.read_csv(progress_file)
            df_results = pd.concat([df_existing, df_results], ignore_index=True)
        df_results.to_csv(progress_file, index=False)

        # Merge with original dataframe
        df = df.merge(
            df_results[['title', 'downloaded', 'local_path', 'error']],
            on='title',
            how='left',
            suffixes=('', '_new')
        )

        return df

    def generate_summary(self, df: pd.DataFrame):
        """
        Generate download summary statistics

        Args:
            df: DataFrame with download results
        """
        print("\n" + "="*60)
        print("📊 DOWNLOAD SUMMARY")
        print("="*60)

        total = len(df)
        successful = df['downloaded'].sum()
        failed = (df['downloaded'] == False).sum()

        print(f"\nTotal papers: {total}")
        print(f"Successfully downloaded: {successful} ({successful/total*100:.1f}%)")
        print(f"Failed: {failed} ({failed/total*100:.1f}%)")

        if failed > 0:
            print(f"\nFailure Reasons:")
            error_counts = df[df['downloaded'] == False]['error'].value_counts()
            for error, count in error_counts.head(5).items():
                print(f"  {error}: {count}")

        # Calculate total size
        downloaded_files = df[df['downloaded'] == True]['local_path'].tolist()
        total_size = sum(Path(f).stat().st_size for f in downloaded_files if Path(f).exists())
        print(f"\nTotal size: {total_size / (1024*1024):.1f} MB")
        print(f"Average size: {total_size / successful / 1024:.1f} KB per PDF")

        print(f"\n💾 PDFs saved to: {self.output_dir}")
        print("="*60)

        # Save final metadata
        metadata_file = self.output_dir / "papers_metadata.csv"
        df.to_csv(metadata_file, index=False)
        print(f"\n💾 Metadata saved to: {metadata_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Download PDFs for relevant papers"
    )
    parser.add_argument(
        '--project',
        required=True,
        help='Path to project directory'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=2.0,
        help='Delay between downloads in seconds (default: 2.0)'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='Download timeout in seconds (default: 30)'
    )

    args = parser.parse_args()

    # Validate project path
    project_path = Path(args.project)
    if not project_path.exists():
        print(f"❌ Error: Project path does not exist: {project_path}")
        sys.exit(1)

    # Initialize downloader
    downloader = PDFDownloader(args.project)
    downloader.delay_between_downloads = args.delay
    downloader.timeout = args.timeout

    # Load relevant papers
    df = downloader.load_relevant_papers()

    # Download PDFs
    df = downloader.download_all_pdfs(df)

    # Generate summary
    downloader.generate_summary(df)

    print("\n✨ Next step: Build RAG system")
    print(f"   python scripts/05_build_rag.py --project {args.project}")


if __name__ == '__main__':
    main()
