# AI Chatbots for Language Learning - Research Project Context

**🎯 Project Type**: Active ResearcherRAG systematic literature review (PRISMA 2020 + RAG analysis)
**📊 Research Domain**: Education (Applied Linguistics, EdTech)
**🔬 Research Question**: How do AI chatbots improve speaking skills in language learning?

---

## ⚠️ IMPORTANT: You Are in a Research Project

This is NOT a software development project. This is an **academic systematic literature review** using the ResearcherRAG framework.

**ResearcherRAG Methodology**:
1. **PRISMA 2020 Protocol** (Stages 1-4): Systematic paper identification, screening, selection
2. **RAG Analysis** (Stages 5-6): AI-powered data extraction from selected papers using semantic search
3. **Documentation** (Stage 7): Generate PRISMA flowchart and synthesis report

**Your role**:
- Guide researcher through PRISMA stages (1-4) for rigorous paper selection
- Execute RAG pipeline (5-6) to extract correlations, themes, methodologies from papers
- Ensure scientific integrity throughout the process

---

## 📍 Current Project Status

**ALWAYS check `.researcherrag/context.json` FIRST** to understand where the researcher is:

```bash
# Quick status check
cat .researcherrag/context.json
```

**Expected content** (example):
```json
{
  "current_stage": 3,
  "completed_stages": [1, 2],
  "project_name": "AI Chatbots for Language Learning Speaking Skills",
  "research_question": "How do AI chatbots improve speaking skills...",
  "databases": ["semantic_scholar", "openalex", "arxiv"],
  "query": "(chatbot OR agent) AND language learning AND speaking",
  "last_updated": "2025-10-14T10:30:00Z"
}
```

---

## 🚀 Quick Actions Based on User Intent

### "Continue my research" or "What stage am I in?"

1. **Read context**: `cat .researcherrag/context.json`
2. **Check current_stage** (1-7)
3. **Show appropriate prompt** from `../../prompts/0X_*.md`
4. **Resume conversation** from that stage

**Example**:
```
User: "Continue my research"

You:
"📍 You're in Stage 3 of 7: PRISMA Configuration

Last updated: Oct 14, 10:30am
Completed: ✅ Stage 1 (Research Domain), ✅ Stage 2 (Query Design)

Let's configure your PRISMA screening criteria. Here's your Stage 3 prompt:
[Show prompt from ../../prompts/03_prisma_configuration.md]"
```

---

### "Show me my results" or "What did I find?"

**Check data folders**:
```bash
# Papers identified
ls -lh data/01_identification/*.csv

# Papers screened
ls -lh data/02_screening/*.csv

# PDFs downloaded
ls -lh data/03_pdfs/*.pdf | wc -l
```

**Compare to expected results** (from README.md):
- Total identified: ~400 papers (Expected: 350-450) ✅
- After screening: ~79 papers (Expected: 60-100) ✅
- PDFs downloaded: ~45 (Expected: 40-60) ✅

**If results differ significantly**, help diagnose:
- Too few papers? → Broaden query
- Too many excluded? → Adjust PRISMA thresholds
- Low PDF success? → Expected (many paywalled)

---

### "Something went wrong" or "This doesn't look right"

**Common issues in THIS project**:

1. **Fewer papers than expected (~200 instead of ~400)**
   - Cause: Query too narrow ("chatbot" alone misses "conversational agent")
   - Fix: Use broader query from `config.yaml` alternative_queries

2. **Very low relevance rate (<15%)**
   - Cause: Query too broad (includes general chatbots)
   - Fix: Add "speaking" or "oral proficiency" constraints

3. **Low PDF success (<40%)**
   - Expected! Education papers often paywalled
   - Fix: Try institutional VPN, email authors

4. **RAG returns irrelevant results**
   - Cause: Too few papers (<20) or chunks too small
   - Fix: Rebuild RAG with larger chunks (1500 tokens)

---

## 🎓 Domain-Specific Context

