<!-- METADATA
stage: 5
stage_name: "Execution & Build"
stage_goal: "Execute full pipeline: fetch papers, deduplicate, screen, download PDFs, build RAG"
expected_duration: "2-4 hours (mostly automated)"
conversation_mode: "execution_monitoring"
prerequisites:
  - stage: 4
    requirement: "All configurations saved (query, PRISMA, RAG)"
outputs:
  - fetched_papers: "Papers from Semantic Scholar, OpenAlex, arXiv"
  - deduplicated_papers: "Duplicates removed by DOI/title"
  - screened_papers: "Papers passing PRISMA screening"
  - downloaded_pdfs: "PDFs successfully retrieved"
  - vector_database: "ChromaDB with embedded paper chunks"
validation_rules:
  api_keys_present:
    required: true
    check: "ANTHROPIC_API_KEY in environment"
    validation: "Required for RAG and screening"
  paper_count:
    required: true
    range: [20, 5000]
    validation: "Realistic paper count for processing"
  pdf_success_rate:
    required: false
    range: [0.3, 0.8]
    validation: "Expected 30-80% PDF download success"
cli_commands:
  - command: "python scripts/01_fetch_papers.py"
    when: "Stage 5 starts"
    auto_execute: true
  - command: "python scripts/02_deduplicate.py"
    when: "After 01_fetch_papers.py completes"
    auto_execute: true
  - command: "python scripts/03_screen_papers.py"
    when: "After 02_deduplicate.py completes"
    auto_execute: true
  - command: "python scripts/04_download_pdfs.py"
    when: "After 03_screen_papers.py completes"
    auto_execute: true
  - command: "python scripts/05_build_rag.py"
    when: "After 04_download_pdfs.py completes"
    auto_execute: true
scripts_triggered:
  - scripts/01_fetch_papers.py
  - scripts/02_deduplicate.py
  - scripts/03_screen_papers.py
  - scripts/04_download_pdfs.py
  - scripts/05_build_rag.py
next_stage:
  stage: 6
  condition: "RAG system built successfully and tested"
  prompt_file: "06_research_conversation.md"
divergence_handling:
  common_divergences:
    - pattern: "User wants to skip a script"
      response: "All scripts are necessary for PRISMA compliance. If you want partial execution, this may not be the right tool for your needs."
    - pattern: "Script fails with error"
      response: "Let me help troubleshoot. Common issues: API keys missing, rate limits hit, network errors. Please share the error message."
    - pattern: "User asks about results before completion"
      response: "The pipeline is still running. I'll show results after each script completes. Current progress: [X/5 scripts complete]"
conversation_flow:
  expected_turns: 3-8
  typical_pattern:
    - turn: 1
      user_action: "Confirms ready to execute pipeline"
      claude_action: "Verify API keys, show execution plan with time estimates"
    - turn: 2
      user_action: "Confirms execution"
      claude_action: "Run scripts/01_fetch_papers.py, show progress"
    - turn: 3-6
      user_action: "Monitors progress, may ask questions"
      claude_action: "Run remaining scripts sequentially, report after each"
    - turn: 7
      user_action: "Reviews final statistics"
      claude_action: "Test RAG with sample query, show Stage 6 prompt"
validation_checklist:
  - "Papers fetched from all configured databases"
  - "Duplicates removed (typically 20-40% reduction)"
  - "PRISMA screening completed (20-70% pass rate expected)"
  - "PDFs downloaded (30-80% success rate expected)"
  - "Vector database built and validated with test query"
  - "Ready to proceed to research conversations"
-->

# Stage 5: Execution & Build

**🎯 Your Current Stage**: Stage 5 of 7
**⏱️ Expected Time**: 2-4 hours (mostly automated)
**💬 Format**: Execution monitoring with Claude Code
**📋 Prerequisites**: Stages 1-4 completed (all configs saved)

---

## 🚀 Quick Start

I'm ready to execute the full pipeline. Let's build my RAG system!

**Configuration Summary**:
- Research question: [From Stage 1]
- Search query: [From Stage 2]
- PRISMA thresholds: [From Stage 3]
- RAG settings: [From Stage 4]

Please execute:
1. Fetch papers from databases
2. Remove duplicates
3. Run PRISMA screening
4. Download PDFs
5. Build vector database
6. Test with sample query

---

## 📋 What Happens in This Stage

