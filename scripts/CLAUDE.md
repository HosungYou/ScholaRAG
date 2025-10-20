# Scripts Folder - Claude Code Instructions

**Context**: You are in the scripts folder of ScholarRAG, which contains 7 Python scripts for executing the PRISMA 2020 + RAG pipeline.

---

## 🎯 What This Folder Contains

### 7 Pipeline Scripts (Sequential Execution)

1. **01_fetch_papers.py** - Fetch papers from academic databases (Semantic Scholar, OpenAlex, arXiv)
2. **02_deduplicate.py** - Remove duplicate papers by DOI/title
3. **03_screen_papers.py** - PRISMA screening using LLM-powered 6-dimension criteria
4. **04_download_pdfs.py** - Download PDFs for screened papers (Open Access + institutional)
5. **05_build_rag.py** - Build RAG system (extract text, chunk, embed, store in ChromaDB)
6. **06_query_rag.py** - Query RAG interface for literature analysis
7. **07_generate_prisma.py** - Generate PRISMA flowchart with actual pipeline counts

**Execution Order**: MUST run sequentially 01 → 02 → 03 → 04 → 05 → 06 → 07

---

## 🧠 PRISMA + RAG Pipeline Architecture

### Stage 1-4: PRISMA Protocol (Paper Selection)
```
01_fetch_papers.py       → 500 papers identified
02_deduplicate.py        → 400 unique papers (20% duplicates removed)
03_screen_papers.py      → 75 relevant papers (26% relevance rate)
04_download_pdfs.py      → 45 PDFs downloaded (60% success rate)
```

**PRISMA ensures**: Systematic, transparent, rigorous paper selection

### Stage 5-6: RAG Analysis (Deep Analysis)
```
05_build_rag.py          → Vector DB built from 45 PRISMA-selected PDFs
06_query_rag.py          → Query RAG: "Extract correlation coefficients"
                         → Returns: r=0.45 from Paper 12, r=0.62 from Paper 34
```

**RAG enables**: AI-powered data extraction, semantic search, citation-backed synthesis

### Stage 7: Documentation
```
07_generate_prisma.py    → PRISMA flowchart (500→400→75→45)
```

---

## 📋 How to Work with These Scripts

### For Researchers (Users)

**DON'T** run scripts manually - Claude Code executes them automatically when you complete each conversation stage in `../prompts/`.

**Expected workflow**:
1. Copy prompt from `../prompts/01_research_domain_setup.md`
2. Have conversation with Claude Code
3. Claude Code auto-executes `01_fetch_papers.py` when conversation completes
4. Repeat for stages 2-7

**Only run manually if**:
- Debugging script failures
- Re-running a specific stage after fixing data
- Testing script modifications

---

### For Claude Code (AI Assistant)

**CRITICAL: Read each script's docstring before execution**

Every script has a detailed docstring explaining:
- What it does in the PRISMA/RAG context
- Input files required
- Output files generated
- Expected statistical ranges
- Common errors and solutions

**Execution pattern**:

```python
# Stage 5 example (after user completes Stage 5 conversation)

# 1. Verify prerequisites
import os
assert os.path.exists('config.yaml'), "config.yaml missing"
assert os.path.exists('data/03_pdfs'), "PDFs not downloaded"

# 2. Run script
import subprocess
result = subprocess.run(
    ['python', 'scripts/05_build_rag.py', '--project', project_path],
    capture_output=True,
    text=True
)

# 3. Check result
if result.returncode != 0:
    print(f"❌ Error: {result.stderr}")
    # Show error to user, suggest fixes
else:
    print(result.stdout)
    # Parse output, validate results, show next stage prompt
```

**Validation after each script**:

```python
# Example: After 03_screen_papers.py
import pandas as pd

identified = len(pd.read_csv('data/01_identification/deduplicated.csv'))
screened = len(pd.read_csv('data/02_screening/relevant_papers.csv'))
relevance = screened / identified

# Validate range
if not (0.15 <= relevance <= 0.70):
    print(f"⚠️ Warning: Relevance rate {relevance:.1%} outside normal range 15-70%")
    print("   This may indicate:")
    print("   - Query too broad (low relevance)")
    print("   - PRISMA criteria too strict (very low relevance)")
    print("   - PRISMA criteria too loose (very high relevance)")
```

---

## 🔧 Script-Specific Guidance

### 01_fetch_papers.py

**What it does**: Queries academic databases with user's search query

**PRISMA stage**: Identification (Stage 1)

**Input**:
- `config.yaml` with query and databases
- API keys: `SEMANTIC_SCHOLAR_API_KEY` (optional), `OPENALEX_API_KEY` (optional)

