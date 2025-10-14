# Example Project: AI Chatbots for Language Learning Speaking Skills

This is a **complete example project** demonstrating the full ResearcherRAG workflow for conducting a systematic literature review.

**Research Question**: How do AI chatbots improve speaking skills in language learning, and what are the key factors contributing to their effectiveness?

---

## Quick Start

### Prerequisites
1. ✅ Claude API key configured in `.env`
2. ✅ Python 3.8+ with dependencies installed
3. ✅ ~4 hours of time
4. ✅ ~$15-25 budget for API costs

### Run Full Pipeline

```bash
# From ResearcherRAG root directory

# Stage 1: Fetch papers (15-20 minutes)
python scripts/01_fetch_papers.py \
  --project examples/ai-chatbots-language-learning \
  --query "chatbot language learning speaking"

# Stage 2: Deduplicate (1-2 minutes)
python scripts/02_deduplicate.py \
  --project examples/ai-chatbots-language-learning

# Stage 3: AI-assisted screening (30-60 minutes, $3-6)
python scripts/03_screen_papers.py \
  --project examples/ai-chatbots-language-learning \
  --question "How do AI chatbots improve speaking skills in language learning?"

# Stage 4: Download PDFs (20-40 minutes)
python scripts/04_download_pdfs.py \
  --project examples/ai-chatbots-language-learning

# Stage 5: Build RAG system (10-15 minutes)
python scripts/05_build_rag.py \
  --project examples/ai-chatbots-language-learning

# Stage 6: Interactive queries ($10-20 for 100-200 queries)
python scripts/06_query_rag.py \
  --project examples/ai-chatbots-language-learning \
  --interactive

# Stage 7: Generate PRISMA diagram (1 minute)
python scripts/07_generate_prisma.py \
  --project examples/ai-chatbots-language-learning
```

---

## Project Structure

After running the full pipeline, your directory will look like this:

```
examples/ai-chatbots-language-learning/
├── config.yaml                          # Project configuration
├── README.md                            # This file
│
├── data/
│   ├── 01_identification/              # Stage 1: Paper fetching
│   │   ├── semantic_scholar_results.csv (210 papers)
│   │   ├── openalex_results.csv        (175 papers)
│   │   ├── arxiv_results.csv           (18 papers)
│   │   └── deduplicated.csv            (301 papers after dedup)
│   │
│   ├── 02_screening/                   # Stage 2: AI screening
│   │   ├── relevant_papers.csv         (79 papers, 26% relevance)
│   │   ├── excluded_papers.csv         (222 papers)
│   │   └── screening_progress.csv
│   │
│   ├── 03_pdfs/                        # Stage 3: PDF downloads
│   │   ├── 0001_Chatbot_Language_Learning.pdf
│   │   ├── 0002_Speaking_Skills_AI.pdf
│   │   ├── ... (79 PDFs)
│   │   └── papers_metadata.csv
│   │
│   ├── 04_rag/                         # Stage 4: Vector database
│   │   ├── chroma_db/
│   │   │   ├── index/
│   │   │   ├── chroma.sqlite3
│   │   │   └── embeddings.parquet
│   │   └── rag_config.json
│   │
│   └── 05_analysis/                    # Stage 5: Query results
│       ├── query_session_20251013.json
│       └── query_session_20251013.md
│
└── outputs/                            # Stage 6: Final outputs
    ├── prisma_diagram.png
    ├── prisma_diagram.pdf
    ├── statistics_report.md
    └── statistics.json
```

---

## Expected Results

Based on our test run, you should see approximately:

### Stage 1: Identification
- **Semantic Scholar**: ~210 papers
- **OpenAlex**: ~175 papers
- **arXiv**: ~18 papers
- **Total identified**: ~403 papers

### Stage 2: Deduplication
- **After deduplication**: ~301 papers (25% duplicates)
- **Duplicates removed**: ~102 papers
  - By DOI: ~45
  - By arXiv ID: ~5
  - By title similarity: ~52

