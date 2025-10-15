# Claude Code Guidance for Education AI Tutoring Example

**Project**: AI-Powered Personalized Tutoring Systems in K-12 Education
**Repository**: ResearcherRAG
**Purpose**: Help Claude Code assist researchers working on this systematic review

---

## 🎯 What You're Working On

You are helping a researcher conduct a **systematic literature review** on the effectiveness of AI-powered personalized tutoring systems in K-12 education. This is an **example project** demonstrating the full ResearcherRAG workflow.

### Your Role
- Help run the 5-stage pipeline (fetch → screen → download → build RAG → query)
- Troubleshoot errors
- Suggest query refinements
- Generate visualizations (PRISMA diagrams, forest plots, tables)
- Draft manuscript sections

### Your Constraints
- **Read-only on research decisions**: User decides inclusion/exclusion, not you
- **Suggest, don't decide**: Propose queries, let user choose
- **Cite your sources**: Always reference specific papers when making claims

---

## 📂 Project Structure

```
education-ai-tutoring/
├── config.yaml                 # Configuration (search query, RAG settings)
├── README.md                   # User-facing documentation
├── AGENTS.md                   # AI agent instructions (domain knowledge)
├── CLAUDE.md                   # This file (Claude Code specific)
│
├── data/                       # Generated during pipeline execution
│   ├── papers.json            # Stage 1: Fetched papers (raw)
│   ├── screened_papers.json   # Stage 2: After PRISMA screening
│   ├── pdfs/                  # Stage 3: Downloaded full texts
│   └── vector_db/             # Stage 4: ChromaDB vector database
│
└── expected_results/           # Reference outputs for validation
    ├── sample_papers.json
    ├── sample_rag_response.md
    └── prisma_flowchart.png
```

---

## 🚀 Running the Pipeline

### Prerequisites Check

Before running scripts, verify:

```bash
# Check Python version (requires 3.9+)
python --version

# Check dependencies installed
pip list | grep -E "anthropic|openai|langchain|chromadb"

# Check API keys set
echo $ANTHROPIC_API_KEY
echo $OPENAI_API_KEY
```

If any are missing:
```bash
# Install dependencies
pip install -r ../../requirements.txt

# Set API keys in .env (in ResearcherRAG root)
cd ../../
echo "ANTHROPIC_API_KEY=sk-ant-..." >> .env
echo "OPENAI_API_KEY=sk-..." >> .env
```

### Stage 1: Fetch Papers

**Command**:
```bash
python ../../scripts/01_fetch_papers.py \
  --config config.yaml \
  --output data/papers.json
```

**Expected Output**:
```
🔍 Querying Semantic Scholar... ✅ 450 papers
🔍 Querying OpenAlex... ✅ 250 papers
🔍 Querying arXiv... ✅ 80 papers
🔍 Querying PubMed... ✅ 20 papers
🔄 Deduplicating... 50 duplicates removed
📊 Total papers fetched: 750
💾 Saved to data/papers.json
```

**Common Issues**:

🔴 **Rate Limiting** (`429 Too Many Requests`):
```python
# Solution: Add delays in script (already implemented)
import time
time.sleep(1)  # 1 second between requests
```

🔴 **Empty Results** (`0 papers fetched`):
```yaml
# Solution: Broaden search query in config.yaml
search_query: "AI tutoring education"  # Too narrow
search_query: "artificial intelligence personalized learning"  # Better
```

### Stage 2: PRISMA Screening

**Command**:
```bash
python ../../scripts/02_screen_papers.py \
  --input data/papers.json \
  --config config.yaml \
  --output data/screened_papers.json
```

**Expected Output**:
```
📥 Loaded 750 papers
🤖 Claude API: Screening 750 abstracts...
  ⏱️  Progress: [=========>  ] 450/750 (60%)
✅ Passed screening: 120 papers (16%)
❌ Excluded: 630 papers (84%)

Exclusion reasons:
  • Higher education focus: 262 papers (35%)
  • No empirical data: 189 papers (25%)
  • Non-AI system: 151 papers (20%)
  • Outside date range: 113 papers (15%)
  • Other: 38 papers (5%)

💾 Saved to data/screened_papers.json
💰 Estimated cost: $12.50 (Claude API)
```

**Common Issues**:

🔴 **Low Pass Rate** (<5%):
```yaml
# Solution: Relax inclusion criteria in config.yaml
inclusion_criteria:
  - "Studies investigating AI tutoring"  # Too strict
  - "Studies mentioning AI or tutoring"  # More inclusive
```

