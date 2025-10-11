# Stage 5: Execution Plan Prompt

After completing RAG design (Stage 4), use this prompt to execute the full pipeline:

---

I've configured my RAG system design. Now I need help executing the pipeline to build and test my RAG system.

**Configuration Summary**:
- Papers to process: [X] papers
- PDF strategy: [Open Access / Institutional / Both]
- Embedding model: [model name]
- Vector DB: [ChromaDB / other]

Please help me:
1. Generate all necessary Python scripts (scripts 3-6)
2. Execute PDF download
3. Extract text from PDFs
4. Build vector database
5. Create query interface
6. Test with sample questions
7. Troubleshoot any issues

---

## What Claude Code Will Do

Claude will:
1. **Generate Scripts**: Create Python scripts for execution
2. **Guide Execution**: Walk you through running each script
3. **Monitor Progress**: Help interpret output and logs
4. **Handle Errors**: Troubleshoot failures (API limits, PDF issues, etc.)
5. **Test RAG**: Validate system with sample queries
6. **Optimize**: Tune retrieval settings based on results

---

## Execution Timeline

```
Total Time: 3-4 hours

Phase 1: PDF Download (2-3 hours)
├─ Open access papers (~20 min)
├─ Institutional access (~40 min)
└─ Author requests (background, async)

Phase 2: Text Extraction (30 minutes)
├─ PyMuPDF extraction (~15 min)
├─ Quality checks (~10 min)
└─ OCR fallback (~5 min for failures)

Phase 3: Vector DB Build (15 minutes)
├─ Text chunking (~5 min)
├─ Generate embeddings (~8 min)
└─ Store in ChromaDB (~2 min)

Phase 4: RAG Testing (15 minutes)
├─ Test queries (~10 min)
├─ Evaluate answers (~5 min)
└─ Adjust settings if needed
```

---

## Script 3: Download PDFs

**Claude will generate**: `scripts/3_download_pdfs.py`

**Key Features**:
- Multi-tier download strategy (Open Access, Institutional, Author requests)
- Progress bar with tqdm
- Retry logic (3 attempts per paper)
- Error logging
- Resume capability (skip already downloaded)

**Example Output**:
```
Downloading PDFs for 139 papers...

Tier 1: Open Access
[████████████████████] 56/56 (100%) - 3m 42s
✓ 53 succeeded, ✗ 3 failed

Tier 2: Institutional Access
[████████████████    ] 22/28 (79%) - 8m 15s
✓ 22 succeeded, ✗ 6 failed

Overall: 75/139 PDFs (54%) - Total time: 12m 17s

Saved to: data/pdfs/
Log: data/logs/pdf_download.log
```

---

## Script 4: Extract Text

**Claude will generate**: `scripts/4_extract_text.py`

**Key Features**:
- PyMuPDF primary, pdfplumber backup, Tesseract OCR fallback
- Quality checks (min 1,000 words)
- Extract metadata (authors, year, title from PDF if missing)
- Save to text files with paper ID

**Example Output**:
```
Extracting text from 75 PDFs...

[████████████████████] 75/75 (100%) - 18m 34s

✓ 71 succeeded (PyMuPDF: 65, pdfplumber: 4, OCR: 2)
✗ 4 failed (corrupted PDFs)

Quality summary:
- Mean words/paper: 7,234
- Min words: 1,203
- Max words: 14,567

Saved to: data/texts/
Log: data/logs/text_extraction.log
```

---

## Script 5: Build Vector Database

**Claude will generate**: `scripts/5_build_vectordb.py`

**Key Features**:
- Load texts from data/texts/
- Chunk with specified size and overlap
- Generate embeddings with chosen model
- Store in ChromaDB with metadata
- Display statistics

**Example Output**:
```
Building vector database...

Loading texts...
✓ Loaded 71 papers (513,614 total words)

Chunking texts...
✓ Created 687 chunks (avg 748 words/chunk)

Generating embeddings...
Model: sentence-transformers/all-MiniLM-L6-v2
[████████████████████] 687/687 - 6m 42s

Storing in ChromaDB...
Collection: ai_education_chatbot_2025
✓ Indexed 687 chunks

Database info:
- Location: data/vector_db/ai_education_chatbot/
- Size: 23.4 MB
- Papers: 71
- Chunks: 687
- Embedding dim: 384

✅ Vector database built successfully!
```

