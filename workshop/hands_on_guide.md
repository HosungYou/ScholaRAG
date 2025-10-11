# Workshop: Building Your Research RAG System with Claude Code

**Duration**: 3 hours
**Prerequisites**: VS Code installed, Claude Code extension enabled
**Goal**: Build a functional RAG system for your own research project

---

## Pre-Workshop Setup (15 minutes before class)

### 1. Install Required Software

**VS Code** (if not already installed):
- Download: https://code.visualstudio.com/
- Install and open

**Claude Code Extension**:
1. Open VS Code
2. Click Extensions icon (left sidebar)
3. Search "Claude Code"
4. Click Install
5. Sign in with your Anthropic account

**Python** (version 3.9+):
```bash
# Check if Python is installed
python3 --version

# If not installed, download from:
# https://www.python.org/downloads/
```

### 2. Download Workshop Materials

```bash
# Create workshop folder
mkdir ~/workshop_rag
cd ~/workshop_rag

# Clone ResearcherRAG repository
git clone https://github.com/[your-repo]/ResearcherRAG.git
cd ResearcherRAG

# Install dependencies
pip3 install -r requirements.txt
```

### 3. Get API Keys (Optional but Recommended)

**Semantic Scholar** (free, no key needed):
- Rate limit: 5,000 requests per 5 minutes
- Sufficient for workshop

**OpenAlex** (free, no key needed):
- Rate limit: 100,000 requests per day
- Backup option

**Note**: For PDF downloads from publisher sites, institutional access (university VPN) is recommended but not required for today's workshop.

---

## Part 1: Introduction & Demo (30 minutes)

### Live Demo: Watch Instructor Build a RAG System

The instructor will demonstrate building a complete RAG system in real-time:

**Demo Project**: "AI Chatbots in Language Learning"

**Timeline**:
- 0:00 - Initial prompt to Claude Code
- 0:05 - Research scope defined, query designed
- 0:10 - Papers collected (568 papers from Semantic Scholar)
- 0:12 - PRISMA profile generated
- 0:15 - Screening executed (115 papers passed)
- 0:18 - RAG system built
- 0:20 - Live query demo
- 0:25 - Q&A about the process

**Key Observations**:
- How to structure prompts for Claude
- How to refine configurations through conversation
- How to handle errors and iterate
- What the final output looks like

---

## Part 2: Hands-On Exercises (90 minutes)

### Exercise 1: Define Your Research Project (20 minutes)

**Objective**: Have a clear research scope before starting implementation.

**Step 1: Brainstorm Your Topic** (5 min)

Write down:
1. Your research question in one sentence
2. Your academic field
3. Key concepts/keywords you already know
4. Any constraints (year, method, population)

**Example**:
```
Research Question: Do mindfulness interventions reduce teacher burnout?
Field: Educational Psychology
Key concepts: mindfulness, teacher wellbeing, stress, burnout
Constraints: 2010-2024, quantitative studies only, K-12 teachers
```

**Step 2: Open Claude Code** (5 min)

1. Open VS Code
2. Open a new terminal (Terminal → New Terminal)
3. Create your project folder:
```bash
mkdir ~/workshop_rag/my_project
cd ~/workshop_rag/my_project
```

4. Open Claude Code chat (Cmd+Shift+P → "Claude: Open Chat")

**Step 3: Use the Research Domain Setup Prompt** (10 min)

Copy the template from `prompts/01_research_domain_setup.md` and fill it in with your research details.

Paste it into Claude Code chat.

**What to expect**:
- Claude will ask clarifying questions
- Answer each question thoughtfully
- Don't rush - this foundation is critical
- Ask Claude to explain anything unclear

**Success Criteria**:
- ✅ Claude understands your research domain
- ✅ You have a clear list of domain/method/topic keywords
- ✅ You have an estimated paper count (ballpark: 200-1000 papers)

---

### Exercise 2: Design Search Query (20 minutes)