### The Complete Pipeline Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│                    STAGE 5: EXECUTION & BUILD                    │
│              Transform Configuration → Working System            │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│ 01_fetch_papers.py   │  ⏱️  10-30 min
│ Databases queried    │  📊 Expected: 100-5000 papers
└──────────┬───────────┘
           │  papers.json (500 papers)
           ▼
┌──────────────────────┐
│ 02_deduplicate.py    │  ⏱️  1-5 min
│ Remove duplicates    │  📊 Reduction: 20-40%
└──────────┬───────────┘
           │  unique_papers.json (400 papers)
           ▼
┌──────────────────────┐
│ 03_screen_papers.py  │  ⏱️  5-20 min
│ PRISMA screening     │  📊 Pass rate: 20-70%
└──────────┬───────────┘
           │  screened_papers.json (75 papers)
           ▼
┌──────────────────────┐
│ 04_download_pdfs.py  │  ⏱️  1-3 hours (longest!)
│ Fetch full-text PDFs │  📊 Success: 30-80%
└──────────┬───────────┘
           │  pdf_files/ (45 PDFs)
           ▼
┌──────────────────────┐
│ 05_build_rag.py      │  ⏱️  10-30 min
│ Build vector DB      │  📊 ~50 chunks/paper
└──────────┬───────────┘
           │
           ▼
    ✅ RAG System Ready!
    Ready for research conversations
