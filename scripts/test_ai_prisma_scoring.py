#!/usr/bin/env python3
"""
Test script for AI-PRISMA 6-dimension scoring

Creates sample test papers to verify the scoring system works correctly
before running on real data.

Usage:
    python scripts/test_ai_prisma_scoring.py
"""

import pandas as pd
import yaml
from pathlib import Path
import sys

# Sample test papers with known expected outcomes
TEST_PAPERS = [
    {
        "title": "AI Chatbots Improve Speaking Proficiency in Second Language Learners: An RCT Study",
        "abstract": """This randomized controlled trial examined the effectiveness of AI-powered
        chatbots in improving speaking proficiency among 120 English language learners.
        Participants used conversational AI for 30-minute daily sessions over 8 weeks.
        Pre- and post-intervention speaking tests (TOEFL iBT speaking section) showed
        significant improvements in the chatbot group (p < 0.01, d = 0.85). Qualitative
        interviews revealed increased confidence and reduced anxiety. Results suggest
        AI chatbots can effectively supplement traditional instruction for speaking skills.""",
        "expected_decision": "auto-include",
        "expected_score_range": (40, 50),
        "reasoning": "Perfect match: AI chatbots + language learning + speaking proficiency + RCT methodology"
    },
    {
        "title": "The Role of Physical Exercise in Cardiovascular Health Among Elderly Populations",
        "abstract": """This meta-analysis examined 45 studies investigating the relationship
        between regular physical exercise and cardiovascular outcomes in adults aged 65+.
        Results indicate that moderate-intensity exercise (3-5 times weekly) significantly
        reduces risk of coronary heart disease (RR = 0.65, 95% CI: 0.58-0.73). Subgroup
        analysis revealed greater benefits for those with pre-existing conditions.
        Healthcare providers should encourage regular physical activity in elderly patients.""",
        "expected_decision": "auto-exclude",
        "expected_score_range": (-20, 5),
        "reasoning": "Completely off-topic: cardiovascular health, not language learning"
    },
    {
        "title": "Technology-Enhanced Language Teaching: A Survey of Current Practices",
        "abstract": """This survey study explored technology use in language classrooms across
        200 institutions in Europe and Asia. Results showed that 78% of teachers use some
        form of digital technology, with mobile apps (45%), video conferencing (32%), and
        learning management systems (23%) being most common. However, only 12% reported using
        AI-based tools. Teachers cited lack of training and institutional support as barriers.
        The study provides a snapshot of current technology adoption in language education.""",
        "expected_decision": "human-review",
        "expected_score_range": (15, 35),
        "reasoning": "Partial match: technology + language learning, but no specific focus on chatbots or speaking"
    },
    {
        "title": "Automated Feedback Systems for Writing Improvement in University Students",
        "abstract": """This quasi-experimental study investigated an AI-powered writing feedback
        system with 80 university students enrolled in academic writing courses. The system
        provided real-time grammar, style, and structure suggestions. Students using the system
        showed improved writing quality scores (t = 3.45, p < 0.01) compared to control group.
        Survey data indicated high user satisfaction (4.2/5.0). While focused on writing rather
        than speaking, findings contribute to understanding AI's role in language skill development.""",
        "expected_decision": "human-review",
        "expected_score_range": (20, 35),
        "reasoning": "AI + language learning, but focused on writing not speaking"
    },
    {
        "title": "Chatbot Applications in Customer Service: Industry Best Practices",
        "abstract": """This industry report examines successful chatbot implementations across
        50 companies in retail, banking, and telecommunications sectors. Analysis reveals that
        well-designed chatbots reduce customer service costs by 30-40% while maintaining
        satisfaction scores above 4.0/5.0. Key success factors include natural language
        understanding, seamless human handoff, and continuous training. The report provides
        recommendations for organizations considering chatbot deployment in customer-facing roles.""",
        "expected_decision": "auto-exclude",
        "expected_score_range": (-10, 10),
        "reasoning": "Chatbots mentioned but in customer service context, not language learning"
    },
    {
        "title": "Virtual Reality Simulation for Speaking Anxiety Reduction in Language Learners",
        "abstract": """This mixed-methods study examined virtual reality (VR) environments for
        reducing speaking anxiety in 60 intermediate-level English learners. Participants
        engaged in VR-simulated conversations with virtual characters in realistic scenarios
        (job interviews, presentations). Pre-post Foreign Language Classroom Anxiety Scale
        (FLCAS) scores showed significant anxiety reduction (p < 0.001). Speaking performance
        on standardized tests also improved. Technology differs from chatbots but addresses
        similar speaking proficiency goals through immersive practice.""",
        "expected_decision": "human-review",
        "expected_score_range": (25, 40),
        "reasoning": "Not chatbots but VR, but still relevant to speaking proficiency in language learning"
    }
]