---

## Script 6: Query RAG

**Claude will generate**: `scripts/6_query_rag.py`

**Key Features**:
- Interactive command-line interface
- Retrieve relevant chunks
- Generate answer with citations
- Display sources
- Save query history

**Example Session**:
```
🤖 RAG System Ready!
Database: 71 papers, 687 chunks

Enter your question (or 'quit' to exit):
> Do chatbots improve speaking proficiency?

Retrieving relevant papers...
Found 8 relevant chunks (similarity: 0.72-0.89)

Generating answer...

📝 Answer:

Research shows that chatbot interventions demonstrate moderate to large
positive effects on speaking proficiency:

**Fluency Improvements**:
Chatbot-based practice increased speaking rate by 15-30% [Kim et al., 2023,
RCT, N=120, d=0.68, p<.001]. Lower-proficiency learners benefited most
[Lee & Park, 2022, Quasi-exp, N=89, η²=0.42].

**Accuracy Gains**:
Grammatical accuracy improved significantly in experimental groups [Chen,
2024, RCT, N=156, d=0.51, p<.01], particularly for syntax errors [Wang,
2023, N=73, p<.05].

**Self-Reported Confidence**:
Learners reported increased willingness to communicate (WTC) after 8 weeks
of chatbot practice [Martinez et al., 2023, Pre-post, N=94, d=0.73].

**Limitations**:
- Most studies short-term (<3 months)
- Self-report bias in confidence measures
- Limited diversity in L1 backgrounds studied

📚 Sources (8 papers cited):
1. Kim et al. (2023) - RCT, N=120 [Score: 0.89]
2. Lee & Park (2022) - Quasi-experimental, N=89 [Score: 0.87]
3. Chen (2024) - RCT, N=156 [Score: 0.84]
...

---

> What design features are most effective?

[Next query...]
```

---

## Troubleshooting Guide

### Issue 1: Low PDF Download Success (<40%)

**Diagnosis**:
```
You: "Only 32/139 PDFs downloaded (23%). Expected 54%."

Claude: "Let's diagnose:

1. Check error log: data/logs/pdf_download.log
   - What are the main error types?
   - Connection timeout? 401 Unauthorized? 404 Not Found?

2. Common causes:
   A) No institutional access configured
      → Solution: Set up VPN or library proxy
   B) Rate limits hit (429 errors)
      → Solution: Slow down requests (add delays)
   C) Bad DOIs in metadata
      → Solution: Use alternative IDs (PMID, arXiv ID)

Which errors do you see most?"
```

**Solutions**:
- Enable Unpaywall: `UNPAYWALL_EMAIL=your@email.edu`
- Add delays: `time.sleep(2)` between requests
- Try OpenAlex fallback: `--source openalex`

### Issue 2: Text Extraction Failing (>20% failure rate)

**Diagnosis**:
```
Claude: "15/75 PDFs failed extraction (20%). Let's check:

1. Are they scanned PDFs (images, not text)?
   → Enable Tesseract OCR: `--enable-ocr`

2. Are they corrupted files?
   → Re-download: `--redownload-failed`

3. Non-English text?
   → Configure language: `--lang=korean`

Run this diagnostic:
python scripts/4_extract_text.py --diagnose
```

### Issue 3: RAG Answers Too Generic

**Problem**: Not citing specific papers, giving general knowledge

**Solution**:
```
Claude: "Your RAG is using LLM general knowledge, not your papers.

Fixes:
1. Lower similarity threshold (0.65 → 0.55)
   → Retrieves more chunks

2. Increase top-k (10 → 20)
   → More context for LLM

3. Strengthen citation requirement:
   Add to system prompt:
   'You MUST cite at least 3 papers. If you cannot find evidence,
    say so explicitly. Do NOT use general knowledge.'

4. Check retrieval:
   python scripts/test_retrieval.py --query 'your question'
   → See what chunks are retrieved
```

### Issue 4: Out of Memory

**Problem**: Embedding generation crashes

