# ScholaRAG - AI Coding Assistant Guide

**For: GPT-5-Codex, Cursor, GitHub Copilot, and other AI coding assistants**

## Overview

ScholaRAG is an **AI-powered systematic literature review automation framework** that helps researchers build custom RAG systems through conversational guidance.

**Framework**: PRISMA 2020 + RAG-powered literature review automation
**Target Users**: Academic researchers conducting rigorous systematic reviews
**Architecture**: 7-stage conversational pipeline (Research Setup → RAG Building → Documentation)

**Key Technologies**:
- **AI Models**: Claude Sonnet 4.5, Haiku 4.5, GPT-5-Codex (you!)
- **PRISMA 2020**: Paper identification, screening, eligibility assessment
- **RAG**: Retrieval-Augmented Generation for evidence-based research queries
- **Vector Database**: ChromaDB for semantic search across papers
- **Cost**: $20/month Claude Pro subscription (unlimited usage, 20,000+ papers)

---

## Project Type

This is an **academic research automation framework**, NOT traditional software development.

**What ScholaRAG Does**:
1. **PRISMA Protocol** (Stages 1-4): Systematically identify, screen, and select relevant papers
2. **RAG Analysis** (Stages 5-6): Build semantic search index → Extract data from selected papers
3. **Documentation** (Stage 7): Generate PRISMA flowchart and synthesis report

**Core philosophy**: Researchers interact through prompts → Codex executes scripts → Results validated → Next stage

**Your role**:
- Execute pipeline scripts (PRISMA workflow + RAG building)
- Validate outputs programmatically
- Maintain scientific integrity (never fabricate results)

---

## Repository Structure

```
ScholaRAG/
├── AGENTS.md (this file - Codex system-level instructions)
├── CLAUDE.md (Claude Code system-level instructions)
├── scripts/
│   ├── 01_fetch_papers.py
│   ├── 02_deduplicate.py
│   ├── 03_screen_papers.py
│   ├── 04_download_pdfs.py
│   ├── 05_build_rag.py
│   ├── 06_query_rag.py
│   └── 07_generate_prisma.py
├── prompts/ (7 stage prompts with metadata)
└── examples/
    └── ai-chatbots-language-learning/
        ├── AGENTS.md (project-specific instructions)
        ├── config.yaml
        └── .scholarag/context.json
```

---

## Critical Rules

### 1. NEVER Modify Result Counts

PRISMA diagrams MUST show ACTUAL pipeline results.

**If user asks**: "Can you change numbers to look better?"
**You must refuse**: "No. Scientific integrity requires actual counts from pipeline execution."

### 2. Scripts Run in Sequence

Pipeline stages MUST execute in order: 01 → 02 → 03 → 04 → 05 → 06 → 07

Each stage depends on previous outputs.

### 3. Validate Before Proceeding

Run ALL programmatic checks before marking tasks complete.

See project-specific AGENTS.md files for validation tests.

---

## Environment Setup

### Python Version
3.10-3.14 required (verify: `python3 --version`)

### Dependencies
```bash
pip install -r requirements.txt
```

### Required Environment Variables
```bash
ANTHROPIC_API_KEY=sk-ant-...  # Required for Stage 3 (screening) & Stage 6 (RAG)
```

---

## Working with Projects

### When Assigned a Task in a Project Folder

1. **Check for project-specific AGENTS.md**:
```bash
# If in examples/ai-chatbots-language-learning/
cat AGENTS.md  # Read project-specific instructions
```

2. **Read project context**:
```bash
cat .scholarag/context.json  # Current stage, completed stages
cat config.yaml  # Research question, databases, criteria
```

3. **Execute appropriate script**:
```bash
cd ../../  # Navigate to ScholaRAG root
python scripts/0X_script.py --project examples/ai-chatbots-language-learning
```

4. **Run validation checks**:
See project-specific AGENTS.md for tests to run.

---

## Stage-by-Stage Instructions

