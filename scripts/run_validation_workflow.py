#!/usr/bin/env python3
"""
Complete AI-PRISMA Validation Workflow

Orchestrates the full validation workflow:
1. Load AI screening results
2. Extract random sample for human review
3. (Optional) Guide user through human review CLI
4. Calculate Cohen's Kappa
5. Generate validation report

Usage:
    python scripts/run_validation_workflow.py --project <project_path> [--sample-size 50]

Example:
    python scripts/run_validation_workflow.py \\
        --project projects/2025-10-13_AI-Chatbots \\
        --sample-size 50 \\
        --review-mode interactive
"""

import argparse
import pandas as pd
from pathlib import Path
import sys
import subprocess
import random


class ValidationWorkflow:
    """Orchestrate complete validation workflow"""

    def __init__(self, project_path: str, sample_size: int = 50, review_mode: str = 'interactive'):
        self.project_path = Path(project_path)
        self.sample_size = sample_size
        self.review_mode = review_mode
        self.data_dir = self.project_path / "data" / "02_screening"

        # File paths
        self.ai_decisions_file = self.data_dir / "all_screened_papers.csv"
        self.human_review_queue_file = self.data_dir / "human_review_queue.csv"
        self.human_decisions_file = self.data_dir / "human_review_decisions.csv"
        self.sample_file = self.data_dir / "validation_sample.csv"
        self.kappa_report_file = self.data_dir / "kappa_report.md"

    def check_prerequisites(self):
        """Check that AI screening has been completed"""
        if not self.ai_decisions_file.exists():
            print("❌ Error: AI screening not found")
            print(f"   Expected: {self.ai_decisions_file}")
            print("   Run screening first: python scripts/03_screen_papers.py")
            sys.exit(1)

        print(f"✓ Found AI screening results: {self.ai_decisions_file}")

    def create_validation_sample(self):
        """Create stratified random sample for validation"""

        print(f"\n📋 Creating validation sample...")

        # Load AI decisions
        df_ai = pd.read_csv(self.ai_decisions_file)
        print(f"   Total papers: {len(df_ai)}")

        # Check if we should sample from human review queue or all papers
        if self.human_review_queue_file.exists():
            df_queue = pd.read_csv(self.human_review_queue_file)
            print(f"   Human review queue: {len(df_queue)} papers (11-89% confidence)")

            # Sample from queue (priority)
            sample_from_queue = min(self.sample_size, len(df_queue))
            if sample_from_queue < len(df_queue):
                df_sample = df_queue.sample(n=sample_from_queue, random_state=42)
            else:
                df_sample = df_queue.copy()

            print(f"   ✓ Sampled {len(df_sample)} papers from human review queue")

            # If sample size not met, add from auto-include/exclude
            if len(df_sample) < self.sample_size:
                remaining = self.sample_size - len(df_sample)

                # Get auto-include and auto-exclude papers
                auto_papers = df_ai[df_ai['decision'].isin(['auto-include', 'auto-exclude'])]

                if len(auto_papers) > 0:
                    # Stratified sampling (proportional to include/exclude ratio)
                    auto_include = auto_papers[auto_papers['decision'] == 'auto-include']
                    auto_exclude = auto_papers[auto_papers['decision'] == 'auto-exclude']

                    n_include = min(remaining // 2, len(auto_include))
                    n_exclude = min(remaining - n_include, len(auto_exclude))

                    sample_include = auto_include.sample(n=n_include, random_state=42) if n_include > 0 else pd.DataFrame()
                    sample_exclude = auto_exclude.sample(n=n_exclude, random_state=42) if n_exclude > 0 else pd.DataFrame()

                    df_sample = pd.concat([df_sample, sample_include, sample_exclude], ignore_index=True)

                    print(f"   ✓ Added {n_include} auto-include + {n_exclude} auto-exclude papers")

        else:
            # No human review queue - sample from all papers (stratified)
            print(f"   No human review queue found - sampling from all papers")

            # Stratified sampling by decision
            decisions = df_ai['decision'].unique()
            samples = []

            for decision in decisions:
                df_decision = df_ai[df_ai['decision'] == decision]
                n_sample = min(
                    int(self.sample_size * len(df_decision) / len(df_ai)),
                    len(df_decision)
                )
                if n_sample > 0:
                    samples.append(df_decision.sample(n=n_sample, random_state=42))
                    print(f"   ✓ Sampled {n_sample} papers from {decision}")

            df_sample = pd.concat(samples, ignore_index=True)

        # Add paper_id if not present (needed for Cohen's Kappa)
        if 'paper_id' not in df_sample.columns:
            df_sample['paper_id'] = df_sample.apply(
                lambda row: f"{row['title']}_{row.get('year', 'unknown')}",
                axis=1
            )

        # Save sample
        df_sample.to_csv(self.sample_file, index=False)
        print(f"\n   ✓ Validation sample saved: {self.sample_file}")
        print(f"   ✓ Sample size: {len(df_sample)} papers")

        return df_sample

    def run_human_review(self):
        """Run interactive human review CLI"""

        if self.review_mode == 'skip':
            print("\n⏭️  Skipping human review (manual mode)")
            print(f"   Please review papers manually and save results to:")
            print(f"   {self.human_decisions_file}")
            input("\nPress Enter when human review is complete...")
            return

        print(f"\n🚀 Launching human review CLI...")
        print(f"   Mode: {self.review_mode}")

        # Run 03b_human_review.py
        cmd = [
            'python3',
            'scripts/03b_human_review.py',
            '--project', str(self.project_path)
        ]

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Human review failed: {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            print(f"\n⚠️  Human review interrupted")
            sys.exit(1)

    def calculate_kappa(self):
        """Calculate Cohen's Kappa"""

        print(f"\n📊 Calculating Cohen's Kappa...")

        # Check human decisions exist
        if not self.human_decisions_file.exists():
            print(f"❌ Error: Human decisions not found")
            print(f"   Expected: {self.human_decisions_file}")
            print(f"   Run human review first")
            sys.exit(1)

        # Prepare AI decisions for validation
        # Read human decisions to get paper_ids
        df_human = pd.read_csv(self.human_decisions_file)
        paper_ids = set(df_human['paper_id'])

        # Read AI decisions and filter to matching papers
        df_ai = pd.read_csv(self.ai_decisions_file)

        # Add paper_id if not present
        if 'paper_id' not in df_ai.columns:
            df_ai['paper_id'] = df_ai.apply(
                lambda row: f"{row['title']}_{row.get('year', 'unknown')}",
                axis=1
            )

        # Filter to validation sample
        df_ai_sample = df_ai[df_ai['paper_id'].isin(paper_ids)].copy()

        # Create ai_decision column from decision
        df_ai_sample['ai_decision'] = df_ai_sample['decision'].apply(
            lambda x: 'include' if 'include' in x.lower() else 'exclude'
        )

        # Save prepared AI decisions
        ai_for_validation_file = self.data_dir / "ai_decisions_for_validation.csv"
        df_ai_sample.to_csv(ai_for_validation_file, index=False)

        print(f"   ✓ Prepared AI decisions: {len(df_ai_sample)} papers")

        # Run validation
        cmd = [
            'python3',
            'scripts/validate_human_ai_agreement.py',
            '--ai-decisions', str(ai_for_validation_file),
            '--human-validation', str(self.human_decisions_file),
            '--output', str(self.kappa_report_file)
        ]

        try:
            result = subprocess.run(cmd, check=False, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(result.stderr)

            # Check if validation passed
            if result.returncode == 0:
                print(f"\n✅ Validation PASSED")
            else:
                print(f"\n⛔ Validation FAILED")

        except Exception as e:
            print(f"❌ Error running validation: {e}")
            sys.exit(1)

    def run(self):
        """Execute complete workflow"""

        print("="*70)
        print("AI-PRISMA VALIDATION WORKFLOW")
        print("="*70)

        # Step 1: Check prerequisites
        print("\n[1/4] Checking prerequisites...")
        self.check_prerequisites()

        # Step 2: Create validation sample
        print("\n[2/4] Creating validation sample...")
        df_sample = self.create_validation_sample()

        # Step 3: Human review
        print("\n[3/4] Human review...")
        self.run_human_review()

        # Step 4: Calculate Cohen's Kappa
        print("\n[4/4] Calculating Cohen's Kappa...")
        self.calculate_kappa()

        # Done
        print("\n" + "="*70)
        print("✨ VALIDATION WORKFLOW COMPLETE")
        print("="*70)
        print(f"\n📊 View results:")
        print(f"   Validation report: {self.kappa_report_file}")
        print(f"   Human decisions: {self.human_decisions_file}")
        print(f"\n📝 Next steps:")
        print(f"   1. Review {self.kappa_report_file}")
        print(f"   2. If κ < 0.61: Refine rubric in config.yaml and re-run screening")
        print(f"   3. If κ ≥ 0.61: Proceed to PDF download and RAG building")


def main():
    parser = argparse.ArgumentParser(
        description="Complete AI-PRISMA validation workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Workflow Steps:

  1. Check prerequisites (AI screening completed)
  2. Create validation sample (stratified random)
  3. Run human review (interactive CLI or manual)
  4. Calculate Cohen's Kappa (inter-rater reliability)

Examples:

  # Interactive validation (default)
  python scripts/run_validation_workflow.py \\
      --project projects/2025-10-13_AI-Chatbots

  # Custom sample size
  python scripts/run_validation_workflow.py \\
      --project projects/2025-10-13_AI-Chatbots \\
      --sample-size 100

  # Manual review mode (skip interactive CLI)
  python scripts/run_validation_workflow.py \\
      --project projects/2025-10-13_AI-Chatbots \\
      --review-mode skip
        """
    )

    parser.add_argument(
        '--project',
        required=True,
        help='Path to project directory'
    )

    parser.add_argument(
        '--sample-size',
        type=int,
        default=50,
        help='Number of papers for validation sample (default: 50)'
    )

    parser.add_argument(
        '--review-mode',
        choices=['interactive', 'skip'],
        default='interactive',
        help='Review mode: interactive CLI or manual (default: interactive)'
    )

    args = parser.parse_args()

    # Validate project path
    project_path = Path(args.project)
    if not project_path.exists():
        print(f"❌ Error: Project path does not exist: {project_path}")
        sys.exit(1)

    # Run workflow
    workflow = ValidationWorkflow(
        project_path=args.project,
        sample_size=args.sample_size,
        review_mode=args.review_mode
    )

    workflow.run()


if __name__ == '__main__':
    main()
