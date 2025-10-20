# scripts/validate_config.py

import yaml
from pathlib import Path
import sys


def validate_config(config_path):
    """
    Validate config.yaml against schema and best practices

    Returns: (is_valid, errors[], warnings[])
    """

    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        return False, [f"❌ Failed to parse YAML: {e}"], []

    errors = []
    warnings = []

    # Check 1: Required top-level fields
    required_fields = ["project_name", "databases", "search_query"]
    for field in required_fields:
        if field not in config:
            errors.append(f"❌ Missing required field: {field}")

    # Check 2: Database configuration
    if "databases" in config:
        dbs = config["databases"]

        # Open access databases
        if "open_access" in dbs:
            oa = dbs["open_access"]
            enabled_oa = sum(1 for db in oa.values() if db.get("enabled", False))

            if enabled_oa == 0:
                errors.append(
                    "❌ No open access databases enabled!\n"
                    "   → Enable at least one: openalex, semantic_scholar, or arxiv"
                )
            elif enabled_oa == 1:
                warnings.append(
                    "⚠️  Only 1 database enabled\n"
                    "   → Systematic reviews typically use 2-3 databases"
                )

        # Institutional databases
        if "institutional" in dbs:
            inst = dbs["institutional"]

            if inst.get("scopus", {}).get("enabled", False):
                warnings.append(
                    "ℹ️  Scopus ENABLED\n"
                    "   → Ensure SCOPUS_API_KEY and SCOPUS_INST_TOKEN in .env\n"
                    "   → Note: Metadata only (NO PDFs)\n"
                    "   → Guide: https://scholarag.io/docs/institutional-apis/scopus"
                )

            if inst.get("web_of_science", {}).get("enabled", False):
                warnings.append(
                    "ℹ️  Web of Science ENABLED\n"
                    "   → Ensure WOS_API_KEY in .env\n"
                    "   → Note: Metadata only (NO PDFs)\n"
                    "   → Guide: https://scholarag.io/docs/institutional-apis/wos"
                )

    # Check 3: AI-PRISMA Rubric (if enabled)
    if "ai_prisma_rubric" in config and config["ai_prisma_rubric"].get("enabled", False):
        rubric = config["ai_prisma_rubric"]

        # Check LLM specified
        if "llm" not in rubric:
            errors.append("❌ AI-PRISMA enabled but no LLM specified")

        # Check decision confidence thresholds
        if "decision_confidence" in rubric:
            dc = rubric["decision_confidence"]
            auto_include = dc.get("auto_include", 0)
            auto_exclude = dc.get("auto_exclude", 0)

            if auto_include <= auto_exclude:
                errors.append(
                    f"❌ Invalid confidence thresholds\n"
                    f"   → auto_include ({auto_include}) must be > auto_exclude ({auto_exclude})"
                )

            if auto_include < 80:
                warnings.append(
                    f"⚠️  auto_include threshold ({auto_include}) is low\n"
                    f"   → Recommended: ≥90 for high-confidence decisions"
                )

        # Check sub-criteria
        if "sub_criteria" not in rubric or not rubric["sub_criteria"]:
            warnings.append(
                "⚠️  AI-PRISMA enabled but no sub_criteria defined\n"
                "   → Define at least 3 criteria (e.g., population, intervention, outcomes)"
            )

        # Check API key based on LLM
        llm_model = rubric.get("llm", "")
        if "claude" in llm_model.lower():
            warnings.append(
                f"ℹ️  Using Claude for AI-PRISMA\n"
                f"   → Ensure ANTHROPIC_API_KEY in .env\n"
                f"   → Model: {llm_model}"
            )
        elif "gpt" in llm_model.lower():
            warnings.append(
                f"ℹ️  Using OpenAI for AI-PRISMA\n"
                f"   → Ensure OPENAI_API_KEY in .env\n"
                f"   → Model: {llm_model}"
            )

    # Check 4: Retrieval settings
    if "retrieval_settings" in config:
        rs = config["retrieval_settings"]

        threshold = rs.get("user_confirmation_threshold", 15000)
        if threshold > 20000:
            warnings.append(
                f"⚠️  User confirmation threshold ({threshold:,}) is very high\n"
                f"   → Consider 10,000-15,000 for better UX"
            )

        # Check year range
        if "year_range" in rs:
            yr = rs["year_range"]
            if yr.get("start", 2015) > yr.get("end", 2024):
                errors.append(
                    f"❌ Invalid year range: start ({yr['start']}) > end ({yr['end']})"
                )

    # Check 5: RAG settings
    if "rag_settings" in config:
        rag = config["rag_settings"]

        if "llm" not in rag:
            warnings.append(
                "⚠️  No LLM specified for RAG\n"
                "   → Will use default (claude-3-5-sonnet-20241022)"
            )

    is_valid = len(errors) == 0

    return is_valid, errors, warnings


def print_validation_report(config_path, is_valid, errors, warnings):
    """Print formatted validation report"""

    print("\n" + "="*60)
    print("📋 CONFIG VALIDATION REPORT")
    print("="*60)
    print(f"\nFile: {config_path}\n")

    if errors:
        print("❌ ERRORS (must fix):")
        print("-" * 60)
        for err in errors:
            print(f"{err}\n")

    if warnings:
        print("⚠️  WARNINGS (recommendations):")
        print("-" * 60)
        for warn in warnings:
            print(f"{warn}\n")

    if not errors and not warnings:
        print("✅ CONFIG VALIDATION PASSED")
        print("   All checks successful!")

    elif not errors:
        print("✅ CONFIG VALIDATION PASSED (with warnings)")
        print("   No blocking errors, but review warnings above")

    else:
        print("❌ CONFIG VALIDATION FAILED")
        print("   Fix errors above before proceeding")

    print("="*60 + "\n")


# CLI usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_config.py <path-to-config.yaml>")
        print("Example: python validate_config.py config.yaml")
        sys.exit(1)

    config_path = sys.argv[1]

    if not Path(config_path).exists():
        print(f"❌ Config file not found: {config_path}")
        sys.exit(1)

    is_valid, errors, warnings = validate_config(config_path)
    print_validation_report(config_path, is_valid, errors, warnings)

    sys.exit(0 if is_valid else 1)