**Output**:
- `data/01_identification/semantic_scholar_results.csv`
- `data/01_identification/openalex_results.csv`
- `data/01_identification/arxiv_results.csv`

**Expected results**:
- Total papers: 100-5000 (varies by query)
- Semantic Scholar: Usually largest source
- arXiv: Usually smallest (preprints only)

**Common issues**:
- API rate limiting → Retry after 60 seconds
- Network errors → Check internet connection
- Empty results → Query too narrow or wrong field

**Validation**:
```python
total_papers = len(ss_df) + len(oa_df) + len(ar_df)
assert 50 <= total_papers <= 10000, f"Unexpected total: {total_papers}"
```

---

### 02_deduplicate.py

**What it does**: Removes duplicate papers by DOI/title matching

**PRISMA stage**: Identification (Stage 1 continuation)

**Input**:
- `data/01_identification/*_results.csv` (from Script 01)

**Output**:
- `data/01_identification/deduplicated.csv`
- `data/01_identification/duplicates_removed.csv` (log)

**Expected results**:
- Duplicate rate: 20-40% (typical)
- Higher for broad queries (same papers in multiple databases)

**Validation**:
```python
df = pd.read_csv('data/01_identification/deduplicated.csv')
assert df.duplicated(subset=['doi']).sum() == 0, "Duplicates still present"
```

---

### 03_screen_papers.py

**What it does**: Applies PRISMA 6-dimension criteria using LLM

**PRISMA stage**: Screening (Stage 2)

**Input**:
- `data/01_identification/deduplicated.csv`
- `config.yaml` with PRISMA criteria
- `ANTHROPIC_API_KEY` (required)

**Output**:
- `data/02_screening/relevant_papers.csv`
- `data/02_screening/excluded_papers.csv`
- `data/02_screening/screening_log.json`

**Expected results**:
- Relevance rate: 15-40% (field-dependent)
- Education: ~25-30%
- Medicine: ~15-25% (more specific)
- Computer Science: ~30-40% (broader)

**6-Dimension scoring**:
```python
# Each paper scored on 6 dimensions (0 or 1)
# Must score >= threshold to pass (typically 4/6)
dimensions = [
    'domain',      # Correct research field?
    'method',      # Right methodology?
    'topic',       # Specific topic match?
    'context',     # Appropriate setting?
    'exclusion',   # Meets quality standards?
    'title'        # Title suggests relevance?
]
```

**Validation**:
```python
relevance = len(relevant_df) / len(deduplicated_df)
if relevance < 0.10:
    print("⚠️ Very low relevance (< 10%) - criteria may be too strict")
if relevance > 0.70:
    print("⚠️ Very high relevance (> 70%) - criteria may be too loose")
```

---

### 04_download_pdfs.py

**What it does**: Downloads PDFs for papers that passed screening

**PRISMA stage**: Full-text retrieval (Stage 3)

**Input**:
- `data/02_screening/relevant_papers.csv`

**Output**:
- `data/03_pdfs/*.pdf` (downloaded PDFs)
- `data/03_pdfs/papers_metadata.csv` (download status)

**Expected results**:
- Success rate: 30-80% (highly variable)
- Open Access fields (CS, preprints): 60-80%
- Paywalled fields (Medicine, journals): 30-50%

**Why low success is normal**:
- Many papers behind paywalls
- DOI links broken/outdated
- Publisher restrictions
- NOT a script error

**Validation**:
```python
metadata = pd.read_csv('data/03_pdfs/papers_metadata.csv')
success_rate = metadata['downloaded'].sum() / len(metadata)

# Success rate varies widely - all acceptable
if success_rate >= 0.30:
    print(f"✅ {success_rate:.1%} success rate (acceptable)")
else:
    print(f"⚠️ {success_rate:.1%} success rate (low but not uncommon for paywalled journals)")
```

---

### 05_build_rag.py

**What it does**: Builds RAG system from PRISMA-selected PDFs

**PRISMA-RAG transition**: PRISMA complete → RAG begins

**Critical understanding**:
```
PRISMA (Scripts 01-04): 500 papers → 75 relevant → 45 PDFs
RAG (Script 05):       Build vector DB from those 45 PDFs ONLY
                       (not all 500 original papers)
```

**Input**:
- `data/03_pdfs/*.pdf` (from Script 04)
- `data/03_pdfs/papers_metadata.csv`
- `config.yaml` with RAG settings

**Output**:
- `data/04_rag/chroma_db/` (ChromaDB vector database)
- `data/04_rag/rag_config.json` (configuration)

**What happens**:
1. Extract text from PDFs (PyMuPDF)
2. Chunk into ~1000-token semantic units
3. Generate embeddings (sentence-transformers or OpenAI)
4. Store in ChromaDB with metadata

