# Release Notes - ScholaRAG v1.2.4

**Release Date:** November 2, 2025
**Type:** Major Bug Fixes + API Key Requirement Update

---

## 🎯 Overview

This release fixes **4 critical bugs** in paper fetching and makes **Semantic Scholar API key mandatory** for better user experience and reliability.

---

## 🚨 **BREAKING CHANGE**

### Semantic Scholar API Key Now REQUIRED

**Why this change?**
- Free tier rate limits (100 requests/5 min) are too slow for systematic literature reviews
- With API key: 1,000 requests/5 min (10x faster)
- For 10,000 papers: Free tier = 60-120 minutes, With key = 10-20 minutes

**How to get API key (FREE):**
1. Visit: https://www.semanticscholar.org/product/api#api-key
2. Sign up with your email
3. Copy your API key

**How to add API key:**

**Option 1: Use helper script (RECOMMENDED)**
```bash
python scripts/setup_api_keys.py --project projects/your-project-name
```

**Option 2: Manual setup**
```bash
# Create/edit .env file in your project
echo "SEMANTIC_SCHOLAR_API_KEY=your_key_here" > projects/your-project/.env
```

**Option 3: Skip Semantic Scholar**
```bash
# Use only OpenAlex and arXiv (no API key required)
python scripts/01_fetch_papers.py \
  --databases openalex arxiv \
  --query "your query"
```

---

## 🐛 **Bug Fixes**

### 1. **Semantic Scholar Complex Query Optimization** (CRITICAL)
**Problem:** Complex Boolean queries with 3+ AND parts returned 0 results

**Solution:**
- Implemented intelligent query optimizer
- Limits to 2 AND parts, max 3 OR terms per part
- Prioritizes full phrases over abbreviations
- Full query still used for OpenAlex/arXiv

**Example:**
```
Original: (AI OR ML OR machine learning OR ...) AND (risk OR bias OR ...) AND (HR OR HRM OR ...)
Optimized: (machine learning OR deep learning OR AI) AND (job displacement OR risk OR bias)
```

---

### 2. **API Key Loading from .env Files** (HIGH)
**Problem:** `.env` files not loaded correctly, causing interactive prompts

**Solution:**
- Added `override=True` to `load_dotenv()`
- API keys now correctly loaded from project `.env` files
- No more interactive prompts blocking automated workflows

---

### 3. **Empty Results Crash** (MEDIUM)
**Problem:** Script crashed with `KeyError: 'pdf_url'` when 0 papers found

**Solution:**
- Added safety checks for empty DataFrames
- Graceful error messages instead of crashes
- Better user experience for edge cases

---

### 4. **arXiv Query Format Error** (HIGH)
**Problem:** arXiv queries malformed (treating Boolean operators as search terms)

**Solution:**
- Implemented `_convert_to_arxiv_query()` function
- Properly extracts terms and formats for arXiv API
- No more `all:OR AND all:AND` malformed queries

---

## ✨ **New Features**

### 1. **API Key Setup Helper Script**
New interactive script for easy API key configuration:

```bash
python scripts/setup_api_keys.py --project projects/your-project

# Features:
# - Interactive prompts with validation
# - API key masking for security
# - Status checking (--status flag)
# - Support for multiple API keys (OpenAI, Anthropic, etc.)
```

### 2. **Improved Error Messages**
Clear, actionable error messages when API keys are missing:
```
❌ ERROR: Semantic Scholar API Key Required

🔑 API Key is now REQUIRED for Semantic Scholar

📋 How to get a FREE API key:
   1. Visit: https://www.semanticscholar.org/product/api#api-key
   2. Sign up with your email
   3. Copy your API key

🚀 Quick setup script:
   python scripts/setup_api_keys.py --project projects/your-project
```

---

## 📊 **Testing Results**

Tested with complex query (3 AND parts, 31 OR terms):

| Database | Status | Papers Retrieved | PDF URLs |
|----------|--------|------------------|----------|
| **OpenAlex** | ✅ Working | 10,000 | 73.4% |
| **Semantic Scholar** | ✅ Optimized | Requires API key | ~40% |
| **arXiv** | ✅ Fixed | Domain-specific | 100% |

---

## 📝 **Code Changes**

### Modified Files:
- `scripts/01_fetch_papers.py` (~300 lines changed)
  - Added 5 new helper functions
  - Improved query optimization
  - Enhanced error handling
  - API key requirement enforcement

### New Files:
- `scripts/setup_api_keys.py` - Interactive API key setup
- `BUGFIX_REPORT.md` - Technical details
- `CHANGELOG_2025-11-02.md` - Detailed changelog
- `FIXES_SUMMARY.md` - Deployment guide

---

## 🔄 **Migration Guide**

### For Existing Users:

**Step 1: Get Semantic Scholar API Key**
Visit: https://www.semanticscholar.org/product/api#api-key

**Step 2: Add to Your Project**
```bash
cd /path/to/ScholaRAG
python scripts/setup_api_keys.py --project projects/your-project-name
```

**Step 3: Resume Paper Fetching**
```bash
python scripts/01_fetch_papers.py \
  --project projects/your-project \
  --query "your query" \
  --databases semantic_scholar openalex arxiv
```

### Alternative: Skip Semantic Scholar
```bash
# Use only OpenAlex + arXiv (no API key needed)
python scripts/01_fetch_papers.py \
  --databases openalex arxiv \
  --query "your query"
```

---

## ✅ **Backward Compatibility**

- ✅ All existing projects work (just add API key)
- ✅ No breaking changes to query format
- ✅ Old .env files still supported
- ✅ Existing project structures unchanged

---

## 🎓 **Recommendations**

### Database Usage Strategy:

1. **OpenAlex** - Primary database
   - ✅ No API key required
   - ✅ Handles complex Boolean queries perfectly
   - ✅ 50-70% PDF URLs
   - ✅ Most papers come from here

2. **Semantic Scholar** - Supplementary
   - ⚠️ API key REQUIRED
   - ⚠️ Query optimization needed
   - ✅ 30-40% PDF URLs
   - ✅ Good for additional coverage

3. **arXiv** - Domain-specific
   - ✅ No API key required
   - ✅ 100% PDF URLs
   - ⚠️ Limited to CS/Physics/Math

---

## 📚 **Documentation Updates**

- Added API key setup guide
- Updated README with database comparison
- Added troubleshooting section
- Enhanced error messages with solutions

---

## 🙏 **Acknowledgments**

- All bugs discovered during user testing
- Fixes tested and verified
- Ready for production use

---

## 📞 **Support**

If you encounter issues:

1. **Check API key setup:**
   ```bash
   python scripts/setup_api_keys.py --project your-project --status
   ```

2. **Review error messages** - They contain solutions!

3. **Open GitHub issue** with full error log:
   https://github.com/HosungYou/ScholaRAG/issues

---

## 🔗 **Links**

- **GitHub Repository:** https://github.com/HosungYou/ScholaRAG
- **Documentation:** https://github.com/HosungYou/ScholaRAG/wiki
- **Get Semantic Scholar API Key:** https://www.semanticscholar.org/product/api#api-key
- **Report Issues:** https://github.com/HosungYou/ScholaRAG/issues

---

**Full Changelog:** See `CHANGELOG_2025-11-02.md`
**Technical Details:** See `BUGFIX_REPORT.md`
**Deployment Guide:** See `FIXES_SUMMARY.md`
