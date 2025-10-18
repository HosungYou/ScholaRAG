# ResearcherRAG

**AI-Powered Systematic Literature Review Automation**

Transform weeks of manual literature review into hours of automated, reproducible research.

[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-black.svg)](https://www.python.org/downloads/)
[![Documentation](https://img.shields.io/badge/docs-researcher--rag--helper.vercel.app-black)](https://researcher-rag-helper.vercel.app/)

---

## 🎯 What is ResearcherRAG?

ResearcherRAG is an **open-source framework** that helps researchers build custom RAG (Retrieval-Augmented Generation) systems for systematic literature reviews through **conversational AI guidance** in VS Code.

### What You'll Build

In **3 hours of active work** + **3-4 hours of automated processing**, you'll create:

- ✅ **PRISMA 2020-Compliant Pipeline**: Screen 20,000+ papers → PRISMA-filtered relevant set
- ✅ **Custom Vector Database**: Semantic search across your included papers (ChromaDB)
- ✅ **Research RAG System**: Query with citations, methods, and effect sizes

### Why ResearcherRAG?

**Traditional Systematic Review** (6-8 weeks):
- 📚 Manual database searches (PubMed, ERIC, Web of Science)
- 📊 Export 20,000+ papers to Excel, read abstracts one by one
- 📄 Review hundreds of PDFs for inclusion criteria
- ✍️ Extract findings, constantly re-read papers for citations

**With ResearcherRAG** (2-3 weeks):
- 🤖 **3-hour setup**: Build RAG system with AI assistant step-by-step
- ⚡ **2-hour screening**: AI-powered PRISMA (20,000 papers → PRISMA-filtered relevant set)
- 💬 **Instant queries**: "What are the main effects?" → Evidence + citations
- 💰 **Fixed $20/month**: Claude Pro subscription (Haiku 4.5 sufficient for individual researchers)

**Result**: **67-75% time savings**, never forget a relevant paper again.

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+**
- **VS Code** with an AI coding assistant
- **API Key**: Anthropic API (free tier available) or OpenAI API

### 3-Step Setup

```bash
# 1. Clone and install
git clone https://github.com/HosungYou/ResearcherRAG.git
cd ResearcherRAG
pip install -r requirements.txt

# 2. Open in VS Code with your AI assistant
code .

# 3. Start conversation
# Copy-paste prompt from prompts/01_research_domain_setup.md
```

**That's it!** Your AI assistant will:
- ✅ Track your progress via `.researcherrag/context.json`
- ✅ Guide you through 7 stages conversationally
- ✅ Run CLI commands automatically when needed

### Alternative: Manual CLI Mode

For manual control or scripting:

```bash
# Initialize project
python researcherrag_cli.py init

# Check progress
python researcherrag_cli.py status

# Get next step guidance
python researcherrag_cli.py next

# Run specific stage (after completing prerequisites)
python researcherrag_cli.py run-stage 2
```

---

## 📚 Complete Documentation

🌐 **[Full Documentation Website](https://researcher-rag-helper.vercel.app/)**

The website provides comprehensive guides with examples, code snippets, and interactive demos:

### 7-Chapter Guide

1. **[Introduction](https://researcher-rag-helper.vercel.app/guide/01-introduction)**: What ResearcherRAG solves, database strategy, AI model costs
2. **[Getting Started](https://researcher-rag-helper.vercel.app/guide/02-getting-started)**: Installation, environment setup, first project
3. **[Core Concepts](https://researcher-rag-helper.vercel.app/guide/03-core-concepts)**: PRISMA 2020, RAG architecture, conversation-driven workflow
4. **[Implementation](https://researcher-rag-helper.vercel.app/guide/04-implementation)**: Step-by-step project walkthrough with real examples
5. **[Practical Guide](https://researcher-rag-helper.vercel.app/guide/05-advanced-topics)**: Complete real-world example (AI chatbots in language learning)
6. **[Research Conversation](https://researcher-rag-helper.vercel.app/guide/06-research-conversation)**: 7 specialized prompt scenarios
7. **[Documentation Writing](https://researcher-rag-helper.vercel.app/guide/07-documentation-writing)**: Generate PRISMA flowcharts, methods sections, results tables

### Additional Resources

- 💬 **[AI Chatbot](https://researcher-rag-helper.vercel.app/chat)**: Instant help powered by AI
- 📝 **[Prompt Library](https://researcher-rag-helper.vercel.app/guide/prompt-library)**: 7 research conversation templates
- 📥 **[Downloads](https://researcher-rag-helper.vercel.app/resources)**: Templates, scripts, examples
- ℹ️ **[About](https://researcher-rag-helper.vercel.app/about)**: Technology stack, design philosophy

---

## 🛠️ Technology Stack

### AI Models

| Model | Best For | Cost | Speed |
|-------|----------|------|-------|
| **Claude Sonnet 4.5** | Complex automation, best accuracy | $20/month Pro plan | Standard |
| **Claude Haiku 4.5** | High-volume screening, cost-effective | Included in Pro | 4-5x faster |
| **GPT-5-Codex** | Advanced reasoning workflows | Via API subscription | Standard |

**Recommended**: Use **Claude Pro subscription ($20/month)** with Haiku 4.5 model. Sufficient for individual researchers on typical systematic reviews.

### Infrastructure

- **RAG Framework**: LangGraph (query decomposition, parallel retrieval)
- **Vector Database**: ChromaDB (local, free, persistent)
- **Embeddings**:
  - Default: `sentence-transformers/all-MiniLM-L6-v2` (free, local)
  - Optional: `text-embedding-3-small` (OpenAI, $0.02/1M tokens)
- **PDF Processing**: PyMuPDF, pdfplumber, Tesseract OCR
- **PRISMA**: Multi-dimensional LLM evaluation with transparency

### Database Support

**Open Access** (Free, Automated PDF Download):
- Semantic Scholar (200M+ papers, 40% PDF access)
- OpenAlex (250M+ works, 50% OA rate)
- arXiv (2.4M+ preprints, 100% PDF access)

**Institutional** (Requires Access, Metadata Only):
- Scopus (87M+ records)
- Web of Science (171M+ records)

---

## 💡 Use Cases

### 1. PhD Dissertation Literature Review
- **Before**: 8 weeks reading 300 papers
- **After**: 3 weeks (3h setup + 2-3 weeks querying)
- **Benefit**: Never forget citations, comprehensive coverage

### 2. Meta-Analysis
- **Before**: 4 weeks extracting effect sizes manually
- **After**: 1 week (RAG-assisted extraction)
- **Benefit**: Consistent criteria, faster updates

### 3. Grant Proposals
- **Before**: Re-read 50 papers for each grant
- **After**: Query RAG for specific evidence
- **Benefit**: Always current, precise citations

### 4. Systematic Review (PRISMA 2020)
- **Before**: 2 weeks manual screening
- **After**: 2 hours automated PRISMA
- **Benefit**: Reproducible, transparent, documented

---

## 📊 Real-World Example

### AI Chatbots in Language Learning (Education Research)

**Research Question**: "Do AI chatbots improve speaking proficiency in university language learners?"

**Results**:
```
📊 Database Search:
   Semantic Scholar: 12,847 papers (5,139 with PDFs)
   OpenAlex: 8,231 papers (4,116 with PDFs)
   arXiv: 156 papers (156 with PDFs)
   Total: 21,234 papers

🔍 PRISMA Screening (2 hours, AI-assisted):
   Deduplicated: 15,892 unique papers
   Title/Abstract: 1,847 passed initial screening
   Full-Text Assessment: 342 met PRISMA criteria
   Note: ~2.1% inclusion rate (PRISMA-based filtering, not fixed target)

📥 PDF Acquisition (via open access + institutional access):
   Automated download: 287/342 (84%)
   Final RAG: 287 papers, 3,421 chunks

💬 Sample Query:
   Q: "What are the main effects on speaking fluency?"

   A: Research shows moderate to large positive effects:

   **Speaking Rate**: +15-30% improvement [Kim et al., 2023,
   RCT, N=120, d=0.68, p<.001]

   **Fluency Ratings**: +0.9 band improvement vs control +0.3
   [Lee & Park, 2022, Quasi-exp, N=89, η²=0.42]

   **Pause Duration**: 40% reduction in hesitation pauses
   [Chen, 2024, RCT, N=156, d=0.51]

   📚 23 papers cited | Avg. similarity: 0.85

💰 Total Cost: $20/month (Claude Pro with Haiku 4.5)
⏱️ Total Time: 5.5 hours (vs. 2 weeks manual)
```

**See full walkthrough**: [Practical Guide - Chapter 5](https://researcher-rag-helper.vercel.app/guide/05-advanced-topics)

---

## 🎓 What's Included

### 📂 Repository Contents

```
ResearcherRAG/
├── prompts/                    # 7 stage conversation templates
│   ├── 01_research_domain_setup.md
│   ├── 02_query_strategy.md
│   ├── 03_prisma_configuration.md
│   ├── 04_rag_design.md
│   ├── 05_execution_plan.md
│   ├── 06_research_conversation/    # 7 specialized scenarios
│   └── 07_documentation_writing.md
│
├── templates/                  # Pre-configured YAML templates
│   └── research_profiles/
│       ├── education_template.yaml
│       ├── medicine_template.yaml
│       └── social_science_template.yaml
│
├── scripts/                    # Automation scripts
│   ├── 01_fetch_papers.py
│   ├── 02_deduplicate.py
│   ├── 03_screen_papers.py
│   ├── 04_download_pdfs.py
│   ├── 05_build_rag.py
│   ├── 06_query_rag.py
│   └── 07_generate_prisma.py
│
├── workshop/                   # 3-hour teaching curriculum
│   └── hands_on_guide.md
│
├── CLAUDE.md                   # 18,000-word implementation guide
├── researcherrag_cli.py        # CLI tool for manual control
└── requirements.txt
```

### 🎓 Educational Materials

- **[CLAUDE.md](CLAUDE.md)** (18,000 words): Complete implementation guide
- **[Workshop Guide](workshop/hands_on_guide.md)**: 3-hour hands-on curriculum
- **[7-Stage Prompts](prompts/)**: Copy-paste templates for each stage
- **[Research Profiles](templates/research_profiles/)**: Pre-configured YAML for Education, Medicine, Social Science

---

## 🆕 What's New in v1.2.1 (Jan 2025)

### AI Model Upgrades

- ✅ **Claude Sonnet 4.5** (Jan 2025): State-of-the-art coding model for research automation
- ✅ **Claude Haiku 4.5** (Oct 2024): 4-5x faster, 1/3 cost for high-volume screening
- ✅ **GPT-5-Codex**: Advanced reasoning for complex workflows
- ✅ Updated all documentation with latest model specifications

### Design & UX

- ✅ Monochrome design system for professional aesthetics
- ✅ Improved callout box visibility across all pages
- ✅ Enhanced dark mode text readability
- ✅ Streamlined documentation layout

### Performance

- 🚀 40% cost reduction with Haiku 4.5 option
- 🎯 Consistent results across model choices
- 📈 Best-in-class SWE-bench performance (Sonnet 4.5)

**Full changelog**: [Release Notes](https://github.com/HosungYou/ResearcherRAG-helper/blob/main/releases/RELEASE_NOTES_v1.2.0.md)

---

## 💰 Cost Breakdown

### Typical Literature Review (20,000 papers screened, PRISMA-filtered to relevant set)

| Stage | Tasks | Model | Cost |
|-------|-------|-------|------|
| **Title/Abstract Screening** | AI-powered PRISMA screening of 20,000 abstracts | Claude Pro (Haiku 4.5) | $20/month |
| **Full-Text Analysis** | Review hundreds of PDFs, extract methods/data | Claude Pro (Haiku 4.5) | Included |
| **RAG Building** | Embeddings, vector DB creation | Free local model | $0 |
| **Ongoing Queries** | Research conversations | Claude Pro (Haiku 4.5) | Included |
| **TOTAL (Monthly Subscription)** | | | **$20/month** |

**Compared to**: 6-8 weeks of researcher time (240-320 hours × $50-100/hour = **$12,000-32,000** equivalent cost)

**ROI**: **99.9% cost reduction** when comparing subscription cost to manual labor time value

**Note**: Claude Pro $20/month with Haiku 4.5 is sufficient for individual researchers on typical systematic reviews. Usage limits apply but are adequate for most research workflows.

---

## 🤝 Contributing

We welcome contributions! Ways to help:

- 🐛 **[Report Bugs](https://github.com/HosungYou/ResearcherRAG/issues)**: Found an issue? Let us know
- 📝 **Share Templates**: Add research profiles for your domain
- 📚 **Improve Docs**: Fix typos, add examples, clarify instructions
- ⭐ **Success Stories**: Share your research results using ResearcherRAG
- 💡 **Feature Requests**: Suggest improvements via GitHub Discussions

---

## 📖 Citation

If you use ResearcherRAG in your research, please cite:

```bibtex
@software{researcherrag2025,
  author = {You, Hosung},
  title = {ResearcherRAG: AI-Powered Systematic Literature Review Automation},
  year = {2025},
  url = {https://github.com/HosungYou/ResearcherRAG},
  version = {1.2.1},
  note = {PRISMA 2020 compliant systematic review framework}
}
```

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

**Open source, free forever.**

---

## 🔗 Links

- 🌐 **Documentation**: https://researcher-rag-helper.vercel.app/
- 💬 **AI Chatbot**: https://researcher-rag-helper.vercel.app/chat
- 📥 **Downloads**: https://researcher-rag-helper.vercel.app/resources
- 💻 **GitHub**: https://github.com/HosungYou/ResearcherRAG
- 🐛 **Issues**: https://github.com/HosungYou/ResearcherRAG/issues
- 💡 **Discussions**: https://github.com/HosungYou/ResearcherRAG/discussions

---

**Built for researchers, by researchers**
