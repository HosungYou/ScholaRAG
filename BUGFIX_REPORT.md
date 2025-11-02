# ScholaRAG Bug Fix Report

## Date: 2025-11-02
## Reporter: User Testing Session

---

## 🐛 Issues Found

### 1. **Semantic Scholar Complex Query Failure** (CRITICAL)

**Problem:**
- Boolean queries with 3+ AND parts return 0 results
- Even 2-part queries with many OR conditions fail
- Example failing query: `(AI OR ML OR ...[7 terms]) AND (risk OR bias OR ...[11 terms])`
- Test query that works: `(AI OR ML) AND risk` → 14,191 results

**Root Cause:**
- Semantic Scholar API has undocumented limitations on query complexity
- Too many OR conditions within parentheses cause query to fail silently
- Current simplification logic only removes 3rd AND part, doesn't optimize OR conditions

**Impact:**
- Users get 0 results from Semantic Scholar for complex systematic review queries
- Reduces paper coverage by 30-40% (Semantic Scholar has ~40% open access PDFs)

---

### 2. **API Key Loading Issue** (HIGH)

**Problem:**
- `load_dotenv()` fails to load .env file from project directory
- Script prompts for API key interactively even when .env exists
- Interactive prompt blocks automated workflows

**Root Cause:**
- `load_dotenv()` without explicit path doesn't check project subdirectories
- Missing `override=True` parameter allows system env vars to override project .env

**Impact:**
- Users must manually input API key every time
- API rate limits apply (100 req/5min instead of 1000 req/5min)
- Cannot run in automated/CI environments

**Current Fix:**
```python
# Before
load_dotenv(env_path)

# After
load_dotenv(env_path, override=True)
```

---

### 3. **Empty Results Error** (MEDIUM)

**Problem:**
- `print_summary()` crashes when DataFrame is empty
- Error: `KeyError: 'pdf_url'` when accessing non-existent column

**Root Cause:**
- Empty DataFrame doesn't have column structure
- Code assumes `pdf_url` column always exists

**Impact:**
- Script crashes instead of showing "0 papers found"
- Poor user experience for edge cases

**Current Fix:**
```python
# Check if column exists and has data
with_pdf = df['pdf_url'].notna().sum() if 'pdf_url' in df.columns and papers > 0 else 0
```

---

### 4. **Query Simplification Logic Incomplete** (HIGH)

**Problem:**
- Current implementation only removes 3rd AND part
- Doesn't optimize OR conditions (e.g., reducing 7 OR terms to 3)
- No fallback strategy when simplified query still fails

**Root Cause:**
- Naive string parsing approach
- No testing against Semantic Scholar API limits
- No progressive simplification strategy

**Impact:**
- Users still get 0 results after "simplification"
- False confidence that query was optimized

---

## ✅ Recommended Fixes

### Fix 1: Intelligent Query Optimizer for Semantic Scholar

**Strategy:**
1. Limit OR conditions to max 3-4 per group
2. Prioritize most important terms (by TF-IDF or user config)
3. Progressive simplification with validation
4. Fallback to multiple simple queries

**Implementation:**
```python
def _optimize_semantic_scholar_query(self, query: str) -> str:
    """
    Optimize complex queries for Semantic Scholar API.

    Rules:
    - Max 2 AND-separated parts
    - Max 3-4 OR conditions per part
    - Prioritize core terms
    """
    # Parse query
    # Limit OR terms
    # Test with API
    # Fallback if needed
```

---

### Fix 2: Robust API Key Loading

**Changes:**
1. Use `override=True` in `load_dotenv()`
2. Check environment variable after loading
3. Add debug logging (optional via --verbose flag)
4. Support multiple .env locations (project root, user home)

---

### Fix 3: Comprehensive Error Handling

**Changes:**
1. Handle empty DataFrames gracefully
2. Validate column existence before access
3. Provide informative error messages
4. Log errors to file for debugging

---

### Fix 4: Progressive Query Simplification

**Strategy:**
1. Try full query first
2. If 0 results, simplify and retry (up to 3 attempts)
3. Warn user about simplifications
4. Suggest manual query refinement if all attempts fail

---

## 📊 Testing Plan

1. **Unit Tests:**
   - Test query parser with complex Boolean queries
   - Test API key loading from different locations
   - Test empty DataFrame handling

2. **Integration Tests:**
   - Test full workflow with complex queries
   - Test with/without API keys
   - Test edge cases (no results, API errors)

3. **User Acceptance Tests:**
   - Run with real systematic review queries
   - Verify papers retrieved match expectations
   - Check error messages are helpful

---

## 🚀 Priority Order

1. **HIGH**: Fix Semantic Scholar query optimizer (biggest impact)
2. **HIGH**: Fix API key loading (usability issue)
3. **MEDIUM**: Fix empty results error (edge case)
4. **LOW**: Add comprehensive logging (developer experience)

---

## 📝 Notes

- All fixes should maintain backward compatibility
- Add deprecation warnings if changing API
- Update documentation and examples
- Consider adding `--dry-run` flag for testing queries
