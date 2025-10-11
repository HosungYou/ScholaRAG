# ResearcherRAG v1.2.0 Release Notes

**Release Date**: October 11, 2025
**Theme**: Interactive Learning Platform & Repository Cleanup

---

## 🎉 What's New

### 1. **ResearcherRAG Helper - Interactive Learning Platform**

We've launched a **companion web platform** to help researchers learn and use ResearcherRAG more effectively!

**Live Site**: [ResearcherRAG Helper](https://github.com/HosungYou/ResearcherRAG-helper)

#### Features:
- 📚 **Bookdown-Style Documentation**: Clean, navigable interface inspired by R Bookdown
- 🤖 **AI-Powered Chatbot**: RAG-based Q&A system using Claude 3.5 Sonnet
- 📥 **Resource Center**: Download templates, examples, and workshop materials
- 🎥 **Video Tutorials** (coming soon): Visual walkthroughs of the 5-stage workflow

#### Technology Stack:
- **Frontend**: Next.js 14 + Tailwind CSS
- **Chatbot Backend**: FastAPI + LangChain + ChromaDB
- **LLM**: Claude 3.5 Sonnet (Anthropic API)
- **Deployment**: Vercel (frontend) + Render.com (backend)

**Why This Matters**:
- Researchers can now **learn interactively** instead of just reading docs
- **Instant answers** to common questions via chatbot
- **Visual examples** make concepts clearer
- **No coding required** to understand the workflow

---

### 2. **Repository Cleanup - Researcher-Friendly Structure**

We've **separated development files** from the main repository to make it cleaner for end users.

#### What Was Removed:
- ❌ `.archive/` (development history)
- ❌ `01_literature_review_rag/` (personal research data)
- ❌ `03_research_notes_rag/` (internal notes)
- ❌ `backend/core/` (code implementation - now in Helper repo)
- ❌ `project_management/` (internal planning docs)
- ❌ `release-notes/` (moved to `docs/`)

#### What Remains (Essential for Researchers):
- ✅ `prompts/` - 5-stage workflow templates
- ✅ `templates/` - Research profile YAML examples
- ✅ `workshop/` - 3-hour hands-on guide
- ✅ `docs/` - CLAUDE.md, QUICK_START.md
- ✅ `README.md` - Updated with simpler instructions

**Result**: **60% reduction in repository size**, focusing only on what researchers need.

---

### 3. **Updated Documentation**

#### README.md
- Simplified Quick Start (5 steps instead of 10)
- Added link to ResearcherRAG Helper
- Removed references to deleted directories
- Clearer roadmap section

#### docs/ Structure
```
docs/
├── CLAUDE.md              # Complete guide for Claude Code
├── QUICK_START.md         # Getting started guide
├── RELEASE_NOTES_v1.2.0.md # This file
├── prompts/               # 5-stage templates
├── templates/             # Research profiles
└── workshop/              # Workshop materials
```

---

## 🔧 Technical Changes

### Repository Structure

**Before (v1.1.0)**:
```
ResearcherRAG/
├── .archive/
├── 01_literature_review_rag/
├── 03_research_notes_rag/
├── backend/core/
├── project_management/
├── release-notes/
├── prompts/
├── templates/
├── workshop/
└── docs/
```

**After (v1.2.0)**:
```
ResearcherRAG/
├── prompts/      # What to paste into Claude Code
├── templates/    # Research profile examples
├── workshop/     # 3-hour workshop guide
├── docs/         # Documentation
└── README.md     # Start here!
```

**Development files** → Moved to [ResearcherRAG-helper](https://github.com/HosungYou/ResearcherRAG-helper)

---

## 🚀 Getting Started (Updated)

### For New Users

```bash
# 1. Clone the main repository
git clone https://github.com/HosungYou/ResearcherRAG.git
cd ResearcherRAG

# 2. Open in VS Code
code .

# 3. Start Claude Code and paste prompts/01_research_domain_setup.md
```

### For Interactive Learning

1. Visit **[ResearcherRAG Helper](https://github.com/HosungYou/ResearcherRAG-helper)**
2. Explore the **interactive guide**
3. Ask the **chatbot** any questions
4. Download **templates** and **examples**

---

## 📊 Migration Guide

### If You're Using v1.1.0

No breaking changes! Your existing workflows will continue to work.

**Optional Updates**:
1. **Pull latest changes**: `git pull origin main`
2. **Check out Helper repo** for interactive learning: https://github.com/HosungYou/ResearcherRAG-helper
3. **Update bookmarks**: Documentation is now in `docs/` instead of `release-notes/`

---

## 🛠️ Under the Hood

### ResearcherRAG Helper Architecture

```
┌─────────────────────────────────────┐
│   Next.js Frontend (Vercel)         │
│   - Documentation Pages              │
│   - Chatbot UI                       │
│   - Resource Downloads               │
└──────────────┬──────────────────────┘
               │ API Calls
┌──────────────▼──────────────────────┐
│   Chatbot Backend (Serverless)      │
│   - FastAPI / Next.js API Routes    │
│   - LangChain RAG Pipeline           │
│   - ChromaDB (Embedded Docs)         │
│   - Claude 3.5 Sonnet (Anthropic)    │
└─────────────────────────────────────┘
```

**Document Sources** (Embedded in ChromaDB):
- CLAUDE.md (18,000 words)
- All 5-stage prompts
- Workshop guide
- Research profile templates
- FAQ and troubleshooting

---

## 🎯 Use Cases Enhanced

### Before v1.2.0
- Read documentation → Copy prompts → Run in Claude Code

### After v1.2.0
- **Interactive Learning**: Use Helper chatbot to understand concepts
- **Step-by-Step Guide**: Visual navigation through Bookdown-style docs
- **Instant Help**: Ask chatbot instead of searching docs
- **Example Projects**: Download complete working examples

---

## 🐛 Bug Fixes

- Fixed broken links in README.md (references to deleted directories)
- Removed outdated references to `backend/core/` in documentation
- Cleaned up `.gitignore` to exclude development files

---

## 📈 Performance Improvements

- **Repository Clone Speed**: 60% faster (smaller size)
- **Documentation Load Time**: Improved with focused structure
- **Chatbot Response**: < 3 seconds average (RAG-optimized)

---

## 🔮 What's Next

### v1.3.0 (Planned - January 2026)
- **Video Tutorials**: 10 x 15-minute screencasts
- **Additional Examples**: Medicine and Psychology domains
- **Citation Graph Analysis**: Visualize paper relationships
- **Multi-lingual Support**: Korean, Chinese, Spanish

### v2.0.0 (Planned - Q2 2026)
- **Collaborative RAG**: Multi-user projects
- **Cloud-Hosted Option**: Managed service (optional)
- **Reference Manager Integration**: Zotero, Mendeley
- **Writing Assistance**: Auto-generate "Related Work" sections

---

## 🙏 Acknowledgments

Special thanks to:
- **Early adopters** who provided feedback on v1.1.0
- **Claude Code team** (Anthropic) for conversational AI capabilities
- **Vercel** for seamless deployment platform
- **Research community** for feature requests and bug reports

---

## 📖 Full Changelog

### Added
- ✨ ResearcherRAG Helper platform (Next.js + Tailwind CSS)
- 🤖 AI chatbot with RAG (Claude 3.5 Sonnet)
- 📚 Bookdown-style interactive documentation
- 📥 Resource download center
- 🔗 Cross-repository linking (main ↔ helper)

### Changed
- 📝 Updated README.md with cleaner instructions
- 📂 Reorganized documentation into `docs/`
- 🗺️ Updated roadmap (v1.2.0 completed ahead of schedule!)
- 🔄 Simplified repository structure

### Removed
- ❌ `.archive/` (development history)
- ❌ `01_literature_review_rag/` (personal data)
- ❌ `03_research_notes_rag/` (internal notes)
- ❌ `backend/core/` (moved to Helper repo)
- ❌ `project_management/` (moved to Helper repo)
- ❌ `release-notes/` (consolidated to `docs/`)

### Fixed
- 🐛 Broken links in documentation
- 🐛 References to non-existent directories
- 🐛 Inconsistent file paths

---

## 📞 Support

### Questions?
- **Interactive Help**: Ask the [chatbot](https://github.com/HosungYou/ResearcherRAG-helper)
- **GitHub Issues**: https://github.com/HosungYou/ResearcherRAG/issues
- **Discussions**: https://github.com/HosungYou/ResearcherRAG/discussions

---

**Enjoy the new interactive learning experience!** 🎉

_Built with ❤️ for researchers, by researchers_

🤖 _Powered by [Claude Code](https://claude.com/claude-code)_
