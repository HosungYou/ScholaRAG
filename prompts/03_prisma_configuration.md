# Stage 3: PRISMA Configuration Prompt

After completing Stage 1 (Research Domain Setup) and Stage 2 (Query Strategy), use this prompt to configure your PRISMA systematic review pipeline:

---

I've collected papers using our search query. Now I need help configuring PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) screening.

**Papers Collected**: [number] papers from [data source(s)]
**Saved at**: `data/raw/papers_metadata.csv`

Please help me:
1. Analyze the paper metadata (year distribution, keywords, methodologies)
2. Generate a research profile (YAML configuration) with appropriate keywords and weights
3. Set reasonable thresholds for each PRISMA stage
4. Create and run the PRISMA screening pipeline

---

## What Claude Code Will Do

Claude will guide you through building a customized PRISMA configuration:

1. **Analyze Metadata**: Extract patterns from collected papers
2. **Propose Keywords**: Domain, method, topic keywords with weights
3. **Set Thresholds**: Screening, eligibility, and inclusion cutoffs
4. **Generate Code**: Python script to run PRISMA pipeline
5. **Interpret Results**: Explain pass rates and suggest adjustments

---

## PRISMA Overview

PRISMA 2020 consists of 4 stages:

```
Stage 1: Identification
├─ Records identified from database (X papers)
└─ Records after duplicates removed (Y papers)
    ↓
Stage 2: Screening (Title/Abstract)
├─ Records screened (Y papers)
├─ Records excluded (too low relevance score)
└─ Records passing to eligibility (Z papers)
    ↓
Stage 3: Eligibility (Detailed Assessment)
├─ Records assessed for eligibility (Z papers)
├─ Records excluded (detailed screening)
├─ Records needing manual review (borderline scores)
└─ Records eligible (W papers)
    ↓
Stage 4: Inclusion
└─ Studies included in synthesis (W papers)
```

---

## Multi-Dimensional Scoring System

Your papers will be scored across 6 dimensions:

### 1. Domain Match (0-10 points)
**Keywords**: Core research domain
- Example (Education): "education", "learning", "pedagogy"
- Example (Medicine): "clinical", "patient", "treatment"

**Scoring**:
- 10 points: Perfect match (3+ domain keywords)
- 7-9 points: Good match (2 domain keywords)
- 4-6 points: Moderate match (1 domain keyword)
- 0-3 points: Poor match (no domain keywords)

---

### 2. Method Match (0-5 points)
**Keywords**: Research methodology
- Example: "RCT", "randomized", "experimental", "survey"

**Scoring**:
- 5 points: Preferred method (e.g., RCT)
- 3-4 points: Acceptable method (e.g., quasi-experimental)
- 1-2 points: Weak method (e.g., case study)
- 0 points: No method mentioned

---

### 3. Topic Match (0-5 points)
**Keywords**: Specific research focus
- Example: "chatbot", "learning outcomes", "engagement"

**Scoring**:
- 5 points: Highly relevant (3+ topic keywords)
- 3-4 points: Relevant (2 topic keywords)
- 1-2 points: Somewhat relevant (1 topic keyword)
- 0 points: Not relevant

---

### 4. Context Match (0-10 points)
**Keywords**: Research context/outcomes
- Example: "effectiveness", "impact", "performance"

**Scoring**:
- 10 points: Perfect context (strong outcomes focus)
- 7-9 points: Good context
- 4-6 points: Moderate context
- 0-3 points: Poor context

---

### 5. Exclusion Penalty (-20 to 0 points)
**Keywords**: Papers to exclude
- Example: "K-12" (if focusing on higher education)
- Example: "animal study" (if human-only research)

**Scoring**:
- -20 points: Hard exclusion (automatically fails)
- -10 points: Strong exclusion
- -5 points: Soft exclusion
- 0 points: No exclusion keywords

---

### 6. Title Bonus (0 or 10 points)
**Logic**: Keywords in title are stronger signals than in abstract

**Scoring**:
- +10 points: Domain keyword appears in title
- 0 points: No domain keyword in title

---

## Total Score Calculation

```
Total Score =
  Domain Match (0-10) +
  Method Match (0-5) +
  Topic Match (0-5) +
  Context Match (0-10) +
  Exclusion Penalty (-20 to 0) +
  Title Bonus (0 or 10)

Range: -20 to 50 points
```

---

## Threshold Settings

### Recommended Thresholds

