# Stage 6: Research Conversation

**Load when**: Stage 6 prompt or RAG system built

**Duration**: Ongoing (hours to weeks)

**Goal**: Use RAG to extract insights, answer research questions

---

## Quick Overview

**7 Research Scenarios**:

| Scenario | Purpose | Example Query | Output |
|----------|---------|---------------|--------|
| **overview** | High-level themes | "What are main themes?" | Narrative summary |
| **hypothesis** | Evidence validation | "Does X improve Y?" | For/against with effect sizes |
| **statistics** | Data extraction | "Extract all correlations" | CSV table |
| **methods** | Methodology comparison | "What RCT designs used?" | Method taxonomy |
| **contradictions** | Conflict detection | "Where do findings disagree?" | Contradiction analysis |
| **policy** | Practice translation | "What should policymakers do?" | Recommendations |
| **grant** | Future research | "What gaps remain?" | Research proposals |

---

## Conversation Flow by Scenario

### Scenario 1: Overview (Thematic Analysis)

**User query**: "What are the main themes in chatbot research for speaking skills?"

**Your action**: Run RAG query, synthesize themes

```python
# Query RAG
results = query_rag(
    project="projects/2025-10-24_AI-Chatbots",
    query="What are the main themes, findings, and approaches in AI chatbot research for improving speaking skills?",
    top_k=10
)

# Synthesize themes
YOU: "Based on 50 papers in your RAG database, I've identified 5 main themes:

**Theme 1: Feedback Mechanisms** (mentioned in 34 papers)
- Real-time pronunciation feedback via ASR
- Corrective feedback vs implicit feedback
- Multimodal feedback (text + audio + visual)
【F:pdfs/0023_Chen_2022.pdf†L145】【F:pdfs/0045_Garcia_2023.pdf†L89】

**Theme 2: Speaking Practice Types** (28 papers)
- Scripted dialogues vs free conversation
- Role-play scenarios
- Task-based interactions
【F:pdfs/0012_Kim_2021.pdf†L234】【F:pdfs/0037_Rodriguez_2023.pdf†L67】

**Theme 3: Learner Anxiety Reduction** (22 papers)
- Less anxiety vs human partners
- Willingness to communicate increased
- Safe practice environment
【F:pdfs/0008_Lee_2020.pdf†L178】【F:pdfs/0029_Taylor_2022.pdf†L203】

**Theme 4: Personalization & Adaptation** (19 papers)
- Difficulty adjustment based on proficiency
- Topic selection based on interests
- Pacing adapted to learner needs
【F:pdfs/0041_Zhang_2023.pdf†L156】

**Theme 5: Measurement Approaches** (all 50 papers)
- Pre-post test designs (40 papers)
- Automated speaking assessment tools (15 papers)
- Human rater evaluations (35 papers)

Would you like me to dive deeper into any theme?"
```

### Scenario 2: Hypothesis Testing

**User query**: "Does chatbot practice improve speaking proficiency more than human tutors?"

**Your action**: Extract comparative studies, synthesize evidence

```python
YOU: "I've searched for comparative studies (chatbot vs human tutor). Here's the evidence:

**Papers with Direct Comparison**: 8 studies found

**FOR (Chatbots outperform or equal to human tutors)**: 5 studies
1. Chen et al. (2022): Chatbot group (d=0.68) > Human tutor group (d=0.52) on pronunciation accuracy
   【F:pdfs/0023_Chen_2022.pdf†L289】
2. Garcia (2023): No significant difference (p=0.23) - chatbot equivalent to human tutor
   【F:pdfs/0045_Garcia_2023.pdf†L134】
3. Kim & Park (2021): Chatbot superior for anxiety reduction (η²=0.41 vs 0.18)
   【F:pdfs/0012_Kim_2021.pdf†L267】
4. Rodriguez (2023): Chatbot better for practice quantity (5.2 hours/week vs 2.1 hours/week)
   【F:pdfs/0037_Rodriguez_2023.pdf†L198】
5. Taylor (2022): Chatbot equivalent on fluency (d=0.45 vs d=0.49, not significant)
   【F:pdfs/0029_Taylor_2022.pdf†L223】

**AGAINST (Human tutors outperform chatbots)**: 3 studies
1. Lee et al. (2020): Human tutor superior on pragmatic competence (d=0.89 vs 0.34)
   【F:pdfs/0008_Lee_2020.pdf†L201】
2. Zhang (2023): Human tutor better for complex grammar correction (76% vs 58% accuracy)
   【F:pdfs/0041_Zhang_2023.pdf†L178】
3. Brown (2021): Human tutor advantages in cultural context teaching
   【F:pdfs/0018_Brown_2021.pdf†L145】

**SYNTHESIS**:
- ✅ Chatbots excel at: Pronunciation, fluency practice, anxiety reduction, practice quantity
- ✅ Human tutors excel at: Pragmatics, complex grammar, cultural nuances
- ⚖️ No difference: Basic speaking proficiency gains (when measured by standardized tests)

**Recommendation**: Blended approach - chatbot for frequent practice + human tutor for complex skills

**Limitations**:
- Small sample (8 comparative studies)
- Heterogeneous outcome measures
- Potential publication bias (positive results more likely published)

Would you like me to extract effect sizes for meta-analysis?"
```

