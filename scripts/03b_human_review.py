#!/usr/bin/env python3
"""
Stage 3b: Human Review of Borderline Papers

Interactive CLI for human reviewers to make final decisions on papers
flagged by AI-PRISMA as requiring expert validation (11-89% confidence).

This implements the Zone 3 workflow of the Human-AI Collaboration Model:
- Zone 1: 100% AI automation (deduplication, format validation)
- Zone 2: AI-assisted (≥90% or ≤10% confidence) with sample validation
- Zone 3: Human-required (11-89% confidence) - 100% dual screening

Usage:
    python scripts/03b_human_review.py --project <project_path>

Example:
    python scripts/03b_human_review.py --project projects/2025-10-13_AI-Chatbots

Features:
    - Interactive terminal interface for reviewing borderline papers
    - Display AI scores + reasoning + evidence quotes
    - Collect human decisions (include/exclude + reason)
    - Resume functionality (tracks progress)
    - Export results to CSV for Cohen's Kappa validation
"""

import pandas as pd
import argparse
from pathlib import Path
import sys
import os
from datetime import datetime
import json


class HumanReviewer:
    """Interactive human review interface for borderline papers"""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.input_dir = self.project_path / "data" / "02_screening"
        self.review_file = self.input_dir / "human_review_queue.csv"
        self.progress_file = self.input_dir / "human_review_progress.json"
        self.output_file = self.input_dir / "human_review_decisions.csv"

        # Validate files exist
        if not self.review_file.exists():
            print("❌ Error: Human review queue not found")
            print(f"   Expected: {self.review_file}")
            print("   Run screening first: python scripts/03_screen_papers.py")
            sys.exit(1)

    def load_papers(self) -> pd.DataFrame:
        """Load papers requiring human review"""
        df = pd.read_csv(self.review_file)
        print(f"\n📋 Human Review Queue: {len(df)} papers requiring expert validation")
        print("="*70)
        return df

    def load_progress(self) -> dict:
        """Load review progress if exists"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                progress = json.load(f)
            print(f"\n✓ Found existing progress: {progress['reviewed_count']}/{progress['total_count']} papers reviewed")

            resume = input("Resume from last session? (y/n): ").lower()
            if resume == 'y':
                return progress

        return {'reviewed_papers': [], 'reviewed_count': 0, 'total_count': 0}

    def save_progress(self, progress: dict):
        """Save current review progress"""
        with open(self.progress_file, 'w') as f:
            json.dump(progress, f, indent=2)

    def display_paper(self, row: pd.Series, idx: int, total: int):
        """Display paper information for review"""
        print("\n" + "="*70)
        print(f"Paper [{idx+1}/{total}]")
        print("="*70)

        print(f"\n📄 Title:")
        print(f"   {row['title']}")

        print(f"\n👥 Authors: {row.get('authors', 'N/A')}")
        print(f"📅 Year: {row.get('year', 'N/A')}")
        print(f"🔗 DOI: {row.get('doi', 'N/A')}")

        print(f"\n📝 Abstract:")
        abstract = row.get('abstract', 'No abstract available')
        # Split into paragraphs for readability
        if len(abstract) > 500:
            print(f"   {abstract[:500]}...")
            print(f"   ... ({len(abstract) - 500} more characters)")
        else:
            print(f"   {abstract}")

        print(f"\n🤖 AI-PRISMA Assessment:")
        print(f"   ├─ Total Score: {row['total_score']}/50")
        print(f"   ├─ Confidence: {row['confidence']}%")
        print(f"   └─ Decision: {row['decision']} (borderline)")

        print(f"\n📊 Dimension Breakdown:")
        print(f"   ├─ Domain (0-10):       {row.get('domain_score', 0):.0f}")
        print(f"   ├─ Intervention (0-10): {row.get('intervention_score', 0):.0f}")
        print(f"   ├─ Method (0-5):        {row.get('method_score', 0):.0f}")
        print(f"   ├─ Outcomes (0-10):     {row.get('outcomes_score', 0):.0f}")
        print(f"   ├─ Exclusion (-20-0):   {row.get('exclusion_score', 0):.0f}")
        print(f"   └─ Title Bonus (0/10):  {row.get('title_bonus', 0):.0f}")

        print(f"\n💭 AI Reasoning:")
        print(f"   {row.get('reasoning', 'No reasoning provided')}")

        # Display evidence quotes if available
        if 'evidence_quotes' in row and pd.notna(row['evidence_quotes']):
            print(f"\n📌 Evidence Quotes (from abstract):")
            try:
                # Handle both string representation and actual list
                quotes = row['evidence_quotes']
                if isinstance(quotes, str):
                    quotes = eval(quotes)  # Safe for our controlled data
                if quotes:
                    for i, quote in enumerate(quotes[:5], 1):  # Show max 5 quotes
                        print(f"   {i}. \"{quote[:100]}{'...' if len(quote) > 100 else ''}\"")
                else:
                    print(f"   (No evidence quotes provided)")
            except:
                print(f"   (Could not parse evidence quotes)")

    def get_human_decision(self, paper_idx: int, total: int) -> dict:
        """Get human decision for a paper"""

        print("\n" + "-"*70)
        print("📝 Your Decision:")
        print("-"*70)

        # Decision loop
        while True:
            print("\nOptions:")
            print("  [i] Include - Paper meets inclusion criteria")
            print("  [e] Exclude - Paper does not meet criteria")
            print("  [s] Skip - Review later")
            print("  [v] View abstract again")
            print("  [q] Quit and save progress")

            decision = input("\nYour choice: ").lower().strip()

            if decision == 'v':
                return {'action': 'view'}
            elif decision == 's':
                return {'action': 'skip'}
            elif decision == 'q':
                return {'action': 'quit'}
            elif decision in ['i', 'e']:
                break
            else:
                print("❌ Invalid input. Please enter i, e, s, v, or q.")

        # Get reasoning
        print(f"\n{'✅ INCLUDE' if decision == 'i' else '⛔ EXCLUDE'}")
        reasoning = input("Brief reasoning (or press Enter to skip): ").strip()
        if not reasoning:
            reasoning = "No reasoning provided"

        # Confidence in decision
        while True:
            try:
                confidence = input("How confident are you? (1=low, 2=medium, 3=high): ").strip()
                if confidence in ['1', '2', '3']:
                    confidence_map = {'1': 'low', '2': 'medium', '3': 'high'}
                    confidence = confidence_map[confidence]
                    break
                print("❌ Please enter 1, 2, or 3")
            except:
                print("❌ Please enter 1, 2, or 3")

        return {
            'action': 'decide',
            'decision': 'include' if decision == 'i' else 'exclude',
            'reasoning': reasoning,
            'confidence': confidence
        }

    def review_papers(self):
        """Main review loop"""

        # Load papers and progress
        df = self.load_papers()
        progress = self.load_progress()

        # Track which papers have been reviewed
        reviewed_papers = set(progress.get('reviewed_papers', []))
        results = []

        # Load existing decisions if resuming
        if self.output_file.exists():
            existing_results = pd.read_csv(self.output_file)
            results = existing_results.to_dict('records')
            print(f"   Loaded {len(results)} previous decisions")

        print(f"\n🎯 Starting review session")
        print(f"   Papers to review: {len(df) - len(reviewed_papers)}")
        print(f"   Progress: {len(reviewed_papers)}/{len(df)} ({len(reviewed_papers)/len(df)*100:.1f}%)")

        papers_reviewed_this_session = 0

        # Review each paper
        for idx, row in df.iterrows():
            # Skip already reviewed papers
            paper_id = f"{row['title']}_{row.get('year', 'unknown')}"
            if paper_id in reviewed_papers:
                continue

            # Display paper
            self.display_paper(row, idx, len(df))

            # Get human decision
            while True:
                decision_result = self.get_human_decision(idx, len(df))

                if decision_result['action'] == 'view':
                    self.display_paper(row, idx, len(df))
                    continue
                elif decision_result['action'] == 'skip':
                    print("⏭️  Skipped - will review later")
                    break
                elif decision_result['action'] == 'quit':
                    print("\n⚠️  Review interrupted. Progress saved.")
                    self.save_results(results)
                    self.save_progress({
                        'reviewed_papers': list(reviewed_papers),
                        'reviewed_count': len(reviewed_papers),
                        'total_count': len(df),
                        'last_updated': datetime.now().isoformat()
                    })
                    return
                elif decision_result['action'] == 'decide':
                    # Record decision
                    result = {
                        'paper_id': paper_id,
                        'title': row['title'],
                        'authors': row.get('authors', 'N/A'),
                        'year': row.get('year', 'N/A'),
                        'doi': row.get('doi', 'N/A'),
                        'ai_decision': row['decision'],
                        'ai_total_score': row['total_score'],
                        'ai_confidence': row['confidence'],
                        'ai_reasoning': row.get('reasoning', ''),
                        'human_decision': decision_result['decision'],
                        'human_reasoning': decision_result['reasoning'],
                        'human_confidence': decision_result['confidence'],
                        'agreement': (decision_result['decision'] == 'include' and
                                    row['decision'] == 'auto-include') or \
                                   (decision_result['decision'] == 'exclude' and
                                    row['decision'] == 'auto-exclude'),
                        'reviewed_at': datetime.now().isoformat()
                    }

                    results.append(result)
                    reviewed_papers.add(paper_id)
                    papers_reviewed_this_session += 1

                    print(f"✓ Recorded: {decision_result['decision'].upper()} (confidence: {decision_result['confidence']})")

                    # Save progress periodically (every 5 papers)
                    if papers_reviewed_this_session % 5 == 0:
                        self.save_results(results)
                        self.save_progress({
                            'reviewed_papers': list(reviewed_papers),
                            'reviewed_count': len(reviewed_papers),
                            'total_count': len(df),
                            'last_updated': datetime.now().isoformat()
                        })
                        print(f"\n💾 Progress saved ({len(reviewed_papers)}/{len(df)})")

                    break

        # Save final results
        self.save_results(results)
        self.save_progress({
            'reviewed_papers': list(reviewed_papers),
            'reviewed_count': len(reviewed_papers),
            'total_count': len(df),
            'last_updated': datetime.now().isoformat(),
            'completed': len(reviewed_papers) == len(df)
        })

        # Display summary
        self.display_summary(results, df)

    def save_results(self, results: list):
        """Save review results to CSV"""
        if not results:
            return

        df_results = pd.DataFrame(results)
        df_results.to_csv(self.output_file, index=False)
        print(f"\n💾 Saved {len(results)} decisions to: {self.output_file}")

    def display_summary(self, results: list, df_original: pd.DataFrame):
        """Display review session summary"""

        if not results:
            print("\n⚠️  No papers reviewed in this session")
            return

        df_results = pd.DataFrame(results)

        print("\n" + "="*70)
        print("📊 HUMAN REVIEW SUMMARY")
        print("="*70)

        print(f"\n📋 Coverage:")
        print(f"   Total papers in queue: {len(df_original)}")
        print(f"   Reviewed this session: {len(results)}")
        print(f"   Remaining: {len(df_original) - len(results)}")

        print(f"\n✅ Your Decisions:")
        included = (df_results['human_decision'] == 'include').sum()
        excluded = (df_results['human_decision'] == 'exclude').sum()
        print(f"   Include: {included} ({included/len(results)*100:.1f}%)")
        print(f"   Exclude: {excluded} ({excluded/len(results)*100:.1f}%)")

        print(f"\n🎯 Confidence Distribution:")
        conf_counts = df_results['human_confidence'].value_counts()
        for conf, count in conf_counts.items():
            print(f"   {conf.capitalize()}: {count} ({count/len(results)*100:.1f}%)")

        print(f"\n🤝 Agreement with AI:")
        agreement = df_results['agreement'].sum()
        disagreement = len(results) - agreement
        agreement_rate = agreement / len(results) * 100
        print(f"   Agree: {agreement} ({agreement_rate:.1f}%)")
        print(f"   Disagree: {disagreement} ({100-agreement_rate:.1f}%)")

        # Show disagreement patterns
        if disagreement > 0:
            print(f"\n⚠️  Disagreement Examples:")
            disagreed = df_results[~df_results['agreement']]
            for idx, row in disagreed.head(3).iterrows():
                print(f"\n   • {row['title'][:60]}...")
                print(f"     AI: {row['ai_decision']} ({row['ai_confidence']:.0f}%)")
                print(f"     Human: {row['human_decision']} ({row['human_confidence']})")
                print(f"     Reason: {row['human_reasoning'][:80]}...")

        print(f"\n" + "="*70)
        print(f"✨ Next Steps:")
        print(f"="*70)

        if len(results) < len(df_original):
            print(f"\n⏭️  Continue Review:")
            print(f"   Run this script again to review remaining {len(df_original) - len(results)} papers")
        else:
            print(f"\n✅ All papers reviewed! Ready for validation.")

        print(f"\n📊 Calculate Cohen's Kappa:")
        print(f"   python scripts/validate_human_ai_agreement.py \\")
        print(f"       --ai-decisions {self.input_dir / 'all_screened_papers.csv'} \\")
        print(f"       --human-decisions {self.output_file} \\")
        print(f"       --output {self.input_dir / 'kappa_report.md'}")

        print(f"\n📄 Generate PRISMA Diagram:")
        print(f"   python scripts/07_generate_prisma.py --project {self.project_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Interactive human review of borderline papers (AI-PRISMA Zone 3)"
    )
    parser.add_argument(
        '--project',
        required=True,
        help='Path to project directory'
    )

    args = parser.parse_args()

    # Validate project path
    project_path = Path(args.project)
    if not project_path.exists():
        print(f"❌ Error: Project path does not exist: {project_path}")
        sys.exit(1)

    # Initialize and run reviewer
    reviewer = HumanReviewer(args.project)
    reviewer.review_papers()

    print("\n✨ Human review session complete!")


if __name__ == '__main__':
    main()