```

### Claude Code Will:

1. **Verify Prerequisites** (Turn 1)
   ```bash
   ✓ Check ANTHROPIC_API_KEY in environment
   ✓ Check OPENAI_API_KEY in environment
   ✓ Verify config.yaml exists and is valid
   ✓ Estimate total execution time: 2-4 hours
   ```

2. **Execute Script 01: Fetch Papers** (Turn 2)
   ```bash
   $ python scripts/01_fetch_papers.py --project /path/to/project

   [10:00:00] Querying Semantic Scholar...
   [10:05:23] Found 312 papers from Semantic Scholar
   [10:05:24] Querying OpenAlex...
   [10:12:45] Found 156 papers from OpenAlex
   [10:12:46] Querying arXiv...
   [10:15:02] Found 35 papers from arXiv

   ✅ Total fetched: 503 papers
   📂 Saved to: data/01_fetch/papers.json
   ```

3. **Execute Script 02: Deduplicate** (Turn 3)
   ```bash
   $ python scripts/02_deduplicate.py --project /path/to/project

   [10:15:10] Checking for duplicates by DOI...
   [10:15:45] Found 78 duplicates by DOI
   [10:15:46] Checking title similarity (90% threshold)...
   [10:17:12] Found 25 duplicates by title

   ✅ Removed: 103 duplicates (20.5%)
   ✅ Unique papers: 400
   📂 Saved to: data/02_deduplicate/unique_papers.json
   ```

4. **Execute Script 03: PRISMA Screening** (Turn 4)
   ```bash
   $ python scripts/03_screen_papers.py --project /path/to/project

   [10:17:20] Screening paper 1/400: "AI Chatbots in Language Learning"
   [10:17:35] ✓ PASS (Score: 90.3/100)
   [10:17:36] Screening paper 2/400: "Opinion: Future of AI"
   [10:17:48] ✗ FAIL (Score: 45.2/100) - Exclusion criteria: opinion piece
   ...
   [10:32:15] Screening complete!

   ✅ Passed PRISMA: 79 papers (19.8%)
   ✅ Failed: 321 papers
   📂 Saved to: data/03_screen/screened_papers.json

   📊 Score breakdown:
      Domain:     avg 82.3 (70+ required)
      Method:     avg 68.5 (60+ required)
      Topic:      avg 88.1 (80+ required)
      Context:    avg 71.2 (65+ required)
      Exclusion:  avg 95.0 (80+ required)
      Title:      avg 79.4 (75+ required)
   ```

5. **Execute Script 04: Download PDFs** (Turn 5 - LONGEST STEP)
   ```bash
   $ python scripts/04_download_pdfs.py --project /path/to/project

   [10:32:30] Attempting to download 79 PDFs...
   [10:32:31] Paper 1/79: Checking Unpaywall...
   [10:32:45] ✓ Downloaded from Unpaywall
   [10:32:46] Paper 2/79: Checking Unpaywall...
   [10:33:01] ✗ Not available on Unpaywall, trying CORE...
   [10:33:15] ✓ Downloaded from CORE
   [10:33:16] Paper 3/79: Checking Unpaywall...
   [10:33:30] ✗ Not available (paywalled)
   ...
   [13:15:42] Download complete!

   ✅ Successfully downloaded: 45 PDFs (57.0%)
   ✗ Failed (paywalled): 34 papers
   📂 Saved to: data/04_pdfs/pdf_files/

   📊 Source breakdown:
      Unpaywall:  28 PDFs (62%)
      CORE:       12 PDFs (27%)
      arXiv:       5 PDFs (11%)
   ```

6. **Execute Script 05: Build RAG** (Turn 6)
   ```bash
   $ python scripts/05_build_rag.py --project /path/to/project

   [13:15:50] Extracting text from 45 PDFs...
   [13:18:23] PDF 1/45: 8 pages → 4,234 tokens
   [13:20:45] PDF 2/45: 12 pages → 6,891 tokens
   ...
   [13:35:12] Text extraction complete!

   [13:35:15] Chunking documents (size: 1000, overlap: 200)...
   [13:37:42] Created 2,250 chunks (avg 50 per paper)

   [13:37:45] Generating embeddings with text-embedding-3-small...
   [13:42:18] Embedded 2,250 chunks (dimension: 1536)

   [13:42:20] Storing in ChromaDB vector database...
   [13:43:55] Vector database built successfully!

   ✅ RAG system ready!
   📂 Database: data/04_rag/chroma_db/
   📊 Stats:
      Papers processed: 45
      Total chunks: 2,250
      Chunks per paper: 50
      Embedding model: text-embedding-3-small
   ```

7. **Test RAG System** (Turn 7)
   ```bash
   [13:44:00] Testing RAG with sample query...

   Query: "What methodologies are used in chatbot studies?"

   Retrieved chunks (top 5):
   1. Smith et al. 2023, p.3: "RCT with 120 participants..."
   2. Jones et al. 2022, p.5: "Qualitative interviews with..."
   3. Lee et al. 2024, p.2: "Mixed methods design combining..."
   4. Chen et al. 2023, p.4: "Experimental study with control group..."
   5. Kim et al. 2023, p.6: "Survey-based methodology..."

   Generated answer:
   "Based on the PRISMA-selected literature, three main methodologies
   emerge: (1) RCT and experimental designs (Smith 2023, Chen 2023),
   (2) qualitative approaches (Jones 2022), and (3) mixed methods
   (Lee 2024). The majority (60%) employ quantitative methods..."

   ✅ RAG test successful! Citations are working correctly.
   ```

8. **Final Summary & Transition** (Turn 8)
   ```
   🎉 PIPELINE COMPLETE!

   📊 Final Statistics:
   ┌─────────────────────────┬──────────┬──────────┐
   │ Stage                   │ Input    │ Output   │
   ├─────────────────────────┼──────────┼──────────┤
   │ 01. Fetch Papers        │ -        │ 503      │
   │ 02. Deduplicate         │ 503      │ 400      │
   │ 03. PRISMA Screen       │ 400      │ 79       │
   │ 04. Download PDFs       │ 79       │ 45       │
   │ 05. Build RAG           │ 45       │ 2,250    │
   └─────────────────────────┴──────────┴──────────┘

   ⏱️  Total execution time: 3 hours 29 minutes

   ✅ You're ready for Stage 6: Research Conversation!
   ```

### ✅ Stage Completion Checklist

Pipeline succeeds when:

- [ ] **Papers fetched** from all databases (expect 100-5000)
- [ ] **Duplicates removed** (20-40% reduction typical)
- [ ] **PRISMA screening** complete (20-70% pass rate)
- [ ] **PDFs downloaded** (30-80% success rate)
- [ ] **Vector database built** and tested
- [ ] **Sample query works** with proper citations

---

## 🎯 Stage 5 Success Criteria

✅ All 5 scripts executed successfully
✅ PRISMA pass rates are realistic (not 0% or 100%)
✅ PDF download success rate is 30-80%
✅ Vector database returns relevant results
✅ Ready to start research conversations

---

## 📍 Your Progress

```
[●●●●●○○] Stage 5/7: Execution & Build
```

**Next**: Stage 6 - Research Conversation (ongoing)
**After That**: Stage 7 - Documentation & Writing

**Progress So Far**: ~95-140 minutes of planning
**Executing Now**: 2-4 hours automated pipeline
**Remaining**: Stage 6-7 (ongoing research work)

---

**Ready to execute?** Confirm and Claude will start the pipeline!
