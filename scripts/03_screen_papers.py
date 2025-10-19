#!/usr/bin/env python3
"""
Stage 3: AI-Assisted Paper Screening for Relevance

Uses Claude API to screen papers based on title and abstract relevance
to the research question. Implements PRISMA screening criteria.

Usage:
    python scripts/03_screen_papers.py --project <project_path> --question <research_question>

Example:
    python scripts/03_screen_papers.py \
        --project projects/2025-10-13_AI-Chatbots \
        --question "How do AI chatbots improve speaking skills in language learning?"
"""

import argparse
import pandas as pd
import sys
import os
from pathlib import Path
from typing import Dict, List
import anthropic
import time
from dotenv import load_dotenv
import yaml


class PaperScreener:
    """AI-assisted screening of papers for relevance"""

    def __init__(self, project_path: str, research_question: str):
        self.project_path = Path(project_path)
        self.research_question = research_question
        self.input_dir = self.project_path / "data" / "01_identification"
        self.output_dir = self.project_path / "data" / "02_screening"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load project config
        self.load_config()

        # Load API key
        load_dotenv()
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            print("❌ Error: ANTHROPIC_API_KEY not found in environment")
            print("   Add to .env file: ANTHROPIC_API_KEY=sk-ant-api03-xxxxx")
            sys.exit(1)

        self.client = anthropic.Anthropic(api_key=api_key)

    def load_config(self):
        """Load project configuration and set screening parameters based on project_type"""
        config_file = self.project_path / "config.yaml"
        if config_file.exists():
            with open(config_file, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = {}

        # Set screening thresholds based on project_type
        project_type = self.config.get('project_type', 'systematic_review')

        if project_type == 'knowledge_repository':
            # Lenient thresholds for comprehensive coverage
            self.screening_threshold = self.config.get('ai_prisma_rubric', {}).get('decision_confidence', {}).get('auto_include', 50)
            self.exclude_threshold = self.config.get('ai_prisma_rubric', {}).get('decision_confidence', {}).get('auto_exclude', 20)
            self.require_human_review = False
            print(f"   📊 Project type: Knowledge Repository (lenient filtering)")
        else:
            # Strict thresholds for systematic review
            self.screening_threshold = self.config.get('ai_prisma_rubric', {}).get('decision_confidence', {}).get('auto_include', 90)
            self.exclude_threshold = self.config.get('ai_prisma_rubric', {}).get('decision_confidence', {}).get('auto_exclude', 10)
            self.require_human_review = self.config.get('ai_prisma_rubric', {}).get('human_validation', {}).get('required', False)
            print(f"   📊 Project type: Systematic Review (strict filtering)")

        print(f"   ✓ Include threshold: {self.screening_threshold}%")
        print(f"   ✓ Exclude threshold: {self.exclude_threshold}%")
        print(f"   ✓ Human review: {'Required' if self.require_human_review else 'Not required'}")

    def load_papers(self) -> pd.DataFrame:
        """
        Load deduplicated papers

        Returns:
            DataFrame with deduplicated papers
        """
        print("\n📂 Loading deduplicated papers...")

        dedup_file = self.input_dir / "deduplicated.csv"
        if not dedup_file.exists():
            print(f"❌ Error: Deduplicated file not found: {dedup_file}")
            print("   Run deduplication first: python scripts/02_deduplicate.py")
            sys.exit(1)

        df = pd.read_csv(dedup_file)
        print(f"   ✓ Loaded {len(df)} papers")

        return df

    def screen_paper(self, title: str, abstract: str) -> Dict[str, any]:
        """
        Screen a single paper using Claude API

        Args:
            title: Paper title
            abstract: Paper abstract

        Returns:
            Dictionary with screening decision and reasoning
        """
        if pd.isna(abstract) or not abstract or abstract.strip() == "":
            return {
                'relevant': False,
                'confidence': 'low',
                'reasoning': 'No abstract available for screening'
            }

        prompt = f"""You are a research assistant conducting a systematic literature review.

Research Question: {self.research_question}

Paper Title: {title}

Abstract: {abstract}

Task: Determine if this paper is relevant to the research question.

Respond in JSON format:
{{
  "relevant": true/false,
  "confidence": "high/medium/low",
  "reasoning": "Brief explanation (1-2 sentences)"
}}

Screening Criteria:
- INCLUDE if the paper directly addresses the research question
- INCLUDE if the paper provides relevant methodology or theoretical framework
- EXCLUDE if the paper is off-topic or only tangentially related
- EXCLUDE if the abstract is too vague to determine relevance"""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            result_text = response.content[0].text.strip()

            # Parse JSON response
            import json
            result = json.loads(result_text)

            return result

        except Exception as e:
            print(f"   ⚠️  API Error: {e}")
            return {
                'relevant': None,
                'confidence': 'error',
                'reasoning': str(e)
            }

    def screen_all_papers(self, df: pd.DataFrame, batch_size: int = 50) -> pd.DataFrame:
        """
        Screen all papers with progress tracking

        Args:
            df: DataFrame with papers to screen
            batch_size: Save progress every N papers

        Returns:
            DataFrame with screening results
        """
        print("\n" + "="*60)
        print("🔍 PAPER SCREENING")
        print("="*60)
        print(f"\nResearch Question: {self.research_question}")
        print(f"Total papers to screen: {len(df)}")
        print(f"Estimated time: {len(df) * 3 / 60:.1f} minutes")
        print(f"Estimated cost: ${len(df) * 0.01:.2f} (Claude API)")

        # Check if screening already in progress
        progress_file = self.output_dir / "screening_progress.csv"
        if progress_file.exists():
            print(f"\n✓ Found existing progress file")
            df_progress = pd.read_csv(progress_file)
            print(f"  Already screened: {len(df_progress)} papers")

            # Merge with original dataframe
            df = df.merge(
                df_progress[['title', 'relevant', 'confidence', 'reasoning']],
                on='title',
                how='left',
                suffixes=('', '_screened')
            )

            # Continue from where we left off
            df_to_screen = df[df['relevant'].isna()]
            already_screened = len(df) - len(df_to_screen)
            print(f"  Remaining to screen: {len(df_to_screen)}")
        else:
            df_to_screen = df.copy()
            already_screened = 0

        if len(df_to_screen) == 0:
            print("\n✓ All papers already screened!")
            return df

        print(f"\n⏳ Starting screening...")

        results = []
        for idx, row in df_to_screen.iterrows():
            # Screen paper
            result = self.screen_paper(row['title'], row['abstract'])

            # Add to results
            results.append({
                'title': row['title'],
                'relevant': result['relevant'],
                'confidence': result['confidence'],
                'reasoning': result['reasoning']
            })

            # Progress indicator
            screened_count = len(results) + already_screened
            print(f"   [{screened_count}/{len(df)}] {row['title'][:60]}... → {result['relevant']}")

            # Save progress periodically
            if len(results) % batch_size == 0:
                df_batch = pd.DataFrame(results)
                if already_screened > 0:
                    # Append to existing progress
                    df_existing = pd.read_csv(progress_file)
                    df_batch = pd.concat([df_existing, df_batch], ignore_index=True)
                df_batch.to_csv(progress_file, index=False)
                print(f"   💾 Progress saved ({screened_count}/{len(df)})")

            # Rate limiting
            time.sleep(1)

        # Save final results
        df_results = pd.DataFrame(results)
        if already_screened > 0:
            df_existing = pd.read_csv(progress_file)
            df_results = pd.concat([df_existing, df_results], ignore_index=True)
        df_results.to_csv(progress_file, index=False)

        # Merge with original dataframe
        df = df.merge(
            df_results[['title', 'relevant', 'confidence', 'reasoning']],
            on='title',
            how='left',
            suffixes=('', '_screened')
        )

        return df

    def save_results(self, df: pd.DataFrame):
        """
        Save screening results with statistics

        Args:
            df: DataFrame with screening results
        """
        print("\n" + "="*60)
        print("📊 SCREENING RESULTS")
        print("="*60)

        # Calculate statistics
        total = len(df)
        relevant = df['relevant'].sum()
        irrelevant = (df['relevant'] == False).sum()
        errors = df['relevant'].isna().sum()

        print(f"\nTotal papers: {total}")
        print(f"Relevant: {relevant} ({relevant/total*100:.1f}%)")
        print(f"Irrelevant: {irrelevant} ({irrelevant/total*100:.1f}%)")
        if errors > 0:
            print(f"Errors: {errors} ({errors/total*100:.1f}%)")

        # Confidence breakdown
        print(f"\nConfidence Levels:")
        confidence_counts = df['confidence'].value_counts()
        for conf, count in confidence_counts.items():
            print(f"  {conf}: {count} ({count/total*100:.1f}%)")

        # Save relevant papers
        df_relevant = df[df['relevant'] == True].copy()
        relevant_file = self.output_dir / "relevant_papers.csv"
        df_relevant.to_csv(relevant_file, index=False)
        print(f"\n💾 Relevant papers saved to: {relevant_file}")

        # Save excluded papers
        df_excluded = df[df['relevant'] == False].copy()
        excluded_file = self.output_dir / "excluded_papers.csv"
        df_excluded.to_csv(excluded_file, index=False)
        print(f"💾 Excluded papers saved to: {excluded_file}")

        # Save all with screening results
        all_file = self.output_dir / "all_screened_papers.csv"
        df.to_csv(all_file, index=False)
        print(f"💾 All papers with screening: {all_file}")

        print("="*60)

        # Show some examples
        if relevant > 0:
            print("\n📋 Sample Relevant Papers:")
            for idx, row in df_relevant.head(3).iterrows():
                print(f"\n  • {row['title']}")
                print(f"    Confidence: {row['confidence']}")
                print(f"    Reasoning: {row['reasoning']}")

        if irrelevant > 0:
            print("\n📋 Sample Excluded Papers:")
            for idx, row in df_excluded.head(2).iterrows():
                print(f"\n  • {row['title']}")
                print(f"    Reasoning: {row['reasoning']}")


def main():
    parser = argparse.ArgumentParser(
        description="AI-assisted screening of papers for relevance"
    )
    parser.add_argument(
        '--project',
        required=True,
        help='Path to project directory'
    )
    parser.add_argument(
        '--question',
        required=True,
        help='Research question for screening'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=50,
        help='Save progress every N papers (default: 50)'
    )

    args = parser.parse_args()

    # Validate project path
    project_path = Path(args.project)
    if not project_path.exists():
        print(f"❌ Error: Project path does not exist: {project_path}")
        sys.exit(1)

    # Initialize screener
    screener = PaperScreener(args.project, args.question)

    # Load papers
    df = screener.load_papers()

    # Screen papers
    df = screener.screen_all_papers(df, batch_size=args.batch_size)

    # Save results
    screener.save_results(df)

    print("\n✨ Next step: Download PDFs for relevant papers")
    print(f"   python scripts/04_download_pdfs.py --project {args.project}")


if __name__ == '__main__':
    main()
