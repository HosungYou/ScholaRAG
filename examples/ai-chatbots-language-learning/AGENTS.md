# AI Chatbots for Language Learning - Codex Agent Instructions

Project: Active ResearcherRAG systematic literature review
Domain: Education (Applied Linguistics, Educational Technology)
Framework: PRISMA 2020 + RAG (Retrieval-Augmented Generation)

**Methodology**:
1. **PRISMA 2020** (Stages 1-4): Systematic paper identification, screening, selection
2. **RAG Analysis** (Stages 5-6): Semantic search and data extraction from selected papers
3. **Documentation** (Stage 7): PRISMA flowchart and synthesis report

---

## Project Type and Scope

This is an **academic systematic literature review project**, NOT a software development project.

**Research Question**: How do AI chatbots improve speaking skills in language learning, and what are the key factors contributing to their effectiveness?

**Your role as Codex agent**:
- Execute ResearcherRAG pipeline scripts in correct sequence (PRISMA → RAG → Documentation)
- Validate outputs against expected statistical ranges
- Run all programmatic checks before marking tasks complete
- Preserve scientific integrity (NEVER modify result counts)
- Build and query RAG system for data extraction (Stages 5-6)

---

## Critical File Locations

### Configuration (READ FIRST)
- `config.yaml` - All project parameters
- `.researcherrag/context.json` - Current pipeline state

### Data Pipeline Outputs
- `data/01_identification/*.csv` - Papers from Semantic Scholar, OpenAlex, arXiv
- `data/02_screening/relevant_papers.csv` - Papers passing PRISMA screening
- `data/03_pdfs/*.pdf` - Downloaded PDF files
- `data/04_rag/chroma_db/` - ChromaDB vector database

### Validation Targets
- `expected_results/EXPECTED_STATISTICS.md` - Expected paper counts
- `README.md` - Detailed expected outcomes by stage

---

## Execution Instructions

### Environment Setup

**Required environment variables** (check `.env` in project root):
```bash
ANTHROPIC_API_KEY=sk-ant-...  # Required for screening & RAG
```

**Python version**: 3.10-3.14 (verify with `python3 --version`)

**Dependencies**: Install from project root
```bash
cd ../../  # Navigate to ResearcherRAG root
pip install -r requirements.txt
```

### Pipeline Execution Sequence

**IMPORTANT**: Scripts MUST run in order 01 → 02 → 03 → 04 → 05 → 06 → 07

Each script depends on outputs from previous stage.

#### Stage 1: Fetch Papers
```bash
cd ../../  # From ResearcherRAG root
python scripts/01_fetch_papers.py \
  --project examples/ai-chatbots-language-learning \
  --query "chatbot language learning speaking"
```

**Expected output**:
- `data/01_identification/semantic_scholar_results.csv` (~210 papers)
- `data/01_identification/openalex_results.csv` (~175 papers)
- `data/01_identification/arxiv_results.csv` (~18 papers)

**Validation check**:
```bash
wc -l examples/ai-chatbots-language-learning/data/01_identification/*.csv
# Total should be 350-450 papers across all files
```

**If validation fails**: Check logs at `logs/fetch_papers.log` for API errors

---

#### Stage 2: Deduplicate
```bash
python scripts/02_deduplicate.py \
  --project examples/ai-chatbots-language-learning
```

**Expected output**:
- `data/01_identification/deduplicated.csv` (~301 papers, 25% reduction)

**Validation check**:
```bash
wc -l examples/ai-chatbots-language-learning/data/01_identification/deduplicated.csv
# Should be ~301 lines (±50)
```

---

#### Stage 3: Screen Papers (AI-assisted)
```bash
python scripts/03_screen_papers.py \
  --project examples/ai-chatbots-language-learning \
  --question "How do AI chatbots improve speaking skills in language learning?"
```

**Expected output**:
- `data/02_screening/relevant_papers.csv` (~79 papers, 26% relevance rate)
- `data/02_screening/excluded_papers.csv` (~222 papers)

**Validation checks**:
```bash
# Count relevant papers
wc -l examples/ai-chatbots-language-learning/data/02_screening/relevant_papers.csv
# Should be 60-100 papers

# Calculate relevance rate
# relevant / total should be 0.20-0.35 (20-35%)
```

**If relevance <15%**: Query too broad, consider refining
**If relevance >50%**: Query too narrow, may miss papers

