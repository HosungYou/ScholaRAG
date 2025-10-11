# Changelog

All notable changes to the ResearcherRAG project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2025-10-11 (In Progress)

### 🎯 Major Changes

#### **Project Pivot: Web Service → Workshop Materials**

**Rationale**: Original plan to build web-based RAG service doesn't align with researcher workflow. Researchers work in IDEs (VS Code), need terminal access for PDF downloads and Python execution, and prefer conversational setup over form-based configuration.

**New Direction**: Educational materials for building RAG systems with Claude Code in VS Code.

---

### Added

#### Documentation
- **CLAUDE.md** (renamed from CLAUDE_FOR_RESEARCHERS.md): Comprehensive 18,000-word guide for Claude Code
  - 5-stage workflow (Research Domain Setup → Query Strategy → PRISMA Configuration → RAG Design → Execution)
  - Conversation examples for each stage
  - Troubleshooting guide (10+ common issues)
  - Domain-specific templates (Education, Medicine, Psychology)
  - Teaching mode for workshop context

- **docs/project_pivot_discussion.md**: Detailed documentation of project direction change
  - Comparison of initial misunderstanding vs. actual intent
  - Key design decisions and rationale
  - Success metrics for v1.1.0

- **docs/new_folder_structure.md**: Complete reorganization plan
  - New structure optimized for workshop materials
  - Migration plan for obsolete files
  - Implementation phases

#### Prompt Templates
- **prompts/01_research_domain_setup.md**: Research scope definition prompt
  - Copy-paste template for Claude Code
  - Examples for Education and Medicine domains
  - Tips for effective scope definition

- **prompts/02_query_strategy.md**: Search query design prompt
  - Boolean operator cheat sheet
  - Query trade-offs explanation (broad/focused/narrow)
  - Decision tree for query selection
  - Multi-source data collection strategy

#### Workshop Materials
- **workshop/hands_on_guide.md**: Complete 3-hour workshop structure
  - Pre-workshop setup instructions (VS Code, Python, API keys)
  - Part 1: Introduction & Demo (30 min)
  - Part 2: Hands-on exercises (90 min)
    - Exercise 1: Define research project (20 min)
    - Exercise 2: Design search query (20 min)
    - Exercise 3: Collect papers & build PRISMA profile (40 min)
    - Exercise 4: Build RAG system (30 min)
  - Part 3: Advanced topics (30 min) - troubleshooting, multi-project management
  - Part 4: Wrap-up (30 min) - resources, homework, Q&A

#### Project Management
- **project_management/TODO.md**: Comprehensive task tracker
  - High priority items (v1.1.0 release blockers)
  - Medium priority items (v1.2.0 features)
  - Low priority items (future enhancements)
  - Completion tracking

- **project_management/ROADMAP.md**: Long-term vision and milestones
  - Phase 1: Foundation (v1.0.0) ✅
  - Phase 2: Workshop Pivot (v1.1.0) 🚧
  - Phase 3: Community & Templates (v1.2.0) 📅
  - Phase 4: Advanced Features (v1.3.0) 📅
  - Phase 5: Platform & Scale (v2.0.0) 🔮
  - Metrics and KPIs for each phase

- **project_management/CHANGELOG.md**: This file

