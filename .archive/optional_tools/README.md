# Optional Tools: AI-PRISMA Validation

**For researchers who want to validate AI screening quality**

## What's Here

These tools help you measure how well AI screening (Stage 3) matches human expert judgment.

### 1. evaluate_with_ai_prisma.py
**Purpose**: Compare AI screening vs human screening

**When to use**:
- You want to publish a methodological paper about AI-assisted systematic reviews
- You need to report inter-rater reliability (Cohen's Kappa) for your review
- Your institution requires validation of AI screening accuracy

**How it works**:
1. Randomly samples papers from Stage 3 screening results
2. You manually review them (human screening)
3. Compares AI decisions vs your decisions
4. Calculates agreement metrics (Cohen's Kappa)

**Usage**:
```bash
cd projects/YYYY-MM-DD_ProjectName
python ../../.archive/optional_tools/evaluate_with_ai_prisma.py --project .
```

**Output**:
- `human_review_queue.csv` - Papers for you to manually review
- `screening_log.json` - Agreement metrics

### 2. generate_ai_prisma_rubric.py
**Purpose**: Generate scoring rubric for AI screening

**When to use**: Advanced customization of screening criteria

### 3. validate_ai_prisma_human.py
**Purpose**: Human validation workflow

**When to use**: Large-scale human validation needed

## For Most Researchers

**You DON'T need these tools** for a standard systematic review.

The core pipeline (scripts/01-07_*.py) is sufficient for:
- Dissertation systematic reviews
- Journal publication manuscripts
- Meta-analysis studies

**Use these tools ONLY if**:
- Your review committee requires AI validation data
- You're publishing about AI-assisted methodology
- You want to report inter-rater reliability statistics

## Support

Questions? See main documentation: https://www.scholarag.com/

---

**Last Updated**: 2025-10-24
**For**: ScholaRAG v2.0+
