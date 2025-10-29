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

    def build_prisma_prompt(self, title: str, abstract: str) -> str:
        """
        Build template-free AI-PRISMA scoring prompt with 6-dimension rubric.

        Claude interprets the research question directly without keyword templates.
        This provides flexibility for any research domain without manual configuration.

        Framework: PICOC+S-derived relevance scoring with automation-aware prioritisation.
        - Domain (PICOC: Context) → Context-sensitive population definition (Booth et al., 2012)
        - Intervention (PICO: same) → Technology/tool being studied (Richardson et al., 1995)
        - Method (PICOS: Study design) → Study design rigor prioritization (Higgins et al., 2022)
        - Outcomes (PICO: same) → Measurable results (Richardson et al., 1995)
        - Exclusion (PRISMA 2020) → PRISMA-derived eligibility criteria (Page et al., 2021)
        - Title Bonus (Automation) → Title-abstract alignment (O'Mara-Eves et al., 2015)

        See RELEASE_NOTES_v1.1.6.md for complete academic lineage with 13 scholarly citations.
        """

        prompt = f"""You are a research assistant conducting a PRISMA 2020 systematic literature review using AI-PRISMA methodology.

Research Question: {self.research_question}

Paper Title: {title}

Abstract: {abstract}

═══════════════════════════════════════════════════════════════════
TASK: Evaluate this paper using the 6-dimension scoring rubric based on PICOC+S-derived framework.

NOTE: This rubric synthesizes PICOC (Booth et al., 2012), PICOS (Higgins et al., 2022),
and PRISMA 2020 (Page et al., 2021) with automation research (O'Mara-Eves et al., 2015).
See RELEASE_NOTES_v1.1.6.md for complete academic lineage with 13 scholarly citations.
═══════════════════════════════════════════════════════════════════

SCORING RUBRIC:

1. DOMAIN (PICOC: Context) - 0-10 points
   Evaluate if the paper addresses the core research domain/population relevant to the research question.
   Context-sensitive population definition following PICOC framework (Booth et al., 2012).

   Scoring Guidelines:
   - 10 points: Directly addresses the target domain/population
   - 7-9 points: Related domain with significant overlap
   - 4-6 points: Mentions domain but not primary focus
   - 1-3 points: Tangentially related
   - 0 points: Unrelated or no clear domain match

   Examples for "{self.research_question}":
   - Identify the target domain (e.g., "higher education", "K-12", "workplace training")
   - Award 10 if paper explicitly focuses on this domain
   - Award 7-9 if domain is major component
   - Award 0-3 if domain is different or unclear

2. INTERVENTION (PICO: Intervention) - 0-10 points
   Evaluate if the paper discusses the specific intervention, technology, or tool mentioned in the research question.

   Scoring Guidelines:
   - 10 points: Intervention is the primary focus of the study
   - 7-9 points: Intervention is a major component
   - 4-6 points: Intervention mentioned but not central
   - 1-3 points: Intervention vaguely related
   - 0 points: No relevant intervention discussed

   Examples for "{self.research_question}":
   - Identify the main intervention (e.g., "ChatGPT", "chatbot", "AI tool")
   - Award 10 if paper directly studies this intervention
   - Award 0 if intervention is absent or completely different

3. METHOD (PICOS: Study Design) - 0-5 points
   Evaluate the rigor of the research methodology.
   Study design rigor prioritization following PICOS guidance (Higgins et al., 2022; Cochrane Handbook).

   Scoring Guidelines:
   - 5 points: RCT, randomized controlled trial, experimental design
   - 4 points: Quasi-experimental, pre-test/post-test design
   - 3 points: Mixed methods, quantitative survey, longitudinal study
   - 2 points: Qualitative study, interviews, case study
   - 1 point: Descriptive or exploratory study
   - 0 points: No clear methodology, theoretical only, or opinion piece

   Note: Higher scores indicate more rigorous causal inference, not quality judgment

4. OUTCOMES (PICO: Outcomes) - 0-10 points
   Evaluate if outcomes/results are clearly measured and reported.

   Scoring Guidelines:
   - 10 points: Primary outcomes explicitly defined and rigorously measured
   - 7-9 points: Outcomes clearly stated and evaluated
   - 4-6 points: Outcomes mentioned but measurement unclear
   - 1-3 points: Outcomes implied but not explicitly measured
   - 0 points: No measurable outcomes or purely theoretical

   Examples:
   - Look for phrases like "improved by 23%", "significant effect (p<0.05)", "measured using X scale"
   - Award 10 for quantitative outcomes with statistical analysis
   - Award 0 for papers with no empirical results

5. EXCLUSION (PRISMA 2020: Eligibility Criteria) - (-20 to 0 points)
   Apply penalties for papers that should be excluded based on study type or irrelevance.
   PRISMA-derived eligibility exclusions (Page et al., 2021; Higgins et al., 2022).

   Penalty Guidelines:
   - -20 points: Completely irrelevant domain (e.g., medical imaging for education research)
   - -15 points: Wrong population (e.g., K-12 when research targets higher education)
   - -10 points: Meta-analysis, systematic review, or literature review (not original research)
   - -10 points: Editorial, commentary, opinion piece, or book review
   - -5 points: Conference abstract without full paper
   - 0 points: No exclusion criteria met

   Note: Multiple penalties can stack (e.g., -10 for review + -15 for wrong population = -25, capped at -20)

6. TITLE BONUS (Automation Research: Title-Abstract Alignment) - 0 or +10 points
   Award +10 if BOTH the domain AND intervention appear in the title.

   Rationale: Title-abstract term weighting from systematic review automation research
   (O'Mara-Eves et al., 2015; Wallace et al., 2010).

   Examples for "{self.research_question}":
   - If research question is about "ChatGPT in higher education":
     - Title "ChatGPT Use in University Classrooms" → +10 (both present)
     - Title "AI Tools in Higher Education" → +10 (both implied)
     - Title "ChatGPT for K-12 Learning" → 0 (wrong domain)
     - Title "University Teaching Methods" → 0 (intervention missing)

═══════════════════════════════════════════════════════════════════
TOTAL SCORE RANGE: -20 to 50 points
═══════════════════════════════════════════════════════════════════

IMPORTANT REQUIREMENTS:

1. EVIDENCE GROUNDING:
   - You MUST provide direct quotes from the abstract to justify each dimension score
   - Use exact quotes (in "quotation marks")
   - If no evidence exists for a dimension, score it 0 and explain why
   - Do NOT paraphrase - use verbatim text from abstract

2. NO HALLUCINATIONS:
   - Only use information explicitly stated in title or abstract
   - Do not infer or assume information not present
   - If abstract is vague, assign lower scores with explanation
   - If you're uncertain, err on the side of lower scores

3. CONFIDENCE CALCULATION:
   - confidence = 0-100 (quantitative percentage)
   - High confidence (90-100): Clear, explicit evidence for all key dimensions
   - Medium confidence (40-89): Some dimensions unclear or partially addressed
   - Low confidence (0-39): Abstract too vague, off-topic, or missing critical information

   Confidence factors:
   - +20: Abstract explicitly mentions domain AND intervention
   - +15: Clear methodology and outcomes described
   - +10: All 6 dimensions have concrete evidence
   - -20: Abstract is vague or lacks detail
   - -30: Title and abstract seem unrelated to research question

4. DECISION LOGIC:
   Your confidence score determines the final decision:
   - confidence ≥ {self.screening_threshold}% AND total_score ≥ 30 → "auto-include"
   - confidence ≤ {self.exclude_threshold}% OR total_score < 0 → "auto-exclude"
   - Otherwise → "human-review" (requires expert validation)

Respond in JSON format:
{{
  "scores": {{
    "domain": <0-10>,
    "intervention": <0-10>,
    "method": <0-5>,
    "outcomes": <0-10>,
    "exclusion": <-20 to 0>,
    "title_bonus": <0 or 10>
  }},
  "total_score": <sum of all scores>,
  "confidence": <0-100>,
  "decision": "auto-include" | "auto-exclude" | "human-review",
  "reasoning": "Brief explanation of overall decision (2-3 sentences, focus on why this paper is/isn't relevant)",
  "evidence_quotes": [
    "Direct quote from abstract supporting domain score",
    "Direct quote supporting intervention score",
    "Direct quote supporting method score (if applicable)",
    "Direct quote supporting outcomes score (if applicable)"
  ]
}}

DECISION RULES:
- confidence ≥ {self.screening_threshold} AND total_score ≥ 30 → "auto-include"
- confidence ≤ {self.exclude_threshold} OR total_score < 0 → "auto-exclude"
- Otherwise → "human-review" (requires expert validation)
"""
        return prompt

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
            # Check if quote exists in abstract (case-insensitive, ignore punctuation)
            if quote.lower().strip() not in abstract.lower():
                print(f"   ⚠️  Hallucination detected: \"{quote[:50]}...\"")
                return False
        return True

    def determine_decision(self, confidence: int, total_score: int) -> str:
        """
        Determine decision based on confidence and total score

        Args:
            confidence: AI confidence score (0-100)
            total_score: Total 6-dimension score (-20 to 50)

        Returns:
            Decision: "auto-include", "auto-exclude", or "human-review"

        Decision rules (configurable):
        - High confidence (≥90%) AND high score (≥30) → auto-include
        - Low confidence (≤10%) OR negative score → auto-exclude
        - Medium confidence (11-89%) → human-review
        """
        if confidence >= self.screening_threshold and total_score >= 30:
            return 'auto-include'
        elif confidence <= self.exclude_threshold or total_score < 0:
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
        Screen a single paper using AI-PRISMA 6-dimension scoring

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
                'confidence': 0,
                'decision': 'auto-exclude',
                'reasoning': 'No abstract available for screening',
                'evidence_quotes': []
            }

        # Build AI-PRISMA prompt
        prompt = self.build_prisma_prompt(title, abstract)

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,  # Increased for detailed evidence quotes
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            result_text = response.content[0].text.strip()

            # Parse JSON response
            import json
            result = json.loads(result_text)

            # Validate evidence grounding
            if not self.validate_evidence_grounding(result.get('evidence_quotes', []), abstract):
                print(f"   ⚠️  WARNING: Hallucination detected in evidence quotes")
                result['confidence'] = max(0, result['confidence'] - 20)  # Penalty

            # Apply decision rules based on confidence and score
            result['decision'] = self.determine_decision(
                result['confidence'],
                result['total_score']
            )

            return result

        except Exception as e:
            print(f"   ⚠️  API Error: {e}")
            return {
                'scores': {'domain': 0, 'intervention': 0, 'method': 0,
                          'outcomes': 0, 'exclusion': 0, 'title_bonus': 0},
                'total_score': 0,
                'confidence': 0,
                'decision': 'error',
                'reasoning': str(e),
                'evidence_quotes': []
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
                df_progress[['title', 'total_score', 'confidence', 'decision', 'reasoning',
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

        print(f"\n⏳ Starting screening...")

        results = []
        for idx, row in df_to_screen.iterrows():
            # Screen paper
            result = self.screen_paper(row['title'], row['abstract'])

            # Add to results with all scores
            results.append({
                'title': row['title'],
                'domain_score': result['scores']['domain'],
                'intervention_score': result['scores']['intervention'],
                'method_score': result['scores']['method'],
                'outcomes_score': result['scores']['outcomes'],
                'exclusion_score': result['scores']['exclusion'],
                'title_bonus': result['scores']['title_bonus'],
                'total_score': result['total_score'],
                'confidence': result['confidence'],
                'decision': result['decision'],
                'reasoning': result['reasoning']
            })

            # Progress indicator
            screened_count = len(results) + already_screened
            decision_emoji = {'auto-include': '✅', 'auto-exclude': '⛔', 'human-review': '⚠️', 'error': '❌'}
            emoji = decision_emoji.get(result['decision'], '?')
            print(f"   [{screened_count}/{len(df)}] {row['title'][:50]}... → {emoji} {result['decision']} (score: {result['total_score']}, conf: {result['confidence']}%)")

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
            df_results[['title', 'total_score', 'confidence', 'decision', 'reasoning',
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
        print(f"✅ Auto-include (≥{self.screening_threshold}% confidence): {auto_included} ({auto_included/total*100:.1f}%)")
        print(f"⛔ Auto-exclude (≤{self.exclude_threshold}% confidence): {auto_excluded} ({auto_excluded/total*100:.1f}%)")
        print(f"⚠️  Human review required ({self.exclude_threshold+1}-{self.screening_threshold-1}%): {human_review} ({human_review/total*100:.1f}%)")
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
                print(f"    Total Score: {row['total_score']:.0f} | Confidence: {row['confidence']:.0f}%")
                print(f"    Scores: D={row['domain_score']:.0f} I={row['intervention_score']:.0f} M={row['method_score']:.0f} O={row['outcomes_score']:.0f} E={row['exclusion_score']:.0f} TB={row['title_bonus']:.0f}")
                print(f"    Reasoning: {row['reasoning'][:150]}...")

        if human_review > 0:
            print("\n📋 Sample Human Review Queue:")
            for idx, row in df_human_review.head(2).iterrows():
                print(f"\n  • {row['title'][:70]}...")
                print(f"    Total Score: {row['total_score']:.0f} | Confidence: {row['confidence']:.0f}%")
                print(f"    Scores: D={row['domain_score']:.0f} I={row['intervention_score']:.0f} M={row['method_score']:.0f} O={row['outcomes_score']:.0f} E={row['exclusion_score']:.0f} TB={row['title_bonus']:.0f}")
                print(f"    Reasoning: {row['reasoning'][:150]}...")

        if auto_excluded > 0:
            print("\n📋 Sample Auto-Excluded Papers:")
            for idx, row in df_auto_exclude.head(2).iterrows():
                print(f"\n  • {row['title'][:70]}...")
                print(f"    Total Score: {row['total_score']:.0f} | Confidence: {row['confidence']:.0f}%")
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


if __name__ == '__main__':
    main()