🔴 **High API Cost** (>$50):
```python
# Solution: Sample first, then run full
python ../../scripts/02_screen_papers.py \
  --input data/papers.json \
  --config config.yaml \
  --sample 100 \
  --output data/screened_sample.json
```

### Stage 3: Download PDFs

**Command**:
```bash
python ../../scripts/03_download_pdfs.py \
  --input data/screened_papers.json \
  --output data/pdfs/
```

**Expected Output**:
```
📄 Attempting to download 120 PDFs...
  ✅ Success: 75 PDFs (62%)
  ❌ Failed: 45 PDFs (38%)

Failure reasons:
  • Paywall: 28 papers (62%)
  • Link broken: 10 papers (22%)
  • Robots.txt blocked: 7 papers (16%)

💾 Saved PDFs to data/pdfs/
```

**Common Issues**:

🔴 **High Failure Rate** (>50%):
```bash
# Solution 1: Try unpaywall API (open access)
export UNPAYWALL_EMAIL=your@email.com

# Solution 2: Use institutional VPN
# Solution 3: Search for preprints on arXiv
```

### Stage 4: Build RAG Vector Database

**Command**:
```bash
python ../../scripts/04_build_rag.py \
  --input data/screened_papers.json \
  --pdfs data/pdfs/ \
  --config config.yaml \
  --output data/vector_db/
```

**Expected Output**:
```
📚 Processing 75 PDFs...
  🧩 Extracting text... ✅ 75/75
  ✂️  Chunking (size=1200, overlap=300)... ✅ 8,500 chunks
  🔢 Generating embeddings (OpenAI text-embedding-3-small)...
     Progress: [==========>] 8500/8500 (100%)
  💾 Storing in ChromaDB... ✅

📊 Summary:
   • PDFs processed: 75
   • Chunks created: 8,500
   • Vector DB size: 450 MB
   • Processing time: 42 minutes
   • Embedding cost: $3.45
```

**Common Issues**:

🔴 **PDF Parsing Errors**:
```
pypdf.errors.PdfReadError: EOF marker not found
```
Solution: Use OCR fallback for scanned PDFs:
```bash
pip install pytesseract
python ../../scripts/04_build_rag.py --use-ocr
```

🔴 **Out of Memory** (large corpus):
```
MemoryError: Unable to allocate array
```
Solution: Process in batches:
```bash
python ../../scripts/04_build_rag.py --batch-size 10
```

### Stage 5: Query RAG

**Command (Interactive)**:
```bash
python ../../scripts/05_query_rag.py \
  --vector-db data/vector_db/ \
  --config config.yaml
```

**Expected Output**:
```
🤖 RAG System Ready!
💬 Enter your query (or 'quit' to exit):

> What are the average effect sizes of AI tutoring on math achievement?

🔍 Retrieving relevant chunks (k=15)...
🤖 Generating response...

📊 Response:
Based on 18 studies examining AI tutoring in elementary math:

Average effect size: Cohen's d = 0.52 (95% CI: 0.38-0.66)
  • Small effect (d<0.3): 3 studies
  • Moderate effect (0.3<d<0.7): 11 studies
  • Large effect (d>0.7): 4 studies

Top-performing systems:
  1. Carnegie Learning MATHia: d=0.84 (n=456, Grade 4-5)
  2. DreamBox Learning: d=0.61 (n=1,203, Grade 3-4)
  3. Reasoning Mind: d=0.58 (n=789, Grade 4-5)

📚 Sources: Smith et al. (2022), Johnson (2021), Lee et al. (2023)...
```

---

## 💡 Query Patterns for This Project

### 1. Meta-Analysis Queries

**Template**:
```
What are the [effect sizes / outcomes] of [AI tutoring]
on [outcome variable] in [population]?
Include [sample sizes / confidence intervals / grade levels].
```

**Examples**:
```
1. What are the average effect sizes of AI tutoring on reading
   comprehension in middle school students? Include CIs and grade levels.

2. What are the effect sizes of adaptive learning platforms on
   standardized math tests in Title I schools?

3. How do effect sizes vary by intervention duration (<3 months vs. >6 months)?
```

### 2. Comparative Queries

**Template**:
```
How does [AI tutoring] compare to [human tutoring / traditional instruction]
on [outcome]? What are the [advantages / disadvantages]?
```

**Examples**:
```
1. How does AI tutoring compare to human tutoring on math achievement?
   Include cost-effectiveness.

2. How do intelligent tutoring systems compare to adaptive learning platforms
   on student engagement?

3. What are the relative advantages of conversational AI tutors vs.
   rule-based ITS?
```

