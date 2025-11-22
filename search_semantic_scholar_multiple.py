#!/usr/bin/env python3
"""
Multiple query strategy for Semantic Scholar to overcome API limitations

Usage:
    python search_semantic_scholar_multiple.py --project projects/your-project

With custom queries:
    python search_semantic_scholar_multiple.py --project projects/your-project \
        --queries "AI AND innovation" "ML AND creativity"

With year range:
    python search_semantic_scholar_multiple.py --project projects/your-project \
        --year-start 2020 --year-end 2025
"""

import os
import sys
import time
import argparse
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

def fetch_semantic_scholar(query: str, api_key: str, year_start: int, year_end: int):
    """Fetch papers from Semantic Scholar with given query"""

    papers = []
    offset = 0
    limit = 100
    max_papers = 1000  # Per query

    headers = {
        'x-api-key': api_key
    }

    while len(papers) < max_papers:
        params = {
            'query': query,
            'year': f'{year_start}-{year_end}',
            'fields': 'title,abstract,authors,year,citationCount,openAccessPdf,externalIds',
            'offset': offset,
            'limit': limit
        }

        try:
            response = requests.get(
                'https://api.semanticscholar.org/graph/v1/paper/search',
                params=params,
                headers=headers,
                timeout=30
            )

            if response.status_code != 200:
                print(f"   ⚠️  API returned status {response.status_code}")
                break

            data = response.json()

            if 'data' not in data or not data['data']:
                break

            for paper in data['data']:
                # Extract PDF URL
                pdf_url = None
                if paper.get('openAccessPdf'):
                    pdf_url = paper['openAccessPdf'].get('url')

                # Extract authors
                authors = []
                if paper.get('authors'):
                    authors = [a.get('name', '') for a in paper['authors'] if a.get('name')]

                # Extract DOI
                doi = None
                if paper.get('externalIds'):
                    doi = paper['externalIds'].get('DOI')

                papers.append({
                    'title': paper.get('title', ''),
                    'abstract': paper.get('abstract', ''),
                    'authors': '; '.join(authors),
                    'year': paper.get('year'),
                    'citations': paper.get('citationCount', 0),
                    'doi': doi,
                    'pdf_url': pdf_url,
                    'source': 'Semantic Scholar',
                    'query_used': query
                })

            # Check if there are more results
            if 'total' in data and offset + limit >= data['total']:
                break
            if len(data['data']) < limit:
                break

            offset += limit

            # Rate limiting: 10 requests per second for API key users
            time.sleep(0.15)

        except Exception as e:
            print(f"   ⚠️  Error: {str(e)}")
            break

    return papers

def get_default_queries():
    """Get default queries for AI + workplace innovation"""
    return [
        {
            "query": "artificial intelligence AND innovation AND workplace",
            "description": "AI + innovation + workplace"
        },
        {
            "query": "machine learning AND creativity AND employee",
            "description": "ML + creativity + employee"
        },
        {
            "query": "AI adoption AND innovative behavior",
            "description": "AI adoption + innovative behavior"
        },
        {
            "query": "automation AND innovative work behavior",
            "description": "Automation + IWB"
        },
        {
            "query": "artificial intelligence use AND employee innovation",
            "description": "AI use + employee innovation"
        },
        {
            "query": "machine learning AND idea generation AND organization",
            "description": "ML + idea generation + org"
        },
        {
            "query": "artificial intelligence AND creative performance AND work",
            "description": "AI + creative performance + work"
        },
    ]

def main():
    parser = argparse.ArgumentParser(
        description="Fetch papers from Semantic Scholar using multiple targeted queries"
    )
    parser.add_argument(
        '--project',
        required=True,
        help='Path to project directory (e.g., projects/2025-10-13_AI-Chatbots)'
    )
    parser.add_argument(
        '--queries',
        nargs='+',
        help='Custom query strings (e.g., "AI AND innovation" "ML AND creativity")'
    )
    parser.add_argument(
        '--year-start',
        type=int,
        default=2015,
        help='Start year for paper search (default: 2015)'
    )
    parser.add_argument(
        '--year-end',
        type=int,
        default=2025,
        help='End year for paper search (default: 2025)'
    )

    args = parser.parse_args()

    # Validate project path
    project_dir = Path(args.project)
    if not project_dir.exists():
        print(f"❌ ERROR: Project directory does not exist: {project_dir}")
        sys.exit(1)

    # Load environment variables
    env_file = project_dir / ".env"
    if env_file.exists():
        load_dotenv(env_file, override=True)
    else:
        print(f"⚠️  WARNING: .env file not found at {env_file}")
        print("   Trying to load from system environment...")

    api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    if not api_key:
        print("❌ ERROR: SEMANTIC_SCHOLAR_API_KEY not found")
        print("   Please add it to .env file or set as environment variable")
        sys.exit(1)

    # Prepare queries
    if args.queries:
        queries = [{"query": q, "description": q} for q in args.queries]
    else:
        print("ℹ️  No custom queries provided, using default queries...")
        queries = get_default_queries()

    print("\n🔍 Searching Semantic Scholar with multiple targeted queries...")
    print(f"   Project: {project_dir}")
    print(f"   Year range: {args.year_start}-{args.year_end}")
    print(f"   Total queries: {len(queries)}")
    print()

    all_papers = []

    for idx, query_info in enumerate(queries, 1):
        query = query_info["query"]
        desc = query_info["description"]

        print(f"   [{idx}/{len(queries)}] {desc}")
        print(f"       Query: {query}")

        papers = fetch_semantic_scholar(
            query,
            api_key,
            args.year_start,
            args.year_end
        )

        print(f"       ✓ Found {len(papers)} papers")
        all_papers.extend(papers)

        # Delay between queries
        if idx < len(queries):
            time.sleep(1)

    print()
    print(f"📊 Total papers retrieved: {len(all_papers)}")

    # Remove duplicates based on title (case-insensitive)
    df = pd.DataFrame(all_papers)

    if len(df) > 0:
        print(f"   Removing duplicates...")

        # Remove duplicates by title (case-insensitive)
        df['title_lower'] = df['title'].str.lower().str.strip()
        df_unique = df.drop_duplicates(subset=['title_lower'], keep='first')
        df_unique = df_unique.drop(columns=['title_lower'])

        print(f"   ✓ Unique papers: {len(df_unique)} (removed {len(df) - len(df_unique)} duplicates)")

        # Create output directory if it doesn't exist
        output_dir = project_dir / "data/01_identification"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save to CSV
        output_file = output_dir / "semantic_scholar_results.csv"
        df_unique.to_csv(output_file, index=False)

        print(f"   💾 Saved to {output_file}")

        # Statistics
        with_pdf = df_unique['pdf_url'].notna().sum()
        pdf_percentage = (with_pdf / len(df_unique) * 100) if len(df_unique) > 0 else 0

        print()
        print("=" * 60)
        print("📊 SEMANTIC SCHOLAR SEARCH SUMMARY")
        print("=" * 60)
        print(f"  Papers found: {len(df_unique)}")
        print(f"  With PDF URLs: {with_pdf} ({pdf_percentage:.1f}%)")
        print(f"  Year range: {args.year_start}-{args.year_end}")
        print("=" * 60)

        print("\n✨ Next step: Run deduplication")
        print(f"   python scripts/02_deduplicate.py --project {args.project}")

    else:
        print("   ⚠️  No papers found")

if __name__ == "__main__":
    main()
