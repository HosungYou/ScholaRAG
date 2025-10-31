# ScholaRAG v1.1.7 Release Notes

**Release Date**: 2025-10-31
**Type**: Critical Bug Fix + Documentation Clarification
**Status**: Stable

---

## 🎯 What's New: Stage Workflow Clarification & Environment Loading Fixes

ScholaRAG v1.1.7 addresses **critical misunderstandings** about the Stage 1-3 workflow and fixes environment variable loading issues in scripts. This release ensures researchers have **clear visibility** into how `project_type` affects the PRISMA screening process.

---

## 🔧 Critical Fixes

### 1. **Stage 1-3 Workflow Clarification**

**Problem**: Documentation incorrectly implied that `project_type` affects **initial paper fetching** (Stage 1).

**Reality**:
- **Stage 1-2 (Fetch & Dedup)**: Both `knowledge_repository` and `systematic_review` fetch **IDENTICAL** papers (10K-20K)
- **Stage 3 (PRISMA Screening)**: `project_type` triggers different confidence thresholds:
  - `knowledge_repository`: 50% threshold → retains ~5K-15K papers
  - `systematic_review`: 90% threshold → retains ~50-300 papers

**What Changed**:
- ✅ **CLAUDE.md**: Updated all workflow descriptions to clarify Stage 3 threshold behavior
- ✅ **AGENTS.md**: Mirrored changes for Codex/Cursor users
- ✅ **ARCHITECTURE_CLARIFICATION.md**: New comprehensive architecture documentation

**Impact**: Researchers now understand that:
- NO manual paper count limits exist in Stage 1
- Papers are **naturally filtered** through PRISMA AI confidence scoring
- `project_type` is a **screening parameter**, not a fetching parameter

---

### 2. **Mandatory `project_type` Selection**

**Problem**: Claude Code was auto-selecting `project_type` without user input, causing confusion.

**Solution**:
- ✅ **CLAUDE.md**: Added explicit requirement: "ALWAYS ask user to choose `project_type`"
- ✅ **AGENTS.md**: Mirrored requirement for consistency
- ✅ Stage 1 examples now show mandatory user selection step

**New Behavior**:
```
Claude Code → Researcher:
"I need to know which project type to use:

**Option 1: knowledge_repository**
- Stage 1-2: Fetch & deduplicate ~10K-20K papers
- Stage 3 PRISMA: 50% threshold → ~5K-15K papers pass
- Best for: Domain exploration, teaching materials

**Option 2: systematic_review**
- Stage 1-2: Fetch & deduplicate ~10K-20K papers (SAME)
- Stage 3 PRISMA: 90% threshold → ~50-300 papers pass
- Best for: Journal publication, meta-analysis

Which matches your goals?"

Researcher → Selects Option

Claude Code → Executes with user choice
```

---

### 3. **Environment Variable Loading Fixes**

**Problem**: Scripts couldn't load `.env` from project directories, causing `ANTHROPIC_API_KEY not found` errors.

**Solution**:
- ✅ **01_fetch_papers.py**: Added project-level `.env` loading with fallback
- ✅ **03_screen_papers.py**: Added project-level `.env` loading with fallback
- ✅ **Semantic Scholar API key**: Now properly loaded from project `.env`

**Loading Priority** (new):
```python
1. Project-level: projects/YYYY-MM-DD_Name/.env
2. ScholaRAG root: ScholaRAG/.env
3. System environment variables
```

**Files Modified**:
- `scripts/01_fetch_papers.py`: Lines 38-41 (env loading), 56-57 (API key usage), 96-98 (header injection)
- `scripts/03_screen_papers.py`: Lines 42-47 (env loading with project path)

---

## 📊 Detailed Changes

### Documentation Updates

#### CLAUDE.md
**Line 21**: Added `✅ ALWAYS ask user to choose project_type`
**Line 28**: Added `❌ Auto-select project_type without explicit confirmation`
**Lines 198-216**: Rewrote Stage 1 workflow with mandatory project_type selection
**Lines 234-268**: Clarified that both modes fetch identical papers in Stage 1-2

**Key Addition**:
```markdown
⚠️  CRITICAL: Both modes fetch IDENTICAL papers in Stage 1-2.
Stage 3 PRISMA screening naturally filters based on confidence threshold.
NO manual paper count limits in Stage 1!
```

#### AGENTS.md
**Lines 85-102**: Rewrote Quick Context for project_type decision
**Key Addition**:
```markdown
⚠️  **CRITICAL Understanding**:
- Stage 1 fetches IDENTICAL papers regardless of project_type
- Stage 3 applies confidence threshold via AI scoring (NOT manual limits)
- Papers naturally filter through PRISMA protocol, not arbitrary cutoffs
```

#### ARCHITECTURE_CLARIFICATION.md (New)
**Purpose**: Comprehensive architecture documentation for developers
**Contents**:
- File role clarification (CLAUDE.md vs AGENTS.md vs SKILL.md)
- Stage 1-3 workflow logic explanation
- Prompts ↔ Scripts integration flow
- Future improvements roadmap