### Scenario 3: Statistical Extraction

**User query**: "Extract all correlation coefficients between chatbot use frequency and speaking scores"

**Your action**: Search for statistical tables, extract to CSV

```python
YOU: "I've extracted correlation data from papers reporting frequency-outcome relationships:

**Correlation Extraction Results** (12 papers with correlations):

| Study | Sample Size | Frequency Measure | Outcome Measure | r | p-value | Citation |
|-------|-------------|-------------------|-----------------|---|---------|----------|
| Chen 2022 | 156 | Hours/week | TOEFL Speaking | 0.62 | <.001 | 【F:pdfs/0023_Chen_2022.pdf†L312】 |
| Garcia 2023 | 89 | Sessions/month | Pronunciation | 0.54 | .002 | 【F:pdfs/0045_Garcia_2023.pdf†L167】 |
| Kim 2021 | 203 | Total interactions | Fluency WPM | 0.48 | <.001 | 【F:pdfs/0012_Kim_2021.pdf†L289】 |
| Rodriguez 2023 | 67 | Minutes/session | Oral accuracy | 0.71 | <.001 | 【F:pdfs/0037_Rodriguez_2023.pdf†L234】 |
| Taylor 2022 | 124 | Weeks of use | Speaking confidence | 0.39 | .008 | 【F:pdfs/0029_Taylor_2022.pdf†L256】 |
| Lee 2020 | 178 | Total prompts | IELTS Speaking | 0.44 | .001 | 【F:pdfs/0008_Lee_2020.pdf†L223】 |
| Zhang 2023 | 95 | Days active | Pronunciation score | 0.58 | <.001 | 【F:pdfs/0041_Zhang_2023.pdf†L198】 |
| Brown 2021 | 112 | Practice hours | Speaking test | 0.51 | .003 | 【F:pdfs/0018_Brown_2021.pdf†L178】 |
| Smith 2022 | 143 | Messages sent | Oral fluency | 0.46 | .002 | 【F:pdfs/0034_Smith_2022.pdf†L201】 |
| Johnson 2023 | 201 | Session frequency | Speaking gains | 0.63 | <.001 | 【F:pdfs/0027_Johnson_2023.pdf†L267】 |
| Wang 2021 | 88 | Total time | TOEIC Speaking | 0.55 | .001 | 【F:pdfs/0015_Wang_2021.pdf†L189】 |
| Martinez 2022 | 76 | Weeks enrolled | Speaking proficiency | 0.49 | .006 | 【F:pdfs/0039_Martinez_2022.pdf†L145】 |

**Summary Statistics**:
- **Mean r**: 0.53 (medium-large effect)
- **Range**: 0.39 - 0.71
- **All significant**: p < .01
- **Total participants**: 1,532 learners

**Interpretation**: Consistent moderate-to-strong positive correlation between practice frequency and speaking outcomes across all studies.

**Saved to**: projects/2025-10-24_AI-Chatbots/outputs/correlation_extraction.csv

Would you like me to calculate a meta-analytic correlation (Fisher's Z transformation)?"
```

### Scenario 4: Methodology Comparison

**User query**: "What research designs were used? Which is most common?"

**Your action**: Extract methodology info, create taxonomy

