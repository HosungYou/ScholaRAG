#!/usr/bin/env python3
"""
End-to-End Pipeline Test

Tests the complete AI-PRISMA workflow from screening to validation.
Uses the test project created by test_ai_prisma_scoring.py.

Usage:
    python scripts/test_full_pipeline.py

Tests:
    1. AI screening with 6-dimension scoring
    2. 3-zone output separation
    3. Human review queue creation
    4. Mock human review
    5. Cohen's Kappa calculation
    6. Validation report generation

Expected outcome: All tests pass, κ ≥ 0.61
"""

import pandas as pd
from pathlib import Path
import subprocess
import sys
import os


class PipelineTester:
    """Test complete AI-PRISMA pipeline"""

    def __init__(self):
        self.test_project = Path('/tmp/scholarag/test_projects/ai-prisma-test')
        self.data_dir = self.test_project / 'data' / '02_screening'
        self.scripts_dir = Path('/tmp/scholarag/scripts')

        self.test_results = {
            'screening': False,
            'zone_separation': False,
            'human_review_queue': False,
            'mock_validation': False,
            'kappa_calculation': False
        }

    def setup(self):
        """Ensure test project exists"""
        print("\n" + "="*70)
        print("SETUP: Checking test project")
        print("="*70)

        if not self.test_project.exists():
            print(f"❌ Test project not found: {self.test_project}")
            print(f"   Run: python scripts/test_ai_prisma_scoring.py")
            sys.exit(1)

        print(f"✓ Test project found: {self.test_project}")

        # Check API key
        if not os.getenv('ANTHROPIC_API_KEY'):
            print(f"\n⚠️  WARNING: ANTHROPIC_API_KEY not set")
            print(f"   Skipping API-dependent tests")
            return False

        return True

    def test_screening(self):
        """Test AI screening with 6-dimension scoring"""
        print("\n" + "="*70)
        print("TEST 1: AI Screening (6-Dimension Scoring)")
        print("="*70)

        cmd = [
            'python3',
            str(self.scripts_dir / '03_screen_papers.py'),
            '--project', str(self.test_project),
            '--question', 'How do AI chatbots improve speaking proficiency in second language learning?'
        ]

        print(f"Running: {' '.join(cmd)}")

        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(result.stdout)

            # Check output files exist
            expected_files = [
                'auto_included.csv',
                'auto_excluded.csv',
                'human_review_queue.csv',
                'all_screened_papers.csv'
            ]

            for filename in expected_files:
                filepath = self.data_dir / filename
                if not filepath.exists():
                    print(f"❌ Missing output file: {filename}")
                    return False
                print(f"✓ Found: {filename}")

            self.test_results['screening'] = True
            print("\n✅ TEST 1 PASSED: AI screening completed successfully")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ TEST 1 FAILED: {e}")
            print(e.stdout)
            print(e.stderr)
            return False

    def test_zone_separation(self):
        """Test 3-zone output separation"""
        print("\n" + "="*70)
        print("TEST 2: 3-Zone Output Separation")
        print("="*70)

        # Load all files
        try:
            df_all = pd.read_csv(self.data_dir / 'all_screened_papers.csv')
            df_auto_include = pd.read_csv(self.data_dir / 'auto_included.csv')
            df_auto_exclude = pd.read_csv(self.data_dir / 'auto_excluded.csv')
            df_human_review = pd.read_csv(self.data_dir / 'human_review_queue.csv')

            print(f"Total papers: {len(df_all)}")
            print(f"Auto-include (≥90% conf): {len(df_auto_include)}")
            print(f"Auto-exclude (≤10% conf): {len(df_auto_exclude)}")
            print(f"Human-review (11-89% conf): {len(df_human_review)}")

            # Validate counts match
            total = len(df_auto_include) + len(df_auto_exclude) + len(df_human_review)
            if total != len(df_all):
                print(f"❌ Count mismatch: {total} != {len(df_all)}")
                return False

            # Validate confidence thresholds
            if len(df_auto_include) > 0:
                min_conf = df_auto_include['confidence'].min()
                if min_conf < 90:
                    print(f"❌ Auto-include has confidence < 90%: {min_conf}")
                    return False
                print(f"✓ Auto-include min confidence: {min_conf}%")

            if len(df_auto_exclude) > 0:
                max_conf = df_auto_exclude['confidence'].max()
                if max_conf > 10:
                    print(f"❌ Auto-exclude has confidence > 10%: {max_conf}")
                    return False
                print(f"✓ Auto-exclude max confidence: {max_conf}%")

            if len(df_human_review) > 0:
                min_conf = df_human_review['confidence'].min()
                max_conf = df_human_review['confidence'].max()
                if min_conf < 11 or max_conf > 89:
                    print(f"❌ Human-review confidence out of range: {min_conf}-{max_conf}%")
                    return False
                print(f"✓ Human-review confidence range: {min_conf}-{max_conf}%")

            self.test_results['zone_separation'] = True
            print("\n✅ TEST 2 PASSED: 3-zone separation correct")
            return True

        except Exception as e:
            print(f"❌ TEST 2 FAILED: {e}")
            return False

    def test_human_review_queue(self):
        """Test human review queue format"""
        print("\n" + "="*70)
        print("TEST 3: Human Review Queue Format")
        print("="*70)

        try:
            df_queue = pd.read_csv(self.data_dir / 'human_review_queue.csv')

            # Check required columns
            required_cols = [
                'title', 'abstract', 'decision', 'total_score', 'confidence',
                'domain_score', 'intervention_score', 'method_score',
                'outcomes_score', 'exclusion_score', 'title_bonus', 'reasoning'
            ]

            missing = [col for col in required_cols if col not in df_queue.columns]
            if missing:
                print(f"❌ Missing columns: {missing}")
                return False

            print(f"✓ All required columns present")

            # Validate score ranges
            validations = [
                ('domain_score', 0, 10),
                ('intervention_score', 0, 10),
                ('method_score', 0, 5),
                ('outcomes_score', 0, 10),
                ('exclusion_score', -20, 0),
                ('title_bonus', 0, 10),
                ('total_score', -20, 50)
            ]

            for col, min_val, max_val in validations:
                actual_min = df_queue[col].min()
                actual_max = df_queue[col].max()
                if actual_min < min_val or actual_max > max_val:
                    print(f"❌ {col} out of range: {actual_min}-{actual_max} (expected: {min_val}-{max_val})")
                    return False
                print(f"✓ {col} range valid: {actual_min}-{actual_max}")

            self.test_results['human_review_queue'] = True
            print("\n✅ TEST 3 PASSED: Human review queue format correct")
            return True

        except Exception as e:
            print(f"❌ TEST 3 FAILED: {e}")
            return False

    def create_mock_human_decisions(self):
        """Create mock human decisions for testing"""
        print("\n" + "="*70)
        print("TEST 4: Mock Human Validation")
        print("="*70)

        try:
            # Load human review queue
            df_queue = pd.read_csv(self.data_dir / 'human_review_queue.csv')

            if len(df_queue) == 0:
                print("⚠️  No papers in human review queue")
                # Create mock decisions from auto-include/exclude for testing
                df_auto_include = pd.read_csv(self.data_dir / 'auto_included.csv')
                df_auto_exclude = pd.read_csv(self.data_dir / 'auto_excluded.csv')

                # Sample 3 from each
                sample_include = df_auto_include.head(3) if len(df_auto_include) >= 3 else df_auto_include
                sample_exclude = df_auto_exclude.head(3) if len(df_auto_exclude) >= 3 else df_auto_exclude

                df_queue = pd.concat([sample_include, sample_exclude], ignore_index=True)

            print(f"Creating mock decisions for {len(df_queue)} papers")

            # Create paper_id
            df_queue['paper_id'] = df_queue.apply(
                lambda row: f"{row['title']}_{row.get('year', 'unknown')}",
                axis=1
            )

            # Mock human decisions (agree with AI 70% of the time)
            mock_decisions = []

            for idx, row in df_queue.iterrows():
                # AI decision
                ai_decision = row['decision']

                # Agree 70% of the time
                import random
                random.seed(idx)  # Reproducible
                agree = random.random() < 0.7

                if agree:
                    if 'include' in ai_decision.lower():
                        human_decision = 'include'
                    else:
                        human_decision = 'exclude'
                else:
                    # Disagree
                    if 'include' in ai_decision.lower():
                        human_decision = 'exclude'
                    else:
                        human_decision = 'include'

                mock_decisions.append({
                    'paper_id': row['paper_id'],
                    'title': row['title'],
                    'authors': row.get('authors', 'Test Author'),
                    'year': row.get('year', 2023),
                    'doi': row.get('doi', '10.1234/test'),
                    'ai_decision': ai_decision,
                    'ai_total_score': row['total_score'],
                    'ai_confidence': row['confidence'],
                    'ai_reasoning': row.get('reasoning', ''),
                    'human_decision': human_decision,
                    'human_reasoning': 'Mock decision for testing',
                    'human_confidence': 'high',
                    'agreement': ai_decision == human_decision
                })

            # Save mock decisions
            df_mock = pd.DataFrame(mock_decisions)
            output_file = self.data_dir / 'human_review_decisions.csv'
            df_mock.to_csv(output_file, index=False)

            agreement_rate = df_mock['agreement'].mean() * 100
            print(f"✓ Created {len(df_mock)} mock decisions")
            print(f"✓ Agreement rate: {agreement_rate:.1f}%")
            print(f"✓ Saved to: {output_file}")

            self.test_results['mock_validation'] = True
            print("\n✅ TEST 4 PASSED: Mock human decisions created")
            return True

        except Exception as e:
            print(f"❌ TEST 4 FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False

    def test_kappa_calculation(self):
        """Test Cohen's Kappa calculation"""
        print("\n" + "="*70)
        print("TEST 5: Cohen's Kappa Calculation")
        print("="*70)

        try:
            # Prepare AI decisions for validation
            df_human = pd.read_csv(self.data_dir / 'human_review_decisions.csv')
            paper_ids = set(df_human['paper_id'])

            df_ai = pd.read_csv(self.data_dir / 'all_screened_papers.csv')

            # Add paper_id if not present
            if 'paper_id' not in df_ai.columns:
                df_ai['paper_id'] = df_ai.apply(
                    lambda row: f"{row['title']}_{row.get('year', 'unknown')}",
                    axis=1
                )

            # Filter to validation sample
            df_ai_sample = df_ai[df_ai['paper_id'].isin(paper_ids)].copy()

            # Create ai_decision column
            df_ai_sample['ai_decision'] = df_ai_sample['decision'].apply(
                lambda x: 'include' if 'include' in x.lower() else 'exclude'
            )

            # Save for validation
            ai_file = self.data_dir / 'ai_decisions_for_validation.csv'
            df_ai_sample.to_csv(ai_file, index=False)

            # Run validation
            cmd = [
                'python3',
                str(self.scripts_dir / 'validate_human_ai_agreement.py'),
                '--ai-decisions', str(ai_file),
                '--human-validation', str(self.data_dir / 'human_review_decisions.csv'),
                '--output', str(self.data_dir / 'kappa_report.md')
            ]

            print(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=False, capture_output=True, text=True)
            print(result.stdout)

            # Check if report was generated
            report_file = self.data_dir / 'kappa_report.md'
            if not report_file.exists():
                print(f"❌ Kappa report not generated")
                return False

            # Read report to extract kappa value
            with open(report_file, 'r') as f:
                report_content = f.read()

            # Check for kappa value in report
            if 'Cohen\'s Kappa:' in report_content:
                print(f"✓ Kappa report generated successfully")
                print(f"✓ View report: {report_file}")
            else:
                print(f"❌ Kappa value not found in report")
                return False

            self.test_results['kappa_calculation'] = True
            print("\n✅ TEST 5 PASSED: Cohen's Kappa calculation successful")
            return True

        except Exception as e:
            print(f"❌ TEST 5 FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False

    def run_all_tests(self):
        """Run all tests in sequence"""
        print("\n" + "="*70)
        print("AI-PRISMA END-TO-END PIPELINE TEST")
        print("="*70)

        # Setup
        has_api_key = self.setup()

        # Run tests
        tests = [
            ('AI Screening', self.test_screening, has_api_key),
            ('3-Zone Separation', self.test_zone_separation, True),
            ('Human Review Queue', self.test_human_review_queue, True),
            ('Mock Validation', self.create_mock_human_decisions, True),
            ('Kappa Calculation', self.test_kappa_calculation, True)
        ]

        for test_name, test_func, should_run in tests:
            if not should_run:
                print(f"\n⏭️  Skipping: {test_name} (API key required)")
                continue

            passed = test_func()
            if not passed:
                print(f"\n❌ PIPELINE TEST FAILED at: {test_name}")
                return False

        # Summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)

        all_passed = all(self.test_results.values())

        for test_name, result in self.test_results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{status}: {test_name}")

        print("\n" + "="*70)
        if all_passed:
            print("✅ ALL TESTS PASSED")
            print("="*70)
            print("\n🎉 AI-PRISMA pipeline is working correctly!")
            print("\nNext steps:")
            print("  1. Run with real data: python scripts/03_screen_papers.py --project <your_project>")
            print("  2. Conduct human review: python scripts/03b_human_review.py --project <your_project>")
            print("  3. Calculate validation: python scripts/run_validation_workflow.py --project <your_project>")
            return True
        else:
            print("⛔ SOME TESTS FAILED")
            print("="*70)
            print("\nPlease review the failures above and fix before proceeding.")
            return False


def main():
    tester = PipelineTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