---

#### Stage 4: Download PDFs
```bash
python scripts/04_download_pdfs.py \
  --project examples/ai-chatbots-language-learning
```

**Expected output**:
- `data/03_pdfs/*.pdf` (~45 PDFs, 57% success rate)
- `data/03_pdfs/papers_metadata.csv`

**Validation checks**:
```bash
# Count PDFs
ls examples/ai-chatbots-language-learning/data/03_pdfs/*.pdf | wc -l
# Should be 40-60 PDFs (50-70% success rate is normal)

# Check for corrupted PDFs
for pdf in examples/ai-chatbots-language-learning/data/03_pdfs/*.pdf; do
  pdfinfo "$pdf" > /dev/null 2>&1 || echo "Corrupted: $pdf"
done
```

**Note**: 30-50% failure rate is EXPECTED (paywalls). This is NOT an error.

---

#### Stage 5: Build RAG System
```bash
python scripts/05_build_rag.py \
  --project examples/ai-chatbots-language-learning
```

**Expected output**:
- `data/04_rag/chroma_db/` directory with vector database
- `data/04_rag/rag_config.json`

**Validation checks**:
```bash
# Check vector DB exists
ls -lh examples/ai-chatbots-language-learning/data/04_rag/chroma_db/
# Should contain index/ folder and chroma.sqlite3

# Estimate database size
du -sh examples/ai-chatbots-language-learning/data/04_rag/chroma_db/
# Should be 80-150 MB for ~45 papers

# Test RAG with sample query
python scripts/06_query_rag.py \
  --project examples/ai-chatbots-language-learning \
  --query "What are the main benefits of chatbots?" \
  --limit 1
# Should return coherent answer with paper citations
```

---

#### Stage 6: Interactive Queries (Optional)
```bash
python scripts/06_query_rag.py \
  --project examples/ai-chatbots-language-learning \
  --interactive
```

**Sample queries for validation**:
1. "What methodologies are used to evaluate chatbot effectiveness?"
2. "How do chatbots compare to human tutors?"
3. "What are the limitations of current systems?"

**Expected behavior**: Each answer includes citations like 【F:data/03_pdfs/0042_paper.pdf†L156】

---

#### Stage 7: Generate PRISMA Diagram
```bash
python scripts/07_generate_prisma.py \
  --project examples/ai-chatbots-language-learning
```

**Expected output**:
- `outputs/prisma_diagram.png`
- `outputs/prisma_diagram.pdf`
- `outputs/statistics.json`

**Validation checks**:
```bash
# Verify PRISMA diagram exists
ls -lh examples/ai-chatbots-language-learning/outputs/prisma_diagram.*

# Validate statistics JSON
cat examples/ai-chatbots-language-learning/outputs/statistics.json
# Should contain actual counts matching data files
```

**CRITICAL**: PRISMA counts MUST match actual pipeline outputs. NEVER use placeholder numbers.

---

## Programmatic Validation (YOU MUST RUN ALL)

After completing ANY task that modifies data files, run ALL validation checks:

### 1. Data Integrity Checks
```bash
# No duplicate papers in final dataset
cd examples/ai-chatbots-language-learning
python -c "
import pandas as pd
df = pd.read_csv('data/02_screening/relevant_papers.csv')
duplicates = df.duplicated(subset=['doi']).sum()
assert duplicates == 0, f'Found {duplicates} duplicate papers'
print('✅ No duplicates')
"
```

### 2. Statistical Range Checks
```bash
# Paper counts within expected ranges
python -c "
import pandas as pd

# Identified papers
identified = len(pd.read_csv('data/01_identification/deduplicated.csv'))
assert 350 <= identified <= 450, f'Identified {identified}, expected 350-450'

# Screened papers
screened = len(pd.read_csv('data/02_screening/relevant_papers.csv'))
assert 60 <= screened <= 100, f'Screened {screened}, expected 60-100'

# Relevance rate
relevance = screened / identified
assert 0.20 <= relevance <= 0.35, f'Relevance {relevance:.2%}, expected 20-35%'

print(f'✅ All statistics valid')
print(f'   Identified: {identified}')
print(f'   Screened: {screened}')
print(f'   Relevance: {relevance:.1%}')
"
```

