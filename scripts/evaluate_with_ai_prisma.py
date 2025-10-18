# scripts/evaluate_with_ai_prisma.py

import yaml
import pandas as pd
import anthropic
from pathlib import Path
from tqdm import tqdm
import json
import os
import sys


def evaluate_paper_with_rubric(paper, config, client):
    """
    Evaluate single paper using AI-PRISMA rubric
    Returns structured decision with evidence
    """

    rubric_config = config["ai_prisma_rubric"]
    sub_criteria = rubric_config.get("sub_criteria", {})

    # Build evaluation prompt
    prompt = f"""Evaluate this paper's relevance for systematic review.

**Title**: {paper.get("title", "")}

**Abstract**: {paper.get("abstract", "")}

Rate each dimension (0-100) with evidence quotes:

"""

    # Add each sub-criterion
    for i, (criterion, details) in enumerate(sub_criteria.items(), 1):
        prompt += f"""{i}. **{criterion.upper().replace("_", " ")}** (0-100):

Description: {details.get("description", "")}

Scoring Rubric:
{details.get("scoring_rubric", "")}

Provide:
- Score: [0-100]
- Evidence: "[Exact quote from title/abstract]"

"""

    prompt += """
**Output Format** (JSON):
```json
{
  "sub_criteria": {
    "population": {
      "score": 100,
      "evidence": "quote from paper"
    },
    "intervention": {
      "score": 95,
      "evidence": "quote from paper"
    },
    "outcomes": {
      "score": 90,
      "evidence": "quote from paper"
    }
  },
  "overall_confidence": 95,
  "decision_reasoning": "High relevance across all criteria...",
  "recommended_decision": "include"
}
```
"""

    # Call LLM
    response = client.messages.create(
        model=rubric_config.get("llm", "claude-3-5-sonnet-20241022"),
        max_tokens=1500,
        temperature=rubric_config.get("temperature", 0.1),
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Parse response
    response_text = response.content[0].text

    # Extract JSON
    if "```json" in response_text:
        json_text = response_text.split("```json")[1].split("```")[0].strip()
    elif "```" in response_text:
        json_text = response_text.split("```")[1].split("```")[0].strip()
    else:
        json_text = response_text

    evaluation = json.loads(json_text)

    # Determine action based on confidence
    confidence = evaluation.get("overall_confidence", 50)
    dc = rubric_config.get("decision_confidence", {})

    if confidence >= dc.get("auto_include", 90):
        action = "auto_include"
    elif confidence <= dc.get("auto_exclude", 10):
        action = "auto_exclude"
    else:
        action = "human_review"

    # Extract scores
    scores = {k: v["score"] for k, v in evaluation.get("sub_criteria", {}).items()}
    evidence = {k: v["evidence"] for k, v in evaluation.get("sub_criteria", {}).items()}

    return {
        "paper_id": paper.get("id", ""),
        "doi": paper.get("doi", ""),
        "title": paper.get("title", ""),
        "decision": evaluation.get("recommended_decision", "exclude"),
        "action": action,
        "confidence": confidence,
        "sub_criteria_scores": scores,
        "sub_criteria_evidence": evidence,
        "reasoning": evaluation.get("decision_reasoning", "")
    }


def prompt_human_validation(results_df, config, project_path, output_path):
    """
    Prompt user for optional human validation
    """

    print("\n" + "="*70)
    print("👥 HUMAN VALIDATION (Optional)")
    print("="*70)

    print("\nWould you like to validate AI decisions with human review?")

    print("\n✅ If YES (perform validation):")
    print("   • Measure AI-human agreement (Cohen's Kappa)")
    print("   • Identify AI over-inclusion/exclusion patterns")
    print("   • Get rubric improvement recommendations")
    print(f"   • Time required: ~{config.get('estimated_time_hours', 2.5)} hours")
    print(f"   • Sample size: {config.get('sample_size', 100)} papers")

    print("\n⏭️  If NO (skip validation):")
    print("   • Use AI evaluation results as-is")
    print("   • Proceed to next step (PDF download)")
    print("   • Can run validation later if needed")

    # Count decision distribution
    auto_include = len(results_df[results_df["action"] == "auto_include"])
    auto_exclude = len(results_df[results_df["action"] == "auto_exclude"])
    human_review = len(results_df[results_df["action"] == "human_review"])

    print(f"\nCurrent AI decisions:")
    print(f"   Auto-include:  {auto_include:>5,} ({auto_include/len(results_df)*100:>5.1f}%)")
    print(f"   Auto-exclude:  {auto_exclude:>5,} ({auto_exclude/len(results_df)*100:>5.1f}%)")
    print(f"   Human review:  {human_review:>5,} ({human_review/len(results_df)*100:>5.1f}%)")

    print("\n" + "-"*70)
    response = input("Perform human validation? (y/n): ").strip().lower()

    if response == 'y':
        print("\n✅ Human validation selected")
        print(f"   Run: python scripts/validate_ai_prisma_human.py {project_path} generate")
        print(f"   Then fill the CSV and run: python scripts/validate_ai_prisma_human.py {project_path} evaluate")
    else:
        print("\n⏭️  Skipping human validation")
        print(f"\n✅ Next step: PDF download")
        print(f"   python scripts/04_download_pdfs.py {project_path}")

    print("="*70 + "\n")


def batch_evaluate_papers(papers_csv, config_path, output_path, sample_size=None):
    """
    Evaluate all papers using AI-PRISMA rubric
    """

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    papers_df = pd.read_csv(papers_csv)

    # Sample if requested
    if sample_size and len(papers_df) > sample_size:
        papers_df = papers_df.sample(n=sample_size, random_state=42)
        print(f"📊 Sampled {sample_size:,} papers from total")

    # Initialize Anthropic client
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment")

    client = anthropic.Anthropic(api_key=api_key)

    # Evaluate papers
    results = []

    print(f"\n🤖 Evaluating {len(papers_df):,} papers with AI-PRISMA rubric...")

    for _, paper in tqdm(papers_df.iterrows(), total=len(papers_df)):
        paper_dict = paper.to_dict()

        try:
            evaluation = evaluate_paper_with_rubric(paper_dict, config, client)
            results.append(evaluation)

        except Exception as e:
            print(f"\n⚠️  Error evaluating paper {paper.get('id', '')}: {e}")
            results.append({
                "paper_id": paper.get("id", ""),
                "decision": "error",
                "action": "human_review",
                "error": str(e)
            })

    # Save results
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_path, index=False)

    # Print summary
    print("\n" + "="*60)
    print("📊 AI-PRISMA EVALUATION SUMMARY")
    print("="*60)

    print(f"\nTotal papers evaluated: {len(results_df):,}")

    action_counts = results_df["action"].value_counts()
    print(f"\n📋 Decision Distribution:")
    print("-" * 60)

    for action, count in action_counts.items():
        pct = count / len(results_df) * 100
        print(f"{action:20} {count:>6,} ({pct:>5.1f}%)")

    print("\n" + "="*60)

    # Human review queue
    human_review = results_df[results_df["action"] == "human_review"]
    if len(human_review) > 0:
        print(f"\n⚠️  {len(human_review):,} papers flagged for human review")
        print(f"   → See: {output_path.parent / 'human_review_queue.csv'}")

        human_review.to_csv(
            output_path.parent / "human_review_queue.csv",
            index=False
        )

    print(f"\n✅ Full results saved to: {output_path}\n")

    # Interactive human validation prompt
    validation_config = config.get("ai_prisma_rubric", {}).get("human_validation", {})

    if validation_config.get("prompt_user", False):
        prompt_human_validation(
            results_df=results_df,
            config=validation_config,
            project_path=output_path.parent.parent,
            output_path=output_path
        )


# CLI
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python evaluate_with_ai_prisma.py <project-path> [sample-size]")
        print("Example: python evaluate_with_ai_prisma.py projects/my-project/ 50")
        sys.exit(1)

    project_path = Path(sys.argv[1])
    sample_size = int(sys.argv[2]) if len(sys.argv) > 2 else None

    papers_csv = project_path / "data/combined/deduplicated.csv"
    config_path = project_path / "config.yaml"
    output_path = project_path / "data/prisma/ai_evaluation_results.csv"

    if not papers_csv.exists():
        print(f"❌ Papers not found: {papers_csv}")
        sys.exit(1)

    batch_evaluate_papers(papers_csv, config_path, output_path, sample_size)
