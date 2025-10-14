# Expected Statistics Report

This document shows the **expected results** when running the full ResearcherRAG pipeline on the "AI Chatbots for Language Learning" example project.

Use this to validate that your pipeline is working correctly.

---

## PRISMA Flow Statistics

### Stage 1: Identification

| Database | Expected Records | Actual |
|----------|------------------|--------|
| Semantic Scholar | 210 ± 30 | _____ |
| OpenAlex | 175 ± 25 | _____ |
| arXiv | 18 ± 5 | _____ |
| **Total Identified** | **403 ± 50** | **_____** |

**Validation**: Total should be between 350-450 papers.

---

### Stage 2: Deduplication

| Metric | Expected | Actual |
|--------|----------|--------|
| Records after deduplication | 301 ± 30 | _____ |
| Duplicates removed | 102 ± 20 | _____ |
| Deduplication rate | 25% ± 5% | _____ |

**Breakdown of duplicates:**
- By DOI (exact match): ~45 papers (44%)
- By arXiv ID: ~5 papers (5%)
- By title similarity (≥85%): ~52 papers (51%)

**Validation**: Deduplication rate should be 20-30%.

---

### Stage 3: Screening

| Metric | Expected | Actual |
|--------|----------|--------|
| Records screened | 301 ± 30 | _____ |
| Relevant papers | 79 ± 15 | _____ |
| Excluded papers | 222 ± 40 | _____ |
| Relevance rate | 26% ± 5% | _____ |

**Confidence levels:**
- High confidence: ~50 papers (63%)
- Medium confidence: ~25 papers (32%)
- Low confidence: ~4 papers (5%)

**Common exclusion reasons:**
1. "No speaking component" (40% of exclusions)
2. "Non-empirical study" (30%)
3. "Off-topic (not language learning)" (20%)
4. "Insufficient abstract information" (10%)

**Validation**: Relevance rate should be 20-35% for well-defined research questions.

---

### Stage 4: Eligibility (PDF Retrieval)

| Metric | Expected | Actual |
|--------|----------|--------|
| Reports sought | 79 ± 15 | _____ |
| PDFs downloaded | 45 ± 10 | _____ |
| PDFs unavailable | 34 ± 10 | _____ |
| Download success rate | 57% ± 10% | _____ |

**Failure reasons:**
| Reason | Expected Count | % of Failures |
|--------|----------------|---------------|
| Paywalled | ~20 | 59% |
| 404 Not Found | ~10 | 29% |
| Timeout | ~4 | 12% |

**PDF availability by database:**
- Semantic Scholar: ~40% success
- OpenAlex: ~55% success
- arXiv: ~100% success

**Validation**: 50-65% success rate is typical for mixed-database searches.

---

### Stage 5: Included

| Metric | Expected | Actual |
|--------|----------|--------|
| Studies included in review | 45 ± 10 | _____ |
| Total chunks generated | 850 ± 150 | _____ |
| Avg chunks per paper | 19 ± 3 | _____ |
| Vector database size | 120 MB ± 30 MB | _____ |

**Validation**:
- Chunks per paper should be 15-25 (chunk_size=1000, typical paper ~20-30 pages)
- Database size should be ~2-4 MB per paper

---

## Overall Statistics

| Metric | Expected | Actual |
|--------|----------|--------|
| Total identified | 403 papers | _____ |
| Final included | 45 papers | _____ |
| Overall inclusion rate | 11% | _____ |
| Screening precision | 26% | _____ |
| PDF retrieval success | 57% | _____ |

**Funnel conversion rates:**
- Identification → Deduplication: 75% retained
- Deduplication → Screening: 26% retained
- Screening → PDF: 57% retained
- **Overall: 11% of identified papers included in final review**

---

## Content Quality Validation

### Expected Themes in Final Dataset

If your RAG system is working correctly, queries should reveal these themes:

#### Theme 1: Speaking Skill Improvements
**Expected prevalence**: ~90% of papers

**Sub-themes:**
- Pronunciation accuracy (60% of papers)
- Fluency development (45%)
- Vocabulary acquisition (40%)
- Grammar accuracy (35%)

**Sample papers expected:**
- "Effects of AI chatbot on speaking anxiety and proficiency"
- "Chatbot-assisted pronunciation training for ESL learners"

#### Theme 2: Learner Engagement & Motivation
**Expected prevalence**: ~70% of papers

**Sub-themes:**
- Reduced speaking anxiety (50%)
- Increased practice frequency (45%)
- Learner enjoyment/satisfaction (60%)
- Willingness to communicate (30%)

#### Theme 3: System Design Features
**Expected prevalence**: ~80% of papers

**Sub-themes:**
- Feedback mechanisms (70%)
- Speech recognition technology (65%)
- Conversational design (50%)
- Personalization/adaptation (40%)

#### Theme 4: Comparative Studies
**Expected prevalence**: ~40% of papers

**Comparisons found:**
- Chatbot vs. human tutor (25%)
- Chatbot vs. no-treatment control (60%)
- Different chatbot designs (15%)

#### Theme 5: Methodologies
**Expected prevalence**: 100%

**Methods distribution:**
- Quantitative (pre/post-test): 55%
- Mixed methods: 30%
- Qualitative (interviews/surveys): 15%

**Measures used:**
- Standardized tests (IELTS, TOEFL): 30%
- Custom speaking tests: 50%
- Self-report surveys: 70%
- Conversation analysis: 20%

---

## Query Response Quality Checks

### Test Query 1: "What are the main benefits of chatbots?"

