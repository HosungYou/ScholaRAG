# Stage 1: Research Domain Setup Prompt

Copy and paste this to Claude Code to start your RAG project:

---

I want to build a RAG (Retrieval-Augmented Generation) system for my research project.

**My Research Topic**: [Describe your research topic in 1-2 sentences]

**Research Field**: [e.g., Education, Medicine, Psychology, Economics, Sociology, etc.]

**Research Questions**:
- [Question 1]
- [Question 2]
- [Optional: Question 3]

**Scope Constraints** (if any):
- Year range: [e.g., 2015-2024, or "no constraint"]
- Publication types: [e.g., peer-reviewed only, include preprints, etc.]
- Languages: [e.g., English only, English + Korean, etc.]
- Study designs: [e.g., only experimental, any quantitative, qualitative OK, etc.]

**Existing Knowledge**:
- I've already done some preliminary searches and found approximately [X] papers on this topic
- Key authors/theories I'm aware of: [list if any, or "none yet"]

**My Goal**:
- Final paper count target: [e.g., "50-100 highly relevant papers" or "comprehensive coverage"]
- Intended use: [e.g., literature review chapter, meta-analysis, background research]

**My Technical Background**:
- Programming experience: [None / Basic Python / Comfortable with code]
- RAG/AI experience: [First time / Familiar with concepts / Have built RAG before]

Please help me design an effective literature search strategy and PRISMA systematic review pipeline for this research project.

---

## What Claude Code Will Do

After receiving this prompt, Claude will:

1. Ask clarifying questions about your research scope
2. Suggest domain-specific keywords
3. Estimate expected paper counts
4. Recommend data sources (Semantic Scholar, OpenAlex, arXiv, PubMed, etc.)
5. Move to Stage 2: Query Strategy Design

## Tips

- **Be specific but not too narrow**: "AI chatbots in language learning" is better than just "AI education"
- **Mention methods if important**: If you only want RCTs, say so upfront
- **State year constraints clearly**: Recent reviews may focus on 2015-2024; historical studies may go back further
- **Don't worry about keywords yet**: Claude will help you brainstorm those in the next stage

## Example (Education Research)

```
I want to build a RAG system for my research project.

**My Research Topic**: I'm studying the effectiveness of AI-powered chatbots
in improving speaking proficiency for second language learners in higher
education contexts.

**Research Field**: Education (Applied Linguistics, Educational Technology)

**Research Questions**:
- Do chatbot interventions improve oral fluency, accuracy, and complexity?
- What design features (e.g., corrective feedback, scaffolding) are most effective?
- How do learners perceive chatbot interactions compared to human tutors?

**Scope Constraints**:
- Year range: 2015-2024 (recent developments in neural chatbots)
- Publication types: Peer-reviewed journals and high-quality conferences
- Languages: English only
- Study designs: Prefer experimental/quasi-experimental, but include surveys

**Existing Knowledge**:
- Preliminary Google Scholar search found ~500 papers on "chatbot language learning"
- Aware of key frameworks: Sociocultural theory, CALL (Computer-Assisted Language Learning)

**My Goal**:
- Target: 80-120 highly relevant papers for dissertation lit review
- Intended use: Comprehensive literature review chapter + meta-analysis of effect sizes

**My Technical Background**:
- Programming experience: Basic Python (can run scripts, not comfortable writing from scratch)
- RAG/AI experience: First time with RAG, but have used ChatGPT extensively

Please help me design an effective literature search strategy and PRISMA
systematic review pipeline for this research project.
```

## Example (Medical Research)

```
I want to build a RAG system for my research project.

**My Research Topic**: Impact of electronic health record (EHR) alert fatigue
on physician clinical decision-making and patient safety outcomes.

**Research Field**: Medicine (Clinical Informatics, Patient Safety)

**Research Questions**:
- What is the prevalence and severity of EHR alert fatigue among physicians?
- How does alert fatigue affect clinical decision accuracy and response time?
- What interventions effectively reduce alert fatigue?

**Scope Constraints**:
- Year range: 2010-2024 (EHR adoption timeline)
- Publication types: Peer-reviewed journals, exclude editorials/commentaries
- Languages: English
- Study designs: RCTs, cohort studies, cross-sectional surveys (no case reports)

**Existing Knowledge**:
- PubMed search for "alert fatigue" returns ~1,200 results (too broad)
- Key terms: decision support systems, clinical decision support, alert override

**My Goal**:
- Target: 60-80 papers for systematic review
- Intended use: Systematic review for quality improvement project

**My Technical Background**:
- Programming experience: None (will need step-by-step guidance)
- RAG/AI experience: First time

Please help me design an effective literature search strategy and PRISMA
systematic review pipeline for this research project.
```

---

## Next Steps

Once Claude responds with clarifying questions:
- Answer thoughtfully (don't rush)
- Ask for explanations if anything is unclear
- Request examples from your field if helpful
- Move to Stage 2 when you feel the scope is well-defined