**Objective**: Create an effective query that balances comprehensiveness and precision.

**Step 1: Request Query Design** (5 min)

Use the prompt from `prompts/02_query_strategy.md`:

```
Now that we've defined my research scope, please help me design
effective search queries. I prefer a **balanced** approach (not too
broad, not too narrow). Please design 2-3 options and recommend
one to start with.
```

**Step 2: Review Claude's Proposals** (10 min)

Claude will provide something like:

```
Query Option 1 (Broad): ~1500 papers
"mindfulness teacher burnout"

Query Option 2 (Focused): ~400 papers [RECOMMENDED]
"(mindfulness OR meditation OR contemplative practice) AND
 (teacher OR educator) AND
 (burnout OR stress OR wellbeing OR mental health) AND
 (K-12 OR school OR elementary OR secondary)"

Query Option 3 (Narrow): ~100 papers
[Option 2] AND (intervention OR trial OR experiment OR RCT)
```

**Evaluate each query**:
- Does it cover all aspects of your research question?
- Are there synonyms missing?
- Are there terms that should be excluded (e.g., "higher education")?

**Step 3: Refine and Finalize** (5 min)

Work with Claude to adjust the query:
- "Can you add [keyword]?"
- "Should we exclude [keyword]?"
- "What if I want to include qualitative studies too?"

**Example refinement conversation**:
```
You: "I'm worried we might miss papers that use 'wellbeing' spelled as
      'well-being' with a hyphen."

Claude: "Great catch! I'll add it as an OR variant:
         (wellbeing OR 'well-being' OR wellness)"

You: "Also, should we exclude higher education teachers? I only want K-12."

Claude: "Yes, let's add: NOT (university OR college OR 'higher education')"
```

**Success Criteria**:
- ✅ You have a finalized query
- ✅ You understand what each part does
- ✅ Estimated paper count is manageable (200-1000)

---

### Exercise 3: Collect Papers & Build PRISMA Profile (40 minutes)

**Objective**: Automatically collect papers and generate a PRISMA screening configuration.

**Step 1: Collect Papers** (10 min)

Ask Claude:
```
Please write a Python script to collect papers from Semantic Scholar
using our finalized query. Save the results to data/raw/papers_metadata.csv.
```

Claude will generate `scripts/1_collect_papers.py`.

**Run it**:
```bash
python3 scripts/1_collect_papers.py
```

**Expected output**:
```
Collecting papers from Semantic Scholar...
Found 427 papers
Saving to data/raw/papers_metadata.csv
Done!
```

**Troubleshooting**:
- **Error: "Module not found"** → Run `pip3 install -r requirements.txt`
- **Error: "API rate limit"** → Wait 5 minutes and try again
- **Fewer papers than expected** → Check query syntax, ask Claude to adjust

**Step 2: Analyze Metadata** (5 min)

Ask Claude:
```
Please analyze the collected papers' metadata and show me:
1. Year distribution
2. Top 20 keywords from abstracts
3. Estimated methodology distribution

This will help me design a good PRISMA profile.
```

Claude will write and run an analysis script, showing output like:
```
📊 Year Distribution:
   2020-2024: 256 papers (60%)
   2015-2019: 128 papers (30%)
   2010-2014:  43 papers (10%)

📊 Top Keywords:
   mindfulness: 389 mentions
   teacher: 367
   burnout: 312
   stress: 287
   wellbeing: 245
   intervention: 198
   ...

📊 Estimated Methodologies:
   Quantitative survey: ~45%
   RCT/Experimental: ~30%
   Qualitative: ~15%
   Mixed methods: ~10%
```

**Step 3: Generate PRISMA Profile** (10 min)

Ask Claude:
```
Based on this metadata analysis, please generate a PRISMA profile
(research_profile.yaml) that:

1. Prioritizes quantitative studies (but doesn't exclude qualitative)
2. Focuses on K-12 teachers (exclude higher ed)
3. Emphasizes intervention studies
4. Expects to pass about 30% of papers (~130 papers)

Please explain the scoring logic.
```

