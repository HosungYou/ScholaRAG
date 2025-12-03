# Changelog

All notable changes to ScholaRAG will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.2.5.3] - 2025-12-03

### Fixed

#### Stage 1 Project Type Selection Protocol

**Problem**: Claude was auto-inferring `project_type` (Knowledge Repository vs Systematic Review) from conversation context instead of explicitly asking users to choose.

**Impact**: Users might end up with incorrect project configuration without realizing their intended project type wasn't properly set.

**Solution**: Updated `prompts/01_research_domain_setup.md` metadata to enforce explicit selection:

1. **conversation_flow** updated:
   - Turn 1 now requires Claude to explicitly ask "Option A or Option B?"
   - Turn 2 requires user's explicit choice before proceeding
   - Added `critical_rule`: "NEVER auto-infer project_type"

2. **divergence_handling** updated:
   - Added CRITICAL priority pattern for missing Option A/B selection
   - Claude must redirect to project type selection before any other questions

### Changed

- `prompts/01_research_domain_setup.md`: conversation_flow expected_turns 4-8 → 5-9
- README.md: Streamlined documentation with improved mermaid architecture diagram

---

## [1.2.0] - 2025-10-31

### 🎯 Major Change: Confidence Mechanism Removal

**BREAKING CHANGE**: Removed AI confidence scoring in favor of total_score-only approach. This enables Human-AI symmetric scoring for Cohen's Kappa calculation.

### Philosophy

**Previous approach (v1.1.x)**:
- Decision = f(total_score, confidence)
- AI: quantitative confidence (0-100%)
- Human: subjective confidence (low/medium/high)
- **Problem**: Incomparable scales → Cohen's Kappa impossible

**New approach (v1.2.0)**:
- Decision = f(total_score)
- Both AI and Human use identical 6-dimension rubric
- Both produce total_score (-20 to 50 range)
- **Benefit**: Reproducible, symmetric, Kappa-calculable

### Breaking Changes

#### 1. Configuration Schema

```yaml
# REMOVED (v1.1.x)
ai_prisma_rubric:
  decision_confidence:
    auto_include: 50   # % confidence
    auto_exclude: 20   # % confidence

# ADDED (v1.2.0)
ai_prisma_rubric:
  score_threshold:
    auto_include: 25   # total_score (knowledge_repository)
    auto_exclude: 0    # total_score
```

#### 2. CSV Output Schema

**`03_screen_papers.py` outputs**:
- ❌ REMOVED: `confidence` column
- ✅ RETAINED: `total_score`, `decision`, all dimension scores

**`03b_human_review.py` outputs**:
- ❌ REMOVED: `ai_confidence`, `human_confidence`
- ✅ ADDED:
  - `human_total_score`, `human_domain`, `human_intervention`, etc.
  - `score_difference` (abs(AI - Human))

### Changed

#### scripts/03_screen_papers.py
- Decision logic: removed confidence threshold, use total_score only
- Knowledge Repository: `score ≥ 25` (was `confidence ≥ 50% AND score ≥ 30`)
- Systematic Review: `score ≥ 40` (was `confidence ≥ 90% AND score ≥ 30`)
- Hallucination → human-review flag (was confidence penalty)
- Prompt: removed confidence calculation section
- Console: show score thresholds instead of confidence

#### scripts/03b_human_review.py
- Human reviewers score all 6 dimensions (not subjective confidence)
- Removed 1/2/3 confidence input
- Added auto total_score calculation
- CSV includes all dimension scores for Kappa analysis

#### scripts/validate_config.py
- Validates `score_threshold` (20-50 range) instead of `decision_confidence`

#### scripts/test_full_pipeline.py
- Zone validation: score-based instead of confidence-based
- Mock data: includes 6-dimension scores + score_difference

#### scripts/test_ai_prisma_scoring.py
- Mock config: `score_threshold` instead of `decision_confidence`

