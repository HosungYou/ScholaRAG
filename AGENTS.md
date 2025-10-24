# AGENTS.md - ScholaRAG

## 🤖 Codex Agent Instructions

**For**: OpenAI Codex, Cursor AI, GitHub Copilot, and other task-oriented coding agents

**Architecture**: Task-based bash workflows with Quick Context embedding + Universal Reference Library

**Designed for**: Researchers who prefer terminal commands over conversation-first interaction (Claude users: see SKILL.md)

---

## 📋 Repository Context

**Type**: Academic research automation framework
**Purpose**: PRISMA 2020-compliant systematic literature review with RAG-powered analysis
**Technology**: Python 3.10+ | ChromaDB | Claude API | Academic APIs (Semantic Scholar, OpenAlex, arXiv)
**Deployment**: Local execution (no cloud deployment)

**⚠️ Critical Philosophy**:
- **Researchers execute commands** → Scripts run → Outputs validated → Next stage
- **Scientific integrity first** → Never fabricate results, always show actual counts
- **SSOT (Single Source of Truth)** → All configuration in `config.yaml`

---

## 🎯 7-Stage Pipeline Overview

| Stage | Script | Duration | Input | Output | Validation |
|-------|--------|----------|-------|--------|------------|
| 1 | `01_fetch_papers.py` | 30-60 min | config.yaml | combined.csv (20K-30K papers) | Paper count check |
| 2 | `02_deduplicate.py` | 5-10 min | combined.csv | deduplicated.csv (60-80% retained) | Duplicate rate |
| 3 | `03_screen_papers.py` | 60-120 min | deduplicated.csv | relevant.csv (50% or 90% threshold) | Relevance rate |
| 4 | `04_download_pdfs.py` | 120-240 min | relevant.csv | pdfs/*.pdf (40-60% success) | PDF count |
| 5 | `05_build_rag.py` | 30-60 min | pdfs/*.pdf | chroma/ (vector DB) | Query test |
| 6 | `06_query_rag.py` | Ongoing | chroma/ | research insights | Citation format |
| 7 | `07_generate_prisma.py` | 5 min | All CSVs | prisma_diagram.png | Count accuracy |

**Expected total duration**: 4-8 hours (mostly automated, run overnight)

---

## 🔑 Critical Branching Point: project_type

### Quick Context (Essential Background)

**ScholaRAG supports 2 modes** that fundamentally change the pipeline behavior:

| Mode | Threshold | Typical Input | Typical Output | Best For |
|------|-----------|---------------|----------------|----------|
| `knowledge_repository` | 50% AI confidence (lenient) | 20K-30K papers | 15K-20K papers | Teaching materials, AI assistant, domain exploration |
| `systematic_review` | 90% AI confidence (strict) | 1K-5K papers | 50-300 papers | Meta-analysis, dissertation, journal publication |

**Key differences**:
- **Screening** (Stage 3): 50% vs 90% threshold in `03_screen_papers.py`
- **PRISMA diagram title** (Stage 7): "Knowledge Repository" vs "Systematic Review"
- **Validation expectations**: Comprehensive breadth vs rigorous quality

**Full decision tree**: [skills/reference/project_type_decision_tree.md](skills/reference/project_type_decision_tree.md)

**When to read decision tree**:
- Researcher asks: "Which mode should I choose?"
- Researcher unsure about expected paper counts
- Stage 1 initialization (proactively suggest based on research goals)

---

## 📋 Task 1: Initialize New Project

### Prerequisites

```bash
# Check Python version (3.10+ required)
python3 --version

# Verify API key exists
grep ANTHROPIC_API_KEY ~/.zshrc || echo "⚠️ Add ANTHROPIC_API_KEY to environment"

# Navigate to ScholaRAG root
cd "/Volumes/External SSD/Projects/Research/ScholaRAG"
```

### Quick Context: project_type Decision

**Ask researcher these 2 questions**:

1. **Will you publish this as a systematic review in an academic journal?**
   - Yes → `systematic_review` ✅ (Skip to Step 2)
   - No → Go to Question 2

2. **Do you need comprehensive domain coverage (15,000+ papers)?**
   - Yes → `knowledge_repository` ✅ (For teaching, AI assistant, exploration)
   - No → `systematic_review` ✅ (Focused high-quality subset)

**Reference**: [skills/reference/project_type_decision_tree.md](skills/reference/project_type_decision_tree.md)

### Execution

```bash
# Interactive initialization
python scholarag_cli.py init

# Follow prompts:
# - Project name: [Descriptive name, e.g., "AI-Chatbots-Language-Learning"]
# - Research question: [Clear, answerable question]
# - Domain: [education, medicine, cs, etc.]
# - project_type: [knowledge_repository OR systematic_review]
# - Year range: [e.g., 2015-2025]
# - Databases: [semantic_scholar, openalex, arxiv]

# Output: projects/YYYY-MM-DD_ProjectName/ created with config.yaml
```

### Validation Checklist

```bash
# 1. Check project folder exists
ls -la "projects/$(date +%Y-%m-%d)"_*

# 2. Validate config.yaml
cat projects/YYYY-MM-DD_ProjectName/config.yaml | grep -E "project_type|research_question|year_start"

# 3. Verify project_type value
PROJECT_TYPE=$(grep "project_type:" projects/YYYY-MM-DD_ProjectName/config.yaml | awk '{print $2}')
if [[ "$PROJECT_TYPE" != "knowledge_repository" && "$PROJECT_TYPE" != "systematic_review" ]]; then
  echo "❌ Invalid project_type: $PROJECT_TYPE"
else
  echo "✅ Valid project_type: $PROJECT_TYPE"
fi

# 4. Check year range is realistic
YEAR_START=$(grep "year_start:" projects/YYYY-MM-DD_ProjectName/config.yaml | awk '{print $2}')
YEAR_END=$(grep "year_end:" projects/YYYY-MM-DD_ProjectName/config.yaml | awk '{print $2}')
YEAR_RANGE=$((YEAR_END - YEAR_START))
if [ $YEAR_RANGE -gt 25 ]; then
  echo "⚠️ Year range >25 years may yield too many papers"
fi
```

### Common Issues

**Issue**: "Too broad research question"
- **Fix**: Ask researcher to narrow scope (specific intervention, population, outcome)
- **Example**: "How do chatbots help?" → "How do AI chatbots improve speaking proficiency in EFL learners?"

**Issue**: "Unsure about project_type"
- **Fix**: Show [decision tree](skills/reference/project_type_decision_tree.md), ask about publication goals

---

## 📋 Task 2: Design Search Query (Stage 2)

### Quick Context: API Limitations

**ScholaRAG uses 3 academic APIs**:

| API | Query Syntax | Rate Limit | PDF Availability |
|-----|--------------|------------|------------------|
| Semantic Scholar | Natural language | 100 req/5min | ~40% |
| OpenAlex | Natural language + filters | 100 req/sec (polite pool) | ~50% |
| arXiv | Boolean (all:term AND all:term) | 1 req/3sec | ~100% |

**Full API reference**: [skills/reference/api_reference.md](skills/reference/api_reference.md)

### Execution

```bash
# Edit config.yaml with search query
cd projects/YYYY-MM-DD_ProjectName
vim config.yaml

# Add search_query field:
# search_query: "(chatbot OR conversational agent) AND (language learning OR L2)"

# Validate query syntax
python ../../scripts/validate_query.py --config config.yaml
```

### Validation Checklist

```bash
# 1. Check query includes Boolean operators
grep -E "AND|OR" config.yaml || echo "⚠️ Consider Boolean operators for specificity"

# 2. Verify synonyms included
echo "Query should include synonyms (e.g., chatbot OR agent, learning OR acquisition)"

# 3. Estimate paper count (dry run)
python ../../scripts/01_fetch_papers.py --project . --dry-run

# Expected ranges by project_type:
# - knowledge_repository: 10K-30K papers
# - systematic_review: 500-5K papers
```

### Common Issues

**Issue**: "Query too narrow (<100 papers)"
- **Fix**: Add synonyms, broaden terms
- **Example**: "AI chatbot speaking" → "(chatbot OR agent) AND (speaking OR oral OR pronunciation)"

**Issue**: "Query too broad (>50K papers)"
- **Fix**: Add specificity (population, intervention type, outcome)
- **Example**: "chatbot learning" → "chatbot AND language AND speaking AND proficiency"

---

## 📋 Task 3: Configure PRISMA Criteria (Stage 3 Prep)

### Quick Context: Threshold Implications

**Stage 3 (`03_screen_papers.py`) uses AI to screen papers for relevance**:

- **knowledge_repository mode** (50% threshold):
  - Lenient: Keeps papers with moderate relevance
  - Removes only spam, off-topic, non-academic
  - Typical retention: 80-90% of deduplicated papers

- **systematic_review mode** (90% threshold):
  - Strict: Keeps only highly relevant papers
  - PRISMA 2020 compliant inclusion criteria
  - Typical retention: 2-10% of deduplicated papers

**Threshold is set automatically** based on `project_type` in config.yaml.

**Reference**: [skills/reference/config_schema.md](skills/reference/config_schema.md)

### Execution

```bash
# Edit config.yaml to add PRISMA criteria
cd projects/YYYY-MM-DD_ProjectName
vim config.yaml

# Add inclusion/exclusion criteria:
# inclusion_criteria:
#   - "RCT or quasi-experimental design"
#   - "Measures speaking proficiency outcome"
#   - "AI chatbot intervention"
# exclusion_criteria:
#   - "Non-English language papers"
#   - "Opinion pieces or editorials"
```

### Validation Checklist

```bash
# 1. Verify criteria are specific
wc -l < <(grep -A 10 "inclusion_criteria" config.yaml) || echo "Add at least 3 inclusion criteria"

# 2. Check for contradictions
echo "Review criteria for conflicts (e.g., exclude qualitative + require interviews)"

# 3. Validate project_type matches criteria strictness
PROJECT_TYPE=$(grep "project_type:" config.yaml | awk '{print $2}')
if [ "$PROJECT_TYPE" = "systematic_review" ]; then
  echo "✅ Strict criteria expected for systematic_review mode"
fi
```

---

## 📋 Task 4: Execute Full Pipeline (Stages 1-5)

### Quick Context: Expected Durations & Success Rates

| Stage | Duration | Success Rate | What Affects It |
|-------|----------|--------------|-----------------|
| Fetch (01) | 30-60 min | N/A | API rate limits, query specificity |
| Dedup (02) | 5-10 min | 60-80% retention | Query overlap across databases |
| Screen (03) | 60-120 min | 50% or 90% | `project_type` setting |
| PDFs (04) | 120-240 min | 40-60% | Open access availability |
| RAG (05) | 30-60 min | N/A | PDF count from Stage 4 |

**Total**: ~4-8 hours (run overnight recommended)

### Execution

```bash
# Navigate to project folder
cd projects/YYYY-MM-DD_ProjectName

# Stage 1: Fetch papers from all 3 databases
python ../../scripts/01_fetch_papers.py --project .

# Stage 2: Remove duplicates
python ../../scripts/02_deduplicate.py --project .

# Stage 3: AI-assisted screening (LONG DURATION - uses Claude API)
python ../../scripts/03_screen_papers.py --project .

# Stage 4: Download PDFs (LONG DURATION - network I/O)
python ../../scripts/04_download_pdfs.py --project .

# Stage 5: Build RAG vector database
python ../../scripts/05_build_rag.py --project .
```

### Validation Checklist

```bash
# After each stage, validate outputs:

# Stage 1: Check paper counts
wc -l data/01_identification/combined.csv
# Expected: 10K-30K (knowledge_repository) or 500-5K (systematic_review)

# Stage 2: Check deduplication rate
BEFORE=$(wc -l < data/01_identification/combined.csv)
AFTER=$(wc -l < data/01_identification/deduplicated.csv)
DEDUP_RATE=$(echo "scale=2; ($BEFORE - $AFTER) / $BEFORE * 100" | bc)
echo "Deduplication removed $DEDUP_RATE% (expected 20-40%)"

# Stage 3: Check screening retention
BEFORE=$(wc -l < data/01_identification/deduplicated.csv)
AFTER=$(wc -l < data/02_screening/relevant.csv)
RETENTION=$(echo "scale=2; $AFTER / $BEFORE * 100" | bc)
PROJECT_TYPE=$(grep "project_type:" config.yaml | awk '{print $2}')
if [ "$PROJECT_TYPE" = "knowledge_repository" ]; then
  echo "Retention: $RETENTION% (expected 80-90% for knowledge_repository)"
elif [ "$PROJECT_TYPE" = "systematic_review" ]; then
  echo "Retention: $RETENTION% (expected 2-10% for systematic_review)"
fi

# Stage 4: Check PDF download success
PDF_COUNT=$(ls data/pdfs/*.pdf 2>/dev/null | wc -l)
EXPECTED=$(wc -l < data/02_screening/relevant.csv)
SUCCESS_RATE=$(echo "scale=2; $PDF_COUNT / $EXPECTED * 100" | bc)
echo "PDF success: $SUCCESS_RATE% (expected 40-60%)"

# Stage 5: Test RAG with sample query
python ../../scripts/06_query_rag.py --project . --query "What are the main findings?" --limit 3
# Expected: 3 relevant excerpts with citations 【F:path†L123】
```

### Common Issues

**Issue**: "Stage 1 returns <100 papers"
- **Diagnosis**: Query too narrow
- **Fix**: See [Task 2: Design Search Query](#task-2-design-search-query-stage-2)

**Issue**: "Stage 3 retention 0% (all papers excluded)"
- **Diagnosis**:
  - 90% threshold too strict for broad query
  - OR inclusion criteria contradict query
- **Fix**:
  ```bash
  # Check project_type
  grep "project_type:" config.yaml
  # If systematic_review, consider switching to knowledge_repository
  # OR narrow query to match strict criteria
  ```

**Issue**: "Stage 4 PDF success <20%"
- **Diagnosis**: Many paywalled papers
- **Fix**: Expected for some domains (medicine, social science). Filter for open access in Stage 1:
  ```python
  # In scripts/01_fetch_papers.py, add filter:
  # OpenAlex: 'filter': 'publication_year:2015-2025,is_oa:true'
  ```

**Reference**: [skills/reference/troubleshooting.md](skills/reference/troubleshooting.md)

---

## 📋 Task 5: Research Conversation (Stage 6)

### Quick Context: 7 Research Scenarios

**Stage 6 branches into specialized conversation modes**:

| Mode | Purpose | Example Query | Output Format |
|------|---------|---------------|---------------|
| **overview** | High-level themes | "What are main themes?" | Narrative summary |
| **hypothesis** | Evidence validation | "Does X improve Y?" | For/against with effect sizes |
| **statistics** | Data extraction | "Extract all correlations" | CSV table |
| **methods** | Methodology comparison | "What RCT designs used?" | Method taxonomy |
| **contradictions** | Conflict detection | "Where do findings disagree?" | Contradiction analysis |
| **policy** | Translation to practice | "What should policymakers do?" | Recommendations |
| **grant** | Future research | "What gaps remain?" | Research proposals |

**Full scenario guide**: [skills/claude_only/stage6_research_conversation.md](skills/claude_only/stage6_research_conversation.md)

### Execution

```bash
# Interactive mode (conversation-style)
cd projects/YYYY-MM-DD_ProjectName
python ../../scripts/06_query_rag.py --project . --interactive

# Batch mode (automated extraction)
python ../../scripts/06_query_rag.py --project . \
  --query "Extract all correlation coefficients between chatbot use and speaking scores" \
  --output extraction_results.csv

# Scenario-specific mode
python ../../scripts/06_query_rag.py --project . \
  --scenario hypothesis \
  --hypothesis "AI chatbots improve speaking proficiency more than human tutors"
```

### Validation Checklist

```bash
# 1. Check citations format
python ../../scripts/06_query_rag.py --project . --query "What are main findings?" | grep -E "【F:.*†L[0-9]+】"
# Should include citations like 【F:pdfs/0042_Smith_2023.pdf†L234】

# 2. Verify no hallucination (all claims cited)
# Manually review 5 random outputs, check each claim has citation

# 3. Test retrieval relevance
python ../../scripts/06_query_rag.py --project . --query "randomXYZ123nonsense"
# Should return: "No relevant information found" (not fabricated answers)
```

---

## 📋 Task 6: Generate PRISMA Diagram (Stage 7)

### Quick Context: PRISMA 2020 Requirements

**PRISMA diagram must show**:
1. **Identification**: Papers from each database
2. **Deduplication**: Papers removed as duplicates
3. **Screening**: Papers excluded by AI relevance screening
4. **Eligibility**: Papers excluded due to no PDF access
5. **Included**: Final papers in RAG database

**Counts MUST be actual** (never fabricate or round for aesthetics).

**Diagram title changes by project_type**:
- `knowledge_repository` → "Knowledge Repository: [Project Name]"
- `systematic_review` → "Systematic Review: [Project Name]"

### Execution

```bash
# Generate PRISMA diagram
cd projects/YYYY-MM-DD_ProjectName
python ../../scripts/07_generate_prisma.py --project .

# Output: outputs/prisma_flowchart.png
```

### Validation Checklist

```bash
# 1. Verify counts match actual CSVs
SEMANTIC_SCHOLAR=$(grep -c "semantic_scholar" data/01_identification/combined.csv || echo 0)
OPENALEX=$(grep -c "openalex" data/01_identification/combined.csv || echo 0)
ARXIV=$(grep -c "arxiv" data/01_identification/combined.csv || echo 0)

COMBINED=$(wc -l < data/01_identification/combined.csv)
DEDUP=$(wc -l < data/01_identification/deduplicated.csv)
RELEVANT=$(wc -l < data/02_screening/relevant.csv)
PDF_COUNT=$(ls data/pdfs/*.pdf 2>/dev/null | wc -l)

echo "Identification: S2=$SEMANTIC_SCHOLAR, OA=$OPENALEX, arXiv=$ARXIV"
echo "Combined: $COMBINED"
echo "After dedup: $DEDUP"
echo "After screening: $RELEVANT"
echo "With PDFs: $PDF_COUNT"

# Compare with diagram (manual inspection):
open outputs/prisma_flowchart.png

# 2. Check diagram title matches project_type
PROJECT_TYPE=$(grep "project_type:" config.yaml | awk '{print $2}')
echo "Diagram title should start with:"
if [ "$PROJECT_TYPE" = "knowledge_repository" ]; then
  echo "  'Knowledge Repository:'"
elif [ "$PROJECT_TYPE" = "systematic_review" ]; then
  echo "  'Systematic Review:'"
fi

# 3. Verify PRISMA 2020 compliance
python ../../scripts/validate_prisma.py --project .
```

### Common Issues

**Issue**: "Counts don't match CSVs"
- **Diagnosis**: Script bug or CSV corruption
- **Fix**:
  ```bash
  # Re-run with debug mode
  python ../../scripts/07_generate_prisma.py --project . --debug
  # Check logs/07_generate_prisma.log for discrepancies
  ```

**Issue**: "Wrong diagram title"
- **Diagnosis**: `project_type` in config.yaml doesn't match intent
- **Fix**:
  ```bash
  # Edit config.yaml
  vim config.yaml
  # Change project_type, re-run:
  python ../../scripts/07_generate_prisma.py --project .
  ```

---

## 📋 Task 7: Sync with Main Repo (For ScholaRAG-helper)

### Quick Context: Repository Relationship

**ScholaRAG** (main repo):
- Code: scripts/, prompts/, scholarag_cli.py
- Documentation: SKILL.md, AGENTS.md, skills/

**ScholaRAG-helper** (homepage repo):
- Website: frontend/app/guide/ (Next.js)
- Discussions: discussion/ (refactoring plans, strategies)

**When to sync**: After code changes in ScholaRAG → Update website docs

### Execution

```bash
# 1. Check main repo for changes
cd "/Volumes/External SSD/Projects/Research/ScholaRAG"
git log --oneline -10

# 2. Identify documentation impacts
# Example: If prompts/02_query_strategy.md updated → Update guide/02-query-strategy/page.tsx

# 3. Navigate to helper repo
cd "/Volumes/External SSD/Projects/Research/ScholaRAG-helper"

# 4. Update corresponding guide page
vim frontend/app/guide/02-query-strategy/page.tsx

# 5. Update search index for new terms
vim frontend/components/SearchBar.tsx
# Add entry:
# {
#   title: 'Query Strategy',
#   href: '/guide/02-query-strategy',
#   excerpt: 'Design Boolean search queries for Semantic Scholar, OpenAlex, arXiv',
#   chapter: 'Chapter 2'
# }

# 6. Test locally
cd frontend
npm run dev
# Open http://localhost:3000/guide
# Press Cmd+K, test search: "query", "Boolean", "API"

# 7. Commit and push
cd ..
git add .
git commit -m "docs: Sync with ScholaRAG v1.0.X query strategy updates"
git push origin main

# 8. Verify Vercel deployment (2-3 min)
# Visit: https://vercel.com/hosung-yous-projects/scholar-rag-helper/deployments
```

**Reference**: [ScholaRAG-helper/AGENTS.md](../ScholaRAG-helper/AGENTS.md)

---

## 🔍 Validation Checklist (Universal)

After ANY changes to ScholaRAG code, run:

```bash
# 1. Python syntax check
python3 -m py_compile scripts/*.py

# 2. Test imports
python3 -c "from scripts.utils.file_manager import load_config; print('✅ Imports OK')"

# 3. Config validation
python3 scripts/validate_config.py --config projects/*/config.yaml

