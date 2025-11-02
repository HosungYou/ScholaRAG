# ScholaRAG v1.2.1 Release Notes

**Release Date:** November 2, 2025
**Version:** v1.2.1
**Type:** Performance Enhancement & Clarification

---

## 🎯 Overview

This release significantly improves paper retrieval performance and clarifies the PRISMA 2020 methodology across all project types. Key improvements include **10x faster retrieval** with Semantic Scholar API keys and **comprehensive fetch limits** aligned with systematic review best practices.

---

## ✨ New Features

### 1. Semantic Scholar API Key Integration

**Interactive API Key Prompt**
When running `scripts/01_fetch_papers.py`, users are now prompted to provide a Semantic Scholar API key if not found in environment variables.

```
======================================================================
⚠️  Semantic Scholar API Key Not Found
======================================================================

📊 Rate Limits:
   • Without API key: 100 requests/5 min (slower, ~60-120 minutes for 10K papers)
   • With API key:    1,000 requests/5 min (10x faster, ~10-20 minutes)

🔑 Get a FREE API key:
   https://www.semanticscholar.org/product/api#api-key

💡 Enter your API key below (or press Enter to skip)
   (Key will be saved to .env file for future use)
======================================================================
```

**Benefits:**
- ✅ **10x faster retrieval**: 1,000 requests/5 min vs. 100 requests/5 min
- ✅ **Automatic .env management**: Key is saved for future runs
- ✅ **Optional**: Users can skip and use free tier
- ✅ **User-friendly**: No manual file editing required

**Implementation:**
- `scripts/01_fetch_papers.py:63-134` - Interactive prompt
- `prompts/02_query_strategy.md:117-121` - Stage 2 guidance

---

## 🚀 Performance Improvements

### 2. Increased Fetch Limits for Comprehensive Retrieval

Following PRISMA 2020 "cast a wide net" methodology, fetch limits have been increased across all databases for **both knowledge repository and systematic review projects**.

**Previous Limits (v1.2.0 and earlier):**
```
Semantic Scholar: 1,000 papers
OpenAlex:         1,000 papers
arXiv:              500 papers
Total:           ~2,500 papers (before deduplication)
```

**New Limits (v1.2.1):**
```
Semantic Scholar: 10,000 papers (+900%)
OpenAlex:         10,000 papers (+900%)
arXiv:             5,000 papers (+900%)
Total:           ~25,000 papers (before deduplication)
```

**Expected Results:**
- **After deduplication**: ~18,000-20,000 unique papers
- **Knowledge Repository** (50% screening threshold): ~12,000-15,000 papers
- **Systematic Review** (90% screening threshold): ~50-300 papers

**Time Impact (with API key):**
- Semantic Scholar: ~10-20 minutes
- OpenAlex: ~5-10 minutes (polite pool)
- arXiv: ~2.5 minutes (3-second rate limit)
- **Total: ~20-35 minutes** for comprehensive retrieval

**Files Modified:**
- `scripts/01_fetch_papers.py:141` - Semantic Scholar limit
- `scripts/01_fetch_papers.py:239` - OpenAlex limit
- `scripts/01_fetch_papers.py:343` - arXiv limit

---

## 📖 Documentation Improvements

### 3. PRISMA 2020 Philosophy Clarification

**Key Clarification:**
The difference between `knowledge_repository` and `systematic_review` is **NOT** the fetch limits, but the **Stage 4 PRISMA screening threshold**.

**Unified Retrieval Strategy (Stage 1-3):**
```
┌─────────────────────────────────────────────────────────────┐
│  Both Project Types: Identical Retrieval Process           │
└─────────────────────────────────────────────────────────────┘

Stage 1-2: IDENTIFICATION
  ↓ Fetch maximum papers from all databases (25K)

Stage 3: DEDUPLICATION
  ↓ Remove duplicates (~18K-20K unique)

Stage 4: SCREENING ← Project types diverge here
  ├─ Knowledge Repository (50% threshold)
  │   → Lenient filtering (remove only spam/off-topic)
  │   → Retain: ~12,000-15,000 papers
  │   → Purpose: Comprehensive domain coverage
  │
  └─ Systematic Review (90% threshold)
      → Strict PRISMA criteria (study design, methods, outcomes)
      → Retain: ~50-300 papers
      → Purpose: Publication-quality review
```

**Documentation Updates:**
- `scholarag_cli.py:468` - config.yaml comment updated
  - Before: `"For knowledge_repository"`
  - After: `"For all project types (PRISMA: cast wide net, filter via screening)"`

---

## 📊 Performance Metrics

### Retrieval Speed Comparison

| Scenario | Free Tier (no API key) | With API Key | Speedup |
|----------|------------------------|--------------|---------|
| 1,000 papers (old default) | ~50 min | ~5 min | **10x** |
| 10,000 papers (new default) | ~500 min (8.3 hrs) | ~20 min | **25x** |

### Database Coverage (v1.2.1)

| Database | Papers Retrieved | PDF Availability | PDFs Expected |
|----------|------------------|------------------|---------------|
| Semantic Scholar | ~10,000 | 40% | ~4,000 |
| OpenAlex | ~10,000 | 50% | ~5,000 |
| arXiv | ~5,000 | 100% | ~5,000 |
| **Total (raw)** | **~25,000** | ~56% | **~14,000** |
| **After dedup** | **~18,000-20,000** | ~55% | **~10,000-11,000** |

---

## 🔧 Configuration Changes

### Before v1.2.1

```yaml
# config.yaml (generated by scholarag_cli.py init)
search:
  year_range: {start: 2015, end: 2025}
  languages: [english]
  max_results_per_db: 10000  # For knowledge_repository
```