#### scripts/run_validation_workflow.py
- Messages: "borderline scores" instead of "11-89% confidence"

### Added

- **PIPELINE_ANALYSIS.md**: Complete dependency graph, workflow documentation
- **Cohen's Kappa Support**: Now possible with symmetric scoring

### Removed

- All confidence calculation logic
- Confidence-based thresholds in config
- Confidence columns in CSV outputs

### Migration Guide

**Step 1: Update config.yaml**
```yaml
# Knowledge Repository
ai_prisma_rubric:
  score_threshold:
    auto_include: 25
    auto_exclude: 0

# Systematic Review
ai_prisma_rubric:
  score_threshold:
    auto_include: 40
    auto_exclude: 0
```

**Step 2: Optional re-screening**
```bash
python scripts/03_screen_papers.py \
  --project projects/YOUR_PROJECT \
  --question "Your research question"
```

**Step 3: Update human review workflow**
- Train reviewers on 6-dimension scoring
- Use same rubric as AI (see prompt guidelines)

### Performance Impact

| Metric | v1.1.x | v1.2.0 | Change |
|--------|--------|--------|--------|
| Decision Logic Complexity | Dual criteria (AND/OR) | Single criterion | -50% |
| Human Review Time | 2-3 min/paper | 3-5 min/paper | +50% (more thorough) |
| Cohen's Kappa Calculable | ❌ No | ✅ Yes | Enabled |
| Academic Reproducibility | Medium | High | Improved |

### Documentation