# 4. PRISMA count integrity
for PROJECT in projects/*/; do
  echo "Validating $PROJECT"
  python3 scripts/validate_prisma.py --project "$PROJECT"
done

# 5. Git sync status
git status
# Should show: "nothing to commit, working tree clean"

# 6. Remote sync
git log origin/main --oneline -3
# Should include your latest commits
```

---

## 📊 Common Workflows

### Workflow 1: Full Review (Start to Finish)

```bash
# Day 1: Setup & Fetch (1-2 hours active, 2-4 hours passive)
python scholarag_cli.py init
cd projects/YYYY-MM-DD_ProjectName
python ../../scripts/01_fetch_papers.py --project .
python ../../scripts/02_deduplicate.py --project .

# Day 2: Screening & PDFs (30 min active, 4-6 hours passive)
python ../../scripts/03_screen_papers.py --project .  # Run overnight
python ../../scripts/04_download_pdfs.py --project .  # Run overnight

# Day 3: RAG & Analysis (2-4 hours active)
python ../../scripts/05_build_rag.py --project .
python ../../scripts/06_query_rag.py --project . --interactive

# Day 4: Documentation (1 hour)
python ../../scripts/07_generate_prisma.py --project .
# Manual: Write synthesis report using RAG insights
```

### Workflow 2: Iterate on Query

```bash
# If Stage 1 yields wrong paper count:

# 1. Edit query
vim config.yaml
# Modify search_query

# 2. Delete old results
rm -rf data/01_identification/*

# 3. Re-run fetch
python ../../scripts/01_fetch_papers.py --project .

# 4. Check new count
wc -l data/01_identification/combined.csv

# 5. Repeat until satisfactory (typical: 2-3 iterations)
```

### Workflow 3: Change project_type Mid-Stream

```bash
# Scenario: Chose systematic_review, got only 20 papers, want to switch to knowledge_repository

# 1. Edit config.yaml
vim config.yaml
# Change: project_type: systematic_review → project_type: knowledge_repository

# 2. Delete screening results
rm -rf data/02_screening/*

# 3. Re-run screening with new threshold (50% instead of 90%)
python ../../scripts/03_screen_papers.py --project .

# 4. Check new count
wc -l data/02_screening/relevant.csv
# Should be much higher (80-90% retention vs 2-10%)

# 5. Continue with Stage 4 (PDF download)
python ../../scripts/04_download_pdfs.py --project .
```

---

## 🚨 Error Recovery

### Build Failure

```bash
# 1. Check Python version
python3 --version
# Required: 3.10-3.14

# 2. Reinstall dependencies
pip install -r requirements.txt --upgrade

# 3. Check API key
echo $ANTHROPIC_API_KEY
# Should show: sk-ant-...

# 4. Run with debug mode
python scripts/03_screen_papers.py --project . --debug
# Check logs/03_screen_papers.log for errors
```

### API Rate Limit

```bash
# Semantic Scholar: 100 req/5min
# If hit:
# 1. Wait 5 minutes
# 2. Script auto-retries with exponential backoff
# 3. Check logs/01_fetch_papers.log for retry count

# arXiv: 1 req/3sec
# If hit:
# 1. Script includes 3-second delay (automatic)
# 2. No manual intervention needed
```

### Low PDF Success (<20%)

```bash
# Expected for paywalled domains (medicine, social science)
# Solutions:

# Option 1: Filter for open access in Stage 1
vim scripts/01_fetch_papers.py
# Line ~120: Add filter:
# 'filter': 'publication_year:2015-2025,is_oa:true'

# Option 2: Use institutional VPN/proxy (manual)
# Option 3: Accept limitation, proceed with available PDFs
```

**Reference**: [skills/reference/troubleshooting.md](skills/reference/troubleshooting.md)

---

## 📝 Documentation Standards

### Commit Messages

```bash
# Format: <type>: <description>
# Types: stage-1, stage-2, ..., stage-7, refactor, docs, fix

# Examples:
git commit -m "stage-1: Fetch 24,567 papers from 3 databases"
git commit -m "stage-3: Screen papers, 12% retention (2,945 relevant)"
git commit -m "fix: Correct deduplication logic for arXiv IDs"
git commit -m "docs: Update PRISMA criteria in config.yaml"
```

### File Naming

```bash
# Papers: 0001_FirstAuthor_Year.pdf
# CSVs: snake_case.csv (e.g., deduplicated.csv)
# Logs: {script_name}.log (e.g., 01_fetch_papers.log)
# Outputs: descriptive_name.{png,csv,json} (e.g., prisma_flowchart.png)
```

### Code Style

```python
# Follow PEP 8
# Use type hints
from pathlib import Path

def load_config(config_path: Path) -> dict:
    """Load YAML configuration file.

    Args:
        config_path: Path to config.yaml

    Returns:
        Dictionary with configuration

    Raises:
        FileNotFoundError: If config.yaml missing
    """
    ...
```

---

## 🔗 External Resources

### Universal Reference Library (Shared with Claude)

- **Project Type Decision Tree**: [skills/reference/project_type_decision_tree.md](skills/reference/project_type_decision_tree.md)
- **API Reference**: [skills/reference/api_reference.md](skills/reference/api_reference.md)
- **Config Schema**: [skills/reference/config_schema.md](skills/reference/config_schema.md)
- **Troubleshooting**: [skills/reference/troubleshooting.md](skills/reference/troubleshooting.md)

### Official Documentation

- **Homepage**: https://www.scholarag.com/
- **User Guides**: https://www.scholarag.com/guide
- **GitHub**: https://github.com/HosungYou/ScholaRAG

---

## ⚡ Quick Reference

### Important Paths

```
ScholaRAG/
├── AGENTS.md (this file - Codex instructions)
├── SKILL.md (Claude Code instructions)
├── skills/
│   ├── reference/ (Universal - both Codex + Claude)
│   └── claude_only/ (Progressive disclosure, Claude only)
├── scripts/ (Pipeline execution)
│   ├── 01_fetch_papers.py
│   ├── 02_deduplicate.py
│   ├── 03_screen_papers.py
│   ├── 04_download_pdfs.py
│   ├── 05_build_rag.py
│   ├── 06_query_rag.py
│   └── 07_generate_prisma.py
├── prompts/ (Stage prompts with metadata)
└── projects/ (User project folders)
    └── YYYY-MM-DD_ProjectName/
        ├── config.yaml (SSOT for all settings)
        ├── data/ (Pipeline outputs)
        └── outputs/ (PRISMA diagram, reports)
```

### Key Commands

```bash
# Initialization
python scholarag_cli.py init

# Pipeline execution (in project folder)
python ../../scripts/01_fetch_papers.py --project .
python ../../scripts/02_deduplicate.py --project .
python ../../scripts/03_screen_papers.py --project .
python ../../scripts/04_download_pdfs.py --project .
python ../../scripts/05_build_rag.py --project .
python ../../scripts/06_query_rag.py --project . --interactive
python ../../scripts/07_generate_prisma.py --project .

# Validation
python scripts/validate_config.py --config projects/*/config.yaml
python scripts/validate_prisma.py --project projects/YYYY-MM-DD_ProjectName

