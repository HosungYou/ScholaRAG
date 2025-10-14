---
layout: default
title: Home
nav_order: 1
description: "ResearcherRAG: PRISMA 2020 + RAG for systematic literature reviews"
permalink: /
---

# ResearcherRAG
{: .fs-9 }

Build rigorous, AI-powered systematic literature reviews in days, not months.
{: .fs-6 .fw-300 }

[Get Started](#quick-start){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View on GitHub](https://github.com/HosungYou/researcherRAG){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## What is ResearcherRAG?

ResearcherRAG combines **PRISMA 2020** systematic review methodology with **RAG** (Retrieval-Augmented Generation) technology to help researchers conduct rigorous literature reviews with AI-powered analysis.

### Why PRISMA + RAG?

```
❌ Traditional Systematic Review (6-8 weeks):
   Manual database searches → Export to Excel → Read 500+ abstracts
   → Full-text review of 200+ papers → Extract findings manually
   → Constantly re-read papers for citations

✅ ResearcherRAG (2-3 weeks):
   3-hour setup with Claude Code → PRISMA screens 500 papers automatically
   → RAG built from 75 selected papers → Query RAG for instant answers with citations
   → Result: 67-75% time savings
```

### How They Work Together

<div class="code-example" markdown="1">

**Without PRISMA** (RAG only):
```
500 papers → RAG database
          ↓
Your question: "What are the main findings?"
          ↓
Answer: Mixed quality (includes blog posts, non-peer-reviewed, irrelevant papers)
```

**With PRISMA + RAG**:
```
500 papers → PRISMA screening → 75 high-quality papers → RAG database
                                                       ↓
Your question: "What are the main findings?"
                                        ↓
Answer: High-quality (peer-reviewed, relevant, methodologically sound)
```

</div>

**Key Insight**: PRISMA ensures you're analyzing the RIGHT papers. RAG enables DEEP analysis of those papers.

---

## Quick Start

### Prerequisites
- Python 3.10-3.14
- VS Code with Claude Code extension
- API keys: `ANTHROPIC_API_KEY` (required), `OPENAI_API_KEY` (optional)

### 3-Minute Setup

```bash
# Clone repository
git clone https://github.com/HosungYou/researcherRAG.git
cd researcherRAG

# Install dependencies
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY="your-key-here"

# You're ready!
# Open prompts/01_research_domain_setup.md in VS Code
```

### 5-Stage Workflow Overview

| Stage | What You Do | Duration | What Happens |
|-------|-------------|----------|--------------|
| **1. Planning** | Define research question, design query | 35-50 min | Prompts 01-02 guide conversation |
| **2. PRISMA Setup** | Configure screening criteria | 25-35 min | Prompt 03 creates PRISMA profile |
| **3. RAG Design** | Design vector database | 20-30 min | Prompt 04 configures RAG architecture |
| **4. Execution** | Click "Execute" in Claude Code | 2-4 hours (automated) | Scripts 01-05 run automatically |
| **5. Analysis** | Ask questions to RAG system | Ongoing | Prompt 06 launches RAG interface |

**Optional**: Stage 6 - Generate PRISMA flowchart and reports (30-60 min)

[Learn more about the 5-stage workflow →]({{ site.baseurl }}{% link stages/index.md %})

---

## Key Features

### 🎯 Conversation-First Automation
Copy prompts, paste to Claude Code, have a conversation. Claude Code executes scripts automatically when stages complete.

### 📊 PRISMA 2020 Compliant
6-dimension screening criteria, transparent reporting, reproducible methodology.

### 🤖 RAG-Powered Analysis
Semantic search across selected papers, citation-backed answers, no hallucination.

### ⚡ 67-75% Time Savings
What took 6-8 weeks now takes 2-3 weeks. Proven across Education, Medicine, and Psychology research.

---

## Example: AI Chatbots for Language Learning

**Research Question**: How do AI chatbots improve speaking skills in language learning?

**Results**:
- **PRISMA**: 403 papers identified → 79 screened as relevant → 45 PDFs downloaded
- **RAG**: Vector database built from 45 papers
- **Analysis**:
  ```
  User: "Extract all correlation coefficients for speaking skills outcomes"
  RAG: "Found 12 correlations:
        - r=0.45 (p<0.001) from Smith et al. 2023, p. 156
        - r=0.62 (p<0.001) from Lee et al. 2022, p. 89
        - ..."
  ```

[View full example project →](https://github.com/HosungYou/researcherRAG/tree/main/examples/ai-chatbots-language-learning)

---

## Why ResearcherRAG?

### For Individual Researchers
- ✅ Complete systematic reviews 2-3x faster
- ✅ Never forget a relevant paper
- ✅ Query your literature like a database
- ✅ PRISMA-compliant documentation generated automatically

### For Research Teams
- ✅ Reproducible workflows (YAML configuration)
- ✅ Shared RAG systems across team
- ✅ Version-controlled research process
- ✅ Transparent screening criteria

### For Academic Institutions
- ✅ Teach systematic review methodology
- ✅ Introduce students to RAG/AI
- ✅ Workshop-ready (3-hour modules)
- ✅ Open-source, no licensing costs

---

## Documentation Structure

### 🔍 Search Documentation

**Use the search box at the top of any page** to quickly find what you need!

**Popular searches**:
- `PRISMA` - PRISMA 2020 methodology, screening, flowchart
- `RAG` - RAG system, vector database, semantic search
- `Stage 4` - Execution, automated pipeline, scripts
- `config.yaml` - Configuration, setup, criteria
- `troubleshooting` - Common issues and solutions

[View complete search guide]({{ site.baseurl }}{% link search-guide.md %}) - Tips for effective searching

### Getting Started
- [Search Guide]({{ site.baseurl }}{% link search-guide.md %}) - 🔍 How to search effectively
- [Glossary]({{ site.baseurl }}{% link glossary.md %}) - 📚 Searchable key terms (120+ definitions)
- [Installation]({{ site.baseurl }}{% link getting-started.md %}) - ⚙️ Set up your environment
- [FAQ]({{ site.baseurl }}{% link faq.md %}) - ❓ Common questions

### 5-Stage Workflow
- [Stage 1: Planning]({{ site.baseurl }}{% link stages/01-planning.md %}) - Research question and query design
- [Stage 2: PRISMA Setup]({{ site.baseurl }}{% link stages/02-prisma.md %}) - Screening criteria configuration
- [Stage 3: RAG Design]({{ site.baseurl }}{% link stages/03-rag-design.md %}) - Vector database architecture
- [Stage 4: Execution]({{ site.baseurl }}{% link stages/04-execution.md %}) - Automated pipeline run
- [Stage 5: Analysis]({{ site.baseurl }}{% link stages/05-analysis.md %}) - RAG query interface

### Reference
- [Prompts]({{ site.baseurl }}{% link reference/prompts.md %}) - All 7 conversation prompts
- [Scripts]({{ site.baseurl }}{% link reference/scripts.md %}) - All 7 Python scripts
- [Outputs]({{ site.baseurl }}{% link reference/outputs.md %}) - Expected files at each stage

---

## Community & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/HosungYou/researcherRAG/issues)
- **Discussions**: [Ask questions, share projects](https://github.com/HosungYou/researcherRAG/discussions)
- **Examples**: [See real research projects](https://github.com/HosungYou/researcherRAG/tree/main/examples)

---

## License

MIT License - Free for academic and commercial use.

**Citation**:
```bibtex
@software{researcherrag2025,
  title = {ResearcherRAG: PRISMA 2020 + RAG for Systematic Literature Reviews},
  author = {You, Hosung},
  year = {2025},
  url = {https://github.com/HosungYou/researcherRAG}
}
```

---

## Next Steps

1. **[Read the Getting Started Guide]({{ site.baseurl }}{% link getting-started.md %})** - 5-minute overview
2. **[Understand Key Terms]({{ site.baseurl }}{% link glossary.md %})** - PRISMA, RAG, ChromaDB, etc.
3. **[Start Stage 1]({{ site.baseurl }}{% link stages/01-planning.md %})** - Begin your first research project

**Ready to build your research RAG system?** Let's get started! 🚀
