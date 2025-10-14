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

### Claude Code Will:

1. **Verify Prerequisites**
   - Check API keys (ANTHROPIC_API_KEY required)
   - Verify config.yaml exists
   - Estimate execution time

2. **Execute Scripts Sequentially** (auto)
   - `scripts/01_fetch_papers.py` (10-30 min)
   - `scripts/02_deduplicate.py` (1-5 min)
   - `scripts/03_screen_papers.py` (5-20 min)
   - `scripts/04_download_pdfs.py` (1-3 hours)
   - `scripts/05_build_rag.py` (10-30 min)

3. **Monitor Progress**
   - Show output after each script
   - Report statistics (papers fetched, duplicates removed, etc.)
   - Handle errors and suggest fixes

4. **Validate Results**
   - Test RAG with sample query
   - Verify vector database
   - Show final statistics

5. **Transition to Stage 6** (automatic)
   - Show Stage 6 prompt for research conversations

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