#### Code Reorganization
- **backend/core/**: Core implementation modules (copied from 01_literature_review_rag/)
  - `prisma_pipeline.py`: PRISMA systematic review implementation
  - `research_profile.py`: Profile management and YAML loading
  - `prisma_integration.py`: PRISMA + RAG integration layer
  - `rag_graph.py`: LangGraph-based RAG retrieval
  - `retrieval.py`: Vector DB retrieval logic
  - `ingestion.py`: Document ingestion and preprocessing
  - `config.py`: Configuration management

- **templates/research_profiles/**: YAML templates (copied from 01_literature_review_rag/config/)
  - `default.yaml`: General research template
  - `hrm_ai_bias.yaml`: HRM/HRD AI bias research template

---

### Changed

#### Project Focus
- **Before**: Build web-based RAG service (Next.js frontend + FastAPI backend)
- **After**: Educational materials for VS Code + Claude Code workflow

#### User Journey
- **Before**: User fills web form → API generates code → User downloads and runs
- **After**: User talks to Claude in VS Code → Claude generates code → User runs in terminal

#### Deliverable
- **Before**: Hosted RAG system (researcher queries pre-built system)
- **After**: Local RAG system (researcher builds their own with guidance)

#### Documentation Approach
- **Before**: Technical API documentation and deployment guides
- **After**: Step-by-step conversational prompts and workshop exercises

#### File Names
- **Renamed**: `CLAUDE_FOR_RESEARCHERS.md` → `CLAUDE.md` (standard Claude Code filename)

---

### Removed (Archived to `.archive/`)

#### Obsolete Documentation
- `CLAUDE_CODE_PROMPTS.md` → Superseded by `prompts/` folder
- `PROJECT_SUMMARY.md` → Outdated, replaced by new README
- `ACLOD_Summit_Abstract.md` → Conference-specific, not core material
- `Release Notes/2025-10-03_Initial_Release.md` → Duplicate of `release-notes/v1.0.0.md`

#### Frontend Strategy Docs (No Longer Primary)
- `docs/vercel_frontend_strategy.md` → Archived to `.archive/frontend_plans/`
- `improvement_discussions/Vercel-Frontend-Detailed-Strategy.md` → Archived

#### Module-Based Docs (Replaced by Workshop Structure)
- `docs/module_1_basic_rag_concept.md` → Archived to `.archive/old_modules/`
- `docs/module_2_literature_review_rag.md` → Archived
- `docs/module_3_qualitative_coding_rag.md` → Archived
- `docs/module_4_research_notes_and_collaboration.md` → Archived

#### Deployment Guides (Not Needed for Workshop)
- `docs/deployment_huggingface_guide.md` → Archived to `.archive/old_docs/`
- `01_literature_review_rag/DEPLOYMENT.md` → Archived

#### Old Discussions (Pre-Pivot)
- `improvement_discussions/2025-01-ResearcherRAG-Review.md` → Archived to `.archive/old_discussions/`
- `improvement_discussions/PRISMA-LiteratureRAG-Strategy.md` → Archived
- `improvement_discussions/RAG-Value-Creation-Strategy.md` → Archived
- `improvement_discussions/RAG-for-Researchers-Practical-Strategy.md` → Archived

#### Empty Directories
- `improvement_discussions/` → Removed (all files archived)
- `Release Notes/` → Removed (duplicate of `release-notes/`)

---

### Technical Details

#### Folder Structure Before

```
ResearcherRAG/
├── README.md
├── CLAUDE_FOR_RESEARCHERS.md
├── docs/ (8 files, mixed focus)
├── improvement_discussions/ (5 files)
├── Release Notes/ (1 file)
├── 01_literature_review_rag/ (implementation)
├── 03_research_notes_rag/ (separate module)
└── release-notes/ (duplicate)
```

#### Folder Structure After

```
ResearcherRAG/
├── README.md (to be updated)
├── QUICK_START.md (to be updated)
├── CLAUDE.md (renamed, comprehensive guide)
│
├── docs/
│   ├── project_pivot_discussion.md (new)
│   ├── new_folder_structure.md (new)
│   ├── workshop_planning.md (to create)
│   └── FAQ.md (to create)
│
├── prompts/ (stage-by-stage templates)
│   ├── 01_research_domain_setup.md (new)
│   ├── 02_query_strategy.md (new)
│   ├── 03_prisma_configuration.md (to create)
│   ├── 04_rag_design.md (to create)
│   └── 05_execution_plan.md (to create)
│
├── templates/
│   ├── research_profiles/ (copied from 01_lit_review)
│   └── scripts/ (to create templates)
│
├── examples/ (to create sample projects)
│   └── ai_education_chatbot/
│
├── workshop/
│   ├── hands_on_guide.md (new)
│   ├── sample_data/ (to create)
│   └── exercises/ (to create)
│
├── backend/core/ (reorganized from 01_lit_review)
│
├── project_management/ (new)
│   ├── TODO.md
│   ├── ROADMAP.md
│   └── CHANGELOG.md (this file)
│
├── release-notes/
│   ├── v1.0.0.md
│   └── v1.1.0.md (to create)
│
├── .archive/ (obsolete files preserved)
│   ├── frontend_plans/
│   ├── old_docs/
│   ├── old_discussions/
│   └── old_modules/
│
├── 01_literature_review_rag/ (keep for reference)
└── 03_research_notes_rag/ (keep as optional module)
```

---

### Migration Guide

If you have existing work based on v1.0.0:

#### 1. Update Your Clone
```bash
git pull origin main
```

#### 2. Core Implementation Moved
- **Old**: `01_literature_review_rag/backend/core/`
- **New**: `backend/core/`

Update your imports:
```python
# Old
from 01_literature_review_rag.backend.core import prisma_pipeline

# New
from backend.core import prisma_pipeline
```

#### 3. Research Profiles Moved
- **Old**: `01_literature_review_rag/config/research_profiles/`
- **New**: `templates/research_profiles/`

Update your paths:
```python
# Old
profile = ResearchProfile.from_yaml("01_literature_review_rag/config/research_profiles/default.yaml")

# New
profile = ResearchProfile.from_yaml("templates/research_profiles/default.yaml")
```

#### 4. Documentation References
- **Old**: Refer to `CLAUDE_FOR_RESEARCHERS.md`
- **New**: Refer to `CLAUDE.md`

#### 5. Archived Files
If you need old documentation, it's preserved in `.archive/`:
```bash
# Find archived file
find .archive/ -name "vercel_frontend_strategy.md"
```

---

### Breaking Changes

#### ⚠️ Import Paths Changed
If you imported Python modules from `01_literature_review_rag.backend.core`, update to `backend.core`.

#### ⚠️ Research Profile Paths Changed
YAML profile paths changed from `01_literature_review_rag/config/research_profiles/` to `templates/research_profiles/`.

#### ⚠️ Documentation Moved
Many documentation files moved to `.archive/`. Use the new `CLAUDE.md` and `prompts/` folder instead.

---

### Deprecations

#### Deprecated in v1.1.0
- Old module-based documentation (see `.archive/old_modules/`)
- Frontend strategy documents (see `.archive/frontend_plans/`)

#### Will Be Removed in v1.2.0
- `01_literature_review_rag/` directory (replaced by `backend/` and `templates/`)
- `03_research_notes_rag/` (to be integrated into main workflow or deprecated)

---

### Known Issues

- [ ] README.md still reflects v1.0.0 (web service focus) - needs update
- [ ] QUICK_START.md needs rewrite for workshop workflow
- [ ] Import paths in existing scripts need updating
- [ ] No example projects yet (ai_education_chatbot in progress)
- [ ] Prompt templates 3-5 not yet created

---

### Performance Improvements

- N/A (this is a documentation and structure update)

---

### Contributors

- **Project Lead**: [Your Name]
- **AI Assistant**: Claude (Anthropic)

---

## [1.0.0] - 2025-10-03

### Added

#### Core Features
- PRISMA systematic review pipeline (4 stages: Identification, Screening, Eligibility, Inclusion)
- Multi-dimensional relevance scoring system
  - Domain match (0-10 points)
  - Method match (0-5 points)
  - Topic match (0-5 points)
  - Context match (0-10 points)
  - Exclusion penalty (-20 to 0 points)
  - Title bonus (0 or 10 points)
- Research profile system (YAML-based configuration)
- Vector database integration (ChromaDB)
- RAG query system using LangGraph
  - Query decomposition
  - Parallel retrieval
  - Re-ranking
  - Synthesis

#### Implementation
- `01_literature_review_rag/backend/core/prisma_pipeline.py`: Core PRISMA logic
- `01_literature_review_rag/backend/core/research_profile.py`: Profile management
- `01_literature_review_rag/backend/core/prisma_integration.py`: PRISMA + RAG integration
- `01_literature_review_rag/backend/core/rag_graph.py`: LangGraph implementation
- `01_literature_review_rag/config/research_profiles/default.yaml`: Default profile
- `01_literature_review_rag/config/research_profiles/hrm_ai_bias.yaml`: HRM research profile

#### Interface
- Gradio web interface (`app_with_prisma.py`)
  - Research profile selector
  - Paper upload with PRISMA screening
  - PRISMA flow diagram (Mermaid)
  - Manual review queue
  - RAG query interface
  - Quality score badges on citations

#### Documentation
- Release notes (v1.0.0)
- HOW_TO_UPLOAD_PAPERS.md
- BULK_UPLOAD_GUIDE.md
- DEPLOYMENT.md

---

### Performance

#### PRISMA Screening (v1.0.0)
- **Speed**: 3.8 seconds for 50 papers (~13 papers/sec)
- **Filtering Rate**: 50% (estimated, depends on thresholds)
- **Precision**: 96% (based on manual validation of 100 papers)

#### PDF Processing (Real-world: AI failure_HR project)
- **Success Rate**: 53.4% (316/592 papers)
- **Reasons for Failure**:
  - Paywall restrictions: ~40%
  - Broken DOI/URLs: ~5%
  - Format issues: ~2%

---

### Testing

#### Manual Testing (v1.0.0)
- Tested with AI failure_HR dataset (20,555 papers)
- PRISMA screening: 20,555 → 9,192 → 592 papers (2.9% final selection rate)
- RAG query testing: 50 sample questions, 90% relevant answers

---

## [Unreleased]

### Planned for v1.1.0 (Current)
- Complete remaining prompt templates (Stage 3-5)
- Create code templates (6 Python scripts)
- Create research profile templates (3 domains)
- Build example project (ai_education_chatbot)
- Write Release Note v1.1.0
- Update README and QUICK_START

### Planned for v1.2.0
- Workshop presentation slides
- Additional example projects (medical, psychology)
- Video tutorial series
- Community forum setup

### Planned for v1.3.0
- Citation graph analysis
- Temporal trend analysis
- Multi-lingual RAG support
- Automated effect size extraction

---

## Version Numbering

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR** version (1.x.x): Incompatible API/structure changes
- **MINOR** version (x.1.x): New features, backwards-compatible
- **PATCH** version (x.x.1): Bug fixes, backwards-compatible

---

**Changelog Maintained By**: Project Lead
**Last Updated**: 2025-10-11
**Next Review**: After v1.1.0 release
