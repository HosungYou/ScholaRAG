#!/usr/bin/env python3
"""
Multiple query strategy for Semantic Scholar to overcome API limitations
"""

import os
import sys
import time
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
project_dir = Path("projects/2025-11-21_AI-Tools-Workplace-Innovation")
env_file = project_dir / ".env"
if env_file.exists():
    load_dotenv(env_file)

API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
if not API_KEY:
    print("❌ ERROR: SEMANTIC_SCHOLAR_API_KEY not found")
    sys.exit(1)

# Multiple targeted queries to maximize coverage
QUERIES = [
    # Query 1: AI + innovation + workplace
    {
        "query": "artificial intelligence AND innovation AND workplace",
        "description": "AI + innovation + workplace"
    },
    # Query 2: Machine learning + creativity + employee
    {
        "query": "machine learning AND creativity AND employee",
        "description": "ML + creativity + employee"
    },
    # Query 3: AI adoption + innovative behavior
    {
        "query": "AI adoption AND innovative behavior",
        "description": "AI adoption + innovative behavior"
    },
    # Query 4: Automation + innovative work behavior
    {
        "query": "automation AND innovative work behavior",
        "description": "Automation + IWB"
    },
    # Query 5: AI use + employee innovation
    {
        "query": "artificial intelligence use AND employee innovation",
        "description": "AI use + employee innovation"
    },
    # Query 6: Machine learning + idea generation + organization
    {
        "query": "machine learning AND idea generation AND organization",
        "description": "ML + idea generation + org"
    },
    # Query 7: AI + creative performance + work
    {
        "query": "artificial intelligence AND creative performance AND work",
        "description": "AI + creative performance + work"
    },
]

def fetch_semantic_scholar(query: str, year_start: int = 2015, year_end: int = 2025):
    """Fetch papers from Semantic Scholar with given query"""

    papers = []
    offset = 0
    limit = 100
    max_papers = 1000  # Per query

    headers = {
        'x-api-key': API_KEY
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

def main():
    print("🔍 Searching Semantic Scholar with multiple targeted queries...")
    print(f"   Total queries: {len(QUERIES)}")
    print()

    all_papers = []

    for idx, query_info in enumerate(QUERIES, 1):
        query = query_info["query"]
        desc = query_info["description"]

        print(f"   [{idx}/{len(QUERIES)}] {desc}")
        print(f"       Query: {query}")

        papers = fetch_semantic_scholar(query)

        print(f"       ✓ Found {len(papers)} papers")
        all_papers.extend(papers)

        # Delay between queries
        if idx < len(QUERIES):
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

        # Save to CSV
        output_file = project_dir / "data/01_identification/semantic_scholar_results.csv"
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
        print("=" * 60)
    else:
        print("   ⚠️  No papers found")

if __name__ == "__main__":
    main()
