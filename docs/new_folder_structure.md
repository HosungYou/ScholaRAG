# ResearcherRAG v1.1.0 Folder Structure

## New Structure (Workshop-Focused)

```
ResearcherRAG/
│
├── README.md                          # Project overview (workshop focus)
├── QUICK_START.md                     # 5-minute getting started guide
├── CLAUDE.md                          # Claude Code instructions (renamed)
│
├── docs/                              # Documentation
│   ├── project_pivot_discussion.md    # Why we changed direction
│   ├── workshop_planning.md           # Workshop logistics
│   └── FAQ.md                         # Common questions
│
├── prompts/                           # Stage-by-stage prompt templates
│   ├── 01_research_domain_setup.md
│   ├── 02_query_strategy.md
│   ├── 03_prisma_configuration.md     # TO CREATE
│   ├── 04_rag_design.md               # TO CREATE
│   └── 05_execution_plan.md           # TO CREATE
│
├── templates/                         # Reusable code templates
│   ├── research_profiles/
│   │   ├── education_template.yaml    # TO CREATE
│   │   ├── medicine_template.yaml     # TO CREATE
│   │   └── social_science_template.yaml  # TO CREATE
│   │
│   └── scripts/                       # Python script templates
│       ├── 1_collect_papers_template.py   # TO CREATE
│       ├── 2_run_prisma_template.py       # TO CREATE
│       ├── 3_download_pdfs_template.py    # TO CREATE
│       ├── 4_extract_text_template.py     # TO CREATE
│       ├── 5_build_vectordb_template.py   # TO CREATE
│       └── 6_query_rag_template.py        # TO CREATE
│
├── examples/                          # Complete sample projects
│   ├── ai_education_chatbot/          # Example 1
│   │   ├── README.md                  # Project description
│   │   ├── conversation_log.md        # Claude dialogue transcript
│   │   ├── config/
│   │   │   └── research_profile.yaml
│   │   └── scripts/
│   │       ├── 1_collect_papers.py
│   │       ├── 2_run_prisma.py
│   │       └── ...
│   │
│   └── medical_ehr_workflow/          # Example 2 (TO CREATE)
│
├── workshop/                          # Workshop materials
│   ├── hands_on_guide.md              # 3-hour workshop guide
│   ├── slides.pdf                     # Presentation (TO CREATE)
│   ├── sample_data/                   # Pre-collected papers for demo
│   │   └── 50_sample_papers.zip       # TO CREATE
│   └── exercises/                     # Practice exercises
│       ├── exercise_1_query_design.md
│       └── exercise_2_prisma_config.md
│
├── backend/                           # Core implementation (reference)
│   └── core/
│       ├── prisma_pipeline.py         # PRISMA implementation
│       ├── research_profile.py        # Profile management
│       └── rag_graph.py               # RAG retrieval logic
│
├── release-notes/                     # Version history
│   ├── v1.0.0.md                      # Initial release
│   └── v1.1.0.md                      # Workshop pivot (TO CREATE)
│
├── project_management/                # Project tracking (NEW)
│   ├── TODO.md                        # Current tasks
│   ├── ROADMAP.md                     # Future plans
│   └── CHANGELOG.md                   # Detailed changes
│
└── .archive/                          # Obsolete files (moved, not deleted)
    ├── old_frontend_plans/
    ├── initial_release_note/
    └── superseded_docs/
```

---

## Files to DELETE (Obsolete)

### 1. Duplicate/Superseded Documentation
- ❌ `/CLAUDE_CODE_PROMPTS.md` → Superseded by `prompts/` folder
- ❌ `/PROJECT_SUMMARY.md` → Outdated, replaced by new README
- ❌ `/ACLOD_Summit_Abstract.md` → Conference-specific, not core material
- ❌ `/Release Notes/2025-10-03_Initial_Release.md` → v1.0.0 already in `release-notes/`

### 2. Frontend Strategy Docs (No Longer Primary Focus)
- ❌ `/docs/vercel_frontend_strategy.md` → Move to `.archive/`
- ❌ `/improvement_discussions/Vercel-Frontend-Detailed-Strategy.md` → Move to `.archive/`

### 3. Outdated Improvement Discussions
- ❌ `/improvement_discussions/2025-01-ResearcherRAG-Review.md` → Pre-pivot discussion
- ⚠️  Keep but move to `.archive/`:
  - `improvement_discussions/PRISMA-LiteratureRAG-Strategy.md`
  - `improvement_discussions/RAG-Value-Creation-Strategy.md`
  - `improvement_discussions/RAG-for-Researchers-Practical-Strategy.md`

### 4. Module-Based Docs (Replaced by Workshop Structure)
- ❌ `/docs/module_1_basic_rag_concept.md` → Move to `.archive/`
- ❌ `/docs/module_2_literature_review_rag.md` → Move to `.archive/`
- ❌ `/docs/module_3_qualitative_coding_rag.md` → Move to `.archive/`
- ❌ `/docs/module_4_research_notes_and_collaboration.md` → Move to `.archive/`

### 5. Deployment Guides (Not Needed for Workshop)
- ❌ `/docs/deployment_huggingface_guide.md` → Move to `.archive/`
- ❌ `/01_literature_review_rag/DEPLOYMENT.md` → Move to `.archive/`

---

## Files to RENAME

- ✅ `/CLAUDE_FOR_RESEARCHERS.md` → `/CLAUDE.md` (standard Claude Code filename)

---

## Files to KEEP (Essential)

### Core Documentation
- ✅ `/README.md` (update for workshop focus)
- ✅ `/QUICK_START.md` (update for workshop workflow)