| Stage | Threshold | Expected Pass Rate | Purpose |
|-------|-----------|-------------------|---------|
| **Screening** | 25 points | 50-60% | Remove obviously irrelevant |
| **Eligibility** | 45 points | 20-30% | High-quality papers only |
| **Review Queue** | 35-44 points | 10-15% | Manual review needed |
| **Auto-include** | 50 points | 5-10% | Perfect matches |

### How to Adjust

**If too many papers pass (>70%)**:
- Increase screening threshold (25 → 30)
- Add more exclusion keywords
- Increase method/topic weights

**If too few papers pass (<20%)**:
- Decrease screening threshold (25 → 20)
- Remove or soften exclusion keywords
- Add more inclusive domain keywords

---

## Research Profile Template

Claude will generate a YAML file like this:

```yaml
name: "Your Research Project Name"
description: "Brief description of research focus"

# Domain keywords (max weight: 10)
domain_keywords:
  - keyword1: 10
  - keyword2: 9
  - keyword3: 8

# Method keywords (max weight: 5)
method_keywords:
  - experimental: 5
  - RCT: 5
  - survey: 3

# Topic keywords (max weight: 5)
topic_keywords:
  - topic1: 5
  - topic2: 4
  - topic3: 3

# Context keywords (max weight: 10)
context_keywords:
  - effectiveness: 10
  - impact: 9
  - outcomes: 8

# Exclusion keywords (negative weights)
exclusion_keywords:
  - exclude1: -20  # Hard exclusion
  - exclude2: -10  # Strong exclusion
  - exclude3: -5   # Soft exclusion

# Thresholds
thresholds:
  screening: 25        # Stage 2 cutoff
  eligibility: 45      # Stage 3 cutoff
  review_queue: 35     # Manual review needed
  min_inclusion: 50    # Auto-include threshold
```

---

## Example Conversation

### Education Research Example

```
You: "I've collected 568 papers on AI chatbots in language learning.
     Please analyze the metadata and create a PRISMA profile."

Claude: "Let me analyze your papers...

📊 Year Distribution:
   2020-2024: 342 papers (60%)
   2015-2019: 168 papers (30%)
   2010-2014: 58 papers (10%)

📊 Top Keywords (from abstracts):
   - language learning: 423 mentions
   - chatbot: 389
   - conversational agent: 267
   - learning outcomes: 198
   - engagement: 156
   - higher education: 134

📊 Estimated Methodologies:
   - Experimental/RCT: ~234 papers (41%)
   - Survey: ~189 papers (33%)
   - Case study: ~145 papers (26%)

Based on this analysis, I'll create a PRISMA profile optimized for
experimental studies on chatbot language learning in higher education.

[Claude generates YAML file]

With these settings, I estimate:
- Stage 2 pass: ~340 papers (60%)
- Stage 3 pass: ~170 papers (30%)
- Final inclusion: ~115 papers (20%)

Does this align with your research goals?"

You: "Yes, but I'm worried about excluding K-12 studies too harshly.
     Some papers compare K-12 and university settings."

Claude: "Excellent point! That's a common issue in education research.

I'll adjust the exclusion:

BEFORE:
  exclusion_keywords:
    - K-12: -20  # Hard exclusion

AFTER:
  exclusion_keywords:
    - K-12: -5   # Soft exclusion (penalty, not elimination)

This way, papers focused solely on K-12 get penalized, but comparative
studies (K-12 + university) can still pass if they have strong scores
in other dimensions.

New estimates:
- Stage 2 pass: ~380 papers (67%)
- Stage 3 pass: ~195 papers (34%)
- Final inclusion: ~130 papers (23%)

Better?"

You: "Perfect! Let's run the screening."

Claude: "I'll create and run the PRISMA pipeline script now..."

[Claude writes scripts/2_run_prisma.py]

```

---

## Step-by-Step Process

### Step 1: Metadata Analysis (Claude does this)

Claude will read your `data/raw/papers_metadata.csv` and extract:
- Year distribution
- Top 20 keywords from titles/abstracts
- Methodology patterns (based on keyword occurrences)
- Author affiliations (if available)
- Journal/venue patterns

**Example Output**:
```
Analyzing 568 papers...

Year distribution:
  2020-2024: ████████████████ 60%
  2015-2019: ████████ 30%
  2010-2014: ████ 10%

Top keywords:
  1. language learning (423)
  2. chatbot (389)
  3. conversational agent (267)
  ...

Methodologies (estimated from keywords):
  - "experiment/RCT": 234 papers
  - "survey/questionnaire": 189 papers
  - "case study/interview": 145 papers
```

---

### Step 2: Profile Generation (Claude proposes, you adjust)

Claude generates a research profile YAML and explains the reasoning:

