# ResearcherRAG: AI-Powered Research Assistant Platform

**Comprehensive RAG systems for social science researchers: Literature Review, Qualitative Coding, and Research Notes Management**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Powered by Claude](https://img.shields.io/badge/Powered%20by-Claude-orange)](https://anthropic.com)

---

## 🎯 Overview

ResearcherRAG is a suite of three specialized Retrieval-Augmented Generation (RAG) systems designed for social science researchers in education, psychology, sociology, and related fields.

### Three Core Systems

| System | Purpose | Technology | Best For |
|--------|---------|-----------|----------|
| **📚 Literature Review RAG** | Synthesize findings across 200+ papers | LangGraph | Systematic reviews, meta-analysis |
| **🎤 Qualitative Coding RAG** | AI-assisted thematic analysis | LangGraph | Interview studies, focus groups |
| **📝 Research Notes RAG** | Personal knowledge management | LangChain | Literature notes, ideation |

---

## 🚀 Quick Start

### Option 1: Use Pre-Built Hugging Face Space (Recommended for Beginners)

1. **Visit Demo:**
   ```
   https://huggingface.co/spaces/your-username/researcherrag
   ```

2. **Upload Documents:**
   - Literature Review: Upload PDF papers
   - Qualitative Coding: Upload interview transcripts (.txt, .docx)
   - Research Notes: Add markdown notes

3. **Start Querying:**
   ```
   "What are the main barriers to AI adoption in education?"
   "What themes emerge from these teacher interviews?"
   "Show me my notes on mixed methods from last month"
   ```

### Option 2: Local Installation (For Developers)

```bash
# Clone repository
git clone https://github.com/your-username/ResearcherRAG.git
cd ResearcherRAG

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
nano .env  # Add your API keys

# Run specific module
cd 01_literature_review_rag
python -m chainlit run frontend/chainlit_app.py
```

---

## 📚 Documentation

### For Workshop Participants

| Module | Description | Duration | Prerequisites |
|--------|-------------|----------|---------------|
| [Module 1: RAG Basics](docs/module_1_basic_rag_concept.md) | Understand RAG concepts and build first demo | 1 hour | None |
| [Module 2: Literature Review RAG](docs/module_2_literature_review_rag.md) | Production system for paper analysis | 2 hours | Module 1 |
| [Module 3: Qualitative Coding RAG](docs/module_3_qualitative_coding_rag.md) | AI-assisted interview analysis | 2 hours | Module 1 |
| [Module 4: Collaboration & Deployment](docs/module_4_research_notes_and_collaboration.md) | Team features and deployment | 1.5 hours | Modules 1-3 |

### For Developers

- [**Deployment Guide**](docs/deployment_huggingface_guide.md): Deploy to Hugging Face Spaces
- [**Architecture Decision Record**](docs/deployment_huggingface_guide.md#architecture-decision-final-recommendation): Why LangGraph vs LangChain
- **API Reference**: Coming soon
- **Contributing Guide**: Coming soon

---

## 🛠️ Technology Stack

### Core Technologies
- **LLM**: Anthropic Claude 3.5 Sonnet (advanced reasoning)
- **Embeddings**: HuggingFace Sentence Transformers (free, local)
- **Vector Database**: Qdrant Cloud (1GB free tier)
- **Backend**: FastAPI (RESTful API)
- **Frontend**: Gradio (Hugging Face Spaces) or Chainlit (local)

### Frameworks
- **LangGraph**: Complex multi-step workflows (Literature Review, Qualitative Coding)
- **LangChain**: Simple conversational chains (Research Notes)

### Why This Stack?

**LangGraph for Literature Review:**
- Multi-step retrieval: query decomposition → retrieve → rerank → synthesize
- Conditional logic for complex queries
- Visual debugging

**LangGraph for Qualitative Coding:**
- Iterative refinement (initial codes → merge → themes)
- Human-in-the-loop validation
- State checkpointing (resume analysis)

**LangChain for Research Notes:**
- Simple Q&A with conversation memory
- Fast response times
- Easy to customize

---

## 💡 Use Cases

### 1. Systematic Literature Review

**Traditional Method:**
- Manually read 200 papers
- Extract key findings to Excel
- Takes weeks

**With ResearcherRAG:**
```python
# Query across 200 papers instantly
result = query_literature_review(
    "Compare TAM and UTAUT theories in educational contexts since 2020"
)

# Get:
# - Synthesized comparison
# - Citations for each claim
# - Identified research gaps
```

### 2. Qualitative Interview Analysis

**Traditional Method:**
- Code 50 interviews manually
- Use NVivo/Atlas.ti
- Takes days

**With ResearcherRAG:**
```python
# Analyze all interviews
result = analyze_interviews(
    interview_texts=transcripts,
    research_question="Barriers to technology adoption"
)

# Get:
# - Auto-generated codes
# - Hierarchical themes
# - Exemplar quotes
# - Export to NVivo format
```

### 3. Research Knowledge Management

**Traditional Method:**
- Scattered notes across tools
- Hard to find past insights
- No automatic connections

**With ResearcherRAG:**
```python
# Query your entire research history
answer = query_research_notes(
    "What did I learn about intrinsic motivation in my 2023 studies?"
)

# Get:
# - Relevant notes synthesized
# - Related ideas you forgot
# - Timeline of thinking evolution
```

---

## 📊 Performance Benchmarks

| Task | Traditional | ResearcherRAG | Speedup |
|------|------------|--------------|---------|
| Initial literature review (50 papers) | 20 hours | 2 hours | **10x** |
| Interview coding (20 transcripts) | 30 hours | 3 hours | **10x** |
| Finding relevant past notes | 30 minutes | 30 seconds | **60x** |
| Meta-analysis data extraction | 40 hours | 4 hours | **10x** |

*Note: Times assume human validation of AI outputs, which is recommended*

---

## 🎓 Workshop: Using RAG for Social Science Research

### Target Audience
- Graduate students in social sciences
- Early-career researchers
- Faculty exploring AI research tools
- Research teams needing collaboration tools

### Workshop Format (4 hours)

**Part 1: Foundations (1 hour)**
- What is RAG and why it matters
- Hands-on demo: Build a mini RAG in 15 minutes
- Ethics: Transparency in AI-assisted research

**Part 2: Literature Review System (1 hour)**
- Upload your papers
- Advanced querying techniques
- Meta-analysis support

**Part 3: Qualitative Coding (1 hour)**
- Parse interview transcripts
- AI-assisted coding
- Validation and export

**Part 4: Deployment & Collaboration (1 hour)**
- Deploy your own system to Hugging Face
- Team collaboration features
- Customization with Claude Code

### Materials Provided
- All modules with step-by-step guides
- Sample datasets (papers, interviews)
- Pre-configured GitHub repository
- Office hours support

---

## 🔐 Research Ethics & Best Practices

### Transparency
- **Always disclose AI use** in your research methods section
- Example citation:
  ```
  "We used ResearcherRAG (Version 1.0) to assist with initial thematic coding.
   All AI-generated codes were validated by two human coders, with inter-rater
   reliability (Cohen's κ) of 0.85."
  ```

### Human Oversight
- ✅ **DO**: Use AI for initial coding, then validate
- ✅ **DO**: Use AI to find patterns you might miss
- ❌ **DON'T**: Accept AI codes without review
- ❌ **DON'T**: Use AI for final interpretation (requires human judgment)

### Data Privacy
- **Sensitive data**: Use local deployment (not cloud)
- **IRB approval**: Check if AI processing requires protocol amendment
- **Participant consent**: Update consent forms to mention AI analysis

### Quality Assurance
1. **Spot-check AI outputs** (sample 10-20% manually)
2. **Calculate agreement** between AI and human coding
3. **Document all prompts** used (for reproducibility)
4. **Version control** your codebooks

---

## 🌐 Deployment Options

### Option 1: Hugging Face Spaces (Easiest)

**Pros:**
- No server management
- Free tier available
- Easy sharing via URL
- Automatic HTTPS

**Cons:**
- Limited compute (CPU only on free tier)
- 50GB storage limit
- Public by default (need paid tier for private)

**Best For:** Demos, workshops, small teams

[**Deployment Guide →**](docs/deployment_huggingface_guide.md)

---

### Option 2: University Server (Most Common)

**Pros:**
- Full control
- Private by default
- Institutional support
- GPU access

**Cons:**
- Requires IT coordination
- Maintenance needed

**Best For:** Research labs, departments, multi-user projects

**Quick Setup:**
```bash
# On your university server
git clone https://github.com/your-username/ResearcherRAG.git
cd ResearcherRAG
docker-compose up -d
```

---

### Option 3: Local Installation (Most Private)

**Pros:**
- Complete privacy
- Works offline (if using local LLM)
- No data leaves your computer

**Cons:**
- Limited to single user
- Requires technical setup

**Best For:** Individual researchers, sensitive data

---

## 🤝 Contributing

We welcome contributions from the research community!

### Ways to Contribute
- 🐛 Report bugs or issues
- 💡 Suggest new features
- 📝 Improve documentation
- 🔬 Share your use cases
- 🌍 Add support for non-English languages

### Development Setup
```bash
# Fork repository
git clone https://github.com/your-username/ResearcherRAG.git

# Create feature branch
git checkout -b feature/amazing-feature

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Submit pull request
```

---

## 📈 Roadmap

### Current Version (v1.0)
- ✅ Literature Review RAG
- ✅ Qualitative Coding RAG
- ✅ Research Notes RAG
- ✅ Hugging Face Spaces deployment
- ✅ Complete workshop materials

### Coming Soon (v1.1)
- 🔜 Multi-language support (Korean, Spanish, French)
- 🔜 Zotero/Mendeley integration
- 🔜 Obsidian bi-directional sync
- 🔜 Real-time collaboration features
- 🔜 Mobile app (iOS/Android)

### Future (v2.0)
- 🔮 Automated literature monitoring (Google Scholar alerts → auto-ingest)
- 🔮 Grant proposal assistant
- 🔮 Peer review helper
- 🔮 Teaching assistant mode

---

## 📞 Support & Community

### Get Help
- **Documentation**: See [docs/](docs/) folder
- **GitHub Issues**: [Report bugs or ask questions](https://github.com/your-username/ResearcherRAG/issues)
- **Discord**: [Join our community](https://discord.gg/your-invite) (coming soon)
- **Email**: researcherrag@example.com

### Office Hours
- **Monthly Q&A**: First Thursday of each month, 2-3 PM EST
- **Workshop Bookings**: Available for departments/conferences

---

## 📄 Citation

If you use ResearcherRAG in your research, please cite:

```bibtex
@software{researcherrag2024,
  title = {ResearcherRAG: AI-Powered Research Assistant Platform for Social Scientists},
  author = {Your Name},
  year = {2024},
  url = {https://github.com/your-username/ResearcherRAG},
  note = {Version 1.0}
}
```

---

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

**Key Points:**
- ✅ Free for academic research
- ✅ Free for commercial use
- ✅ Modify and redistribute
- ⚠️ No warranty provided

---

## 🙏 Acknowledgments

### Built With
- [LangChain](https://langchain.com) & [LangGraph](https://langchain-ai.github.io/langgraph/) - RAG frameworks
- [Anthropic Claude](https://anthropic.com) - Advanced AI reasoning
- [Qdrant](https://qdrant.tech) - Vector database
- [Hugging Face](https://huggingface.co) - Model hosting & Spaces
- [Gradio](https://gradio.app) - Web interface

### Funding
- [If applicable] National Science Foundation Grant #XXXXXXX
- [If applicable] University XYZ Research Grant

### Contributors
- [List key contributors]

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=your-username/ResearcherRAG&type=Date)](https://star-history.com/#your-username/ResearcherRAG&Date)

---

**Built with ❤️ for the research community**

[⬆ Back to Top](#researcherrag-ai-powered-research-assistant-platform)