```python
YOU: "Methodology breakdown across 50 papers:

**Research Designs**:

**RCT (Randomized Controlled Trial)**: 12 papers (24%)
- Gold standard for causal claims
- Chatbot group vs control (no intervention) or comparison (traditional instruction)
- Example: Chen et al. (2022) - 3 groups (chatbot, human tutor, control) 【F:pdfs/0023_Chen_2022.pdf†L89】

**Quasi-Experimental**: 18 papers (36%) ⭐ MOST COMMON
- Non-random assignment (intact classes, convenience sampling)
- Pre-post design with comparison group
- Example: Garcia (2023) - Two university classes, one with chatbot 【F:pdfs/0045_Garcia_2023.pdf†L67】

**Single-Group Pre-Post**: 15 papers (30%)
- No control/comparison group
- Measures gains within same group
- Example: Kim & Park (2021) - 8-week intervention, pre/post tests 【F:pdfs/0012_Kim_2021.pdf†L134】

**Correlational**: 5 papers (10%)
- No intervention, observes natural variation
- Correlates usage patterns with outcomes
- Example: Rodriguez (2023) - Self-selected chatbot use over semester 【F:pdfs/0037_Rodriguez_2023.pdf†L156】

**Measurement Approaches** (can overlap):
- **Standardized tests** (TOEFL, IELTS, TOEIC): 28 papers (56%)
- **Human rater evaluation**: 35 papers (70%)
- **Automated ASR scoring**: 15 papers (30%)
- **Self-report** (confidence, anxiety): 22 papers (44%)

**Duration**:
- < 4 weeks: 8 papers (short-term)
- 4-12 weeks: 32 papers (medium-term) ⭐ MOST COMMON
- > 12 weeks: 10 papers (longitudinal)

**Recommendation for your review**:
Focus on quasi-experimental + RCT studies (30 papers) for strongest causal evidence.

Would you like quality assessment (risk of bias analysis)?"
```

### Scenario 5: Contradiction Detection

**User query**: "Where do findings contradict each other?"

**Your action**: Identify conflicting results, explain discrepancies

```python
YOU: "I've identified 3 key contradictions in the literature:

**CONTRADICTION 1: Feedback Type**
- **Pro-corrective feedback**: Chen et al. (2022) found explicit corrective feedback improved accuracy more than implicit recast (d=0.74 vs 0.43) 【F:pdfs/0023_Chen_2022.pdf†L245】
- **Pro-implicit feedback**: Taylor (2022) found recasts superior - explicit correction increased anxiety, reduced fluency (d=0.29 vs 0.61) 【F:pdfs/0029_Taylor_2022.pdf†L289】

**Possible explanation**:
- Chen studied pronunciation (discrete, teachable)
- Taylor studied fluency (flow, confidence-dependent)
- **Implication**: Feedback type should match skill target

**CONTRADICTION 2: Practice Duration**
- **Long sessions better**: Rodriguez (2023) found 30-min sessions superior to 10-min (r=0.71 vs 0.34) 【F:pdfs/0037_Rodriguez_2023.pdf†L267】
- **Short sessions better**: Lee (2020) found 10-min sessions showed higher retention, less fatigue (completion rate 89% vs 56%) 【F:pdfs/0008_Lee_2020.pdf†L234】

**Possible explanation**:
- Rodriguez measured immediate gains (within-session)
- Lee measured long-term adherence (across semester)
- **Implication**: Trade-off between intensity and sustainability

**CONTRADICTION 3: Learner Proficiency Level**
- **Benefits all levels**: Garcia (2023) found no interaction between proficiency and gains (F=0.87, p=.43) 【F:pdfs/0045_Garcia_2023.pdf†L198】
- **Benefits beginners only**: Zhang (2023) found effect only for A1-A2 learners (d=0.89), not B1+ learners (d=0.12, ns) 【F:pdfs/0041_Zhang_2023.pdf†L223】

**Possible explanation**:
- Garcia used adaptive chatbot (difficulty adjusted)
- Zhang used fixed-difficulty chatbot (too easy for advanced)
- **Implication**: Personalization critical for advanced learners

**Recommendation**:
- Flag these contradictions in your discussion section
- Propose moderator variables for meta-analysis
- Suggest future RCTs to resolve discrepancies

Would you like me to search for moderators (e.g., proficiency level subgroup analysis)?"
```

---

## Common Query Templates

### Extract Effect Sizes
```
"Extract all effect sizes (Cohen's d, r, η²) for speaking proficiency outcomes"
```

### Find Gaps
```
"What populations, contexts, or outcomes are underresearched?"
```

### Synthesize Mechanisms
```
"How do researchers explain WHY chatbots improve speaking? What theoretical mechanisms?"
```

### Compare Interventions
```
"Compare pronunciation-focused vs fluency-focused chatbots. Which is more effective?"
```

---

## Citation Format

**ALL answers must include citations**:
- Format: 【F:path/to/pdf.pdf†L123】
- Multiple citations: 【F:pdf1.pdf†L45】【F:pdf2.pdf†L67】
- Page ranges: 【F:pdf.pdf†L45-L67】

**Validation**: Check that every factual claim has a citation

---

## Completion

**Stage 6 is ongoing** - researcher continues querying RAG until satisfied

**When ready for Stage 7**: User says "I'm done with analysis, let's document this"

---

## Next Stage

[skills/claude_only/stage7_documentation.md](stage7_documentation.md)

---

**Version**: 2.0 | **Token Budget**: ~450 lines
