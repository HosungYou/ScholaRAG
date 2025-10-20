# ScholarRAG v1.0.12 Release Notes

**Release Date**: 2025-10-19

## 🎯 Major Feature: Dual-Mode Support

ScholarRAG now supports **two distinct project types** to serve different research needs:

### 📊 Two Project Modes

#### 1. Knowledge Repository Mode 🗂️
**Purpose**: Build comprehensive knowledge bases for interactive exploration

- **Query Strategy**: Broad queries to maximize domain coverage (20,000-30,000 papers)
- **PRISMA Filtering**: Minimal - technical criteria only (language, format, duplicates)
- **Retention Rate**: 80-90% of initial papers
- **Human Review**: Not required - AI screening is sufficient
- **Use Cases**: Interactive Q&A, domain mapping, teaching materials, exploratory research

#### 2. Systematic Review Mode 📄
**Purpose**: Produce publication-quality systematic reviews following PRISMA 2020

- **Query Strategy**: Focused queries for manageable datasets (1,000-5,000 papers)
- **PRISMA Filtering**: Strict - detailed inclusion/exclusion criteria
- **Retention Rate**: 2-10% of initial papers
- **Human Review**: Required - AI assists but researcher makes final decisions
- **Use Cases**: Meta-analysis, systematic review publication, clinical guidelines, dissertations

---

## ✨ What's New

### Stage 1: Research Domain Setup
- **NEW**: Project type selection at the start of workflow
- Users choose between Knowledge Repository or Systematic Review mode
- Metadata validation now includes `project_type` field
- Success criteria adjusted for each mode

### Stage 2: Query Strategy Design
- **NEW**: Query breadth recommendations split by project type
- **Knowledge Repository**:
  - Comprehensive (20K-30K papers) ⭐ Recommended
  - Moderate (5K-10K papers)
- **Systematic Review**:
  - Broad (1.5K-5K papers)
  - Balanced (500-800 papers) ⭐ Recommended
  - Narrow (100-300 papers)
- **NEW**: Separate trade-off tables and decision trees for each mode

### Stage 3: PRISMA Configuration
- **NEW**: Completely different workflows for each project type
- **Knowledge Repository**:
  - Minimal filtering (language, format, spam only)
  - Lenient thresholds (auto_include: 50, auto_exclude: 20)
  - No human review required
- **Systematic Review**:
  - Detailed PRISMA criteria (6 dimensions)
  - Strict thresholds (auto_include: 90, auto_exclude: 10)
  - Human review optional but recommended

### Configuration Template
- **NEW**: `project_type` field in `config.yaml`
- **NEW**: Inline documentation explaining configuration differences
- **NEW**: Mode-specific AI-PRISMA rubric settings

### Script Automation
- **`03_screen_papers.py`**:
  - Automatically reads `project_type` from config
  - Adjusts screening thresholds based on mode
  - Displays project type and thresholds at startup
- **`07_generate_prisma.py`**:
  - Changes diagram title based on project type
  - Knowledge Repository: "Paper Processing Pipeline"
  - Systematic Review: "PRISMA 2020 Flow Diagram"

---

## 🔄 Updated Documentation

### Prompts
- `prompts/01_research_domain_setup.md`: Added project type selection
- `prompts/02_query_strategy.md`: Split query strategy by project type
- `prompts/03_prisma_configuration.md`: Dual-mode PRISMA configuration

### Templates
- `templates/config_base.yaml`: Added `project_type` field with documentation

### Scripts
- `scripts/03_screen_papers.py`: Project type-aware screening
- `scripts/07_generate_prisma.py`: Project type-aware diagram generation

---

## 📈 Benefits

### For Knowledge Repository Projects
- **Comprehensive coverage**: 20,000+ papers for complete domain mapping
- **Faster workflow**: Minimal filtering reduces screening time
- **No human bottleneck**: AI-only screening enables full automation
- **Better semantic search**: Larger dataset improves RAG performance

### For Systematic Review Projects
- **Publication-ready**: Follows PRISMA 2020 guidelines strictly
- **High precision**: Strict criteria ensure relevant papers only
- **Manageable dataset**: 50-300 final papers for deep analysis
- **Transparent process**: Human review ensures quality and reproducibility

---

## 🚀 Upgrade Guide

### For New Projects
1. Start Stage 1 and choose your project type at the beginning
2. All subsequent prompts and scripts will automatically adapt

### For Existing Projects
1. Add `project_type: "systematic_review"` to your `config.yaml` (defaults to systematic review)
2. Re-run Stage 3 if you want to switch to Knowledge Repository mode
3. Adjust `ai_prisma_rubric` thresholds if needed

Example `config.yaml` update:
```yaml
# Add this field after project_name
project_type: "knowledge_repository"  # or "systematic_review"

# Adjust thresholds for knowledge repository
ai_prisma_rubric:
  decision_confidence:
    auto_include: 50  # Lower for knowledge repository
    auto_exclude: 20  # Lower for knowledge repository
  human_validation:
    required: false   # Not required for knowledge repository
```

---

## 📝 Breaking Changes

None - this release is fully backward compatible. Existing projects default to `systematic_review` mode if `project_type` is not specified.

---

## 🐛 Bug Fixes

None in this release.

---

## 📚 Related Updates

- **ScholarRAG-helper v1.1.1**: Updated paper count expectations (100-1,000+)
- **ScholarRAG-helper v1.1.1**: Added Semantic Scholar API key requirement

---

## 🙏 Acknowledgments

This release was designed to support both comprehensive knowledge graph construction (for AI-powered research assistants) and traditional systematic literature reviews (for academic publication).

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/HosungYou/researcherRAG.git
cd researcherRAG

# Install dependencies
pip install -r requirements.txt

# Set up API keys
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

---

## 🔗 Links

- **GitHub Repository**: https://github.com/HosungYou/researcherRAG
- **Documentation**: https://github.com/HosungYou/ScholarRAG-helper
- **Previous Release**: v1.0.11

---

## 📅 Next Steps

- v1.1.0 (planned): Enhanced human validation workflow for systematic reviews
- v1.1.0 (planned): Export to reference management tools (Zotero, Mendeley)
- v1.2.0 (planned): Multi-language support for non-English papers