```
I've created a profile emphasizing:

1. Domain: Language learning + higher education (high weights)
2. Methods: Experimental studies preferred (RCT=5, survey=3)
3. Topics: Chatbots and learning outcomes (high weights)
4. Exclusions: K-12 softly excluded (-5), children excluded (-10)

Key decisions:
- "chatbot" weighted same as "conversational agent" (synonyms)
- "engagement" lower weight (4) than "learning outcomes" (5)
  because outcomes are more relevant to your RQ
- "higher education" = 7 to prioritize but not hard require
  (some good papers might not mention it explicitly)

Thresholds set conservatively:
- Screening: 25 (expect 60% pass)
- Eligibility: 45 (expect 30% final)
```

**You can adjust**:
- "Can you increase the weight of 'speaking proficiency'? That's my main focus."
- "Let's exclude 'review article' papers (-10 penalty)."
- "What if I lower screening threshold to 20? How many would pass?"

---

### Step 3: Run PRISMA Pipeline

Claude creates `scripts/2_run_prisma.py`:

```python
from backend.core.prisma_pipeline import LiteratureReviewPRISMA
from backend.core.research_profile import ResearchProfile

# Load your custom profile
profile = ResearchProfile.from_yaml(
    "config/research_profiles/your_project.yaml"
)

# Initialize PRISMA pipeline
prisma = LiteratureReviewPRISMA(profile)

# Load papers from CSV
import pandas as pd
papers_df = pd.read_csv("data/raw/papers_metadata.csv")

# Convert to Document format
from langchain.schema import Document
documents = [
    Document(
        page_content=f"{row['title']} {row['abstract']}",
        metadata={
            'title': row['title'],
            'authors': row['authors'],
            'year': row['year'],
            'doi': row['doi']
        }
    )
    for _, row in papers_df.iterrows()
]

# Run PRISMA stages
print("Stage 1: Identification")
stage1 = prisma.stage1_identification(documents)
print(f"  Total collected: {len(stage1.documents)}")

print("\nStage 2: Screening (title/abstract)")
stage2 = prisma.stage2_screening(stage1.documents)
print(f"  Passed: {len(stage2.documents_passed)} ({stage2.pass_rate:.1f}%)")

print("\nStage 3: Eligibility (detailed assessment)")
stage3 = prisma.stage3_eligibility(stage2.documents_passed)
print(f"  Passed: {len(stage3.documents_passed)} ({stage3.pass_rate:.1f}%)")
print(f"  Manual review needed: {len(stage3.review_queue)}")

print("\nStage 4: Inclusion")
stage4 = prisma.stage4_inclusion(stage3.documents_passed)
print(f"  Final included: {len(stage4.documents)}")

# Save results
included_df = pd.DataFrame([
    {
        'title': doc.metadata['title'],
        'authors': doc.metadata['authors'],
        'year': doc.metadata['year'],
        'doi': doc.metadata['doi'],
        'prisma_score': doc.metadata.get('prisma_score', 0)
    }
    for doc in stage4.documents
])
included_df.to_csv("data/processed/included_papers.csv", index=False)

# Save review queue
review_df = pd.DataFrame([
    {
        'title': doc.metadata['title'],
        'prisma_score': doc.metadata.get('prisma_score', 0),
        'reason': 'Borderline score (manual review recommended)'
    }
    for doc in stage3.review_queue
])
review_df.to_csv("data/processed/review_queue.csv", index=False)

print(f"\n✅ PRISMA screening complete!")
print(f"   Included: data/processed/included_papers.csv ({len(included_df)} papers)")
print(f"   Review queue: data/processed/review_queue.csv ({len(review_df)} papers)")
```

---

### Step 4: Review Results

Claude will help you interpret the output:

```
PRISMA Results:

Stage 1: Identification
  Total collected: 568 papers

Stage 2: Screening
  Threshold: ≥25 points
  Passed: 342 papers (60.2%)
  Failed: 226 papers

Stage 3: Eligibility
  Threshold: ≥45 points
  Passed: 139 papers (24.5%)
  Failed: 203 papers
  Manual review: 23 papers (scores 35-44)

Stage 4: Inclusion
  Final included: 139 papers
  Auto-included (score ≥50): 67 papers

📊 Score Distribution:
  50-60 points: ████████ 67 papers (perfect matches)
  45-49 points: ██████ 72 papers (high quality)
  35-44 points: ██ 23 papers (manual review)
  25-34 points: ████████████ 203 papers (borderline, excluded)
  <25 points: ████████████████ 226 papers (clearly irrelevant)

✅ These results look reasonable:
   - 24.5% final inclusion rate (good for focused research)
   - 60% passed initial screening (not too strict)
   - 23 papers need manual review (manageable workload)

Would you like to:
[A] Accept these results and move to Stage 4 (PDF download)
[B] Adjust thresholds and re-run
[C] Review the 23 borderline papers before deciding
[D] See example papers from each score range
```