**Expected answer should include:**
- ✅ Reduced speaking anxiety
- ✅ Increased practice opportunities
- ✅ Immediate feedback
- ✅ 24/7 availability
- ✅ Personalized learning

**Expected citations:** 5-8 papers

**Expected response length:** 400-600 words

### Test Query 2: "What methodologies are used?"

**Expected answer should include:**
- ✅ Pre/post-test designs (most common)
- ✅ Control group comparisons
- ✅ Mixed methods approaches
- ✅ Learner surveys/interviews
- ✅ Specific assessment tools mentioned

**Expected citations:** 8-12 papers

### Test Query 3: "What are the limitations?"

**Expected answer should include:**
- ✅ Technical limitations (speech recognition errors)
- ✅ Limited conversational depth
- ✅ Cultural context gaps
- ✅ Teacher replacement concerns
- ✅ Need for human interaction

**Expected citations:** 4-6 papers

---

## Technical Performance Benchmarks

### Embedding Generation
- **Speed**: ~500 papers/minute (local CPU)
- **Memory**: ~2GB RAM peak
- **Time for 45 papers**: ~1-2 minutes

### Vector Search Performance
- **Query time**: <100ms for k=10
- **Accuracy**: Top-5 should be relevant for specific queries
- **Consistency**: Same query should return same top-3 results

### Claude API Performance
- **Screening**: ~3-5 seconds per paper
- **RAG queries**: ~5-10 seconds per query
- **Token usage**:
  - Screening: ~500 tokens input, ~100 output per paper
  - RAG query: ~2000 tokens input, ~600 output per query

---

## Cost Validation

### Expected API Costs

| Stage | Expected Cost | Actual |
|-------|---------------|--------|
| Screening (301 papers) | $3.61 | $_____ |
| Screening output | $0.45 | $_____ |
| RAG queries (100 queries) | $6.00 | $_____ |
| RAG outputs (100 responses) | $9.00 | $_____ |
| **Total Claude API** | **$19.06** | **$_____** |

**Validation**:
- If cost is 50% higher: Check if you're using correct model (should be claude-3-5-sonnet)
- If cost is 50% lower: Check if all stages completed successfully

### Time Validation

| Stage | Expected Time | Actual |
|-------|---------------|--------|
| Paper fetching | 15-20 min | _____ |
| Deduplication | 1-2 min | _____ |
| Screening | 30-60 min | _____ |
| PDF download | 20-40 min | _____ |
| RAG building | 10-15 min | _____ |
| 100 queries | 20-30 min | _____ |
| PRISMA diagram | <1 min | _____ |
| **Total** | **~2-3 hours** | **_____** |

---

## Troubleshooting Deviations

### If Total Papers <<< 403 (e.g., <300)

**Possible causes:**
1. API rate limiting kicked in
2. Internet connection issues
3. Query too specific

**Check:**
```bash
# Verify all 3 CSV files exist:
ls -lh data/01_identification/*.csv

# Check line counts:
wc -l data/01_identification/*.csv
```

### If Relevance Rate <<< 26% (e.g., <15%)

**Possible causes:**
1. Research question too narrow
2. Query retrieved off-topic papers
3. Claude screening too strict

**Fix:**
```bash
# Manually review a few excluded papers:
head -20 data/02_screening/excluded_papers.csv

# If they seem relevant, rerun with adjusted question
```

### If PDF Success Rate <<< 57% (e.g., <40%)

**Expected behavior** for some queries!

**Factors:**
- arXiv papers (if few): 100% success
- Older papers: Lower OA rate
- Non-CS topics: Lower OA rate

**Not a problem** unless <30% success rate.

### If RAG Queries Return Gibberish

**Possible causes:**
1. Embedding model failed to load
2. Vector database corrupted
3. PDFs were corrupted/unreadable

**Check:**
```bash
# Verify vector database exists:
ls -lh data/04_rag/chroma_db/

# Check if papers are readable:
pdftotext data/03_pdfs/0001_*.pdf - | head -100
```

---

## Success Criteria Checklist

Your ResearcherRAG pipeline is working correctly if:

### Data Quantity
- [ ] Total papers identified: 350-450
- [ ] Deduplication rate: 20-30%
- [ ] Relevance rate: 20-35%
- [ ] PDF success rate: 45-70%
- [ ] Final papers in RAG: 35-60

### Data Quality
- [ ] No exact duplicate titles in deduplicated.csv
- [ ] Relevant papers actually match research question
- [ ] Downloaded PDFs are readable (not corrupted)
- [ ] Chunks contain meaningful text (not garbled)

### RAG Performance
- [ ] Test query returns relevant results
- [ ] Citations are accurate (match source papers)
- [ ] Answer quality is coherent and well-reasoned
- [ ] No hallucinations (invented papers/facts)

### Cost & Time
- [ ] Total cost: $15-30
- [ ] Total time: 2-4 hours
- [ ] No API errors or failures

### Reproducibility
- [ ] Running same query twice gives same results
- [ ] PRISMA numbers match actual file counts
- [ ] All intermediate files exist and are non-empty

---

## Contact

If your results deviate significantly from these expectations:

1. **Check GitHub Issues**: [ResearcherRAG/issues](https://github.com/HosungYou/ResearcherRAG/issues)
2. **Review Logs**: Look for error messages in terminal output
3. **Report Bug**: Open issue with your statistics vs. expected

**Include in bug report:**
- All statistics from this checklist
- Error messages (if any)
- Your config.yaml
- Python version and OS

---

*Expected statistics generated from pilot run on 2025-10-13*