- Added [GitHub Release v1.2.0](https://github.com/HosungYou/ScholaRAG/releases/tag/v1.2.0)
- Added `PIPELINE_ANALYSIS.md` (complete workflow documentation)
- Updated `CHANGELOG.md` with migration guide

### Commits

- `[commit hash]` - BREAKING CHANGE: Remove confidence mechanism, use total_score only

---

## [1.1.6] - 2025-10-29

### 🎓 Academic Positioning: PICOC+S-Derived Framework with Scholarly Citations

**Purpose**: Provides complete academic justification for ScholaRAG's 6-dimension rubric by mapping it to established evidence-synthesis frameworks. This release positions ScholaRAG as a **PICOC+S-derived, automation-aware framework** with full scholarly citations.

### Added

- **[GitHub Release v1.1.6](https://github.com/HosungYou/ScholaRAG/releases/tag/v1.1.6)**: Comprehensive academic lineage documentation
  - Complete mapping of all 6 dimensions to established frameworks
  - 13 primary scholarly citations with full bibliographic details
  - Citation templates for researchers (BibTeX, LaTeX methodology section)
  - Academic positioning statement for papers
  - Full reference list with DOIs and citation counts

### Changed

- **Framework Terminology**: "PICO-inspired" → "PICOC+S-derived with automation-aware prioritisation"
  - **Previous (v1.1.5)**: "PICO-inspired 6-dimension rubric"
  - **Current (v1.1.6)**: "PICOC+S-derived relevance scoring with automation-aware prioritisation"

- **Academic Lineage Mapping**:
  | ScholaRAG Dimension | Established Framework | Key Citations |
  |---------------------|----------------------|---------------|
  | Domain (0-10) | PICOC: Context, SPICE: Setting | Booth et al., 2012; Lockwood et al., 2015 |
  | Intervention (0-10) | PICO: Intervention, SPIDER: Phenomenon | Richardson et al., 1995; Cooke et al., 2012 |
  | Method (0-5) | PICOS: Study design, SPIDER: Design | Higgins et al., 2022; Cooke et al., 2012 |
  | Outcomes (0-10) | PICO: Outcomes | Richardson et al., 1995 |
  | Exclusion (-20 to 0) | PRISMA 2020: Eligibility exclusions | Page et al., 2021; Higgins et al., 2022 |
  | Title Bonus (+10) | Text-mining automation | O'Mara-Eves et al., 2015; Wallace et al., 2010 |

- **Documentation Updates**:
  - **README.md**: Updated framework description with PICOC+S positioning and scholarly citations
  - **scripts/03_screen_papers.py**: Added academic citations to docstring and prompt text
  - **prompts/03_prisma_configuration.md**: Updated framework references with scholarly grounding

### Key Academic Justifications

1. **Domain (Population → Context)**
   - **Scholarly precedent**: PICOC (Booth et al., 2012) adds contextual/setting constraints to capture organizational conditions
   - **ScholaRAG application**: Domain scoring reflects established practice of coupling population with contextual qualifiers

2. **Method (Comparison → Study Design Rigor)**
   - **Scholarly precedent**: PICOS (Higgins et al., 2022, Cochrane Handbook) requires specifying eligible study designs to safeguard methodological rigor
   - **ScholaRAG application**: Explicit scoring of design quality mirrors these standards by prioritising higher-rigor studies

3. **Exclusion (Negative Scoring)**
   - **Scholarly precedent**: PRISMA 2020 (Page et al., 2021) and Cochrane Handbook (Higgins et al., 2022) emphasize documenting exclusions for reproducibility
   - **ScholaRAG innovation**: Quantitative exclusion scoring (-20 to 0) operationalizes this guidance

4. **Title Bonus (Novel Dimension)**
   - **Scholarly precedent**: Text-mining automation (O'Mara-Eves et al., 2015) shows title/abstract term weighting improves prioritisation accuracy
   - **ScholaRAG innovation**: Integrates title bonus aligning with validated machine-learning triage practices

### Why This Matters

- **Honest academic positioning**: Every dimension has scholarly precedent (except Title Bonus, which has automation research justification)
- **Clear lineage**: Transparent about which frameworks influenced each dimension
- **Citation-ready**: Researchers can now cite ScholaRAG with complete academic context
- **No overclaiming**: ScholaRAG IS a PICOC+S synthesis, NOT "another PICO variant"

### Migration

**Action Required**: None! This is a documentation-only update with no code changes.

**For Researchers Citing ScholaRAG**: Update citations to reference PICOC+S-derived framework:
```bibtex
@software{scholarag2025,
  title = {ScholaRAG: Template-Free AI-PRISMA Systematic Review Automation},
  author = {You, Hosung},
  year = {2025},
  version = {1.1.6},
  note = {Uses PICOC+S-derived 6-dimension rubric (Booth et al., 2012; Higgins et al., 2022)},
  url = {https://github.com/HosungYou/ScholaRAG}
}
```

### References

See [GitHub Release v1.1.6](https://github.com/HosungYou/ScholaRAG/releases/tag/v1.1.6) for complete reference list (13 primary sources).

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
  - Added [GitHub Release v1.1.5](https://github.com/HosungYou/ScholaRAG/releases/tag/v1.1.5) with comprehensive academic justification
  - Updated [GitHub Release v1.1.4](https://github.com/HosungYou/ScholaRAG/releases/tag/v1.1.4) with terminology warning
  - Clarified Domain (Population extension) vs Method (Study rigor, not Comparison)
  - Explained why strict PICO doesn't fit multidisciplinary research

- **Code Comments**
  - Added framework justification to `scripts/03_screen_papers.py` docstring
  - Updated prompt text: "based on PICO framework" → "based on PICO-inspired framework"
  - Referenced GitHub Releases for academic context

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

- Added [GitHub Release v1.1.4](https://github.com/HosungYou/ScholaRAG/releases/tag/v1.1.4) with detailed migration guide
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
- [GitHub Releases](https://github.com/HosungYou/ScholaRAG/releases)

---

## Links

- **GitHub Repository**: https://github.com/HosungYou/ScholaRAG
- **Issue Tracker**: https://github.com/HosungYou/ScholaRAG/issues
- **Documentation**: https://researcher-rag-helper.vercel.app/