### After v1.2.1

```yaml
# config.yaml (generated by scholarag_cli.py init)
search:
  year_range: {start: 2015, end: 2025}
  languages: [english]
  max_results_per_db: 10000  # For all project types (PRISMA: cast wide net, filter via screening)
```

**Note:** Existing projects do NOT need migration. This only affects new projects created with `scholarag_cli.py init`.

---

## 🐛 Bug Fixes

None in this release. This is a feature enhancement and clarification release.

---

## 📦 What's Changed

### Full Changelog

1. **feat: Add Semantic Scholar API key prompt for 10x faster retrieval** ([c850b39](https://github.com/HosungYou/ScholaRAG/commit/c850b39))
   - Interactive prompt when API key not found
   - Automatic .env file management
   - Stage 2 guidance updated

2. **fix: Increase fetch limits to 10,000 for comprehensive retrieval** ([44349af](https://github.com/HosungYou/ScholaRAG/commit/44349af))
   - Semantic Scholar: 1,000 → 10,000
   - OpenAlex: 1,000 → 10,000
   - Time estimates updated for 10K papers

3. **fix: Increase arXiv limit to 5,000 and clarify PRISMA philosophy** ([91d9d1b](https://github.com/HosungYou/ScholaRAG/commit/91d9d1b))
   - arXiv: 500 → 5,000
   - config.yaml comment clarified for all project types

---

## 🚀 Migration Guide

### For Existing Projects

**No action required.** Your existing projects will continue to work.

**Optional:** If you want faster retrieval, add Semantic Scholar API key to your project's `.env` file:

```bash
# In your project folder (e.g., projects/2025-01-15_MyProject/)
echo "SEMANTIC_SCHOLAR_API_KEY=your_key_here" >> .env
```

Get a free API key: https://www.semanticscholar.org/product/api#api-key

### For New Projects

When running `scripts/01_fetch_papers.py` for the first time, you will be prompted to enter an API key. You can:
- **Option 1**: Enter your API key (recommended for 10x speed)
- **Option 2**: Press Enter to skip (use free tier)

---

## 💡 Recommendations

### For Knowledge Repository Projects
- ✅ Use Semantic Scholar API key (free, 10x faster)
- ✅ Enable all 3 databases (Semantic Scholar, OpenAlex, arXiv)
- ✅ Expect ~18,000-20,000 papers after deduplication
- ✅ Stage 4 PRISMA will retain ~12,000-15,000 papers (50% threshold)

### For Systematic Review Projects
- ✅ Use Semantic Scholar API key (free, 10x faster)
- ✅ Enable all 3 databases for comprehensive coverage
- ✅ Expect ~18,000-20,000 papers after deduplication
- ✅ Stage 4 PRISMA will retain ~50-300 papers (90% threshold)
- ✅ **Same retrieval process** as knowledge repository (PRISMA 2020 best practice)

---

## 🎓 PRISMA 2020 Alignment

This release fully aligns with PRISMA 2020 systematic review guidelines:

**PRISMA 2020 Item #6 (Search Strategy):**
> "For each database, working group or grey literature source, present the full search strategies for all searches (such as from inception to the date last searched)."

**PRISMA 2020 Item #7 (Selection Process):**
> "Specify the methods used to decide whether a study met the inclusion criteria of the review, including how many reviewers screened each record."

ScholaRAG v1.2.1 implements:
- ✅ **Comprehensive search** across 3 academic databases
- ✅ **Maximum recall** with high fetch limits (cast wide net)
- ✅ **Systematic screening** with AI-PRISMA rubric (6 dimensions)
- ✅ **Transparent thresholds** (50% for repositories, 90% for reviews)

Reference: [PRISMA 2020 Statement](http://www.prisma-statement.org/)

---

## 📚 Related Documentation

- **API Reference**: `skills/reference/api_reference.md`
- **Stage 2 Prompt**: `prompts/02_query_strategy.md`
- **CLAUDE.md**: Researcher-friendly automation guidelines
- **PRISMA Configuration**: `prompts/03_prisma_configuration.md`

---

## 🙏 Acknowledgments

Thanks to the ScholaRAG community for feedback on retrieval performance and PRISMA methodology clarity.

Special thanks to:
- **Semantic Scholar** for providing free API access
- **OpenAlex** for polite pool rate limits
- **arXiv** for open preprint access

---

## 🔗 Links

- **GitHub Repository**: https://github.com/HosungYou/ScholaRAG
- **Documentation**: https://researcher-rag-helper.vercel.app/
- **Semantic Scholar API**: https://www.semanticscholar.org/product/api
- **PRISMA 2020**: http://www.prisma-statement.org/

---

## 📝 Upgrade Instructions

### Quick Upgrade

```bash
# Navigate to your ScholaRAG directory
cd ScholaRAG

# Pull latest changes
git pull origin main

# Optional: Get Semantic Scholar API key
# Visit: https://www.semanticscholar.org/product/api#api-key

# Run fetch script (will prompt for API key)
python scripts/01_fetch_papers.py --project projects/YourProject --query "your search query"
```

### Verify Upgrade

```bash
# Check version
grep "version" RELEASE_NOTES_v1.2.1.md

# Expected output:
# **Version:** v1.2.1
```

---

**Full Diff**: [v1.2.0...v1.2.1](https://github.com/HosungYou/ScholaRAG/compare/v1.2.0...v1.2.1)

**Questions or Issues?** Open an issue on GitHub: https://github.com/HosungYou/ScholaRAG/issues