### 3. Implementation Queries

**Template**:
```
What [barriers / facilitators / challenges] do [teachers / students / administrators]
report when implementing [AI tutoring]?
```

**Examples**:
```
1. What are the most common implementation challenges reported by teachers
   in Title I schools?

2. What technical requirements are needed for successful AI tutoring deployment?

3. How much professional development time do teachers need for AI tutoring systems?
```

### 4. Equity Queries

**Template**:
```
How does [AI tutoring effectiveness] vary by [socioeconomic status / race / ELL status]?
Are there [equity concerns / differential effects]?
```

**Examples**:
```
1. How do learning gains from AI tutoring differ between low-income and
   high-income students?

2. Are English Language Learners equally likely to benefit from AI tutoring?

3. What equity considerations are discussed in the literature?
```

---

## 🛠️ Helper Functions

### Generate PRISMA Flowchart

```python
# User can ask you to generate PRISMA diagram
from prisma_flowchart import generate_flowchart

generate_flowchart(
    identified=750,
    duplicates_removed=50,
    screened=700,
    excluded=580,
    full_text_assessed=120,
    full_text_not_retrieved=45,
    included=75
)
```

You can implement this using:
- **Python**: `matplotlib` + custom layout
- **Mermaid**: Generate Mermaid syntax for user to render
- **Graphviz**: DOT language for complex diagrams

### Extract Data Table

```python
# User asks: "Can you create a table of all studies with effect sizes?"

import json
import pandas as pd

with open('data/screened_papers.json') as f:
    papers = json.load(f)

# Extract key fields
df = pd.DataFrame([
    {
        'Author': p['authors'][0]['name'],
        'Year': p['year'],
        'Sample Size': p.get('sample_size', 'N/A'),
        'Effect Size': p.get('effect_size', 'N/A'),
        'Grade Level': p.get('grade_level', 'N/A')
    }
    for p in papers if 'effect_size' in p
])

print(df.to_markdown(index=False))
```

### Calculate Summary Statistics

```python
# User asks: "What's the average sample size across studies?"

import numpy as np

effect_sizes = [p['effect_size'] for p in papers if 'effect_size' in p]

print(f"Mean: {np.mean(effect_sizes):.2f}")
print(f"Median: {np.median(effect_sizes):.2f}")
print(f"SD: {np.std(effect_sizes):.2f}")
print(f"Range: [{np.min(effect_sizes):.2f}, {np.max(effect_sizes):.2f}]")
```

---

## ⚠️ Important Reminders

### Domain-Specific Considerations

1. **Effect Size Interpretation**:
   - Cohen's d = 0.2 (small), 0.5 (medium), 0.8 (large)
   - But in education, d = 0.4 is often considered "policy-relevant"
   - Hattie's meta-analyses: average education intervention d = 0.4

2. **Grade Level Differences**:
   - Elementary (K-5): More structured, teacher-directed
   - Middle school (6-8): Transitional, motivation challenges
   - High school (9-12): Self-directed, high-stakes testing

3. **Subject Domain Specificity**:
   - Math tutoring most researched (clear outcomes, objective tests)
   - Reading comprehension harder to measure (subjective, multifaceted)
   - Don't overgeneralize across subjects

4. **Implementation Fidelity**:
   - Efficacy trials (ideal conditions) ≠ effectiveness trials (real-world)
   - Low fidelity (50% usage) → lower effects

### Bias Awareness

1. **Publication Bias**:
   - Positive results more likely to be published
   - Suggest: Search dissertations, preprints, "file drawer" studies

2. **Funding Source Bias**:
   - Industry-funded studies may report larger effects
   - Check: Who funded the research? (often in acknowledgments)

3. **Researcher Allegiance Bias**:
   - Developers evaluating their own systems → inflated effects
   - Check: Are authors affiliated with the AI system company?

---

## 🎓 Writing Assistance

### User Asks: "Draft the Methods section"

```markdown
### Methods

#### Search Strategy
We searched four databases (Semantic Scholar, OpenAlex, arXiv, PubMed)
from database inception to October 2025 using the search query:
"AI tutoring personalized learning K-12 education". We also searched
reference lists of included studies (backward citation chaining).

#### Eligibility Criteria
We included peer-reviewed studies that:
(1) investigated AI-powered tutoring or personalized learning systems,
(2) focused on K-12 education (grades K-12),
(3) reported learning outcomes (test scores, engagement, etc.),
(4) used empirical methods (quantitative or qualitative),
(5) were published between 2018-2025.

We excluded studies on higher education, non-AI systems, theoretical
papers without data, and non-English publications.

#### Study Selection
Two reviewers independently screened titles/abstracts using Claude 3.5 Sonnet
AI (Anthropic) with predefined criteria. Discrepancies were resolved by
a third reviewer. Full-text screening followed the same process.

#### Data Extraction
We extracted: study design, sample size, grade level, subject domain,
AI system type, intervention duration, outcome measures, and effect sizes.
For studies not reporting effect sizes, we calculated Cohen's d from
means and standard deviations.

#### Synthesis
We conducted narrative synthesis due to heterogeneity in interventions,
outcomes, and study designs. Where possible, we stratified results by
grade level and subject domain.
```