**Expected results**:
- Chunks per paper: 5-100 (depends on paper length)
- Total chunks: `papers × avg_chunks` (e.g., 45 papers × 30 chunks = 1350 chunks)

**Validation**:
```python
import json
with open('data/04_rag/rag_config.json', 'r') as f:
    config = json.load(f)

chunks_per_paper = config['total_chunks'] / config['total_papers']
assert 5 <= chunks_per_paper <= 100, f"Unusual chunks/paper: {chunks_per_paper:.1f}"
```

---

### 06_query_rag.py

**What it does**: Interactive interface to query RAG system

**RAG stage**: Research conversation (Stage 6)

**Input**:
- `data/04_rag/chroma_db/` (from Script 05)
- User queries (interactive mode)

**Output**:
- Answers with citations (console or file)
- `data/05_analysis/conversation_log.json` (optional)

**What you're querying**:
- ONLY the 45 papers that passed PRISMA screening
- NOT the original 500 papers from database search
- Ensures high-quality, relevant answers

**Effective queries**:
```bash
# Good queries (specific, answerable from papers)
"What methodologies are used across my papers?"
"Extract all correlation coefficients for speaking skills outcomes"
"Which studies used randomized controlled trials?"
"What are the research gaps in chatbot interventions?"

# Bad queries (too general, not in papers)
"What is a chatbot?"  # Use Wikipedia instead
"How do I build a chatbot?"  # Not a literature review question
```

**Validation**:
```python
# Check that responses include citations
response = query_rag("What are the main findings?")
assert '【' in response or '[' in response, "No citations in response"
```

---

### 07_generate_prisma.py

**What it does**: Generates PRISMA 2020 flowchart with actual pipeline counts

**PRISMA stage**: Reporting (Stage 7)

**CRITICAL RULE**: Numbers MUST be actual counts from pipeline, NEVER fabricated

**Input**:
- `data/01_identification/deduplicated.csv`
- `data/02_screening/relevant_papers.csv`
- `data/03_pdfs/papers_metadata.csv`
- `data/04_rag/rag_config.json`

**Output**:
- `outputs/prisma_flowchart.png`
- `outputs/prisma_stats.json`

**PRISMA flowchart structure**:
```
Records identified (n=500)
  ↓ (-100 duplicates removed)
Records screened (n=400)
  ↓ (-325 excluded by criteria)
Reports assessed for eligibility (n=75)
  ↓ (-30 PDFs not available)
Studies included in review (n=45)
  ↓
Studies included in RAG analysis (n=45)
```

**Validation (MUST MATCH ACTUAL DATA)**:
```python
import json
import pandas as pd

# Load PRISMA output
with open('outputs/prisma_stats.json', 'r') as f:
    prisma = json.load(f)

# Load actual pipeline data
identified = len(pd.read_csv('data/01_identification/deduplicated.csv'))
screened = len(pd.read_csv('data/02_screening/relevant_papers.csv'))
pdfs = pd.read_csv('data/03_pdfs/papers_metadata.csv')['downloaded'].sum()

# CRITICAL: Validate PRISMA matches reality
assert prisma['identified'] == identified, "PRISMA count mismatch!"
assert prisma['screened'] == screened, "PRISMA count mismatch!"
assert prisma['pdfs_downloaded'] == pdfs, "PRISMA count mismatch!"
```

---

## 🚨 Critical Rules for Claude Code

### 1. Sequential Execution Required

Scripts MUST run in order: 01 → 02 → 03 → 04 → 05 → 06 → 07

**Why**: Each script depends on previous outputs:
- Script 02 needs output from Script 01
- Script 03 needs output from Script 02
- etc.

**If user asks to skip**:
```
USER: "Can we skip deduplication and go straight to screening?"
YOU: "No. Script 03 (screening) requires deduplicated.csv from Script 02.
      Skipping deduplication would cause Script 03 to fail."
```

### 2. Validate After Every Script

Check that outputs are within expected ranges:

```python
# After each script
if script_name == "03_screen_papers.py":
    relevance = screened / identified
    if not (0.15 <= relevance <= 0.70):
        print(f"⚠️ Warning: Relevance {relevance:.1%} outside normal range")
        # Suggest adjustments to PRISMA criteria
```

### 3. NEVER Fabricate PRISMA Numbers

**If user asks**: "Can you make the PRISMA numbers look better?"
**You must refuse**: "No. Scientific integrity requires actual pipeline counts. Fabricating numbers violates PRISMA 2020 guidelines."

### 4. Explain PRISMA-RAG Connection

When user reaches Script 05 (build_rag.py):