### Implementation Code (Reference)
- ✅ `/01_literature_review_rag/backend/core/*.py` → Move to `/backend/core/`
- ✅ `/01_literature_review_rag/config/research_profiles/*.yaml` → Move to `/templates/research_profiles/`
- ✅ `/03_research_notes_rag/` → Keep as optional advanced module

### Release History
- ✅ `/release-notes/v1.0.0.md`

### New Workshop Materials
- ✅ `/prompts/` (keep and expand)
- ✅ `/workshop/` (keep and expand)
- ✅ `/docs/project_pivot_discussion.md` (just created)

---

## Migration Plan

### Phase 1: Archive Obsolete Files
```bash
mkdir -p .archive/{frontend_plans,old_docs,old_discussions,old_modules}

# Move frontend docs
mv docs/vercel_frontend_strategy.md .archive/frontend_plans/
mv improvement_discussions/Vercel-Frontend-Detailed-Strategy.md .archive/frontend_plans/

# Move old module docs
mv docs/module_*.md .archive/old_modules/

# Move old discussions
mv improvement_discussions/2025-01-ResearcherRAG-Review.md .archive/old_discussions/
mv improvement_discussions/PRISMA-LiteratureRAG-Strategy.md .archive/old_discussions/
mv improvement_discussions/RAG-Value-Creation-Strategy.md .archive/old_discussions/

# Move deployment docs
mv docs/deployment_huggingface_guide.md .archive/old_docs/
mv 01_literature_review_rag/DEPLOYMENT.md .archive/old_docs/

# Move duplicate files
mv "Release Notes/2025-10-03_Initial_Release.md" .archive/old_docs/
mv CLAUDE_CODE_PROMPTS.md .archive/old_docs/
mv PROJECT_SUMMARY.md .archive/old_docs/
mv ACLOD_Summit_Abstract.md .archive/old_docs/
```

### Phase 2: Reorganize Core Code
```bash
# Create new backend structure
mkdir -p backend/core

# Move core Python modules
mv 01_literature_review_rag/backend/core/prisma_pipeline.py backend/core/
mv 01_literature_review_rag/backend/core/research_profile.py backend/core/
mv 01_literature_review_rag/backend/core/prisma_integration.py backend/core/
mv 01_literature_review_rag/backend/core/rag_graph.py backend/core/
mv 01_literature_review_rag/backend/core/retrieval.py backend/core/
mv 01_literature_review_rag/backend/core/ingestion.py backend/core/

# Move template profiles
mkdir -p templates/research_profiles
mv 01_literature_review_rag/config/research_profiles/*.yaml templates/research_profiles/
```

### Phase 3: Create New Directories
```bash
# Project management
mkdir -p project_management

# Examples
mkdir -p examples/ai_education_chatbot/{config,scripts,data}

# Workshop materials
mkdir -p workshop/{sample_data,exercises}

# Templates
mkdir -p templates/scripts
```

### Phase 4: Rename Files
```bash
# Rename CLAUDE guide
mv CLAUDE_FOR_RESEARCHERS.md CLAUDE.md

# Clean up Release Notes folder (duplicate)
rmdir "Release Notes"  # Empty after moving files
```

---

## New Files to CREATE

### Documentation
- [ ] `docs/workshop_planning.md` - Workshop logistics and timeline
- [ ] `docs/FAQ.md` - Common questions from researchers

### Prompts (Stage 3-5)
- [ ] `prompts/03_prisma_configuration.md`
- [ ] `prompts/04_rag_design.md`
- [ ] `prompts/05_execution_plan.md`

### Templates
- [ ] `templates/research_profiles/education_template.yaml`
- [ ] `templates/research_profiles/medicine_template.yaml`
- [ ] `templates/research_profiles/social_science_template.yaml`
- [ ] `templates/scripts/1_collect_papers_template.py`
- [ ] `templates/scripts/2_run_prisma_template.py`
- [ ] `templates/scripts/3_download_pdfs_template.py`
- [ ] `templates/scripts/4_extract_text_template.py`
- [ ] `templates/scripts/5_build_vectordb_template.py`
- [ ] `templates/scripts/6_query_rag_template.py`

### Examples
- [ ] `examples/ai_education_chatbot/README.md`
- [ ] `examples/ai_education_chatbot/conversation_log.md`
- [ ] `examples/ai_education_chatbot/config/research_profile.yaml`
- [ ] `examples/ai_education_chatbot/scripts/*.py` (6 scripts)

### Workshop
- [ ] `workshop/slides.pdf` - Presentation
- [ ] `workshop/sample_data/50_sample_papers.zip` - Demo data
- [ ] `workshop/exercises/exercise_1_query_design.md`
- [ ] `workshop/exercises/exercise_2_prisma_config.md`

### Project Management
- [ ] `project_management/TODO.md` - Current tasks
- [ ] `project_management/ROADMAP.md` - Future plans
- [ ] `project_management/CHANGELOG.md` - Detailed changes

### Release Notes
- [ ] `release-notes/v1.1.0.md` - Workshop pivot release

---

## Implementation Order

1. ✅ Create `.archive/` and move obsolete files (preserve history)
2. ✅ Reorganize core code into new `/backend/` structure
3. ✅ Rename `CLAUDE_FOR_RESEARCHERS.md` to `CLAUDE.md`
4. ✅ Create project management structure
5. ⏳ Create remaining prompt templates (Stage 3-5)
6. ⏳ Create code templates (scripts + profiles)
7. ⏳ Create example project (ai_education_chatbot)
8. ⏳ Write v1.1.0 release note
9. ⏳ Update README.md
10. ⏳ Commit and push all changes

---

**Document Status**: Implementation Plan
**Created**: 2025-10-11
**Next Action**: Execute Phase 1 (Archive obsolete files)