Claude will generate `config/research_profiles/your_project.yaml` and explain:
```yaml
name: "Mindfulness Teacher Burnout - K12"

domain_keywords:
  - teacher: 10
  - educator: 9
  - K-12: 8
  - school: 7
  - burnout: 10
  - stress: 8
  - wellbeing: 8

method_keywords:
  - intervention: 5
  - RCT: 5
  - experimental: 5
  - quantitative: 4
  - survey: 3

topic_keywords:
  - mindfulness: 5
  - meditation: 5
  - contemplative: 4
  - mental health: 4

exclusion_keywords:
  - university: -10
  - college: -10
  - higher education: -10
  - student: -5  # We want teacher studies, not student studies

thresholds:
  screening: 30      # ~60% pass (256 papers)
  eligibility: 50    # ~30% pass (128 papers)
  min_inclusion: 60  # Auto-include high scorers
```

**Step 4: Run PRISMA Screening** (10 min)

Ask Claude:
```
Please create a script to run PRISMA screening using this profile.
```

Claude will generate `scripts/2_run_prisma.py`.

**Run it**:
```bash
python3 scripts/2_run_prisma.py
```

**Expected output**:
```
Loading papers from data/raw/papers_metadata.csv...
Loaded 427 papers

Stage 1: Identification
  Total collected: 427 papers

Stage 2: Screening (title/abstract relevance)
  Threshold: ≥30 points
  Passed: 267 papers (62.5%)
  Failed: 160 papers

Stage 3: Eligibility (detailed assessment)
  Threshold: ≥50 points
  Passed: 139 papers (32.6%)
  Failed: 128 papers
  Manual review needed: 23 papers (score 40-50)

Stage 4: Inclusion
  Final included: 139 papers
  Manual review queue: 23 papers

Saved results to:
  - data/processed/included_papers.csv (139 papers)
  - data/processed/review_queue.csv (23 papers)
  - data/processed/prisma_flow_diagram.png

Done!
```

**Review the results**:
1. Open `data/processed/prisma_flow_diagram.png` to see visual summary
2. Open `data/processed/included_papers.csv` to see which papers passed
3. Spot-check a few high-scoring and low-scoring papers - do they make sense?

**If results are off**:
- **Too many papers passed** → Increase thresholds (35, 55)
- **Too few papers passed** → Decrease thresholds (25, 45) or add more keywords
- **Wrong papers passing** → Adjust keyword weights or add exclusions

Ask Claude: "The screening results look [too strict/too lenient]. Can you help me adjust?"

**Success Criteria**:
- ✅ PRISMA screening completed
- ✅ Final paper count is reasonable (50-200 papers)
- ✅ Spot checks show relevant papers are passing
- ✅ You understand the scoring logic

---

### Exercise 4: Build RAG System (30 minutes)

**⚠️ Important Note**: Full PDF download takes 1-3 hours and requires institutional access. For today's workshop, we'll use a **sample dataset** I've prepared.

**Step 1: Download Sample PDFs** (5 min)

```bash
# Download pre-collected sample papers (50 papers)
curl -O https://[workshop-url]/sample_papers.zip
unzip sample_papers.zip -d data/pdfs/
```

**Alternative (if you have time after workshop)**:
```bash
# Try downloading PDFs for your own papers
python3 scripts/3_download_pdfs.py

# Expected success rate: 50-60%
# Time: 1-2 hours for 100-150 papers
```

**Step 2: Extract Text from PDFs** (5 min)

Ask Claude:
```
Please create a script to extract text from PDFs in data/pdfs/
and save to data/texts/. Use PyMuPDF as the primary method,
with pdfplumber as backup.
```

Run the script:
```bash
python3 scripts/4_extract_text.py
```

