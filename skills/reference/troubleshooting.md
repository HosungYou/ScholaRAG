# Troubleshooting Guide

**Purpose**: Common errors, diagnoses, and fixes

**For**: Both Claude Code and Codex agents

**When to load**: User encounters errors or unexpected results

---

## Common Errors by Stage

### Stage 1: Fetch Papers

#### Error 1.1: API Rate Limit Exceeded

**Symptom**:
```
Error: Semantic Scholar API rate limit exceeded (100 requests/5min)
Waiting 300 seconds before retry...
```

**Diagnosis**: Making too many requests too quickly

**Fix**: **NORMAL BEHAVIOR** - Script auto-retries
```bash
# No action needed - wait for automatic retry
# Expected delay: 5-10 minutes total across 1,000+ papers
```

**Prevention**: None (rate limits are API-enforced)

---

#### Error 1.2: No Papers Found (<10 papers)

**Symptom**:
```
✅ Fetch complete
Total papers: 7
```

**Diagnosis**: Query too narrow

**Fix**: Broaden query
```bash
# Check current query
grep "search_query" config.yaml

# Example fix: Add synonyms
# Before: "GPT-4" AND "pronunciation"
# After: "(chatbot OR GPT)" AND "(pronunciation OR speaking)"

# Edit config.yaml
vim config.yaml

# Re-run fetch
rm -rf data/01_identification/*
python ../../scripts/01_fetch_papers.py --project .
```

**Expected**: 500-5,000 papers for systematic_review

---

#### Error 1.3: Too Many Papers (>50,000)

**Symptom**:
```
⚠️  Warning: 63,247 papers found
This may take 10+ hours to screen
```

**Diagnosis**: Query too broad

**Fix**: Add specificity
```bash
# Example fix: Add constraints
# Before: "chatbot" AND "education"
# After: "chatbot" AND "language learning" AND "speaking"

vim config.yaml  # Edit search_query
rm -rf data/01_identification/*
python ../../scripts/01_fetch_papers.py --project .
```

**Target**: 1,000-5,000 papers for systematic_review

---

### Stage 2: Deduplication

#### Error 2.1: High Duplicate Rate (>60%)

**Symptom**:
```
Duplicates removed: 1,847 (74%)
Unique papers: 651
```

**Diagnosis**: Overlapping database coverage (normal for some queries)

**Fix**: **NO ACTION NEEDED** - This is expected
```
# High duplicate rates are NORMAL:
# - Semantic Scholar + OpenAlex often index same papers
# - arXiv papers later published in journals (appear twice)
#
# 30-60% duplicate rate is typical
# 60-80% is high but acceptable
```

**If concerned**: Check deduplicated papers manually
```bash
head -50 data/01_identification/deduplicated.csv
# Verify papers look distinct
```

---

#### Error 2.2: Low Duplicate Rate (<10%)

**Symptom**:
```
Duplicates removed: 89 (4%)
Unique papers: 2,134
```

**Diagnosis**: Databases have little overlap (unusual)

**Possible causes**:
- Query very specific to one database's coverage
- arXiv-heavy results (preprints, not in other DBs)

**Fix**: **Usually harmless** - Proceed to Stage 3
```bash
# Verify databases were actually queried
grep -E "semantic_scholar|openalex|arxiv" data/01_identification/combined.csv | sort | uniq -c

# Should show papers from all 3 databases
```

---

### Stage 3: Screening

#### Error 3.1: All Papers Excluded (0% retention)

**Symptom**:
```
Screening complete
Papers kept: 0 (0.0%)
Papers excluded: 1,586 (100%)
```

**Diagnosis**: Inclusion criteria too strict OR query mismatch

**Fix Option 1**: Check inclusion criteria match query
```bash
# Example mismatch:
# Query: "chatbot" AND "education"
# Criteria: "Must be about language learning" (too specific!)

# Fix: Align criteria with query
vim config.yaml  # Edit prisma.inclusion_criteria

# Re-run screening
rm -rf data/02_screening/*
python ../../scripts/03_screen_papers.py --project .
```

