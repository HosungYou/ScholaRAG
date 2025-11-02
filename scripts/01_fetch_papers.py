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
            load_dotenv(env_path, override=True)  # Use override to ensure it loads

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

    def _show_api_key_requirement(self):
        """
        Show error message when Semantic Scholar API key is missing.

        API key is now REQUIRED for Semantic Scholar (not optional).
        Free tier rate limits are too slow for systematic literature reviews.
        """
        print("\n" + "="*80)
        print("❌ ERROR: Semantic Scholar API Key Required")
        print("="*80)
        print("\n🔑 **API Key is now REQUIRED for Semantic Scholar**")
        print("\nWhy?")
        print("   • Free tier: 100 requests/5 min → Too slow for systematic reviews")
        print("   • With API key: 1,000 requests/5 min → 10x faster retrieval")
        print("   • For 10,000 papers: Free tier = 60-120 min, API key = 10-20 min")
        print("\n📋 How to get a FREE API key:")
        print("   1. Visit: https://www.semanticscholar.org/product/api#api-key")
        print("   2. Sign up with your email")
        print("   3. Copy your API key")
        print("\n💾 How to add API key to your project:")
        print(f"   1. Create/edit: {self.project_path}/.env")
        print(f"   2. Add this line: SEMANTIC_SCHOLAR_API_KEY=your_key_here")
        print("\n🚀 Quick setup script:")
        print(f"   python scripts/setup_api_keys.py --project {self.project_path}")
        print("\n💡 Alternative: Skip Semantic Scholar")
        print("   Use --databases openalex arxiv (OpenAlex works without API key)")
        print("="*80 + "\n")

        # Exit if Semantic Scholar is requested but no API key
        print("❌ Exiting: Please add Semantic Scholar API key to continue.\n")
        sys.exit(1)

    def _parse_and_parts(self, query: str) -> list:
        """
        Parse top-level AND-separated parts from query.

        Returns:
            List of AND-separated query parts
        """
        parts = []
        depth = 0
        current_part = ""

        i = 0
        while i < len(query):
            char = query[i]

            if char == '(':
                depth += 1
                current_part += char
            elif char == ')':
                depth -= 1
                current_part += char
            elif depth == 0 and i + 4 <= len(query) and query[i:i+5] == ' AND ':
                if current_part.strip():
                    parts.append(current_part.strip())
                    current_part = ""
                i += 4  # Skip ' AND'
                continue
            else:
                current_part += char

            i += 1

        # Add last part
        if current_part.strip():
            parts.append(current_part.strip())

        return parts

    def _extract_or_terms(self, part: str) -> list:
        """
        Extract OR-separated terms from a query part.

        Example:
            "(AI OR ML OR machine learning)" -> ["AI", "ML", "machine learning"]
        """
        # Remove outer parentheses
        part = part.strip()
        if part.startswith('(') and part.endswith(')'):
            part = part[1:-1]

        # Split by OR
        terms = []
        depth = 0
        current_term = ""

        i = 0
        while i < len(part):
            char = part[i]

            if char == '(':
                depth += 1
                current_term += char
            elif char == ')':
                depth -= 1
                current_term += char
            elif depth == 0 and i + 4 <= len(part) and part[i:i+4] == ' OR ':
                if current_term.strip():
                    terms.append(current_term.strip())
                    current_term = ""
                i += 3  # Skip ' OR'
                continue
            else:
                current_term += char

            i += 1

        # Add last term
        if current_term.strip():
            terms.append(current_term.strip())

        return terms

    def _select_best_terms(self, or_terms: list, max_terms: int = 3) -> list:
        """
        Select best terms from OR list for Semantic Scholar query.

        Strategy:
        - Prefer full phrases over abbreviations (e.g., "artificial intelligence" > "AI")
        - Balance specificity with query length
        - Avoid overly broad terms alone (e.g., "algorithm", "automation")

        Args:
            or_terms: List of OR-separated terms
            max_terms: Maximum terms to return

        Returns:
            Best terms for Semantic Scholar query
        """
        if len(or_terms) <= max_terms:
            return or_terms

        # Prioritize full phrases (contain spaces)
        phrases = [t for t in or_terms if ' ' in t]
        abbreviations = [t for t in or_terms if ' ' not in t]

        # Mix: prefer 1-2 full phrases + 1-2 abbreviations
        selected = []

        # Add up to 2 shortest full phrases
        if phrases:
            phrases_sorted = sorted(phrases, key=len)
            selected.extend(phrases_sorted[:min(2, len(phrases))])

        # Fill remaining with shortest abbreviations
        if len(selected) < max_terms and abbreviations:
            abbrev_sorted = sorted(abbreviations, key=len)
            remaining = max_terms - len(selected)
            selected.extend(abbrev_sorted[:remaining])

        # If still not enough, add more
        if len(selected) < max_terms:
            all_terms_sorted = sorted(or_terms, key=len)
            for term in all_terms_sorted:
                if term not in selected:
                    selected.append(term)
                    if len(selected) >= max_terms:
                        break

        return selected[:max_terms]

    def _optimize_semantic_scholar_query(self, query: str, max_or_terms: int = 3) -> str:
        """
        Optimize complex Boolean queries for Semantic Scholar API.

        Semantic Scholar has undocumented limitations:
        - Max 2 AND-separated parts work reliably
        - Too many OR terms (>4-5) cause query to fail silently
        - Overly broad terms cause poor results

        Strategy:
        1. Keep only first 2 AND parts
        2. Limit OR terms to max_or_terms (default: 3) per part
        3. Prioritize full phrases over abbreviations

        Args:
            query: Original Boolean query
            max_or_terms: Maximum OR terms to keep per AND part

        Returns:
            Optimized query that Semantic Scholar can handle
        """
        # Parse AND parts
        parts = self._parse_and_parts(query)

        if len(parts) == 0:
            return query

        # Keep only first 2 AND parts
        optimized_parts = []
        simplified = False

        for idx, part in enumerate(parts[:2]):  # Only first 2 parts
            # Extract OR terms
            or_terms = self._extract_or_terms(part)

            if len(or_terms) > max_or_terms:
                # Select best terms (prefer full phrases)
                or_terms = self._select_best_terms(or_terms, max_or_terms)
                simplified = True

            # Reconstruct part
            if len(or_terms) == 1:
                optimized_parts.append(or_terms[0])
            else:
                optimized_parts.append(f"({' OR '.join(or_terms)})")

        if len(parts) > 2:
            simplified = True

        # Combine parts
        optimized_query = ' AND '.join(optimized_parts)

        # Show simplification message
        if simplified:
            print(f"   ⚠️  Query optimized for Semantic Scholar API limitations")
            print(f"   • Original: {len(parts)} AND parts, many OR terms")
            print(f"   • Optimized: {len(optimized_parts)} AND parts, max {max_or_terms} OR terms each")
            print(f"   • Strategy: Prioritized full phrases over abbreviations")
            print(f"   • Note: Full query used for OpenAlex/arXiv (no restrictions)")

        return optimized_query

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
        # REQUIRE API key for Semantic Scholar
        if not self.semantic_scholar_api_key:
            self._show_api_key_requirement()
            # Function above calls sys.exit(1), but return empty DataFrame as fallback
            return pd.DataFrame()

        print(f"\n🔍 Searching Semantic Scholar...")

        # Optimize query for Semantic Scholar's API limitations
        optimized_query = self._optimize_semantic_scholar_query(query, max_or_terms=3)

        print(f"   Query: {optimized_query}")
        print(f"   Years: {year_start}-{year_end}")

        papers = []
        offset = 0
        batch_size = 100  # API limit per request

        while len(papers) < limit:
            params = {
                'query': optimized_query,  # Use optimized query
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

    def _convert_to_arxiv_query(self, query: str) -> str:
        """
        Convert complex Boolean query to arXiv format.

        arXiv API doesn't support complex Boolean queries well.
        Strategy: Extract key terms and create simple query.

        Example:
            "(AI OR ML) AND risk" -> "all:AI AND all:machine AND all:learning AND all:risk"

        Args:
            query: Original Boolean query

        Returns:
            Simple arXiv-compatible query
        """
        # Extract all significant terms (remove parentheses and Boolean operators)
        import re

        # Remove parentheses
        clean_query = query.replace('(', '').replace(')', '')

        # Split by AND and OR
        terms = re.split(r'\s+(?:AND|OR)\s+', clean_query)

        # Filter out short terms (< 3 chars) and common words
        significant_terms = []
        for term in terms:
            term = term.strip()
            if len(term) >= 3 and term.lower() not in ['and', 'or', 'the', 'a', 'an']:
                significant_terms.append(term)

        # Limit to first 8 terms (arXiv has query length limits)
        significant_terms = significant_terms[:8]

        # Create arXiv query with all: prefix
        if significant_terms:
            arxiv_query = ' AND '.join([f'all:"{term}"' for term in significant_terms])
        else:
            arxiv_query = 'all:machine learning'  # Fallback

        return arxiv_query

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
            # Convert query to arXiv format
            arxiv_query = self._convert_to_arxiv_query(query)
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
            # Check if pdf_url column exists and has data
            with_pdf = df['pdf_url'].notna().sum() if 'pdf_url' in df.columns and papers > 0 else 0
            total_papers += papers
            total_with_pdf += with_pdf

            print(f"\n{db_name.upper()}:")
            print(f"  Papers found: {papers}")
            if papers > 0:
                print(f"  With PDF URLs: {with_pdf} ({with_pdf/papers*100:.1f}%)")
            else:
                print(f"  With PDF URLs: 0 (0.0%)")

        print(f"\nTOTAL:")
        print(f"  Papers: {total_papers}")
        if total_papers > 0:
            print(f"  With PDF URLs: {total_with_pdf} ({total_with_pdf/total_papers*100:.1f}%)")
        else:
            print(f"  With PDF URLs: 0 (0.0%)")
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