### Stage 3: Screening
- **Relevant papers**: ~79 (26% relevance rate)
- **Excluded papers**: ~222 (74%)
- **Screening confidence**:
  - High: ~50 papers (63%)
  - Medium: ~25 papers (32%)
  - Low: ~4 papers (5%)

### Stage 4: PDF Download
- **PDFs downloaded**: ~45 (57% success rate)
- **PDFs failed**: ~34 (43%)
- **Failure reasons**:
  - Paywalled: ~20
  - 404 Not Found: ~10
  - Timeout: ~4

### Stage 5: RAG Building
- **Papers in RAG**: ~45
- **Total chunks**: ~850 (avg 19 chunks/paper)
- **Vector database size**: ~120 MB

### Stage 6: Sample Queries

Try these queries in interactive mode:

```
1. "What are the main benefits of AI chatbots for speaking practice?"

Expected findings:
- Reduced speaking anxiety
- Increased practice time
- Immediate feedback
- Personalized learning

2. "What methodologies are used to evaluate chatbot effectiveness?"

Expected findings:
- Pre/post-test designs
- Speaking proficiency tests (IELTS, TOEFL)
- Learner surveys and interviews
- Conversation analysis

3. "What are the limitations of current chatbot systems?"

Expected findings:
- Limited conversational depth
- Pronunciation feedback accuracy
- Cultural context understanding
- Technical barriers for users

4. "How do chatbots compare to human tutors?"

Expected findings:
- Cost effectiveness
- Availability (24/7)
- Consistency in feedback
- But: Less nuanced feedback than humans
```

---

## Key Findings (Expected)

Based on the literature, you should discover:

### 1. Effectiveness Evidence
- **Quantitative**: Most studies show 15-30% improvement in speaking scores
- **Qualitative**: High learner satisfaction (4.2-4.6/5.0)
- **Engagement**: Increased practice frequency (2-3x more than traditional methods)

### 2. Critical Success Factors
1. **Natural Language Processing Quality**
   - Speech recognition accuracy >90%
   - Contextual understanding
   - Error detection capability

2. **Feedback Mechanisms**
   - Immediate pronunciation feedback
   - Grammar correction
   - Vocabulary suggestions

3. **User Experience**
   - Conversational flow
   - Personality/character
   - Gamification elements

4. **Pedagogical Design**
   - Scaffolded difficulty
   - Task variety
   - Progress tracking

### 3. Learner Populations
- **Most studied**: English as Second Language (ESL) learners
- **Age groups**: University students (70%), K-12 (20%), adults (10%)
- **Proficiency levels**: Beginner and intermediate (most common)

### 4. Technology Used
- **Platforms**: Mobile apps (60%), web-based (30%), VR/AR (10%)
- **AI Models**: Rule-based (older studies) → Neural networks (recent)
- **Speech Tech**: Google Speech API, Microsoft Azure, custom models

### 5. Research Gaps Identified
- Limited longitudinal studies (>6 months)
- Few studies on advanced learners
- Lack of cross-cultural comparisons
- Need for standardized evaluation metrics

---

## Validation Checklist

Use this checklist to verify your results match expectations:

### Data Quality Checks
- [ ] Total papers identified: 350-450 (if ~403, ✅)
- [ ] Relevance rate: 20-30% (if ~26%, ✅)
- [ ] PDF success rate: 50-65% (if ~57%, ✅)
- [ ] Average chunks per paper: 15-25 (if ~19, ✅)

### Content Quality Checks
- [ ] Found papers on speaking anxiety reduction
- [ ] Found papers comparing chatbots to human tutors
- [ ] Found papers on pronunciation feedback
- [ ] Found papers with quantitative effectiveness data
- [ ] Found papers on learner motivation

### Technical Quality Checks
- [ ] No duplicate papers in final dataset
- [ ] All PDFs are readable (not corrupted)
- [ ] Vector search returns relevant results
- [ ] Claude generates coherent answers with citations
- [ ] PRISMA diagram matches paper counts