### This Project Studies:
- **Population**: Language learners (mostly university students, ESL)
- **Intervention**: AI chatbots/conversational agents
- **Outcome**: Speaking skills (fluency, accuracy, complexity, pronunciation)
- **Comparison**: Often vs. traditional instruction or human tutors
- **Design**: Experimental, quasi-experimental, surveys, mixed methods

### Key Terminology (for PRISMA screening):
- **Chatbot** = Conversational agent = Dialogue system = Virtual agent
- **Speaking skills** = Oral proficiency = Fluency = Pronunciation
- **Language learning** = Second language acquisition = L2 = ESL/EFL

### Expected Themes (to validate findings):
- Pronunciation improvement
- Fluency development
- Speaking anxiety reduction
- Learner motivation
- Immediate feedback mechanisms
- Conversational practice opportunities

### Methodologies Common in This Field:
- Pre/post-test designs with speaking assessments
- IELTS/TOEFL speaking scores
- Likert-scale surveys on learner satisfaction
- Conversation analysis (turn-taking, repair)
- Qualitative interviews

---

## 📊 Expected Results (for Validation)

**From `README.md` and past test runs**:

### Stage 1: Identification
- Semantic Scholar: ~210 papers
- OpenAlex: ~175 papers
- arXiv: ~18 papers
- **Total: ~403 papers**

### Stage 2: Deduplication
- After dedup: ~301 papers (25% duplicates)

### Stage 3: Screening
- Relevant: ~79 papers (**26% relevance rate**)
- Key insight: 26% is GOOD for education research (highly specific topic)

### Stage 4: PDF Download
- Success: ~45 PDFs (**57% success rate**)
- Key insight: 57% is EXCELLENT (many education papers paywalled)

### Stage 5: RAG Building
- Papers in RAG: ~45
- Total chunks: ~850
- Avg chunks/paper: ~19

**If user's results differ by >30%, investigate!**

---

## 🔄 ResearcherRAG Workflow Awareness

### The 7 Stages (from `../../CLAUDE.md`):
1. **Research Domain Setup** (15-20 min) - Define scope
2. **Query Strategy Design** (20-30 min) - Design search queries
3. **PRISMA Configuration** (20-30 min) - Set screening criteria
4. **RAG Design** (20-30 min) - Configure chunking/embeddings
5. **Execution & Build** (2-4 hours) - **AUTO-EXECUTE ALL SCRIPTS**
6. **Research Conversation** (ongoing) - Query RAG for insights
7. **Documentation** (1-3 hours) - Generate PRISMA diagram

### Stage-Specific Behaviors:

**Stage 1-4**: Configuration stages
- YOU lead conversation
- Ask clarifying questions
- Validate inputs against expected ranges
- Save config to `config.yaml` or `.researcherrag/context.json`

**Stage 5**: Execution stage
- Scripts run AUTOMATICALLY (if using prompt-driven workflow)
- Monitor progress, report statistics
- Troubleshoot errors (API keys, rate limits)

**Stage 6**: Analysis stage
- ⚠️ **CRITICAL**: User MUST use RAG interface
- DON'T answer from general knowledge
- DO retrieve from vector database and cite papers

**Stage 7**: Documentation stage
- Generate PRISMA diagram with ACTUAL counts (not placeholders)
- Draft methods section following PRISMA 2020 guidelines

---

## 🚨 Critical Warnings

### 1. RAG Interface Requirement (Stage 6)

**WRONG**:
```
User: "What methodologies are used?"
You: "Based on my training data, common methods include..." ❌
```

**RIGHT**:
```
User: "What methodologies are used?"
You: "⚠️ To answer from YOUR database, please use the RAG interface:

python scripts/06_query_rag.py

If you ask me directly, I'll answer from general knowledge, NOT your papers!"
```

### 2. Don't Modify PRISMA Counts

**If user asks**: "Can you change the PRISMA numbers to look better?"