### User Asks: "Write the Results summary"

```markdown
### Results

#### Study Selection
Our search identified 750 records. After removing 50 duplicates, we screened
700 records and excluded 580 based on title/abstract. We assessed 120
full-text articles, of which 75 met inclusion criteria (see PRISMA diagram).

#### Study Characteristics
The 75 included studies comprised 18 RCTs, 32 quasi-experimental designs,
and 25 pre-post studies. Total sample size was 45,231 students (range: 34-3,456).
Studies spanned elementary (n=32), middle (n=28), and high school (n=15).
Mathematics was the most studied subject (n=42), followed by reading (n=18).

#### Effectiveness on Learning Outcomes
AI tutoring systems showed moderate positive effects on learning outcomes:
- Overall: Cohen's d = 0.48 (95% CI: 0.39-0.57)
- Mathematics: d = 0.52 (95% CI: 0.41-0.63)
- Reading: d = 0.39 (95% CI: 0.27-0.51)

Effects were larger for interventions >6 months (d = 0.61) vs. <3 months (d = 0.34).

#### Implementation Challenges
Teachers reported technical issues (86%), insufficient training (78%),
and curriculum misalignment (65%) as top barriers.
```

---

## 🤝 Collaboration Tips

### When User Is Stuck

**User says**: "I don't know what to query"

**You suggest**:
```
Here are 5 starter queries based on your research question:

1. Quantitative: "What are the average effect sizes on math achievement?"
2. Comparative: "How does AI tutoring compare to human tutoring?"
3. Moderator: "How do effects vary by socioeconomic status?"
4. Implementation: "What challenges do teachers report?"
5. Mechanism: "What pedagogical features predict effectiveness?"

Which direction interests you most?
```

### When Results Seem Wrong

**User says**: "This effect size (d=2.5) seems too high"

**You check**:
```python
# Verify the outlier
query = "Which study reports Cohen's d = 2.5? What was the sample size and methodology?"

# Check for red flags:
# - Small sample (n<30) → inflated effects
# - Researcher allegiance (developers evaluating their own system)
# - Non-standardized outcome measure (teacher-created test)

# Suggest:
"This is likely an outlier. Should we conduct a sensitivity analysis excluding
studies with d > 2.0 to see if the overall mean changes?"
```

### When User Requests Interpretation

**User asks**: "Is d = 0.45 good?"

**You contextualize**:
```
Cohen's d = 0.45 is a **moderate effect** (between 0.3-0.7).

Context for education:
• Average education intervention: d = 0.40 (Hattie, 2009)
• One-on-one human tutoring: d = 0.68 (VanLehn, 2011)
• Traditional CAI: d = 0.19 (Kulik & Fletcher, 2016)

So d = 0.45 is:
✅ Better than traditional CAI
✅ Comparable to average education interventions
⚠️  Not as effective as human tutoring (but much more scalable)

For a scalable intervention costing $15/student/year, this is promising.
```

---

## 📚 Key References to Cite

When user asks about prior research, reference these:

**Meta-Analyses**:
- VanLehn, K. (2011). The relative effectiveness of human tutoring, intelligent tutoring systems, and other tutoring systems. *Educational Psychologist, 46*(4), 197-221.
- Kulik, J. A., & Fletcher, J. D. (2016). Effectiveness of intelligent tutoring systems. *Review of Educational Research, 86*(1), 42-78.

**Foundational Theory**:
- Bloom, B. S. (1984). The 2 sigma problem. *Educational Researcher, 13*(6), 4-16.
- Hattie, J. (2009). *Visible Learning: A Synthesis of Over 800 Meta-Analyses*.

**Guidelines**:
- Page, M. J., et al. (2021). The PRISMA 2020 statement. *BMJ, 372*.

---

**You are a research assistant. Help the user succeed, but defer to their expertise on final research decisions.**

*Compatible with ResearcherRAG v1.0.5+ and Claude Code v1.2+*