**Fix Option 2**: Check project_type threshold
```bash
grep "project_type" config.yaml

# If systematic_review (90% threshold):
# - Very strict, excludes most papers
# - Expected retention: 2-10%
# - 0% retention means criteria likely mismatch query

# If knowledge_repository (50% threshold):
# - Lenient, should keep 80-90%
# - 0% retention is unusual, check criteria
```

**Fix Option 3**: Manual review of excluded papers
```bash
# Check what was excluded and why
head -20 data/02_screening/excluded.csv
# Read "exclusion_reason" column

# Common reasons:
# - "Wrong population" (criteria too specific?)
# - "No empirical data" (query included reviews/opinions?)
```

---

#### Error 3.2: Low Retention (<2% for systematic_review)

**Symptom**:
```
Papers kept: 12 (0.8%)
```

**Diagnosis**: Expected for some strict systematic reviews, but verify query-criteria match

**Decision tree**:
```
Is retention <2%?
├─ Yes, AND papers look irrelevant → ✅ GOOD (criteria working correctly)
├─ Yes, AND papers look relevant → ❌ BAD (criteria too strict)
└─ No (retention 2-10%) → ✅ EXPECTED for systematic_review
```

**Fix if criteria too strict**:
```bash
# Review excluded papers that seem relevant
grep -v "0.9[0-9]" data/02_screening/excluded.csv | head -20
# ^ Shows papers excluded with 80-89% confidence (borderline)

# Option 1: Manually review borderline papers
# Option 2: Adjust specific criterion
#   Example: "RCT only" → "RCT or quasi-experimental"
vim config.yaml
rm -rf data/02_screening/*
python ../../scripts/03_screen_papers.py --project .
```

---

#### Error 3.3: Screening Stuck/Slow

**Symptom**:
```
Screening progress: 47/1,586 papers (3%)
Elapsed: 25 minutes
Estimated remaining: 8 hours
```

**Diagnosis**: Large paper count + API rate limits

**Fix**: **NORMAL BEHAVIOR** - Run overnight
```bash
# Expected screening rates:
# - Semantic Scholar: ~100 papers/hour (API limits)
# - 1,000 papers → 60-120 minutes
# - 5,000 papers → 5-10 hours

# Recommendation: Run in background
nohup python ../../scripts/03_screen_papers.py --project . > screening.log 2>&1 &

# Monitor progress
tail -f screening.log
```

---

### Stage 4: PDF Download

#### Error 4.1: Low Success Rate (<20%)

**Symptom**:
```
PDFs downloaded: 12/142 (8%)
```

**Diagnosis**: Many paywalled papers (NORMAL for some domains)

**Expected success rates by domain**:
- **Computer Science**: 50-70% (arXiv, open conferences)
- **Education**: 30-50% (mixed OA policies)
- **Medicine**: 20-40% (many paywalled journals)
- **Psychology**: 25-45%

**Fix Option 1**: ✅ **Proceed with available PDFs**
```bash
# 12 PDFs is low but usable for:
# - Narrative synthesis
# - Thematic analysis
# - Preliminary systematic review

# Not sufficient for:
# - Meta-analysis (need 20+ for power)
# - Comprehensive data extraction
```

**Fix Option 2**: Manual download via institution
```bash
# Use university VPN + library access
# Download missing PDFs manually
# Expected gain: +20-30% success rate

# Then re-run RAG build
python ../../scripts/05_build_rag.py --project .
```

**Fix Option 3**: Filter for open access in Stage 1
```bash
# In scripts/01_fetch_papers.py, add OA filter:
# For OpenAlex API:
# params['filter'] = 'is_oa:true'

# Re-run from Stage 1
rm -rf data/*
python ../../scripts/01_fetch_papers.py --project .
# ... continue pipeline
```

---

#### Error 4.2: PDF Download Timeout

