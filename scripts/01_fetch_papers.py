#!/usr/bin/env python3
"""
Stage 1: Paper Fetching from Automation-Friendly Databases

Fetches papers from Semantic Scholar, OpenAlex, and arXiv APIs.
These databases provide both metadata AND direct PDF URLs for automated retrieval.

Usage:
    python scripts/01_fetch_papers.py --project <project_path> --query <search_query>

Example:
    python scripts/01_fetch_papers.py \\
        --project projects/2025-10-13_AI-Chatbots \\
        --query "chatbot language learning speaking"
"""

import argparse
import requests
import pandas as pd
import time
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional
import yaml
from urllib.parse import quote
from dotenv import load_dotenv


class PaperFetcher:
    """Fetch papers from automation-friendly academic databases"""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.output_dir = self.project_path / "data" / "01_identification"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load environment variables from project .env file
        env_path = self.project_path / ".env"
        if env_path.exists():
            load_dotenv(env_path)

        # Load project config
        config_path = self.project_path / "config.yaml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = {}

        # API endpoints
        self.semantic_scholar_api = "https://api.semanticscholar.org/graph/v1/paper/search"
        self.openalex_api = "https://api.openalex.org/works"
        self.arxiv_api = "http://export.arxiv.org/api/query"

        # API keys
        self.semantic_scholar_api_key = os.getenv('SEMANTIC_SCHOLAR_API_KEY')

        # Prompt user for API key if not found
        if not self.semantic_scholar_api_key:
            self._prompt_for_api_key()

    def _prompt_for_api_key(self):
        """
        Prompt user for Semantic Scholar API key if not found in environment.

        Offers 10x rate limit improvement (100 → 1,000 requests/5 min).
        Saves key to project .env file for future use.
        """
        print("\n" + "="*70)
        print("⚠️  Semantic Scholar API Key Not Found")
        print("="*70)
        print("\n📊 Rate Limits:")
        print("   • Without API key: 100 requests/5 min (slower, ~60-120 minutes for 10K papers)")
        print("   • With API key:    1,000 requests/5 min (10x faster, ~10-20 minutes)")
        print("\n🔑 Get a FREE API key:")
        print("   https://www.semanticscholar.org/product/api#api-key")
        print("\n💡 Enter your API key below (or press Enter to skip)")
        print("   (Key will be saved to .env file for future use)")
        print("="*70 + "\n")

        try:
            api_key_input = input("Semantic Scholar API key (or Enter to skip): ").strip()

            if api_key_input:
                # Validate format (basic check)
                if len(api_key_input) < 20:
                    print("⚠️  Warning: API key seems too short. Proceeding anyway...")

                self.semantic_scholar_api_key = api_key_input

                # Save to project .env file
                env_path = self.project_path / ".env"

                # Check if .env exists
                if env_path.exists():
                    # Append to existing .env
                    with open(env_path, 'r') as f:
                        env_content = f.read()

                    # Check if SEMANTIC_SCHOLAR_API_KEY already exists
                    if 'SEMANTIC_SCHOLAR_API_KEY' in env_content:
                        # Replace existing key
                        import re
                        env_content = re.sub(
                            r'SEMANTIC_SCHOLAR_API_KEY=.*',
                            f'SEMANTIC_SCHOLAR_API_KEY={api_key_input}',
                            env_content
                        )
                    else:
                        # Append new key
                        env_content += f"\n# Semantic Scholar API (added {Path(__file__).name})\n"
                        env_content += f"SEMANTIC_SCHOLAR_API_KEY={api_key_input}\n"

                    with open(env_path, 'w') as f:
                        f.write(env_content)
                else:
                    # Create new .env file
                    with open(env_path, 'w') as f:
                        f.write(f"# ScholaRAG Project Environment\n")
                        f.write(f"# Created by {Path(__file__).name}\n\n")
                        f.write(f"SEMANTIC_SCHOLAR_API_KEY={api_key_input}\n")

                print(f"✅ API key saved to {env_path}")
                print("   10x faster retrieval enabled!\n")
            else:
                print("⏩ Skipping API key. Using free tier (100 requests/5 min)")
                print("   (You can add it later to .env file)\n")

        except KeyboardInterrupt:
            print("\n\n⏩ Skipping API key prompt. Using free tier.\n")
        except Exception as e:
            print(f"\n⚠️  Error during API key setup: {e}")
            print("   Continuing with free tier...\n")

    def fetch_semantic_scholar(
        self,
        query: str,
        year_start: int = 2015,
        year_end: int = 2025,
        limit: int = 10000
    ) -> pd.DataFrame:
        """
        Fetch papers from Semantic Scholar API

        Args:
            query: Search query string
            year_start: Start year for publication filter
            year_end: End year for publication filter
            limit: Maximum number of papers to fetch

        Returns:
            DataFrame with paper metadata including PDF URLs
        """
        print(f"\n🔍 Searching Semantic Scholar...")
        print(f"   Query: {query}")
        print(f"   Years: {year_start}-{year_end}")

        papers = []
        offset = 0
        batch_size = 100  # API limit per request

        while len(papers) < limit:
            params = {
                'query': query,
                'year': f'{year_start}-{year_end}',
                'fields': 'title,abstract,authors,year,citationCount,openAccessPdf,externalIds',
                'limit': min(batch_size, limit - len(papers)),
                'offset': offset
            }

            try:
                headers = {}
                if self.semantic_scholar_api_key:
                    headers['x-api-key'] = self.semantic_scholar_api_key

                response = requests.get(
                    self.semantic_scholar_api,
                    params=params,
                    headers=headers,
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()

                if 'data' not in data or not data['data']:
                    break

                for paper in data['data']:
                    # Extract PDF URL if available
                    pdf_url = None
                    if paper.get('openAccessPdf'):
                        pdf_url = paper['openAccessPdf'].get('url')

                    # Get DOI
                    doi = None
                    if paper.get('externalIds'):
                        doi = paper['externalIds'].get('DOI')

                    papers.append({
                        'title': paper.get('title', ''),
                        'abstract': paper.get('abstract', ''),
                        'authors': '; '.join([a.get('name', '') for a in paper.get('authors', [])]),
                        'year': paper.get('year'),
                        'citations': paper.get('citationCount', 0),
                        'doi': doi,
                        'pdf_url': pdf_url,
                        'source': 'Semantic Scholar',
                        'paperId': paper.get('paperId')
                    })

                print(f"   Retrieved {len(papers)} papers so far...")

                offset += batch_size
                time.sleep(3)  # Rate limiting - increased to 3 seconds

                # Check if we've reached the end
                if len(data['data']) < batch_size:
                    break

            except requests.exceptions.RequestException as e:
                print(f"   ⚠️  Error: {e}")
                break

        df = pd.DataFrame(papers)
        if len(df) > 0:
            pdf_count = df['pdf_url'].notna().sum()
            print(f"   ✓ Found {len(df)} papers ({pdf_count} with PDF URLs, {pdf_count/len(df)*100:.1f}%)")
        else:
            print(f"   ⚠️  No papers found")

        return df

    def fetch_openalex(
        self,
        query: str,
        year_start: int = 2015,
        year_end: int = 2025,
        limit: int = 10000
    ) -> pd.DataFrame:
        """
        Fetch papers from OpenAlex API

        Args:
            query: Search query string
            year_start: Start year filter
            year_end: End year filter
            limit: Maximum papers to fetch

        Returns:
            DataFrame with paper metadata including OA URLs
        """
        print(f"\n🔍 Searching OpenAlex...")
        print(f"   Query: {query}")

        papers = []
        page = 1
        per_page = 200  # API max

        # Add polite pool email for higher rate limits
        mailto = "newhosung@gmail.com"

        while len(papers) < limit:
            params = {
                'search': query,
                'filter': f'publication_year:{year_start}-{year_end}',
                'per_page': min(per_page, limit - len(papers)),
                'page': page,
                'mailto': mailto
            }

            try:
                response = requests.get(
                    self.openalex_api,
                    params=params,
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()

                if 'results' not in data or not data['results']:
                    break

                for work in data['results']:
                    # Extract OA PDF URL
                    pdf_url = None
                    if work.get('open_access'):
                        pdf_url = work['open_access'].get('oa_url')

                    # Process abstract (inverted index format)
                    abstract = ""
                    if work.get('abstract_inverted_index'):
                        # Reconstruct abstract from inverted index
                        inv_index = work['abstract_inverted_index']
                        words = {}
                        for word, positions in inv_index.items():
                            for pos in positions:
                                words[pos] = word
                        abstract = ' '.join([words[i] for i in sorted(words.keys())])

                    papers.append({
                        'title': work.get('title', ''),
                        'abstract': abstract,
                        'authors': '; '.join([
                            a['author']['display_name']
                            for a in work.get('authorships', [])
                        ]),
                        'year': work.get('publication_year'),
                        'citations': work.get('cited_by_count', 0),
                        'doi': work.get('doi', '').replace('https://doi.org/', '') if work.get('doi') else None,
                        'pdf_url': pdf_url,
                        'source': 'OpenAlex',
                        'openalex_id': work.get('id')
                    })

                print(f"   Retrieved {len(papers)} papers so far...")

                page += 1
                time.sleep(0.1)  # Polite rate limiting

                # Check if we've reached the end
                if len(data['results']) < per_page:
                    break

            except requests.exceptions.RequestException as e:
                print(f"   ⚠️  Error: {e}")
                break

        df = pd.DataFrame(papers)
        if len(df) > 0:
            pdf_count = df['pdf_url'].notna().sum()
            print(f"   ✓ Found {len(df)} papers ({pdf_count} with PDF URLs, {pdf_count/len(df)*100:.1f}%)")
        else:
            print(f"   ⚠️  No papers found")

        return df

    def fetch_arxiv(
        self,
        query: str,
        year_start: int = 2015,
        year_end: int = 2025,
        max_results: int = 5000
    ) -> pd.DataFrame:
        """
        Fetch papers from arXiv API

        Args:
            query: Search query (all: prefix for all fields)
            year_start: Start year filter
            year_end: End year filter
            max_results: Maximum papers to fetch

        Returns:
            DataFrame with paper metadata (100% PDF access)
        """
        print(f"\n🔍 Searching arXiv...")
        print(f"   Query: {query}")

        papers = []
        start = 0
        batch_size = 100  # Reasonable batch size

        while len(papers) < max_results:
            params = {
                'search_query': query,
                'start': start,
                'max_results': min(batch_size, max_results - len(papers)),
                'sortBy': 'submittedDate',
                'sortOrder': 'descending'
            }

            url = f"{self.arxiv_api}?{requests.compat.urlencode(params)}"

            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()

                # Parse XML response
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.content)

                # Namespace for arXiv
                ns = {'atom': 'http://www.w3.org/2005/Atom'}

                entries = root.findall('atom:entry', ns)
                if not entries:
                    break

                for entry in entries:
                    # Get publication year
                    published = entry.find('atom:published', ns).text
                    year = int(published[:4])

                    # Filter by year
                    if year < year_start or year > year_end:
                        continue

                    # Get arXiv ID for PDF URL
                    arxiv_id = entry.find('atom:id', ns).text.split('/abs/')[-1]
                    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

                    papers.append({
                        'title': entry.find('atom:title', ns).text.strip(),
                        'abstract': entry.find('atom:summary', ns).text.strip(),
                        'authors': '; '.join([
                            author.find('atom:name', ns).text
                            for author in entry.findall('atom:author', ns)
                        ]),
                        'year': year,
                        'citations': 0,  # arXiv doesn't provide citation counts
                        'doi': None,
                        'pdf_url': pdf_url,
                        'source': 'arXiv',
                        'arxiv_id': arxiv_id
                    })

                print(f"   Retrieved {len(papers)} papers so far...")

                start += batch_size
                time.sleep(3)  # arXiv requests 3-second delay

                # Check if we've reached the end
                if len(entries) < batch_size:
                    break

            except Exception as e:
                print(f"   ⚠️  Error: {e}")
                break

        df = pd.DataFrame(papers)
        print(f"   ✓ Found {len(df)} papers (100% with PDF URLs)")

        return df

    def fetch_all(
        self,
        query: str,
        databases: List[str] = None,
        year_start: int = 2015,
        year_end: int = 2025
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch papers from all selected databases

        Args:
            query: Search query
            databases: List of databases to search (default: all)
            year_start: Start year
            year_end: End year

        Returns:
            Dictionary mapping database names to DataFrames
        """
        if databases is None:
            databases = ['semantic_scholar', 'openalex', 'arxiv']

        results = {}

        if 'semantic_scholar' in databases:
            results['semantic_scholar'] = self.fetch_semantic_scholar(
                query, year_start, year_end
            )
            # Save immediately
            output_file = self.output_dir / "semantic_scholar_results.csv"
            results['semantic_scholar'].to_csv(output_file, index=False)
            print(f"   💾 Saved to {output_file}")

        if 'openalex' in databases:
            results['openalex'] = self.fetch_openalex(
                query, year_start, year_end
            )
            # Save immediately
            output_file = self.output_dir / "openalex_results.csv"
            results['openalex'].to_csv(output_file, index=False)
            print(f"   💾 Saved to {output_file}")

        if 'arxiv' in databases:
            # Modify query for arXiv format
            arxiv_query = f"all:{query.replace(' ', ' AND all:')}"
            results['arxiv'] = self.fetch_arxiv(
                arxiv_query, year_start, year_end, max_results=5000
            )
            # Save immediately
            output_file = self.output_dir / "arxiv_results.csv"
            results['arxiv'].to_csv(output_file, index=False)
            print(f"   💾 Saved to {output_file}")

        return results

    def print_summary(self, results: Dict[str, pd.DataFrame]):
        """Print summary statistics"""
        print("\n" + "="*60)
        print("📊 SEARCH SUMMARY")
        print("="*60)

        total_papers = 0
        total_with_pdf = 0

        for db_name, df in results.items():
            papers = len(df)
            with_pdf = df['pdf_url'].notna().sum()
            total_papers += papers
            total_with_pdf += with_pdf

            print(f"\n{db_name.upper()}:")
            print(f"  Papers found: {papers}")
            print(f"  With PDF URLs: {with_pdf} ({with_pdf/papers*100:.1f}%)")

        print(f"\nTOTAL:")
        print(f"  Papers: {total_papers}")
        print(f"  With PDF URLs: {total_with_pdf} ({total_with_pdf/total_papers*100:.1f}%)")
        print(f"\n✓ All results saved to: {self.output_dir}")
        print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch papers from automation-friendly databases (Semantic Scholar, OpenAlex, arXiv)"
    )
    parser.add_argument(
        '--project',
        required=True,
        help='Path to project directory (e.g., projects/2025-10-13_AI-Chatbots)'
    )
    parser.add_argument(
        '--query',
        required=True,
        help='Search query (e.g., "chatbot language learning speaking")'
    )
    parser.add_argument(
        '--databases',
        nargs='+',
        choices=['semantic_scholar', 'openalex', 'arxiv'],
        default=['semantic_scholar', 'openalex', 'arxiv'],
        help='Databases to search (default: all)'
    )
    parser.add_argument(
        '--year-start',
        type=int,
        default=2015,
        help='Start year for publication filter (default: 2015)'
    )
    parser.add_argument(
        '--year-end',
        type=int,
        default=2025,
        help='End year for publication filter (default: 2025)'
    )

    args = parser.parse_args()

    # Validate project path
    project_path = Path(args.project)
    if not project_path.exists():
        print(f"❌ Error: Project path does not exist: {project_path}")
        print(f"   Please run: python scholarag_cli.py init")
        sys.exit(1)

    # Initialize fetcher
    fetcher = PaperFetcher(args.project)

    # Fetch papers
    print(f"\n🚀 Starting paper search...")
    print(f"   Query: {args.query}")
    print(f"   Databases: {', '.join(args.databases)}")
    print(f"   Years: {args.year_start}-{args.year_end}")

    results = fetcher.fetch_all(
        args.query,
        args.databases,
        args.year_start,
        args.year_end
    )

    # Print summary
    fetcher.print_summary(results)

    print("\n✨ Next step: Run deduplication")
    print(f"   python scripts/02_deduplicate.py --project {args.project}")


if __name__ == '__main__':
    main()