---

## Common Issues and Solutions

### Issue 1: Fewer papers than expected (~200 instead of ~400)

**Possible causes:**
- API rate limiting
- Query terms too specific
- Year range too narrow

**Solutions:**
```bash
# Try broader query:
python scripts/01_fetch_papers.py \
  --query "conversational AI language learning" \
  --year-start 2010  # Earlier start year

# Or try multiple queries:
python scripts/01_fetch_papers.py --query "chatbot language learning"
python scripts/01_fetch_papers.py --query "conversational agent second language"
```

### Issue 2: Very low relevance rate (<10%)

**Possible causes:**
- Query too broad
- Screening criteria too strict

**Solutions:**
```bash
# Revise research question to be more specific:
python scripts/03_screen_papers.py \
  --question "Do AI chatbots improve pronunciation in language learning?" \
  # (More specific than "speaking skills")
```

### Issue 3: Low PDF download success (<40%)

**Expected behavior** - many papers are paywalled!

**Solutions:**
- Use VPN through university network (if available)
- Request papers via ResearchGate/Academia.edu
- Email authors directly (surprisingly effective!)

### Issue 4: RAG returns irrelevant results

**Possible causes:**
- Too few papers in database (<20)
- Query too vague

**Solutions:**
```bash
# Increase retrieval count:
python scripts/06_query_rag.py \
  --query "pronunciation feedback mechanisms" \
  --k 20  # Retrieve more chunks

# Or rebuild RAG with larger chunks:
python scripts/05_build_rag.py \
  --chunk-size 1500 \
  --chunk-overlap 300
```

---

## Cost Breakdown

### Actual Costs for This Example Project:

| Stage | Description | Cost |
|-------|-------------|------|
| 1 | Fetch papers (public APIs) | $0 |
| 2 | Deduplication (local) | $0 |
| 3 | AI screening (301 papers) | ~$4.50 |
| 4 | PDF download | $0 |
| 5 | RAG building (local embeddings) | $0 |
| 6 | Queries (100 queries) | ~$12 |
| 7 | PRISMA diagram | $0 |
| **Total** | | **~$16.50** |

**Breakdown of Claude API costs:**
- Screening: 301 papers × 400 tokens avg × $0.003/1K = $3.61
- Output: 301 responses × 100 tokens × $0.015/1K = $0.45
- Queries: 100 queries × 800 tokens input × $0.003/1K = $2.40
- Output: 100 responses × 600 tokens × $0.015/1K = $9.00
- **Total API cost: $15.46**

---

## Next Steps

After completing this example project:

1. **📊 Analyze Your Results**
   - Read the generated summary report
   - Compare findings with expected outcomes
   - Identify surprising/novel patterns

2. **📝 Write Your Literature Review**
   - Use RAG queries to draft sections
   - Cite papers with proper formatting
   - Synthesize themes across studies

3. **🔄 Iterate on Methods**
   - Try different search queries
   - Adjust screening criteria
   - Experiment with RAG parameters

4. **🚀 Apply to Your Own Research**
   - Copy `config.yaml` as template
   - Modify research question
   - Run full pipeline on your topic

5. **🤝 Contribute Back**
   - Share your config.yaml as another example
   - Report bugs or suggest improvements
   - Write tutorials for your domain

---

## Citation

If you use this example project in your research, please cite:

```bibtex
@misc{researcherrag2025,
  title={ResearcherRAG: AI-Powered Systematic Literature Review Automation},
  author={You, Hosung},
  year={2025},
  url={https://github.com/HosungYou/ResearcherRAG}
}
```

---

## Questions or Issues?

- 📧 Email: newhosung@gmail.com
- 💬 GitHub Issues: [github.com/HosungYou/ResearcherRAG/issues](https://github.com/HosungYou/ResearcherRAG/issues)
- 📚 Documentation: See `docs/` folder

---

**Happy researching!** 🎉