# Troubleshooting
python scripts/03_screen_papers.py --project . --debug
tail -f logs/01_fetch_papers.log
```

### Important URLs

- Homepage: https://www.scholarag.com/
- Docs: https://www.scholarag.com/guide
- GitHub: https://github.com/HosungYou/ScholaRAG
- Codebook: https://www.scholarag.com/codebook

---

## 🤝 Integration with Claude Code (SKILL.md)

**For Claude users**: See [SKILL.md](SKILL.md) for conversation-first workflow

**For Codex users (you)**: This file (AGENTS.md) provides task-based bash workflows

**Shared resources**: skills/reference/ folder (Universal Reference Library)

**Workflow comparison**:

| Aspect | Claude (SKILL.md) | Codex (AGENTS.md) |
|--------|-------------------|-------------------|
| **Style** | Conversation, Q&A, progressive disclosure | Bash commands, checklists, task execution |
| **Loading** | On-demand (load stage files as needed) | Upfront (read full file at start) |
| **Context** | Metadata blocks in prompts/*.md | Quick Context sections in tasks |
| **Execution** | Auto-execute after conversation validation | Manual bash commands |
| **Validation** | Completion checklist (conversational) | Bash validation scripts |
| **Reference** | Progressive links (load only when asked) | Quick Context + reference links |

**When to use which**:
- **Researchers** prefer Claude (conversation-first, guidance)
- **Power users** prefer Codex (terminal commands, automation)

---

**Last Updated**: 2025-10-24 (v2.0 - Hybrid Strategy Implementation)
**Replaces**: AGENTS.md v1.2.1 (2025-01-22)
**Compatible with**: ScholaRAG v1.0+, SKILL.md v2.0
**Token Budget**: ~600 lines (this file) + ~400-500 lines (reference files on-demand) = ~1,000 lines per session
