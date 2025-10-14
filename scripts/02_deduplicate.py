#!/usr/bin/env python3
"""
Stage 2: Deduplication of Papers from Multiple Databases

Removes duplicate papers across Semantic Scholar, OpenAlex, and arXiv results.
Uses multiple matching strategies: DOI exact match, title fuzzy matching, and arXiv ID.

Usage:
    python scripts/02_deduplicate.py --project <project_path>

Example:
    python scripts/02_deduplicate.py --project projects/2025-10-13_AI-Chatbots
"""

import argparse
import pandas as pd
import sys
from pathlib import Path
from typing import List, Dict, Tuple
from difflib import SequenceMatcher
import re


class PaperDeduplicator:
    """Remove duplicate papers across multiple database sources"""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.input_dir = self.project_path / "data" / "01_identification"
        self.output_dir = self.input_dir  # Save in same directory

        # Deduplication thresholds
        self.title_similarity_threshold = 0.85  # 85% title similarity = duplicate

    def load_results(self) -> pd.DataFrame:
        """
        Load all database results and combine into single DataFrame

        Returns:
            Combined DataFrame with all papers from all sources
        """
        print("\n📂 Loading database results...")

        all_papers = []

        # Load Semantic Scholar results
        ss_file = self.input_dir / "semantic_scholar_results.csv"
        if ss_file.exists():
            df_ss = pd.read_csv(ss_file)
            print(f"   ✓ Semantic Scholar: {len(df_ss)} papers")
            all_papers.append(df_ss)
        else:
            print(f"   ⚠️  Semantic Scholar results not found")

        # Load OpenAlex results
        oa_file = self.input_dir / "openalex_results.csv"
        if oa_file.exists():
            df_oa = pd.read_csv(oa_file)
            print(f"   ✓ OpenAlex: {len(df_oa)} papers")
            all_papers.append(df_oa)
        else:
            print(f"   ⚠️  OpenAlex results not found")

        # Load arXiv results
        arxiv_file = self.input_dir / "arxiv_results.csv"
        if arxiv_file.exists():
            df_arxiv = pd.read_csv(arxiv_file)
            print(f"   ✓ arXiv: {len(df_arxiv)} papers")
            all_papers.append(df_arxiv)
        else:
            print(f"   ⚠️  arXiv results not found")

        if not all_papers:
            print("\n❌ Error: No database results found!")
            print(f"   Expected files in: {self.input_dir}")
            sys.exit(1)

        # Combine all dataframes
        combined = pd.concat(all_papers, ignore_index=True)
        print(f"\n   Total papers before deduplication: {len(combined)}")

        return combined

    def normalize_title(self, title: str) -> str:
        """
        Normalize title for fuzzy matching

        Args:
            title: Original paper title

        Returns:
            Normalized title (lowercase, no punctuation, no extra spaces)
        """
        if pd.isna(title) or not isinstance(title, str):
            return ""

        # Convert to lowercase
        title = title.lower()

        # Remove punctuation and special characters
        title = re.sub(r'[^\w\s]', ' ', title)

        # Remove extra whitespace
        title = ' '.join(title.split())

        return title

    def calculate_title_similarity(self, title1: str, title2: str) -> float:
        """
        Calculate similarity ratio between two titles using SequenceMatcher

        Args:
            title1: First title
            title2: Second title

        Returns:
            Similarity ratio (0.0 to 1.0)
        """
        norm1 = self.normalize_title(title1)
        norm2 = self.normalize_title(title2)

        if not norm1 or not norm2:
            return 0.0

        return SequenceMatcher(None, norm1, norm2).ratio()

    def deduplicate_by_doi(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
        """
        Remove exact duplicates based on DOI

        Args:
            df: DataFrame with papers

        Returns:
            Tuple of (deduplicated DataFrame, number of duplicates removed)
        """
        print("\n🔍 Stage 1: Removing DOI duplicates...")

        initial_count = len(df)

        # Keep only papers with DOI for this stage
        df_with_doi = df[df['doi'].notna()].copy()
        df_without_doi = df[df['doi'].isna()].copy()

        # Remove duplicates by DOI, keep first occurrence
        # Prioritize: Semantic Scholar > OpenAlex > arXiv
        source_priority = {'Semantic Scholar': 0, 'OpenAlex': 1, 'arXiv': 2}
        df_with_doi['source_priority'] = df_with_doi['source'].map(source_priority)
        df_with_doi = df_with_doi.sort_values('source_priority')

        df_with_doi_dedup = df_with_doi.drop_duplicates(subset='doi', keep='first')
        df_with_doi_dedup = df_with_doi_dedup.drop('source_priority', axis=1)

        # Combine back with papers without DOI
        df_dedup = pd.concat([df_with_doi_dedup, df_without_doi], ignore_index=True)

        removed = initial_count - len(df_dedup)
        print(f"   Removed {removed} exact DOI duplicates")
        print(f"   Remaining papers: {len(df_dedup)}")

        return df_dedup, removed

    def deduplicate_by_arxiv_id(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
        """
        Remove duplicates based on arXiv ID

        Args:
            df: DataFrame with papers

        Returns:
            Tuple of (deduplicated DataFrame, number of duplicates removed)
        """
        print("\n🔍 Stage 2: Removing arXiv ID duplicates...")

        initial_count = len(df)

        # Check if arxiv_id column exists
        if 'arxiv_id' not in df.columns:
            print("   No arXiv ID column found, skipping...")
            return df, 0

        # Keep only papers with arXiv ID for this stage
        df_with_arxiv = df[df['arxiv_id'].notna()].copy()
        df_without_arxiv = df[df['arxiv_id'].isna()].copy()

        # Remove duplicates by arXiv ID
        source_priority = {'arXiv': 0, 'Semantic Scholar': 1, 'OpenAlex': 2}
        df_with_arxiv['source_priority'] = df_with_arxiv['source'].map(source_priority)
        df_with_arxiv = df_with_arxiv.sort_values('source_priority')

        df_with_arxiv_dedup = df_with_arxiv.drop_duplicates(subset='arxiv_id', keep='first')
        df_with_arxiv_dedup = df_with_arxiv_dedup.drop('source_priority', axis=1)

        # Combine back
        df_dedup = pd.concat([df_with_arxiv_dedup, df_without_arxiv], ignore_index=True)

        removed = initial_count - len(df_dedup)
        print(f"   Removed {removed} arXiv ID duplicates")
        print(f"   Remaining papers: {len(df_dedup)}")

        return df_dedup, removed

    def deduplicate_by_title(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
        """
        Remove fuzzy duplicates based on title similarity

        Args:
            df: DataFrame with papers

        Returns:
            Tuple of (deduplicated DataFrame, number of duplicates removed)
        """
        print("\n🔍 Stage 3: Removing title fuzzy duplicates...")
        print(f"   Similarity threshold: {self.title_similarity_threshold}")

        initial_count = len(df)

        # Create list to track which papers to keep
        keep_indices = []
        removed_count = 0

        # Compare each paper with all previous papers
        for i in range(len(df)):
            title_i = df.iloc[i]['title']
            is_duplicate = False

            for j in keep_indices:
                title_j = df.iloc[j]['title']
                similarity = self.calculate_title_similarity(title_i, title_j)

                if similarity >= self.title_similarity_threshold:
                    is_duplicate = True
                    removed_count += 1
                    break

            if not is_duplicate:
                keep_indices.append(i)

            # Progress indicator for large datasets
            if (i + 1) % 100 == 0:
                print(f"   Processed {i + 1}/{len(df)} papers...", end='\r')

        print(f"   Processed {len(df)}/{len(df)} papers...     ")

        # Keep only non-duplicate papers
        df_dedup = df.iloc[keep_indices].copy()

        print(f"   Removed {removed_count} title fuzzy duplicates")
        print(f"   Remaining papers: {len(df_dedup)}")

        return df_dedup, removed_count

    def deduplicate(self) -> pd.DataFrame:
        """
        Run complete deduplication pipeline

        Returns:
            Deduplicated DataFrame
        """
        print("\n" + "="*60)
        print("🧹 PAPER DEDUPLICATION")
        print("="*60)

        # Load all papers
        df = self.load_results()
        initial_count = len(df)

        # Stage 1: DOI exact match
        df, doi_removed = self.deduplicate_by_doi(df)

        # Stage 2: arXiv ID match
        df, arxiv_removed = self.deduplicate_by_arxiv_id(df)

        # Stage 3: Title fuzzy match
        df, title_removed = self.deduplicate_by_title(df)

        # Summary
        final_count = len(df)
        total_removed = initial_count - final_count

        print("\n" + "="*60)
        print("📊 DEDUPLICATION SUMMARY")
        print("="*60)
        print(f"\nInitial papers: {initial_count}")
        print(f"Removed by DOI: {doi_removed}")
        print(f"Removed by arXiv ID: {arxiv_removed}")
        print(f"Removed by title similarity: {title_removed}")
        print(f"\nTotal removed: {total_removed} ({total_removed/initial_count*100:.1f}%)")
        print(f"Final unique papers: {final_count}")

        # Save deduplicated results
        output_file = self.output_dir / "deduplicated.csv"
        df.to_csv(output_file, index=False)
        print(f"\n💾 Saved to: {output_file}")

        # Additional statistics
        print("\n" + "="*60)
        print("📈 DEDUPLICATED DATASET STATISTICS")
        print("="*60)

        print(f"\nBy Source:")
        source_counts = df['source'].value_counts()
        for source, count in source_counts.items():
            print(f"  {source}: {count} ({count/final_count*100:.1f}%)")

        print(f"\nBy Year:")
        year_counts = df['year'].value_counts().sort_index()
        for year, count in year_counts.head(10).items():
            print(f"  {int(year)}: {count}")

        print(f"\nWith PDF URLs:")
        pdf_count = df['pdf_url'].notna().sum()
        print(f"  {pdf_count} papers ({pdf_count/final_count*100:.1f}%)")

        print(f"\nWith DOI:")
        doi_count = df['doi'].notna().sum()
        print(f"  {doi_count} papers ({doi_count/final_count*100:.1f}%)")

        print("="*60)

        return df


def main():
    parser = argparse.ArgumentParser(
        description="Deduplicate papers from multiple database sources"
    )
    parser.add_argument(
        '--project',
        required=True,
        help='Path to project directory (e.g., projects/2025-10-13_AI-Chatbots)'
    )
    parser.add_argument(
        '--threshold',
        type=float,
        default=0.85,
        help='Title similarity threshold for fuzzy matching (default: 0.85)'
    )

    args = parser.parse_args()

    # Validate project path
    project_path = Path(args.project)
    if not project_path.exists():
        print(f"❌ Error: Project path does not exist: {project_path}")
        sys.exit(1)

    # Initialize deduplicator
    deduplicator = PaperDeduplicator(args.project)
    deduplicator.title_similarity_threshold = args.threshold

    # Run deduplication
    df = deduplicator.deduplicate()

    print("\n✨ Next step: Screen papers for relevance")
    print(f"   python scripts/03_screen_papers.py --project {args.project}")


if __name__ == '__main__':
    main()