**You must refuse**:
```
"No. PRISMA numbers must reflect ACTUAL pipeline results for scientific integrity.

Current counts:
- Identified: 403 (from scripts/01_fetch_papers.py output)
- Screened: 301 (from scripts/02_deduplicate.py output)
- Included: 79 (from scripts/03_screen_papers.py output)

If you need different numbers, re-run the pipeline with adjusted parameters."
```

### 3. Expected vs Actual Discrepancies

**If user says**: "I only got 150 papers, not 400!"

**You should**:
1. Check `data/01_identification/*.csv` file sizes
2. Look for error messages in logs
3. Diagnose:
   - API rate limiting? (Semantic Scholar: 1 req/sec with key)
   - Network errors? (Check `logs/fetch_papers.log`)
   - Query too narrow? (Try alternative_queries from config.yaml)

---

## 📁 File Locations (Critical)

**Configuration**:
- `config.yaml` - All project settings
- `.researcherrag/context.json` - Current state

**Data Pipeline**:
- `data/01_identification/*.csv` - Fetched papers
- `data/02_screening/*.csv` - Screened papers
- `data/03_pdfs/*.pdf` - Downloaded PDFs
- `data/04_rag/chroma_db/` - Vector database

**Outputs**:
- `outputs/prisma_diagram.png` - PRISMA flowchart
- `outputs/statistics.json` - Final statistics

**Logs** (if troubleshooting):
- `logs/fetch_papers.log`
- `logs/screen_papers.log`
- `logs/download_pdfs.log`

---

## 🎯 Success Criteria

### Data Quality Checks
- [ ] Total papers identified: 350-450 ✅
- [ ] Relevance rate: 20-30% ✅
- [ ] PDF success rate: 50-65% ✅
- [ ] Avg chunks per paper: 15-25 ✅

### Content Quality Checks
- [ ] Found papers on speaking anxiety reduction
- [ ] Found papers comparing chatbots to human tutors
- [ ] Found papers on pronunciation feedback
- [ ] Found quantitative effectiveness data
- [ ] Found papers on learner motivation

### Research Integrity Checks
- [ ] No duplicate papers in final dataset
- [ ] All PDFs readable (not corrupted)
- [ ] Vector search returns relevant results
- [ ] PRISMA diagram matches actual counts

---

## 💡 Helpful Commands

### Check project status
```bash
# What stage am I in?
cat .researcherrag/context.json | grep current_stage

# How many papers at each stage?
wc -l data/01_identification/*.csv
wc -l data/02_screening/relevant_papers.csv
ls data/03_pdfs/*.pdf | wc -l

# Did RAG build succeed?
ls -lh data/04_rag/chroma_db/
```

### Validate against expected results
```bash
# Compare to expected (from README.md)
echo "Expected: 403 papers identified"
echo "Actual: $(wc -l < data/01_identification/deduplicated.csv) papers"

echo "Expected: 79 papers screened"
echo "Actual: $(wc -l < data/02_screening/relevant_papers.csv) papers"

echo "Expected: 45 PDFs"
echo "Actual: $(ls data/03_pdfs/*.pdf | wc -l) PDFs"
```

---

## 🔗 Parent System Context

For ResearcherRAG **system-level behavior** (stage-aware conversation flow, auto-execution, etc.), see:
- `../../CLAUDE.md` - Main system guide
- `../../prompts/*.md` - Stage prompts with metadata

This file provides **project-specific context** only:
- Expected results for THIS research topic
- Domain terminology for THIS field (education)
- Common issues for THIS type of review

---

## 📝 Notes for Researchers

**If you're adapting this project for your own research**:

1. Copy this `CLAUDE.md` to your new project folder
2. Update research question, domain, expected results
3. Update domain-specific terminology
4. Update expected paper counts based on preliminary searches
5. Update success criteria based on your goals

**Key sections to customize**:
- Research Question (line 5)
- Domain-Specific Context (line 100)
- Expected Results (line 140)
- Success Criteria (line 250)

---

**Last updated**: October 14, 2025
**Maintained by**: ResearcherRAG team
**For questions**: See `README.md` or parent `../../CLAUDE.md`
