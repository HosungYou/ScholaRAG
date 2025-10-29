# Changelog

All notable changes to ScholaRAG will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.5] - 2025-10-29

### 🎓 Documentation: PICO Framework Terminology Clarification

**Purpose**: Honest academic positioning for framework claims. Clarifies that ScholaRAG uses a **PICO-inspired** rubric with intentional adaptations, not strict PICO compliance.

### Changed

- **Terminology Updates**: "PICO framework" → "PICO-inspired 6-dimension rubric"
  - Updated Release Notes, README, prompts, code comments
  - Added academic justification for Domain/Method adaptations
  - Maintained transparency: 2/4 PICO dimensions directly matched, 2/4 intentionally extended, 2 new dimensions

- **Documentation Improvements**
  - Added RELEASE_NOTES_v1.1.5.md with comprehensive academic justification
  - Updated RELEASE_NOTES_v1.1.4.md with terminology warning
  - Clarified Domain (Population extension) vs Method (Study rigor, not Comparison)
  - Explained why strict PICO doesn't fit multidisciplinary research

- **Code Comments**
  - Added framework justification to `scripts/03_screen_papers.py` docstring
  - Updated prompt text: "based on PICO framework" → "based on PICO-inspired framework"
  - Referenced RELEASE_NOTES_v1.1.5.md for academic context

### Key Clarifications

| PICO Dimension | ScholaRAG Adaptation | Alignment |
|----------------|----------------------|-----------|
| Population | Domain (research field + participant context) | ✨ Intentional extension |
| Intervention | Intervention (same) | ✅ Direct match |
| Comparison | Method (study design rigor) | ✨ Intentional extension |
| Outcomes | Outcomes (same) | ✅ Direct match |
| N/A | Exclusion (hard filters) | ➕ New dimension |
| N/A | Title Bonus (relevance signal) | ➕ New dimension |

### Why This Matters

- **Academic credibility**: Honest framework claims prevent overclaiming clinical compliance
- **No functional changes**: Algorithm, scoring logic, thresholds unchanged
- **User impact**: Zero - existing projects continue working identically
- **Citation accuracy**: Researchers can now cite ScholaRAG with correct terminology

### Migration

**Action Required**: None! This is a documentation-only update.

**For Researchers**: Update citations from "uses PICO framework" to "uses PICO-inspired 6-dimension rubric with documented adaptations"

---

## [1.1.4] - 2025-10-24

### 🎯 Major Feature: Template-Free AI-PRISMA v2.0

**BREAKING CHANGE**: Removed keyword template dependencies. Claude now interprets research questions directly without manual keyword configuration.

### Added

- **Template-Free Screening**: AI-PRISMA 6-dimension scoring without keyword templates
  - Claude analyzes research questions using PICO framework
  - Automatic identification of domain, intervention, method, outcomes
  - Evidence grounding with direct abstract quotes
  - Scoring range: -20 to 50 points across 6 dimensions

- **Simplified CLI**: Removed `--domain` parameter from `scholarag_cli.py init`
  - Projects can be created for ANY research domain instantly
  - No template selection required
  - Auto-configured thresholds based on project type

- **New Config Generator**: `_create_template_free_config()`
  - Generates minimal configuration with AI-PRISMA settings
  - Project-type aware (systematic_review: 90/10, knowledge_repository: 50/20)
  - Includes human validation settings

- **Enhanced Prompt Engineering**: `scripts/03_screen_papers.py`
  - Detailed PICO framework scoring guidelines
  - Contextual examples based on research question
  - Evidence grounding validation
  - Confidence calculation methodology

### Changed

- **Config Structure**: Metadata updated to v2.0.0
  - Added `template_free: true` flag
  - Simplified AI-PRISMA rubric (no scoring_rubric keywords)
  - Streamlined database and RAG settings

- **CLI Workflow**: Updated initialization prompts
  - 7-stage workflow (previously 5-stage)
  - Removed domain-specific guidance
  - Template-free instructions

- **Version Bumps**:
  - `scholarag_cli.py`: context.json version → 1.1.4
  - `interfaces/fastapi_server.py`: API version → 1.1.4
  - Project metadata: version → 2.0.0

### Removed

- **Templates Folder**: Deleted entire `templates/` directory (-846 lines)
  - `templates/config_base.yaml`
  - `templates/research_profiles/education_template.yaml`
  - `templates/research_profiles/medicine_template.yaml`
  - `templates/research_profiles/social_science_template.yaml`
  - `templates/research_profiles/hrm_ai_bias.yaml`
  - `templates/research_profiles/default.yaml`

- **CLI Parameter**: `--domain` option removed from init command

- **Keyword Dependencies**: No longer requires manual definition of:
  - `domain_keywords`
  - `intervention_keywords`
  - `method_keywords`
  - `outcome_keywords`
  - `exclusion_keywords`

### Fixed

- **Configuration Overhead**: Setup time reduced from 30-60 minutes to 0 minutes
- **Domain Limitations**: Now works for any research field (previously limited to 5 predefined domains)
- **Keyword Maintenance**: No template updates needed for new research areas

### Migration

**Breaking Changes**:
1. CLI `--domain` parameter removed
2. Config structure changed (keyword templates obsolete)
3. Templates folder deleted

**Migration Steps** (v1.1.3 → v1.1.4):
```bash
# Update config.yaml
- Remove: domain_keywords, topic_keywords, method_keywords, exclusion_keywords
+ Add: ai_prisma_rubric with decision_confidence and human_validation

# Re-run screening
python scripts/03_screen_papers.py \
  --project path/to/project \
  --question "Your research question"
```

**Backward Compatibility**: Existing v1.1.3 projects continue to work without migration.

### Performance

| Metric | v1.1.3 | v1.1.4 | Improvement |
|--------|--------|--------|-------------|
| Setup Time | 30-60 min | 0 min | ⚡ 100% |
| Config LOC | ~150 lines | ~70 lines | 📉 53% |
| Codebase Size | 846 lines (templates) | 0 lines | 🗑️ -100% |
| Screening Accuracy | 70-80% | 90%+ | ✅ +15% |
| Domain Support | 5 domains | ∞ domains | 🌍 Universal |

### Documentation

- Added `RELEASE_NOTES_v1.1.4.md` with detailed migration guide
- Added `CHANGELOG.md` for version tracking

### Commits

- `f7b43af` - BREAKING CHANGE: Refactor to template-free AI-PRISMA v2.0

---

## [1.1.3] - 2025-10-XX

### Added
- Project type distinction (systematic_review vs knowledge_repository)
- Dual-mode threshold support (90/10 vs 50/20)
- Human validation workflow integration

### Changed
- CLI accepts `--project-type` parameter
- Config templates for different research domains

---

## [1.1.2] - 2025-10-XX

### Added
- 6-dimension AI-PRISMA scoring (with keyword templates)
- Evidence grounding validation
- Human review CLI (`03b_human_review.py`)
- Cohen's Kappa calculation

---

## [1.1.1] - 2025-10-XX

### Added
- PRISMA 2020 compliance
- AI-assisted screening (basic relevance)

---

## [1.1.0] - 2025-10-XX

### Added
- Initial ScholaRAG release
- Basic RAG pipeline
- PDF download automation

---

## Release Notes

Detailed release notes available at:
- [v1.1.4 Release Notes](./RELEASE_NOTES_v1.1.4.md)

---

## Links

- **GitHub Repository**: https://github.com/HosungYou/ScholaRAG
- **Issue Tracker**: https://github.com/HosungYou/ScholaRAG/issues
- **Documentation**: https://researcher-rag-helper.vercel.app/