```
YOU: "We're now transitioning from PRISMA to RAG.

PRISMA (Scripts 01-04): Selected 45 high-quality papers from 500 candidates
RAG (Script 05-06): Will build semantic search over those 45 papers

This ensures RAG analyzes only relevant, vetted papers."
```

---

## 📊 Expected Pipeline Statistics

### Typical Ranges (Education Research)

| Stage | Metric | Typical Range | Example |
|-------|--------|---------------|---------|
| **Script 01** | Papers identified | 100-5000 | 500 |
| **Script 02** | Duplicate rate | 20-40% | 20% (100 removed) |
| **Script 02** | Unique papers | 60-80% of identified | 400 |
| **Script 03** | Relevance rate | 20-35% | 26% (79 relevant) |
| **Script 04** | PDF success rate | 50-70% | 57% (45 PDFs) |
| **Script 05** | Chunks per paper | 20-40 | 30 chunks/paper |
| **Script 05** | Total chunks | papers × 20-40 | 45 × 30 = 1350 |

### Field Variations

**Medicine**:
- Lower relevance (15-25%) - more specific terminology
- Lower PDF success (30-50%) - more paywalls

**Computer Science**:
- Higher relevance (30-40%) - broader queries
- Higher PDF success (60-80%) - more open access

**Psychology**:
- Medium relevance (25-30%)
- Medium PDF success (50-60%)

---

## 🔍 Troubleshooting Common Issues

### "Script 01 found fewer papers than expected"

**Check**:
```bash
# Query too narrow?
grep "query:" config.yaml

# API rate limiting?
grep -i "rate limit" logs/*.log

# Network issues?
curl -I https://api.semanticscholar.org/
```

**Solutions**:
- Broaden query (add synonyms with OR)
- Wait 60 seconds for rate limit reset
- Check internet connection

---

### "Script 03 relevance rate is 8% (too low)"

**Check**:
```bash
# PRISMA criteria too strict?
python -c "
import yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
print(f'Min score: {config[\"prisma_criteria\"][\"min_score\"]}/6')
"
```

**Solutions**:
- Lower min_score from 5/6 to 4/6
- Review domain_keywords (too narrow?)
- Review method_requirements (too restrictive?)

---

### "Script 04 PDF success rate is 25% (low)"

**This is often NORMAL**, especially for:
- Medical journals (paywalls)
- Older papers (broken DOI links)
- Non-open access fields

**NOT a script error unless**:
- Success rate is 0% → Network/API issue
- Error messages in logs → Check logs/04_download_pdfs.log

---

### "Script 06 returns generic answers (not citing papers)"

**Check**:
```bash
# RAG database empty?
python -c "
import json
with open('data/04_rag/rag_config.json', 'r') as f:
    config = json.load(f)
print(f'Total papers: {config[\"total_papers\"]}')
print(f'Total chunks: {config[\"total_chunks\"]}')
"
```

**Solutions**:
- If 0 papers: Re-run Script 05 (build_rag.py)
- Check that PDFs were downloaded (Script 04)
- Verify query is specific (not too general)

---

## 📁 File Structure Reference

```
scripts/
├── CLAUDE.md (this file - guidance for Claude Code)
├── AGENTS.md (guidance for OpenAI Codex)
├── 01_fetch_papers.py
├── 02_deduplicate.py
├── 03_screen_papers.py
├── 04_download_pdfs.py
├── 05_build_rag.py
├── 06_query_rag.py
└── 07_generate_prisma.py
```

---

## 🎯 Quick Reference for Claude Code

**When user completes Stage 5 conversation** (from prompts/05_execution_plan.md):

1. Verify prerequisites (API keys, config.yaml)
2. Run scripts sequentially:
   ```python
   for script in ['01', '02', '03', '04', '05']:
       run_script(f'scripts/{script}_*.py', project_path)
       validate_output(script)
       report_progress(script)
   ```
3. Test RAG with sample query
4. Show Stage 6 prompt

**When user runs Stage 6 conversation** (from prompts/06_research_conversation.md):

1. Guide user to run `python scripts/06_query_rag.py --interactive`
2. Remind: This queries PRISMA-selected papers only
3. Suggest effective query patterns
4. When user satisfied, show Stage 7 prompt

**When user completes Stage 7 conversation** (from prompts/07_documentation_writing.md):

1. Run `python scripts/07_generate_prisma.py`
2. Validate PRISMA counts match actual data
3. Review flowchart with user
4. Congratulate on completing pipeline!

---

**Last Updated**: 2025-10-14
**Maintained by**: ScholarRAG Team
**GitHub**: https://github.com/HosungYou/ScholarRAG