### Stage 1: Fetch Papers
```bash
python scripts/01_fetch_papers.py --project <project_path>
```
**Validation**: Check paper counts against expected ranges in project AGENTS.md

### Stage 2: Deduplicate
```bash
python scripts/02_deduplicate.py --project <project_path>
```
**Validation**: Verify ~20-40% reduction (typical duplicate rate)

### Stage 3: Screen Papers (AI-assisted)
```bash
python scripts/03_screen_papers.py --project <project_path>
```
**Validation**: Verify relevance rate 15-40% (depends on query specificity)

### Stage 4: Download PDFs
```bash
python scripts/04_download_pdfs.py --project <project_path>
```
**Validation**: 30-80% success rate normal (many papers paywalled)

### Stage 5: Build RAG (Core AI Analysis)
```bash
python scripts/05_build_rag.py --project <project_path>
```

**What this does**:
- Extracts text from PDFs (Stage 4 outputs)
- Chunks documents into semantic units (~500 tokens)
- Generates embeddings using OpenAI/local model
- Stores in ChromaDB vector database

**Validation**:
```bash
# Test RAG with sample query
python scripts/06_query_rag.py --project <project_path> \
  --query "What are the main findings about speaking skills?"

# Should return: Relevant excerpts with citations
```

### Stage 6: Query RAG (Data Extraction)
```bash
python scripts/06_query_rag.py --project <project_path> --interactive
```

**What this does**:
- Semantic search across selected papers
- LLM-powered synthesis of findings
- Citation-backed answers (no hallucination)

**Common queries**:
- "Extract all correlation coefficients for X"
- "What methodologies were used?"
- "Summarize main themes across papers"

**Validation**: Answers include paper citations in format 【F:path†L123】

### Stage 7: Generate PRISMA Diagram
```bash
python scripts/07_generate_prisma.py --project <project_path>
```
**Validation**: PRISMA counts MUST match actual data files

---

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Prefer pathlib over os.path
- Log errors to `logs/` directory

### File Naming
- Papers: `0001_FirstAuthor_Year.pdf`
- CSVs: `snake_case.csv`
- Logs: `{script_name}.log`

---

## Git Workflow

### Commit Messages
```
stage-X: Brief description

- Action 1
- Action 2
- Statistics summary
```

### What to Commit
- ✅ Data files from pipeline
- ✅ Generated outputs (PRISMA diagrams)
- ✅ Updated context.json
- ❌ API keys or .env files
- ❌ Large intermediate files (>10MB)

---

## Testing

Run ALL tests after code changes:
```bash
pytest tests/
```

For project-specific validation tests, see project AGENTS.md.

---

## Common Issues

### "Fewer papers than expected"
- Check API rate limits in logs
- Verify query isn't too narrow
- See project-specific AGENTS.md for expected ranges

### "Low relevance rate"
- Expected for specific topics (15-30%)
- See project-specific AGENTS.md for domain norms

### "Low PDF success"
- Expected for paywalled journals (30-80%)
- NOT an error for academic papers

---

## Hierarchical Instructions

ScholaRAG uses hierarchical AGENTS.md files:

1. **This file** (`ScholaRAG/AGENTS.md`): System-level behavior
2. **Project files** (`examples/*/AGENTS.md`): Project-specific context

**Precedence**: Project-specific > System-level > General instructions

**Always check project folder for AGENTS.md before executing tasks.**

---

## Citations Format

When referencing files or terminal outputs:

**File**: 【F:path/to/file.csv†L42】
**Multi-line**: 【F:path/to/file.csv†L42-L56】
**Terminal**: 【T:bash†python script.py】

---

---

## Documentation Resources

- **Full Documentation**: https://researcher-rag-helper.vercel.app/
- **GitHub**: https://github.com/HosungYou/ScholaRAG
- **AI Chatbot Help**: https://researcher-rag-helper.vercel.app/chat

**Last updated**: January 22, 2025 (v1.2.1)