### 3. File Integrity Checks
```bash
# All PDFs are readable
cd data/03_pdfs
for pdf in *.pdf; do
  if ! pdfinfo "$pdf" > /dev/null 2>&1; then
    echo "❌ Corrupted PDF: $pdf"
    exit 1
  fi
done
echo "✅ All PDFs readable"
```

### 4. RAG Quality Checks
```bash
# Vector database returns relevant results
cd ../../
python -c "
import sys
sys.path.append('.')
from scripts.06_query_rag import query_rag

result = query_rag(
    project='examples/ai-chatbots-language-learning',
    query='What are the main benefits of AI chatbots?',
    k=5
)

assert len(result['sources']) >= 3, 'RAG returned too few sources'
assert any('chatbot' in s.lower() for s in result['sources']), 'Sources not relevant'

print('✅ RAG quality check passed')
"
```

### 5. PRISMA Diagram Validation
```bash
# PRISMA counts match actual data
python -c "
import json
import pandas as pd

# Load PRISMA statistics
with open('outputs/statistics.json') as f:
    stats = json.load(f)

# Load actual data
identified = len(pd.read_csv('data/01_identification/deduplicated.csv'))
screened = len(pd.read_csv('data/02_screening/relevant_papers.csv'))

# Validate
assert stats['identified'] == identified, f'PRISMA shows {stats[\"identified\"]}, actual {identified}'
assert stats['included'] == screened, f'PRISMA shows {stats[\"included\"]}, actual {screened}'

print('✅ PRISMA diagram accurate')
"
```

---

## Code Style and Conventions

### Python Style
- Follow PEP 8
- Use type hints for function signatures
- Prefer pathlib over os.path for file operations

### File Naming
- Papers: `0001_FirstAuthor_Year.pdf`, `0002_SecondAuthor_Year.pdf`, etc.
- CSVs: snake_case (e.g., `relevant_papers.csv`)
- Logs: `{script_name}.log`

### Error Handling
- Always log errors to `logs/` directory
- Include timestamps in log entries
- Provide actionable error messages

---

## Git Workflow

### Committing Changes

**IMPORTANT**: This is a RESEARCH project, not software development.

**DO commit**:
- New data files from pipeline execution
- Generated outputs (PRISMA diagrams, statistics)
- Updated `.researcherrag/context.json`

**DO NOT commit**:
- API keys or `.env` files
- Temporary files or caches
- Large intermediate files (>10MB)

### Commit Message Format
```
stage-X: Brief description of what was run

- Fetched X papers from Y databases
- Screened Z papers, W relevant
- Downloaded N PDFs (M% success rate)

Statistics: [attach summary]
```

**Example**:
```bash
git add examples/ai-chatbots-language-learning/data/01_identification/*.csv
git commit -m "stage-1: Fetch papers from 3 databases

- Semantic Scholar: 210 papers
- OpenAlex: 175 papers
- arXiv: 18 papers
- Total: 403 papers identified"
```

---

## Domain-Specific Knowledge

### Education Research Terminology
- **Chatbot** = Conversational agent = Dialogue system = Virtual agent (use as synonyms)
- **Speaking skills** = Oral proficiency = Fluency = Pronunciation (outcome measures)
- **Language learning** = Second language acquisition = L2 = ESL/EFL (domain)

### Common Methodologies in This Field
- Pre/post-test designs with speaking assessments (IELTS, TOEFL)
- Likert-scale surveys (learner satisfaction, anxiety, motivation)
- Conversation analysis (turn-taking, error correction)
- Mixed methods (combining quantitative + qualitative)

### Expected Themes (for validation)
When querying RAG, results should include papers on:
- Pronunciation improvement
- Fluency development
- Speaking anxiety reduction
- Learner motivation
- Immediate feedback mechanisms
- Conversational practice opportunities

**If RAG returns ONLY papers on text-based chatbots (no speaking component)**: Something is wrong with screening.

---

## Expected Results (Statistical Targets)

From `expected_results/EXPECTED_STATISTICS.md`:

| Stage | Metric | Expected Value | Tolerance |
|-------|--------|----------------|-----------|
| 1 | Papers identified | 403 | ±50 |
| 1 | Duplicates | 102 (25%) | ±5% |
| 2 | After deduplication | 301 | ±50 |
| 3 | Relevance rate | 26% | 20-35% |
| 3 | Relevant papers | 79 | 60-100 |
| 4 | PDF success rate | 57% | 50-70% |
| 4 | PDFs downloaded | 45 | 40-60 |
| 5 | Papers in RAG | 45 | 40-60 |
| 5 | Total chunks | 850 | 700-1000 |
| 5 | Avg chunks/paper | 19 | 15-25 |