**Solution**:
```
Claude: "Ran out of RAM during embedding generation.

Fixes:
1. Process in batches:
   --batch-size 50  # Instead of all at once

2. Use smaller model:
   all-MiniLM-L6-v2 (384 dim) instead of larger models

3. Clear cache between batches:
   import gc; gc.collect()

I'll update the script with batch processing.
```

---

## Validation Checklist

Before considering your RAG system complete:

### ✅ Data Quality
- [ ] PDF download success ≥50%
- [ ] Text extraction success ≥80%
- [ ] Mean words per paper ≥5,000
- [ ] No corrupted/garbled text

### ✅ Vector Database
- [ ] All papers indexed
- [ ] Metadata correct (titles, authors, years)
- [ ] Chunk count reasonable (~8-10 per paper)
- [ ] Database size appropriate (~20-30 MB for 100 papers)

### ✅ RAG Quality
- [ ] Answers cite specific papers (not generic)
- [ ] Citations include study design and findings
- [ ] Retrieval works (relevant chunks returned)
- [ ] No hallucinations (made-up papers/findings)

### ✅ Testing
- [ ] Test with 5+ different questions
- [ ] Spot-check citations (verify in original papers)
- [ ] Compare answers across similar questions (consistency)
- [ ] Try edge cases (questions with no answer in literature)

---

## Final Output

After successful execution, you'll have:

```
your_project/
├── data/
│   ├── pdfs/ (75 PDFs)
│   ├── texts/ (71 text files)
│   ├── vector_db/ (23 MB database)
│   └── logs/ (execution logs)
│
├── scripts/
│   ├── 3_download_pdfs.py ✅
│   ├── 4_extract_text.py ✅
│   ├── 5_build_vectordb.py ✅
│   └── 6_query_rag.py ✅
│
└── config/
    ├── rag_config.yaml
    └── system_prompt.txt
```

**Ready for research!** 🎉

---

## What's Next

### Option A: Start Querying
Use your RAG system for literature review:
- Generate summaries
- Identify research gaps
- Find supporting evidence for your hypotheses

### Option B: Refine System
Improve RAG quality:
- Tune prompts (add domain-specific instructions)
- Adjust retrieval (top-k, threshold)
- Add re-ranking (better relevance)

### Option C: Scale Up
Expand to multiple projects:
- Create templates for future research
- Set up multi-project dashboard
- Automate updates (new papers added periodically)

### Option D: Advanced Features
Explore advanced capabilities:
- Citation graph analysis
- Temporal trend analysis
- Cross-project queries

---

## Success Stories

### Example 1: Literature Review (Education)
- **Before**: 6 weeks manual review of 500 papers
- **After**: 2 weeks with RAG (139 included papers, instant queries)
- **Time Saved**: 67%

### Example 2: Meta-Analysis (Medicine)
- **Before**: 4 weeks extracting effect sizes manually
- **After**: 1 week with RAG-assisted extraction
- **Time Saved**: 75%

### Example 3: PhD Dissertation (Psychology)
- **Before**: Constantly re-reading papers for citations
- **After**: RAG queries for specific evidence on demand
- **Benefit**: Always up-to-date, never forget relevant papers

---

**Estimated Total Time**: 3-4 hours (mostly PDF download wait time)
**Prerequisites**: Completed Stages 1-4
**Outcome**: Functional RAG system querying 50-150 papers
**Next Steps**: Use for research, refine as needed, scale to future projects

---

## Quick Reference

**Start pipeline**:
```bash
# Step 1: Download PDFs (2-3 hours)
python scripts/3_download_pdfs.py

# Step 2: Extract text (30 min)
python scripts/4_extract_text.py

# Step 3: Build vector DB (15 min)
python scripts/5_build_vectordb.py

# Step 4: Query RAG (interactive)
python scripts/6_query_rag.py
```

**Troubleshoot**:
```bash
# Check logs
cat data/logs/*.log

# Re-run failed steps
python scripts/3_download_pdfs.py --retry-failed
python scripts/4_extract_text.py --reprocess-failed

# Test retrieval
python scripts/test_retrieval.py --query "your test question"
```

**Get help**:
- GitHub Issues: Report bugs
- Workshop forum: Ask questions
- Claude Code: "Help me debug [error message]"

---

**End of Stage 5** - You now have a complete RAG system! 🚀
