# scripts/validate_ai_prisma_human.py

import pandas as pd
import yaml
from pathlib import Path
from sklearn.metrics import cohen_kappa_score, precision_score, recall_score, f1_score
import sys


def generate_validation_sample(ai_results_csv, sample_size=100):
    """
    Generate random sample of AI decisions for human validation
    Stratified by decision type (include/exclude/borderline)
    """

    ai_results = pd.read_csv(ai_results_csv)

    # Stratified sampling
    auto_include = ai_results[ai_results["action"] == "auto_include"]
    auto_exclude = ai_results[ai_results["action"] == "auto_exclude"]
    human_review = ai_results[ai_results["action"] == "human_review"]

    # Sample proportionally
    n_include = min(20, len(auto_include))
    n_exclude = min(20, len(auto_exclude))
    n_borderline = sample_size - n_include - n_exclude

    sample_parts = []
    if len(auto_include) > 0:
        sample_parts.append(auto_include.sample(n=n_include, random_state=42))
    if len(auto_exclude) > 0:
        sample_parts.append(auto_exclude.sample(n=n_exclude, random_state=42))
    if len(human_review) >= n_borderline:
        sample_parts.append(human_review.sample(n=n_borderline, random_state=42))
    elif len(human_review) > 0:
        sample_parts.append(human_review)

    sample = pd.concat(sample_parts)

    # Add columns for human review
    sample["human_decision"] = ""
    sample["human_notes"] = ""

    return sample


def calculate_agreement_metrics(validation_csv):
    """
    Calculate Cohen's Kappa and other agreement metrics
    """

    df = pd.read_csv(validation_csv)

    # Filter completed validations
    validated = df[df["human_decision"].notna() & (df["human_decision"] != "")]

    if len(validated) == 0:
        print("❌ No human validations found")
        return {}

    # Map to binary (include=1, exclude=0)
    ai_binary = (validated["decision"] == "include").astype(int)
    human_binary = (validated["human_decision"] == "include").astype(int)

    # Calculate metrics
    kappa = cohen_kappa_score(human_binary, ai_binary)
    precision = precision_score(human_binary, ai_binary, zero_division=0)
    recall = recall_score(human_binary, ai_binary, zero_division=0)
    f1 = f1_score(human_binary, ai_binary, zero_division=0)

    # Agreement percentage
    agreement = (ai_binary == human_binary).sum() / len(validated)

    # Disagreement patterns
    ai_yes_human_no = ((ai_binary == 1) & (human_binary == 0)).sum()
    ai_no_human_yes = ((ai_binary == 0) & (human_binary == 1)).sum()

    return {
        "cohens_kappa": kappa,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "agreement_rate": agreement,
        "total_validated": len(validated),
        "ai_overinclusive": ai_yes_human_no,
        "ai_overexclusive": ai_no_human_yes
    }


def print_validation_report(metrics):
    """Print formatted validation report"""

    print("\n" + "="*60)
    print("👥 HUMAN VALIDATION REPORT: AI-PRISMA Rubric")
    print("="*60)

    print(f"\nSample size: {metrics['total_validated']} papers")

    print(f"\n📊 Agreement Metrics:")
    print("-" * 60)
    print(f"Cohen's Kappa:     {metrics['cohens_kappa']:.3f}")

    # Kappa interpretation
    kappa_interp = ""
    if metrics['cohens_kappa'] < 0.20:
        kappa_interp = "(Poor agreement)"
    elif metrics['cohens_kappa'] < 0.40:
        kappa_interp = "(Fair agreement)"
    elif metrics['cohens_kappa'] < 0.60:
        kappa_interp = "(Moderate agreement)"
    elif metrics['cohens_kappa'] < 0.80:
        kappa_interp = "(Substantial agreement)"
    else:
        kappa_interp = "(Almost perfect agreement)"

    print(f"                   {kappa_interp}")
    print(f"\nAgreement Rate:    {metrics['agreement_rate']:.1%}")
    print(f"Precision:         {metrics['precision']:.3f}")
    print(f"Recall:            {metrics['recall']:.3f}")
    print(f"F1 Score:          {metrics['f1_score']:.3f}")

    print(f"\n🔍 Disagreement Patterns:")
    print("-" * 60)
    print(f"AI included, Human excluded:  {metrics['ai_overinclusive']}")
    print(f"AI excluded, Human included:  {metrics['ai_overexclusive']}")

    print("\n" + "="*60)

    # Recommendations
    if metrics['cohens_kappa'] < 0.60:
        print("\n⚠️  RECOMMENDATIONS:")
        print("   - Review rubric criteria (may be too broad/narrow)")
        print("   - Check AI reasoning for borderline cases")
        print("   - Consider adjusting confidence thresholds")
    elif metrics['ai_overinclusive'] > metrics['ai_overexclusive'] * 2:
        print("\n⚠️  RECOMMENDATIONS:")
        print("   - AI may be over-inclusive")
        print("   - Consider raising auto-include threshold")
    elif metrics['ai_overexclusive'] > metrics['ai_overinclusive'] * 2:
        print("\n⚠️  RECOMMENDATIONS:")
        print("   - AI may be over-exclusive")
        print("   - Consider lowering auto-exclude threshold")
    else:
        print("\n✅ Validation successful - rubric performs well")

    print("\n")


# CLI
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python validate_ai_prisma_human.py <project-path> <action>")
        print("Actions:")
        print("  generate - Generate validation sample CSV")
        print("  evaluate - Calculate agreement metrics from completed validations")
        sys.exit(1)

    project_path = Path(sys.argv[1])
    action = sys.argv[2]

    if action == "generate":
        ai_results = project_path / "data/prisma/ai_evaluation_results.csv"
        output = project_path / "data/prisma/human_validation_sample.csv"

        if not ai_results.exists():
            print(f"❌ AI results not found: {ai_results}")
            sys.exit(1)

        sample = generate_validation_sample(ai_results, sample_size=100)
        sample.to_csv(output, index=False)

        print(f"✅ Generated validation sample: {output}")
        print(f"   Papers to review: {len(sample)}")
        print(f"\n📝 Next steps:")
        print(f"   1. Open: {output}")
        print(f"   2. Fill 'human_decision' column (include/exclude)")
        print(f"   3. Add notes in 'human_notes' if needed")
        print(f"   4. Run: python validate_ai_prisma_human.py {project_path} evaluate")

    elif action == "evaluate":
        validation_csv = project_path / "data/prisma/human_validation_sample.csv"

        if not validation_csv.exists():
            print(f"❌ Validation file not found: {validation_csv}")
            print("   Run 'generate' action first")
            sys.exit(1)

        metrics = calculate_agreement_metrics(validation_csv)
        if metrics:
            print_validation_report(metrics)

            # Save metrics
            metrics_file = project_path / "data/prisma/validation_metrics.yaml"
            with open(metrics_file, "w") as f:
                yaml.dump(metrics, f, default_flow_style=False)

            print(f"📊 Metrics saved to: {metrics_file}")