**Symptom**:
```
Error downloading PDF for paper_0023.pdf
Timeout after 30 seconds
Retrying (attempt 2/3)...
```

**Diagnosis**: Slow server or network issues

**Fix**: **NORMAL BEHAVIOR** - Script retries 3 times
```bash
# No action needed
# Script will:
# 1. Retry with exponential backoff
# 2. Skip paper if all 3 attempts fail
# 3. Continue to next paper

# Expected: 5-10% of downloads timeout, then succeed on retry
```

**If many timeouts (>50%)**:
```bash
# Check internet connection
ping google.com

# Check disk space
df -h

# Re-run download for failed papers only
python ../../scripts/04_download_pdfs.py --project . --retry-failed
```

---

### Stage 5: RAG Build

#### Error 5.1: Embedding API Error

**Symptom**:
```
Error: OpenAI API key not found
Set OPENAI_API_KEY environment variable
```

**Diagnosis**: Missing API key

**Fix**:
```bash
# Option 1: Set API key temporarily
export OPENAI_API_KEY='sk-...'
python ../../scripts/05_build_rag.py --project .

# Option 2: Set API key permanently
echo 'export OPENAI_API_KEY="sk-..."' >> ~/.zshrc
source ~/.zshrc

# Option 3: Use local embedding model (free)
vim config.yaml
# Change:
# rag:
#   embedding:
#     provider: "local"
#     model: "all-MiniLM-L6-v2"

python ../../scripts/05_build_rag.py --project .
```

---

#### Error 5.2: ChromaDB Collection Already Exists

**Symptom**:
```
Error: Collection 'ai_chatbots_papers' already exists
Cannot create duplicate collection
```

**Diagnosis**: RAG already built (trying to rebuild)

**Fix Option 1**: Delete old collection, rebuild
```bash
rm -rf rag/chroma_db/*
python ../../scripts/05_build_rag.py --project .
```

**Fix Option 2**: Use existing collection
```bash
# Skip RAG build, proceed to Stage 6
python ../../scripts/06_query_rag.py --project . --interactive
```

---

### Stage 6: RAG Queries

#### Error 6.1: No Relevant Results Found

**Symptom**:
```
Query: "What are the main findings?"
Results: No relevant chunks found (similarity < 0.7)
```

**Diagnosis**: Similarity threshold too high OR query mismatch

**Fix Option 1**: Lower similarity threshold
```bash
# Temporary (this query only)
python ../../scripts/06_query_rag.py \
  --project . \
  --query "What are the main findings?" \
  --similarity-threshold 0.5

# Permanent (all queries)
vim config.yaml
# Change:
# rag:
#   retrieval:
#     similarity_threshold: 0.5  # Was 0.7

python ../../scripts/05_build_rag.py --project .  # Rebuild with new threshold
```

**Fix Option 2**: Rephrase query to match paper terminology
```bash
# Bad query: "What are the main findings?"
# (Too vague, papers use specific terms)

# Good query: "What impact do chatbots have on speaking proficiency?"
# (Matches key terms: chatbot, speaking, proficiency)
```

---

#### Error 6.2: Hallucinated Answers (No Citations)

**Symptom**:
```
Query: "What are effect sizes?"
Answer: "Studies found Cohen's d ranging from 0.4 to 0.8..."
Citations: (none)
```

**Diagnosis**: LLM generated answer without RAG retrieval

**Fix**: Validate answer has citations 【F:path†L123】
```bash
# ALL answers MUST have citations
# Format: 【F:pdfs/0023_Chen_2022.pdf†L145】

# If answer has no citations → HALLUCINATION, ignore

# Re-query with explicit citation instruction
python ../../scripts/06_query_rag.py \
  --project . \
  --query "Extract effect sizes with citations. Include file path and line number for each claim."
```

---

## Performance Issues

### Issue: Pipeline Takes >24 Hours

**Diagnosis**: Large paper count + slow APIs