---

### Step 5: Iterate (if needed)

If results don't match expectations, Claude will help adjust:

```
You: "Only 24.5% inclusion seems low. Can we be less strict?"

Claude: "Let's analyze why papers were excluded:

Top exclusion reasons:
1. Missing experimental methodology (103 papers)
   → These are descriptive/theoretical papers
2. Low topic relevance (67 papers)
   → Mentions chatbots but not language learning
3. K-12 focus (34 papers)
   → Your soft exclusion (-5) is working
4. Older papers (22 papers)
   → Pre-2015 with low scores

Options:
A) Lower eligibility threshold (45 → 40)
   → Would add ~45 papers (mostly surveys)
   → New inclusion rate: 32%

B) Allow non-experimental studies
   → Lower method weight requirement
   → Would add ~80 papers
   → New inclusion rate: 38%

C) Keep current settings
   → 24.5% is actually good for focused research
   → Quality > quantity

Which approach fits your research goals?"

You: "Option C - I want high-quality experimental studies only."

Claude: "Great! Proceeding with 139 papers to Stage 4 (PDF download)."
```

---

## Common Pitfalls & Solutions

### Pitfall 1: Too Many Papers Pass (>80%)
**Problem**: Thresholds too lenient, will read too many irrelevant papers

**Solution**:
```
1. Increase screening threshold (25 → 30 or 35)
2. Add exclusion keywords for irrelevant contexts
3. Increase required method match (experimental only)
```

---

### Pitfall 2: Too Few Papers Pass (<10%)
**Problem**: Thresholds too strict, missing relevant papers

**Solution**:
```
1. Decrease screening threshold (25 → 20 or 15)
2. Remove or soften exclusion keywords
3. Add synonyms for domain/topic keywords
4. Lower method requirements (allow surveys)
```

---

### Pitfall 3: Wrong Papers Passing
**Problem**: High scores but not actually relevant

**Solution**:
```
1. Review high-scoring papers manually (sample 10)
2. Identify why they scored high but are irrelevant
3. Adjust keyword weights or add exclusions
4. Example: "learning" too broad → replace with "language learning"
```

---

### Pitfall 4: Good Papers Failing
**Problem**: Relevant papers getting low scores

**Solution**:
```
1. Check if using synonyms (e.g., "conversational agent" vs "chatbot")
2. Lower title bonus requirement (not all good papers have keywords in title)
3. Check exclusion keywords (might be too aggressive)
4. Review failed papers with scores 20-24 (near threshold)
```

---

## Tips for Success

### 1. Start Conservative
- Use recommended thresholds (25/45) first
- Review sample papers from each score range
- Adjust based on actual content, not just numbers

### 2. Iterate Quickly
- Run screening multiple times with different settings
- Compare results (which papers change categories?)
- Converge on settings that match your judgment

### 3. Use Manual Review Queue
- Don't auto-exclude borderline papers (35-44 points)
- Review them manually (usually 20-50 papers)
- This catches edge cases and improves your profile

### 4. Document Your Decisions
- Keep notes on why you set thresholds
- Explain keyword choices in YAML comments
- This helps with reproducibility and paper writing

### 5. Validate with Pilot Set
- If you know 10-20 papers that SHOULD be included
- Check if they pass your PRISMA screening
- Adjust if good papers are failing

---

## Output Files

After running PRISMA, you'll have:

```
data/
├── raw/
│   └── papers_metadata.csv (568 papers)
├── processed/
│   ├── included_papers.csv (139 papers) ← For Stage 4
│   ├── review_queue.csv (23 papers) ← Manual review
│   ├── excluded_papers.csv (406 papers) ← Reference
│   └── prisma_flow_diagram.png ← Visual summary
└── config/
    └── research_profiles/
        └── your_project.yaml ← Saved configuration
```

---

## Next Steps

Once PRISMA screening is complete:

1. **Review Manual Queue** (if any): Check `data/processed/review_queue.csv`
2. **Move to Stage 4**: [prompts/04_rag_design.md](./04_rag_design.md)
3. **Download PDFs**: Prepare for full-text analysis
4. **Build Vector Database**: Create your RAG system

---

**Estimated Time**: 20-30 minutes (including iterations)
**Prerequisites**: Completed Stage 1-2, collected papers
**Next Stage**: [Stage 4: RAG Design](./04_rag_design.md)