---

### Code Fixes

#### scripts/01_fetch_papers.py
**Lines 17-27**: Added imports and environment loading
```python
from dotenv import load_dotenv

# Load environment variables from project .env file
env_path = self.project_path / ".env"
if env_path.exists():
    load_dotenv(env_path)

# API keys
self.semantic_scholar_api_key = os.getenv('SEMANTIC_SCHOLAR_API_KEY')
```

**Lines 96-103**: Added API key header injection for Semantic Scholar
```python
headers = {}
if self.semantic_scholar_api_key:
    headers['x-api-key'] = self.semantic_scholar_api_key

response = requests.get(
    self.semantic_scholar_api,
    params=params,
    headers=headers,
    timeout=30
)
```

#### scripts/03_screen_papers.py
**Lines 42-47**: Fixed environment loading to check project path first
```python
# Load API key from project .env file
env_path = self.project_path / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()  # Try current directory

api_key = os.getenv('ANTHROPIC_API_KEY')
```

---

## 🆚 Comparison: v1.1.6 → v1.1.7

| Aspect | v1.1.6 | v1.1.7 |
|--------|--------|--------|
| **Stage 1 Understanding** | Ambiguous (implied different fetch counts) | ✅ Clarified: Both fetch 10K-20K |
| **project_type Selection** | Auto-selected by Claude Code | ✅ Mandatory user selection |
| **Environment Loading** | System env only | ✅ Project `.env` → Root `.env` → System |
| **Semantic Scholar API** | No API key support | ✅ API key header injection |
| **Architecture Docs** | None | ✅ ARCHITECTURE_CLARIFICATION.md added |

---

## 🎓 For Researchers

### What This Means for Your Workflow

**Before v1.1.7**:
- ❌ Confusion about when papers are filtered
- ❌ `project_type` auto-selected without understanding
- ❌ `.env` files not loaded from project directories

**After v1.1.7**:
- ✅ Clear understanding: Stage 1-2 fetch SAME papers, Stage 3 filters
- ✅ Explicit choice between 50% vs 90% screening thresholds
- ✅ API keys work from project-level `.env` files

### Migration Guide

**If you have existing projects**:
1. No code changes required (backward compatible)
2. Optionally add `.env` to your project folder for API keys
3. Re-read documentation if confused about `project_type`

**If starting a new project**:
1. Claude Code will now **always ask** you to choose `project_type`
2. Understand: Your choice affects **Stage 3 screening**, not Stage 1 fetching
3. Both modes will fetch 10K-20K papers initially

---

## 📚 Related Documentation

- **Architecture Overview**: [ARCHITECTURE_CLARIFICATION.md](ARCHITECTURE_CLARIFICATION.md)
- **Stage Workflow**: [CLAUDE.md](CLAUDE.md) (Lines 198-268)
- **CLI Usage**: [AGENTS.md](AGENTS.md) (Lines 85-102)
- **Previous Release**: [v1.1.6 Release Notes](https://github.com/HosungYou/ScholaRAG/releases/tag/v1.1.6)

---

## 🐛 Known Issues

### 1. Claude Model Name in Old Projects
**Issue**: Projects created before v1.1.7 may have `claude-3-5-sonnet-20241022` in `config.yaml`
**Workaround**: Manually edit `config.yaml` to use `claude-3-5-sonnet-20240620`
**Fix planned**: v1.1.8 will auto-detect and update

### 2. Prompts Metadata Not Updated
**Issue**: `prompts/*.md` metadata blocks don't include `project_type` selection step
**Workaround**: Follow CLAUDE.md instructions (override metadata)
**Fix planned**: v1.2.0 will update all prompt metadata

---

## 🚀 What's Next (v1.2.0)

Planned improvements based on this release:

1. **Prompts Metadata Enhancement**
   - Add `project_type` selection to `prompts/01_research_domain_setup.md`
   - Update `conversation_flow` to include selection step
   - Sync metadata with CLAUDE.md instructions

2. **Config Validation**
   - Auto-detect invalid Claude model names
   - Suggest corrections in real-time
   - Add `scholarag validate` command

3. **Interactive Project Type Wizard**
   - CLI interactive mode with explanations
   - Visual comparison of 50% vs 90% thresholds
   - Sample paper count estimator

---

## 💡 Key Takeaways

### 1. Workflow Transparency
✅ Researchers now have **clear mental model** of Stage 1-3 logic

### 2. User Agency
✅ `project_type` is a **conscious choice**, not a hidden default

### 3. Technical Robustness
✅ Environment variables load reliably from project directories

---

## 📞 Support

### Questions?
- Discussion: https://github.com/HosungYou/ScholaRAG/discussions
- Issues: https://github.com/HosungYou/ScholaRAG/issues

### Found Bugs?
Please report with:
- ScholaRAG version (`v1.1.7`)
- Steps to reproduce
- Expected vs actual behavior

---

**Bottom Line**: v1.1.7 fixes critical workflow misunderstandings and ensures researchers have **full visibility and control** over their systematic review process.