**Expected output**:
```
Extracting text from 50 PDFs...
[1/50] paper_001.pdf: ✓ (PyMuPDF, 8,234 words)
[2/50] paper_002.pdf: ✓ (PyMuPDF, 6,891 words)
[3/50] paper_003.pdf: ✗ PyMuPDF failed, trying pdfplumber...
[3/50] paper_003.pdf: ✓ (pdfplumber, 7,456 words)
...
[50/50] paper_050.pdf: ✓ (PyMuPDF, 9,123 words)

Success: 49/50 (98%)
Failed: 1 paper (corrupted PDF)
Total words extracted: 387,234
```

**Step 3: Design RAG Configuration** (10 min)

Ask Claude:
```
I want to build a RAG system to answer questions about my research topic.

My main research questions are:
1. [Your research question 1]
2. [Your research question 2]
3. [Your research question 3]

Please help me configure:
1. Embedding model (local vs. API)
2. Chunk size and overlap
3. Retrieval strategy (top-k, similarity threshold)
4. System prompt for answer generation

Optimize for: academic rigor and proper citation.
```

Claude will propose:
```yaml
# config/rag_config.yaml

embedding:
  model: "sentence-transformers/all-MiniLM-L6-v2"
  # Why: Fast, good quality, runs locally (no API costs)
  dimension: 384

chunking:
  chunk_size: 1000  # tokens (~750 words)
  chunk_overlap: 200  # tokens
  # Why: Balances context preservation and retrieval precision

retrieval:
  top_k: 10  # Retrieve 10 most similar chunks
  similarity_threshold: 0.65  # Only chunks with >65% similarity
  rerank: true  # Use cross-encoder for better ranking

generation:
  model: "claude-3.5-sonnet"  # High-quality answers
  max_tokens: 1500
  temperature: 0.3  # Lower = more factual, less creative
```

And a system prompt:
```
You are a research assistant specializing in [your field].
You have access to {num_papers} peer-reviewed papers on [your topic].

When answering questions:
1. Cite specific papers: [Author, Year, Study Design, Key Finding]
2. Report effect sizes and statistics when available
3. Acknowledge limitations and gaps in the literature
4. Distinguish between strong evidence (RCTs) and weaker evidence (surveys)
5. If the literature doesn't address the question, say so

Tone: Academic but accessible, critical but constructive.
```

**Step 4: Build Vector Database** (5 min)

Ask Claude:
```
Please create a script to build the vector database using these configurations.
```

Run it:
```bash
python3 scripts/5_build_vectordb.py
```

**Expected output**:
```
Loading texts from data/texts/...
Loaded 49 papers (387,234 words)

Chunking texts...
Created 618 chunks (avg 626 words/chunk)

Generating embeddings...
Model: sentence-transformers/all-MiniLM-L6-v2
[████████████████████] 618/618 chunks (12.3s)

Storing in ChromaDB...
Collection: mindfulness_teacher_burnout
Location: data/vector_db/

✅ Vector database built successfully!
   - 618 chunks indexed
   - 49 papers
   - Database size: 18.4 MB
```

**Step 5: Query Your RAG System** (5 min)

Ask Claude:
```
Please create an interactive query interface where I can ask questions
and get answers with citations.
```

Run it:
```bash
python3 scripts/6_query_rag.py
```

**Try these sample queries**:

```
You: What are the main effects of mindfulness interventions on teacher burnout?

RAG: Based on the literature, mindfulness interventions show moderate to
large effects on reducing teacher burnout:

1. **Burnout Reduction (d=0.58)**: A meta-analysis of 12 RCTs found mindfulness
   programs reduced emotional exhaustion by 0.58 standard deviations [Harris et al.,
   2021, Meta-analysis, N=1,234, p<.001].

2. **Stress Reduction (η²=0.31)**: An 8-week mindfulness-based stress reduction
   (MBSR) program for middle school teachers showed significant decreases in
   perceived stress [Chen & Lee, 2020, RCT, N=89, p<.01].

3. **Wellbeing Improvement**: Teachers reported increased job satisfaction (d=0.44)
   and emotional regulation (d=0.52) after mindfulness training [Park et al., 2019,
   Quasi-experimental, N=156].

**Limitations**:
- Most studies have small sample sizes (N<200)
- Short follow-up periods (3-6 months typical)
- Self-report measures dominate (potential bias)
- Limited diversity in participant demographics

**Gaps**: Few studies examine long-term effects (>1 year) or compare different
mindfulness approaches (MBSR vs. brief interventions).

---
Retrieved from: 8 papers (similarity: 0.72-0.89)
```