**Bottlenecks**:
1. **Stage 1 (Fetch)**: ~1,000 papers/hour (API limits)
2. **Stage 3 (Screen)**: ~100 papers/hour (Claude API limits)
3. **Stage 4 (PDF)**: ~50 PDFs/hour (network I/O)

**Fix**: Optimize query to reduce paper count
```bash
# Target: <5,000 papers for overnight completion

# If >10,000 papers:
# 1. Add specificity to query (Stage 2)
# 2. Tighten inclusion criteria (Stage 3)
# 3. Reduce year range (Stage 1)
```

---

### Issue: High API Costs

**Diagnosis**: Large paper count + OpenAI embeddings

**Costs breakdown**:
```
Screening (Claude API):
  - 1,000 papers × $0.003 / paper ≈ $3

Embeddings (OpenAI):
  - 50 papers × 100 pages × 500 tokens/page × $0.02 / 1M tokens ≈ $50
  (if using text-embedding-3-large)

  - Same with text-embedding-3-small ≈ $2
```

**Fix**: Use cheaper embedding model
```bash
vim config.yaml
# Change:
# rag:
#   embedding:
#     model: "text-embedding-3-small"  # $0.02/1M tokens
#     # OR
#     provider: "local"  # FREE (runs on your machine)
#     model: "all-MiniLM-L6-v2"

python ../../scripts/05_build_rag.py --project .
```

---

## Data Issues

### Issue: Papers in Wrong Language

**Diagnosis**: Database returned non-English papers despite query

**Fix**: Add language filter to screening criteria
```bash
vim config.yaml
# Add to prisma.exclusion_criteria:
# - "Non-English language publications"

# Re-run screening
rm -rf data/02_screening/*
python ../../scripts/03_screen_papers.py --project .
```

---

### Issue: Duplicate Papers After Deduplication

**Diagnosis**: Different DOIs/IDs but same paper (preprint → journal)

**Fix**: Manual review and removal
```bash
# Find potential duplicates by title similarity
cd data/01_identification
python3 << EOF
import pandas as pd
from difflib import SequenceMatcher

df = pd.read_csv('deduplicated.csv')

for i, row1 in df.iterrows():
    for j, row2 in df.iterrows():
        if i >= j:
            continue
        sim = SequenceMatcher(None, row1['title'], row2['title']).ratio()
        if sim > 0.9:
            print(f"Potential duplicate:")
            print(f"  {row1['title']} ({row1['year']})")
            print(f"  {row2['title']} ({row2['year']})")
            print(f"  Similarity: {sim:.2%}\n")
EOF

# Manually remove duplicates from CSV
```

---

## When to Restart from Earlier Stage

| Symptom | Restart From | Commands |
|---------|--------------|----------|
| Query too broad/narrow | Stage 1 | `rm -rf data/*; python scripts/01_fetch_papers.py ...` |
| Wrong inclusion criteria | Stage 3 | `rm -rf data/02_screening/*; python scripts/03_screen_papers.py ...` |
| Need different PDFs | Stage 4 | `rm -rf data/pdfs/*; python scripts/04_download_pdfs.py ...` |
| RAG config wrong | Stage 5 | `rm -rf rag/*; python scripts/05_build_rag.py ...` |

**⚠️ WARNING**: Deleting data requires re-running pipeline (time + API costs)

---

## Getting Help

**If error not listed here**:

1. **Check logs**:
   ```bash
   ls logs/
   tail -50 logs/03_screen_papers.log
   ```

2. **Search GitHub Issues**:
   https://github.com/HosungYou/ScholaRAG/issues

3. **Ask in Discussions**:
   https://github.com/HosungYou/ScholaRAG/discussions

4. **Include in bug report**:
   - Error message (full traceback)
   - config.yaml (remove API keys)
   - Stage where error occurred
   - System info (OS, Python version)

---

**Last Updated**: 2025-10-24
**Version**: 2.0
**For**: ScholaRAG v2.0+
