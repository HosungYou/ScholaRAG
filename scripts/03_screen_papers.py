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
import asyncio
from concurrent.futures import ThreadPoolExecutor


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

        # Load API key from project .env file
        env_path = self.project_path / ".env"
        if env_path.exists():
            load_dotenv(env_path)
        else:
            load_dotenv()  # Try current directory

        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            print("❌ Error: ANTHROPIC_API_KEY not found in environment")
            print("   Add to .env file: ANTHROPIC_API_KEY=sk-ant-api03-xxxxx")
            sys.exit(1)

        self.client = anthropic.Anthropic(
            api_key=api_key,
            default_headers={"anthropic-beta": "prompt-caching-2024-07-31"}
        )

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
            # Lenient threshold for comprehensive coverage
            self.score_threshold_include = self.config.get('ai_prisma_rubric', {}).get('score_threshold', {}).get('auto_include', 25)
            self.score_threshold_exclude = self.config.get('ai_prisma_rubric', {}).get('score_threshold', {}).get('auto_exclude', 0)
            self.require_human_review = False
            print(f"   📊 Project type: Knowledge Repository (lenient filtering)")
        else:
            # Strict threshold for systematic review
            self.score_threshold_include = self.config.get('ai_prisma_rubric', {}).get('score_threshold', {}).get('auto_include', 40)
            self.score_threshold_exclude = self.config.get('ai_prisma_rubric', {}).get('score_threshold', {}).get('auto_exclude', 0)
            self.require_human_review = self.config.get('ai_prisma_rubric', {}).get('human_validation', {}).get('required', False)
            print(f"   📊 Project type: Systematic Review (strict filtering)")

        print(f"   ✓ Include threshold: total_score ≥ {self.score_threshold_include}")
        print(f"   ✓ Exclude threshold: total_score < {self.score_threshold_exclude}")
        print(f"   ✓ Human review: {'Required' if self.require_human_review else 'Not required'}")

    def get_cached_system_prompt(self) -> str:
        """
        Get static system prompt for caching (unchanged across all papers)
        This is cached by Anthropic API to reduce latency and cost
        """
        return f"""You are a research assistant conducting PRISMA 2020 systematic literature review.

Research Question: {self.research_question}

TASK: Score paper relevance using 6-dimension rubric. Respond in JSON only.

SCORING RUBRIC:

1. DOMAIN (0-10): Target population/context relevance
   10=direct match, 7-9=strong overlap, 4-6=partial, 1-3=tangential, 0=unrelated

2. INTERVENTION (0-10): Specific technology/tool focus
   10=primary focus, 7-9=major component, 4-6=mentioned, 1-3=vague, 0=absent

3. METHOD (0-5): Study design rigor
   5=RCT/experimental, 4=quasi-experimental, 3=mixed/survey, 2=qualitative, 1=descriptive, 0=theory/opinion

4. OUTCOMES (0-10): Measured results clarity
   10=explicit+rigorous, 7-9=clear, 4-6=mentioned, 1-3=implied, 0=none

5. EXCLUSION (-20 to 0): Penalties
   -20=wrong domain, -15=wrong population, -10=review/editorial, -5=abstract only, 0=none
   (penalties stack, max -20)

6. TITLE BONUS (0 or 10): Both domain AND intervention in title?
   10=yes, 0=no

TOTAL SCORE RANGE: -20 to 50 points

REQUIREMENTS:
- Provide direct quotes from abstract in evidence_quotes (no labels/prefixes)
- Only use information explicitly stated
- If uncertain, use lower scores
- Calculate total_score = sum of all 6 scores

DECISION RULES:
- total_score ≥ {self.score_threshold_include} → "auto-include"
- total_score < {self.score_threshold_exclude} → "auto-exclude"
- Otherwise → "human-review"

JSON format:
{{
  "scores": {{"domain": <0-10>, "intervention": <0-10>, "method": <0-5>, "outcomes": <0-10>, "exclusion": <-20 to 0>, "title_bonus": <0 or 10>}},
  "total_score": <sum>,
  "decision": "auto-include"|"auto-exclude"|"human-review",
  "reasoning": "Brief explanation (2-3 sentences)",
  "evidence_quotes": ["quote1", "quote2", ...]
}}"""

    def build_paper_content(self, title: str, abstract: str) -> str:
        """
        Build dynamic paper content (changes for each paper)
        """
        return f"""Title: {title}

Abstract: {abstract}"""

    def validate_evidence_grounding(self, quotes: List[str], abstract: str) -> bool:
        """
        Validate that AI evidence quotes are actually in the abstract

        Args:
            quotes: List of quoted evidence from AI
            abstract: Original paper abstract

        Returns:
            True if all quotes are grounded, False if hallucination detected
        """
        if not quotes:
            return True  # No quotes to validate

        for quote in quotes:
            # Remove any labels/prefixes that Claude might add
            # Pattern: "Label: 'actual quote'" or "Label: actual quote"
            clean_quote = quote

            # Remove patterns like "Domain alignment: ", "Evidence: ", etc.
            if ':' in quote:
                # Check if this looks like "Label: 'quote'" or "Label: quote"
                parts = quote.split(':', 1)
                if len(parts) == 2:
                    potential_quote = parts[1].strip()
                    # Remove surrounding quotes if present
                    if potential_quote.startswith("'") and potential_quote.endswith("'"):
                        clean_quote = potential_quote[1:-1]
                    elif potential_quote.startswith('"') and potential_quote.endswith('"'):
                        clean_quote = potential_quote[1:-1]
                    else:
                        clean_quote = potential_quote

            # Check if cleaned quote exists in abstract (case-insensitive)
            if clean_quote.lower().strip() not in abstract.lower():
                print(f"   ⚠️  Hallucination detected: \"{quote[:50]}...\"")
                return False
        return True

    def determine_decision(self, total_score: int) -> str:
        """
        Determine decision based on total score only

        Args:
            total_score: Total 6-dimension score (-20 to 50)

        Returns:
            Decision: "auto-include", "auto-exclude", or "human-review"

        Decision rules (configurable based on project_type):
        - Knowledge Repository: score ≥ 25 → auto-include, < 0 → auto-exclude
        - Systematic Review: score ≥ 40 → auto-include, < 0 → auto-exclude
        - Otherwise → human-review
        """
        if total_score >= self.score_threshold_include:
            return 'auto-include'
        elif total_score < self.score_threshold_exclude:
            return 'auto-exclude'
        else:
            return 'human-review'

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
        Screen a single paper using AI-PRISMA with prompt caching

        Uses Anthropic's prompt caching to cache static rubric (90% cost reduction)

        Args:
            title: Paper title
            abstract: Paper abstract

        Returns:
            Dictionary with scores, decision, and evidence
        """
        if pd.isna(abstract) or not abstract or abstract.strip() == "":
            return {
                'scores': {
                    'domain': 0,
                    'intervention': 0,
                    'method': 0,
                    'outcomes': 0,
                    'exclusion': 0,
                    'title_bonus': 0
                },
                'total_score': 0,
                'decision': 'auto-exclude',
                'reasoning': 'No abstract available for screening',
                'evidence_quotes': []
            }

        try:
            # Use prompt caching: static system prompt is cached across all papers
            response = self.client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=1000,
                system=[
                    {
                        "type": "text",
                        "text": self.get_cached_system_prompt(),
                        "cache_control": {"type": "ephemeral"}
                    }
                ],
                messages=[
                    {
                        "role": "user",
                        "content": self.build_paper_content(title, abstract)
                    }
                ]
            )

            result_text = response.content[0].text.strip()

            # Remove markdown code blocks if present
            if result_text.startswith('```'):
                lines = result_text.split('\n')
                if lines[0].startswith('```'):
                    lines = lines[1:]
                if lines and lines[-1].strip() == '```':
                    lines = lines[:-1]
                result_text = '\n'.join(lines)

            # Parse JSON response
            import json
            decoder = json.JSONDecoder()
            result, end_idx = decoder.raw_decode(result_text)

            # Validate evidence grounding
            if not self.validate_evidence_grounding(result.get('evidence_quotes', []), abstract):
                result['decision'] = 'human-review'
                result['reasoning'] += " [FLAGGED: Potential hallucination in evidence]"
            else:
                result['decision'] = self.determine_decision(result['total_score'])

            return result

        except Exception as e:
            return {
                'scores': {'domain': 0, 'intervention': 0, 'method': 0,
                          'outcomes': 0, 'exclusion': 0, 'title_bonus': 0},
                'total_score': 0,
                'decision': 'error',
                'reasoning': str(e),
                'evidence_quotes': []
            }

    def screen_all_papers(self, df: pd.DataFrame, batch_size: int = 50, max_workers: int = 8) -> pd.DataFrame:
        """
        Screen all papers with parallel processing and progress tracking

        Uses ThreadPoolExecutor for 6-8x speedup via concurrent API calls

        Args:
            df: DataFrame with papers to screen
            batch_size: Save progress every N papers
            max_workers: Number of parallel workers (default: 8)

        Returns:
            DataFrame with screening results
        """
        print("\n" + "="*60)
        print("🔍 PAPER SCREENING (OPTIMIZED)")
        print("="*60)
        print(f"\nResearch Question: {self.research_question}")
        print(f"Total papers to screen: {len(df)}")
        print(f"⚡ Parallel workers: {max_workers}")
        print(f"⚡ Estimated time: {len(df) / (max_workers * 20):.1f} minutes (optimized)")
        print(f"💰 Estimated cost: ${len(df) * 0.002:.2f} (with caching)")

        # Check if screening already in progress
        progress_file = self.output_dir / "screening_progress.csv"
        if progress_file.exists():
            print(f"\n✓ Found existing progress file")
            df_progress = pd.read_csv(progress_file)
            print(f"  Already screened: {len(df_progress)} papers")

            # Merge with original dataframe
            df = df.merge(
                df_progress[['title', 'total_score', 'decision', 'reasoning',
                            'domain_score', 'intervention_score', 'method_score',
                            'outcomes_score', 'exclusion_score', 'title_bonus']],
                on='title',
                how='left',
                suffixes=('', '_screened')
            )

            # Continue from where we left off
            df_to_screen = df[df['decision'].isna()]
            already_screened = len(df) - len(df_to_screen)
            print(f"  Remaining to screen: {len(df_to_screen)}")
        else:
            df_to_screen = df.copy()
            already_screened = 0

        if len(df_to_screen) == 0:
            print("\n✓ All papers already screened!")
            return df

        print(f"\n⏳ Starting parallel screening...")

        results = []
        results_lock = asyncio.Lock()

        def screen_and_format(row):
            """Screen a paper and format result"""
            result = self.screen_paper(row['title'], row['abstract'])
            return {
                'title': row['title'],
                'domain_score': result['scores']['domain'],
                'intervention_score': result['scores']['intervention'],
                'method_score': result['scores']['method'],
                'outcomes_score': result['scores']['outcomes'],
                'exclusion_score': result['scores']['exclusion'],
                'title_bonus': result['scores']['title_bonus'],
                'total_score': result['total_score'],
                'decision': result['decision'],
                'reasoning': result['reasoning']
            }

        # Use ThreadPoolExecutor for parallel API calls
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for idx, row in df_to_screen.iterrows():
                futures.append(executor.submit(screen_and_format, row))

            # Process results as they complete
            from concurrent.futures import as_completed
            for i, future in enumerate(as_completed(futures), 1):
                try:
                    result = future.result()
                    results.append(result)

                    # Progress indicator
                    screened_count = len(results) + already_screened
                    decision_emoji = {'auto-include': '✅', 'auto-exclude': '⛔', 'human-review': '⚠️', 'error': '❌'}
                    emoji = decision_emoji.get(result['decision'], '?')
                    print(f"   [{screened_count}/{len(df)}] {result['title'][:50]}... → {emoji} {result['decision']} (score: {result['total_score']})")

                    # Save progress periodically
                    if len(results) % batch_size == 0:
                        df_batch = pd.DataFrame(results)
                        if already_screened > 0:
                            df_existing = pd.read_csv(progress_file)
                            df_batch = pd.concat([df_existing, df_batch], ignore_index=True)
                        df_batch.to_csv(progress_file, index=False)
                        print(f"   💾 Progress saved ({screened_count}/{len(df)})")

                except Exception as e:
                    print(f"   ❌ Error processing paper: {e}")

        # Save final results
        df_results = pd.DataFrame(results)
        if already_screened > 0:
            df_existing = pd.read_csv(progress_file)
            df_results = pd.concat([df_existing, df_results], ignore_index=True)
        df_results.to_csv(progress_file, index=False)

        # Merge with original dataframe
        df = df.merge(
            df_results[['title', 'total_score', 'decision', 'reasoning',
                       'domain_score', 'intervention_score', 'method_score',
                       'outcomes_score', 'exclusion_score', 'title_bonus']],
            on='title',
            how='left',
            suffixes=('', '_screened')
        )

        return df

    def save_results(self, df: pd.DataFrame):
        """
        Save screening results with AI-PRISMA 3-zone separation

        Args:
            df: DataFrame with screening results
        """
        print("\n" + "="*60)
        print("📊 AI-PRISMA SCREENING RESULTS")
        print("="*60)

        # Calculate statistics by decision
        total = len(df)
        auto_included = (df['decision'] == 'auto-include').sum()
        auto_excluded = (df['decision'] == 'auto-exclude').sum()
        human_review = (df['decision'] == 'human-review').sum()
        errors = (df['decision'] == 'error').sum()

        print(f"\nTotal papers: {total}")
        print(f"✅ Auto-include (score ≥ {self.score_threshold_include}): {auto_included} ({auto_included/total*100:.1f}%)")
        print(f"⛔ Auto-exclude (score < {self.score_threshold_exclude}): {auto_excluded} ({auto_excluded/total*100:.1f}%)")
        print(f"⚠️  Human review required ({self.score_threshold_exclude} ≤ score < {self.score_threshold_include}): {human_review} ({human_review/total*100:.1f}%)")
        if errors > 0:
            print(f"❌ Errors: {errors} ({errors/total*100:.1f}%)")

        # Score distribution
        print(f"\nTotal Score Distribution:")
        print(f"  Mean: {df['total_score'].mean():.1f}")
        print(f"  Median: {df['total_score'].median():.1f}")
        print(f"  Range: {df['total_score'].min():.0f} to {df['total_score'].max():.0f}")

        # Save by decision type (3-Zone Model)

        # Zone 2: Auto-include (high confidence)
        df_auto_include = df[df['decision'] == 'auto-include'].copy()
        auto_include_file = self.output_dir / "auto_included.csv"
        df_auto_include.to_csv(auto_include_file, index=False)
        print(f"\n💾 Auto-included papers: {auto_include_file}")

        # Zone 2: Auto-exclude (high confidence)
        df_auto_exclude = df[df['decision'] == 'auto-exclude'].copy()
        auto_exclude_file = self.output_dir / "auto_excluded.csv"
        df_auto_exclude.to_csv(auto_exclude_file, index=False)
        print(f"💾 Auto-excluded papers: {auto_exclude_file}")

        # Zone 3: Human review queue (medium confidence)
        df_human_review = df[df['decision'] == 'human-review'].copy()
        human_review_file = self.output_dir / "human_review_queue.csv"
        df_human_review.to_csv(human_review_file, index=False)
        print(f"💾 Human review queue: {human_review_file}")

        # Save all with full details
        all_file = self.output_dir / "all_screened_papers.csv"
        df.to_csv(all_file, index=False)
        print(f"💾 All papers with AI-PRISMA scores: {all_file}")

        print("="*60)

        # Show samples from each zone
        if auto_included > 0:
            print("\n📋 Sample Auto-Included Papers:")
            for idx, row in df_auto_include.head(2).iterrows():
                print(f"\n  • {row['title'][:70]}...")
                print(f"    Total Score: {row['total_score']:.0f}")
                print(f"    Scores: D={row['domain_score']:.0f} I={row['intervention_score']:.0f} M={row['method_score']:.0f} O={row['outcomes_score']:.0f} E={row['exclusion_score']:.0f} TB={row['title_bonus']:.0f}")
                print(f"    Reasoning: {row['reasoning'][:150]}...")

        if human_review > 0:
            print("\n📋 Sample Human Review Queue:")
            for idx, row in df_human_review.head(2).iterrows():
                print(f"\n  • {row['title'][:70]}...")
                print(f"    Total Score: {row['total_score']:.0f}")
                print(f"    Scores: D={row['domain_score']:.0f} I={row['intervention_score']:.0f} M={row['method_score']:.0f} O={row['outcomes_score']:.0f} E={row['exclusion_score']:.0f} TB={row['title_bonus']:.0f}")
                print(f"    Reasoning: {row['reasoning'][:150]}...")

        if auto_excluded > 0:
            print("\n📋 Sample Auto-Excluded Papers:")
            for idx, row in df_auto_exclude.head(2).iterrows():
                print(f"\n  • {row['title'][:70]}...")
                print(f"    Total Score: {row['total_score']:.0f}")
                print(f"    Reasoning: {row['reasoning'][:150]}...")

        # Show next step based on human review requirement
        if human_review > 0 and self.require_human_review:
            print("\n" + "="*60)
            print("⚠️  HUMAN REVIEW REQUIRED")
            print("="*60)
            print(f"\n{human_review} papers require expert validation.")
            print(f"See: {human_review_file}")
            print("\nNext step: Conduct human review and calculate Cohen's Kappa")
            print("   python scripts/03b_human_review.py --project <project_path>")
        else:
            print("\n✨ Next step: Download PDFs for included papers")
            print(f"   python scripts/04_download_pdfs.py --project <project_path>")


def main():
    parser = argparse.ArgumentParser(
        description="AI-PRISMA: 6-dimension scoring for systematic literature review screening"
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
    parser.add_argument(
        '--max-workers',
        type=int,
        default=8,
        help='Number of parallel workers (default: 8, max: 10)'
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

    # Screen papers with parallel processing
    df = screener.screen_all_papers(df, batch_size=args.batch_size, max_workers=args.max_workers)

    # Save results
    screener.save_results(df)


if __name__ == '__main__':
    main()