**Test your own questions**:
1. Ask about specific aspects of your research
2. Try comparative questions ("What's more effective: X or Y?")
3. Ask about methodology ("What study designs are most common?")
4. Ask about gaps ("What hasn't been studied yet?")

**Evaluate the quality**:
- Are citations accurate?
- Are answers relevant to the question?
- Does it acknowledge limitations?
- If the answer is generic, ask Claude to improve the prompt

**Success Criteria**:
- ✅ RAG system responds to your queries
- ✅ Answers include specific paper citations
- ✅ You can verify citations by checking the papers
- ✅ System acknowledges when it doesn't know

---

## Part 3: Advanced Topics (30 minutes)

### Troubleshooting Common Issues

#### Issue 1: RAG Gives Generic Answers (Not Using Papers)

**Symptoms**:
```
You: What are the effects of mindfulness on burnout?
RAG: Mindfulness can reduce stress through increased awareness... [generic]
```

**Diagnosis**:
Ask Claude: "Why isn't my RAG citing specific papers?"

**Solutions**:
1. **Check retrieval**: Lower similarity threshold (0.65 → 0.55)
2. **Improve prompt**: Add "You MUST cite at least 3 specific papers with details"
3. **Verify embeddings**: Ensure papers were actually indexed

**Fix**:
```bash
# Re-run with adjusted config
python3 scripts/5_build_vectordb.py --threshold 0.55
python3 scripts/6_query_rag.py
```

---

#### Issue 2: PDF Download Success Rate Too Low

**Symptoms**:
```
Downloading PDFs: 23/150 succeeded (15%)
```

**Diagnosis**:
- Institutional access not configured
- Publisher restrictions
- Incorrect DOI/URLs

**Solutions**:

**Tier 1: Enable Institutional Access**
```bash
# If using university VPN
export INSTITUTION_TOKEN="your_ezproxy_token"
python3 scripts/3_download_pdfs.py --use-institution
```

**Tier 2: Try Unpaywall**
```bash
export UNPAYWALL_EMAIL="your.email@university.edu"
python3 scripts/3_download_pdfs.py --source unpaywall
```

**Tier 3: Use OpenAlex Open Access**
```bash
python3 scripts/3_download_pdfs.py --source openalex --oa-only
```

**Tier 4: Fallback to Abstracts**
```bash
# Build RAG with abstracts for papers without PDFs
python3 scripts/5_build_vectordb.py --use-abstracts-fallback
```

---

#### Issue 3: PRISMA Results Don't Match Expectations

**Symptoms**:
- Expected 150 papers, got 30 (too strict)
- Expected 100 papers, got 300 (too lenient)

**Diagnosis**:
Ask Claude: "Can you analyze the score distribution of my papers?"

Claude will generate a histogram showing:
```
Score Distribution:
 0-10:  ████ (23 papers)
10-20:  ████████ (47 papers)
20-30:  ████████████ (89 papers) ← Most papers here
30-40:  ██████████ (67 papers)
40-50:  ████ (34 papers)
50-60:  ██ (12 papers)
60-70:  █ (5 papers)

Current threshold: 50 (only 17 papers pass)
Suggested threshold: 30 (156 papers pass)
```

**Solutions**:

**Too Strict** → Lower thresholds or add keywords:
```yaml
thresholds:
  screening: 25  # Was 30
  eligibility: 45  # Was 50

# Or add more inclusive keywords
domain_keywords:
  - stress management: 7  # Added
  - coping: 6  # Added
```