def create_test_config(test_dir: Path):
    """Create a minimal test config.yaml with AI-PRISMA rubric"""

    config = {
        'project_name': 'AI-PRISMA Test',
        'project_type': 'systematic_review',
        'research_question': 'How do AI chatbots improve speaking proficiency in second language learning?',
        'ai_prisma_rubric': {
            'scoring_rubric': {
                'domain_keywords': [
                    {'keyword': 'language learning', 'weight': 10},
                    {'keyword': 'second language', 'weight': 10},
                    {'keyword': 'L2', 'weight': 10},
                    {'keyword': 'foreign language', 'weight': 8},
                    {'keyword': 'English learning', 'weight': 8},
                    {'keyword': 'ESL', 'weight': 8},
                    {'keyword': 'EFL', 'weight': 8}
                ],
                'intervention_keywords': [
                    {'keyword': 'chatbot', 'weight': 10},
                    {'keyword': 'conversational AI', 'weight': 10},
                    {'keyword': 'dialogue system', 'weight': 8},
                    {'keyword': 'virtual agent', 'weight': 8},
                    {'keyword': 'AI tutor', 'weight': 8}
                ],
                'method_keywords': [
                    {'keyword': 'RCT', 'weight': 5},
                    {'keyword': 'randomized controlled trial', 'weight': 5},
                    {'keyword': 'experimental', 'weight': 4},
                    {'keyword': 'quasi-experimental', 'weight': 3},
                    {'keyword': 'pre-post test', 'weight': 3}
                ],
                'outcome_keywords': [
                    {'keyword': 'speaking proficiency', 'weight': 10},
                    {'keyword': 'oral proficiency', 'weight': 10},
                    {'keyword': 'speaking skills', 'weight': 9},
                    {'keyword': 'pronunciation', 'weight': 7},
                    {'keyword': 'fluency', 'weight': 7},
                    {'keyword': 'speaking anxiety', 'weight': 6}
                ],
                'exclusion_keywords': [
                    {'keyword': 'animal study', 'penalty': -20},
                    {'keyword': 'in vitro', 'penalty': -20},
                    {'keyword': 'K-12', 'penalty': -15},
                    {'keyword': 'elementary', 'penalty': -15},
                    {'keyword': 'customer service', 'penalty': -15},
                    {'keyword': 'cardiovascular', 'penalty': -20},
                    {'keyword': 'medical', 'penalty': -10}
                ]
            },
            'decision_confidence': {
                'auto_include': 90,
                'auto_exclude': 10
            },
            'human_validation': {
                'required': True,
                'sample_size_percent': 20
            }
        }
    }

    config_file = test_dir / 'config.yaml'
    with open(config_file, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    print(f"✓ Created test config: {config_file}")
    return config_file

def create_test_papers_csv(test_dir: Path):
    """Create CSV with test papers"""

    data_dir = test_dir / 'data' / '01_identification'
    data_dir.mkdir(parents=True, exist_ok=True)

    # Create dataframe
    df = pd.DataFrame([
        {
            'title': paper['title'],
            'abstract': paper['abstract'],
            'authors': 'Test Author et al.',
            'year': 2023,
            'doi': f'10.1234/test.{i}',
            'source': 'test'
        }
        for i, paper in enumerate(TEST_PAPERS)
    ])

    dedup_file = data_dir / 'deduplicated.csv'
    df.to_csv(dedup_file, index=False)

    print(f"✓ Created test papers CSV: {dedup_file}")
    print(f"  Total papers: {len(df)}")
    return dedup_file

def print_expected_outcomes():
    """Print expected test outcomes for manual verification"""

    print("\n" + "="*70)
    print("EXPECTED TEST OUTCOMES")
    print("="*70)

    for i, paper in enumerate(TEST_PAPERS, 1):
        print(f"\n{i}. {paper['title'][:60]}...")
        print(f"   Expected Decision: {paper['expected_decision']}")
        print(f"   Expected Score Range: {paper['expected_score_range']}")
        print(f"   Reasoning: {paper['reasoning']}")

    print("\n" + "="*70)
    print("EXPECTED STATISTICS")
    print("="*70)

    auto_include = sum(1 for p in TEST_PAPERS if p['expected_decision'] == 'auto-include')
    auto_exclude = sum(1 for p in TEST_PAPERS if p['expected_decision'] == 'auto-exclude')
    human_review = sum(1 for p in TEST_PAPERS if p['expected_decision'] == 'human-review')

    print(f"\nTotal papers: {len(TEST_PAPERS)}")
    print(f"✅ Auto-include: {auto_include} ({auto_include/len(TEST_PAPERS)*100:.0f}%)")
    print(f"⛔ Auto-exclude: {auto_exclude} ({auto_exclude/len(TEST_PAPERS)*100:.0f}%)")
    print(f"⚠️  Human review: {human_review} ({human_review/len(TEST_PAPERS)*100:.0f}%)")

def main():
    print("\n" + "="*70)
    print("AI-PRISMA TEST DATA PREPARATION")
    print("="*70)

    # Create test directory
    test_dir = Path('/tmp/scholarag/test_projects/ai-prisma-test')
    test_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n✓ Created test directory: {test_dir}")

    # Create test config
    create_test_config(test_dir)

    # Create test papers
    create_test_papers_csv(test_dir)

    # Print expected outcomes
    print_expected_outcomes()

    print("\n" + "="*70)
    print("✨ TEST SETUP COMPLETE")
    print("="*70)
    print("\nNext steps:")
    print("1. Review expected outcomes above")
    print("2. Set ANTHROPIC_API_KEY in .env file")
    print("3. Run screening test:")
    print(f"\n   python scripts/03_screen_papers.py \\")
    print(f"       --project {test_dir} \\")
    print(f"       --question \"How do AI chatbots improve speaking proficiency in second language learning?\"")
    print("\n4. Compare actual results with expected outcomes above")
    print("5. If results match expectations, AI-PRISMA scoring is working correctly! ✓")

    # Also save expected outcomes to file for reference
    expected_file = test_dir / 'EXPECTED_OUTCOMES.txt'
    with open(expected_file, 'w') as f:
        f.write("="*70 + "\n")
        f.write("EXPECTED TEST OUTCOMES\n")
        f.write("="*70 + "\n\n")

        for i, paper in enumerate(TEST_PAPERS, 1):
            f.write(f"{i}. {paper['title']}\n")
            f.write(f"   Expected Decision: {paper['expected_decision']}\n")
            f.write(f"   Expected Score Range: {paper['expected_score_range']}\n")
            f.write(f"   Reasoning: {paper['reasoning']}\n\n")

    print(f"\n✓ Expected outcomes saved to: {expected_file}")

if __name__ == '__main__':
    main()