**If actual values fall OUTSIDE tolerance**: Investigate before proceeding.

---

## Common Issues and Solutions

### Issue: API Rate Limiting (Stage 1)
**Symptom**: Fewer papers than expected (~200 instead of ~400)
**Diagnosis**: Check `logs/fetch_papers.log` for "429 Too Many Requests"
**Solution**:
```bash
# Semantic Scholar: 1 req/sec with API key, 100/5min without
# Add delays between requests
python scripts/01_fetch_papers.py --delay 2
```

### Issue: Low Relevance Rate (Stage 3)
**Symptom**: <15% papers marked relevant
**Diagnosis**: Query too broad (includes general chatbots without speaking component)
**Solution**:
```bash
# Revise query to be more specific
python scripts/03_screen_papers.py \
  --question "Do AI chatbots improve PRONUNCIATION in language learning?" \
  # More specific than "speaking skills"
```

### Issue: Low PDF Success (Stage 4)
**Symptom**: <40% PDFs downloaded
**Diagnosis**: Many education papers are paywalled
**Solution**: This is EXPECTED. 40-70% success is normal for education research.
```bash
# Optional: Try with institutional VPN or Sci-Hub fallback
python scripts/04_download_pdfs.py --use-scihub  # If implemented
```

### Issue: RAG Returns Irrelevant Results (Stage 6)
**Symptom**: Query "What methods are used?" returns generic ML papers
**Diagnosis**: Too few papers in database OR chunks too small
**Solution**:
```bash
# Rebuild RAG with larger chunks
python scripts/05_build_rag.py \
  --chunk-size 1500 \
  --chunk-overlap 300
```

---

## PR Message Guidelines

When creating pull requests with research results:

**Title Format**: `results: Stage X - [Brief description]`

**Body Format**:
```markdown
## Pipeline Stage

Stage X: [Stage name]

## Execution Summary

- Script: `scripts/0X_script_name.py`
- Runtime: [X minutes/hours]
- Status: ✅ Success / ⚠️ Warnings / ❌ Errors

## Results

| Metric | Expected | Actual | Status |
|--------|----------|--------|--------|
| Papers identified | 403 | 398 | ✅ Within range |
| Relevance rate | 26% | 24% | ✅ Within range |
| PDFs downloaded | 45 | 42 | ✅ Within range |

## Validation Checks

- [x] Data integrity checks passed
- [x] Statistical ranges validated
- [x] File integrity verified
- [x] RAG quality tested (if applicable)

## Files Changed

- Added: `data/0X_stage/*.csv`
- Modified: `.researcherrag/context.json`

## Next Steps

Proceed to Stage X+1: [Next stage name]

---
【F:logs/script_name.log†L1-L50】
```

---

## Testing Instructions

**CRITICAL**: Run ALL tests after code changes, even for documentation.

### Unit Tests
```bash
cd ../../  # ResearcherRAG root
pytest tests/test_fetch_papers.py
pytest tests/test_deduplicate.py
pytest tests/test_screen_papers.py
```

### Integration Tests
```bash
# Test full pipeline on small sample
pytest tests/test_pipeline_integration.py --project examples/ai-chatbots-language-learning
```

### Validation Tests
```bash
# Test expected vs actual results
pytest tests/test_expected_results.py --project examples/ai-chatbots-language-learning
```

---

## Citations Format

When referencing files or terminal outputs in your final response, use:

**File citations**:
`【F:examples/ai-chatbots-language-learning/data/02_screening/relevant_papers.csv†L42】`

**Terminal citations**:
`【T:bash†python scripts/01_fetch_papers.py】`

**Multi-line citations**:
`【F:outputs/statistics.json†L1-L20】`

---

## Parent Project Context

For ResearcherRAG **system-level instructions**, see:
- `../../AGENTS.md` - Main Codex agent instructions
- `../../scripts/README.md` - Script usage documentation

This file provides **project-specific instructions** for:
- Expected results for THIS research topic
- Domain terminology for THIS field (education)
- Validation checks for THIS type of review

---

**Last updated**: October 14, 2025
**Scope**: `examples/ai-chatbots-language-learning/` directory tree
**Maintained by**: ResearcherRAG team