**Too Lenient** → Raise thresholds or add exclusions:
```yaml
thresholds:
  screening: 35  # Was 30
  eligibility: 55  # Was 50

exclusion_keywords:
  - preservice: -8  # Exclude pre-service teachers
  - student teacher: -8
```

---

### Managing Multiple Research Projects

If you work on multiple projects simultaneously:

**Directory Structure**:
```
Research/
├── Project1_Mindfulness_Burnout/
│   ├── config/research_profile.yaml
│   ├── data/vector_db/
│   └── scripts/
│
├── Project2_AI_Chatbot_Learning/
│   ├── config/research_profile.yaml
│   ├── data/vector_db/
│   └── scripts/
│
└── Project3_EHR_Alert_Fatigue/
    ├── config/research_profile.yaml
    ├── data/vector_db/
    └── scripts/
```

**Best Practice**: Each project has its own:
- Research profile (different keywords/thresholds)
- Vector database (isolated collections)
- Scripts (customized for that domain)

**Switching projects**:
```bash
cd ~/Research/Project2_AI_Chatbot_Learning
python3 scripts/6_query_rag.py
```

**Combining projects** (advanced):
```python
# Query multiple RAG systems at once
from rag_merger import MultiProjectRAG

rag = MultiProjectRAG([
    "Project1_Mindfulness_Burnout",
    "Project2_AI_Chatbot_Learning"
])

answer = rag.query("How do AI and mindfulness interventions compare?")
# Retrieves from both databases, synthesizes cross-project insights
```

---

## Part 4: Wrap-Up & Next Steps (30 minutes)

### What You've Accomplished Today

✅ Defined your research scope through conversation with Claude
✅ Designed effective search queries
✅ Collected papers from academic databases
✅ Built a PRISMA systematic review pipeline
✅ Created a custom RAG system for your research
✅ Queried your RAG and got evidence-based answers

### Taking It Further

#### Homework Assignment (Complete by Next Week)

1. **Collect Full Papers** (2-3 hours):
   - Run PDF download for your project: `python3 scripts/3_download_pdfs.py`
   - Try institutional access, Unpaywall, and OpenAlex
   - Document your success rate
   - For missing PDFs, consider emailing authors (Claude can draft template emails)

2. **Query Your RAG with 10 Research Questions** (1 hour):
   - Prepare 10 questions about your research topic
   - Query your RAG system
   - Evaluate answer quality (accuracy, citations, completeness)
   - Note which types of questions work well vs. poorly

3. **Write a Reflection** (30 minutes):
   Share in our workshop forum:
   - What worked well?
   - What challenges did you encounter?
   - How does this compare to your traditional literature review workflow?
   - What features would you want added?

#### Advanced Techniques (Self-Study)

**1. Citation Graph Analysis**:
- Extend RAG to include citation networks
- Find "bridge" papers connecting different research streams
- Identify seminal papers by citation count

**2. Temporal Analysis**:
- Track how research trends evolve over time
- Identify emerging vs. declining topics
- Query: "How has research on [topic] changed from 2015 to 2024?"

**3. Comparative Meta-Analysis**:
- Extract effect sizes from papers automatically
- Generate forest plots
- Query: "What's the average effect size across all studies?"

**4. Cross-Lingual RAG**:
- Include papers in multiple languages
- Use multilingual embedding models
- Query in English, retrieve from Korean/Chinese/Spanish papers

**Ask Claude**: "How can I implement [advanced technique] in my RAG system?"

---

### Resources

**GitHub Repository**:
- https://github.com/[your-repo]/ResearcherRAG
- All templates, scripts, and examples
- Issue tracker for bug reports and feature requests

**Documentation**:
- [CLAUDE_FOR_RESEARCHERS.md](../CLAUDE_FOR_RESEARCHERS.md): Complete guide for Claude Code
- [Prompts](../prompts/): Copy-paste templates for each stage
- [Examples](../examples/): 3 complete research projects

**Community**:
- **Workshop Forum**: [link to Discord/Slack]
- **Office Hours**: Fridays 2-4pm (Zoom link: [link])
- **Mailing List**: [email] for updates and tips

**Academic Papers on RAG**:
- Lewis et al. (2020): "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
- Gao et al. (2023): "Retrieval-Augmented Generation for Large Language Models: A Survey"

**Tools & Libraries**:
- LangChain: https://python.langchain.com/
- ChromaDB: https://www.trychroma.com/
- Semantic Scholar API: https://api.semanticscholar.org/

---

### Feedback & Improvement

Please complete our post-workshop survey: [survey link]

Questions:
1. How confident are you in building a RAG system now? (1-5 scale)
2. What was the most valuable part of the workshop?
3. What was the most confusing part?
4. What should we add/remove for future workshops?
5. Would you recommend this workshop to colleagues? (Yes/No/Maybe)

---

### Certificate of Completion

Congratulations on completing the **Research RAG with Claude Code** workshop!

To receive your certificate:
1. Submit your homework assignment (link above)
2. Share one insight in the workshop forum
3. Complete the feedback survey

Certificates will be emailed within 1 week.

---

## Questions?

**During workshop**: Raise your hand or type in Zoom chat
**After workshop**: Post in workshop forum or attend office hours
**Urgent issues**: Email [instructor-email]

---

## Appendix: Quick Reference

### Command Cheat Sheet

```bash
# Setup
pip3 install -r requirements.txt

# Data collection
python3 scripts/1_collect_papers.py

# PRISMA screening
python3 scripts/2_run_prisma.py

# PDF download (optional, slow)
python3 scripts/3_download_pdfs.py

# Text extraction
python3 scripts/4_extract_text.py

# Build vector database
python3 scripts/5_build_vectordb.py

# Query RAG system
python3 scripts/6_query_rag.py

# Analyze PRISMA scores (troubleshooting)
python3 scripts/analyze_scores.py

# Re-run with different threshold
python3 scripts/2_run_prisma.py --screening 25 --eligibility 45
```

### File Structure Reference

```
your_project/
├── config/
│   ├── research_profiles/
│   │   └── your_profile.yaml          # PRISMA configuration
│   └── rag_config.yaml                 # RAG settings
│
├── data/
│   ├── raw/
│   │   └── papers_metadata.csv         # API results
│   ├── processed/
│   │   ├── included_papers.csv         # PRISMA passed
│   │   ├── review_queue.csv            # Manual review needed
│   │   └── prisma_flow_diagram.png     # Visual summary
│   ├── pdfs/
│   │   └── *.pdf                       # Downloaded papers
│   ├── texts/
│   │   └── *.txt                       # Extracted text
│   └── vector_db/
│       └── chroma.sqlite3              # Vector database
│
├── scripts/
│   ├── 1_collect_papers.py
│   ├── 2_run_prisma.py
│   ├── 3_download_pdfs.py
│   ├── 4_extract_text.py
│   ├── 5_build_vectordb.py
│   └── 6_query_rag.py
│
├── requirements.txt
└── README.md
```

### Claude Code Prompts Reference

| Task | Prompt Template |
|------|-----------------|
| **Setup research** | "I want to build a RAG system for [topic]..." |
| **Design query** | "Help me design search queries for [domain]..." |
| **Build PRISMA profile** | "Generate a PRISMA profile for [research focus]..." |
| **Fix screening** | "Too many/few papers passed. Can you adjust?" |
| **Improve RAG answers** | "Answers are too generic. How do I improve?" |
| **Add feature** | "Can you add [feature] to my RAG system?" |
| **Debug error** | "I got this error: [paste error]. How to fix?" |

---

**End of Workshop Guide** 🎉

Thank you for participating! We're excited to see what you build with your new RAG systems. Remember: research is iterative, and so is RAG development. Don't hesitate to experiment and ask Claude for help along the way!
