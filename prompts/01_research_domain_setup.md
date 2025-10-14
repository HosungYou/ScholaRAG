<!-- METADATA
stage: 1
stage_name: "Research Domain Setup"
stage_goal: "Define research scope and validate feasibility"
expected_duration: "15-20 minutes"
conversation_mode: "interactive"
outputs:
  - research_question: "Clear, answerable research question"
  - research_scope: "Year range, publication types, languages, study designs"
  - feasibility_assessment: "Estimated paper count and data source recommendations"
validation_rules:
  research_question:
    required: true
    min_length: 20
    max_length: 500
    validation: "Must be specific, answerable, and within systematic review scope"
  research_field:
    required: true
    examples: ["Education", "Medicine", "Psychology", "Computer Science"]
  year_range:
    required: false
    default: "no constraint"
    validation: "Must be realistic (e.g., 2010-2024, not 1800-2024 for AI research)"
  target_paper_count:
    required: false
    default: "50-100"
    validation: "Realistic range between 20-500 papers"
cli_commands:
  - command: "researcherrag init"
    when: "After conversation completes and user approves scope"
    auto_execute: true
scripts_triggered:
  - none (initialization only, creates project structure)
next_stage:
  stage: 2
  condition: "User confirms research scope and feasibility"
  prompt_file: "02_query_strategy.md"
divergence_handling:
  common_divergences:
    - pattern: "User asks about downloading PDFs"
      response: "PDF downloading happens in Stage 4. Let's first define your research scope in Stage 1, then design search queries in Stage 2-3."
    - pattern: "User asks about RAG implementation details"
      response: "RAG design happens in Stage 4. Right now in Stage 1, let's focus on defining your research question and scope."
    - pattern: "User jumps to asking about specific databases/APIs"
      response: "Great question! I'll recommend specific databases after understanding your research scope. Let's first clarify your research questions and constraints."
    - pattern: "User wants to skip systematic review"
      response: "This system is designed for systematic PRISMA reviews. If you need quick exploratory search, consider using Google Scholar or Connected Papers instead."
conversation_flow:
  expected_turns: 4-8
  typical_pattern:
    - turn: 1
      user_action: "Provides initial research topic and scope"
      claude_action: "Ask clarifying questions about specificity, constraints, and goals"
    - turn: 2-3
      user_action: "Answers clarifying questions, refines scope"
      claude_action: "Suggest domain-specific keywords, validate feasibility, estimate paper counts"
    - turn: 4-5
      user_action: "Confirms scope or requests adjustments"
      claude_action: "Provide data source recommendations, explain next stages"
    - turn: "final"
      user_action: "Ready to proceed"
      claude_action: "Summarize decisions, initialize project structure, show Stage 2 prompt"
validation_checklist:
  - "Research question is specific and answerable"
  - "Scope constraints are realistic and clearly defined"
  - "Expected paper count is reasonable (20-500 papers)"
  - "User understands systematic review process and time commitment"
  - "Data sources have been recommended based on field"
-->

# Stage 1: Research Domain Setup

**🎯 Your Current Stage**: Stage 1 of 7
**⏱️ Expected Time**: 15-20 minutes
**💬 Format**: Interactive conversation with Claude Code

---

## 🚀 Quick Start

Copy and paste this prompt to Claude Code to start your RAG project:

---

I want to conduct a PRISMA 2020 systematic literature review enhanced with RAG analysis for my research project.

**What is PRISMA + RAG?**
- **PRISMA 2020**: Systematic method to identify, screen, and select relevant papers (ensures rigor and transparency)
- **RAG (Retrieval-Augmented Generation)**: AI-powered system to query and extract insights from selected papers (enables depth)
- **Together**: Rigorous paper selection + intelligent analysis = Comprehensive literature review in days, not months

---

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
- PRISMA/RAG experience: [First time / Familiar with concepts / Have done systematic reviews before]

Please help me design an effective PRISMA 2020 systematic review pipeline enhanced with RAG for deep analysis.

---

## 📋 What Happens in This Stage

### Claude Code Will:

1. **Ask Clarifying Questions** (2-3 rounds)
   - Validate research question specificity
   - Check if scope is too broad/narrow
   - Understand your field's norms and terminology

2. **Suggest Domain-Specific Keywords**
   - Brainstorm search terms from your field
   - Identify synonyms and variations
   - Preview what Stage 2 query design will look like

3. **Estimate Expected Paper Counts**
   - Based on preliminary searches in major databases
   - Warn if scope is too broad (>10,000 papers) or too narrow (<20 papers)
   - Help adjust scope if needed

4. **Recommend Data Sources**
   - Semantic Scholar (AI/CS/interdisciplinary)
   - OpenAlex (comprehensive coverage, all fields)
   - arXiv (cutting-edge preprints)
   - CORE (open access aggregator)
   - Field-specific: PubMed (medicine), PsycINFO (psychology), etc.

5. **Initialize Project Structure** (automatic)
   - Create `config.yaml` with your research parameters
   - Set up project folders (`papers/`, `outputs/`, `logs/`)
   - Prepare for Stage 2 query design

### ✅ Stage Completion Checklist

Before moving to Stage 2, ensure:

- [ ] Research question is **specific and answerable** (not too broad like "AI in education")
- [ ] Scope constraints are **realistic** (year range makes sense, paper count is 20-500)
- [ ] You understand the **7-stage process** and time commitment (~4-8 hours total)
- [ ] Data sources have been **recommended and approved**
- [ ] Project structure has been **initialized** (you'll see confirmation message)

---

## 💡 Tips for Success

### ✅ Good Examples

- **Specific**: "AI chatbots for improving speaking skills in language learning" ✓
- **Methods mentioned**: "If you only want RCTs, say so upfront" ✓
- **Clear constraints**: "2015-2024, peer-reviewed journals, English only" ✓
- **Realistic target**: "80-120 papers for dissertation lit review" ✓

### ❌ Common Pitfalls

- **Too broad**: "AI in education" (could be 100,000+ papers)
- **Too narrow**: "GPT-4 chatbots for Mandarin speaking in Korean universities" (might be 2 papers)
- **Unclear methods**: Not specifying if you want only quantitative studies
- **Unrealistic scope**: "All papers on depression since 1950" (millions of papers)

---

## 📚 Example: Education Research

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

### Expected Conversation Flow

**Claude**: "Great research topic! Let me clarify a few things:
1. By 'higher education contexts', do you mean university students specifically (18-25 age range)?
2. Should I include studies on text-based chatbots, or only voice-enabled ones?
3. Are you interested in both synchronous (real-time) and asynchronous interactions?"

**You**: "Yes, university students. Both text and voice are fine. Synchronous only please."

**Claude**: "Perfect! Based on your scope, I estimate:
- Semantic Scholar: ~150 papers (good for AI/education interdisciplinary work)
- OpenAlex: ~200 papers (comprehensive coverage)
- PubMed: ~30 papers (some health communication studies)

Your target of 80-120 papers is very realistic. Let's move to Stage 2 to design precise search queries."

---

## 📚 Example: Medical Research

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

## 🔄 What Happens Next

### After This Conversation

1. **Project Initialized** ✓
   - `config.yaml` created with your research parameters
   - Project folder structure set up
   - Ready for Stage 2

2. **You Receive Stage 2 Prompt** ➡️
   - Copy/paste to continue conversation
   - Design precise search queries with Boolean operators
   - Expected time: 20-30 minutes

3. **Progress Tracking**
   - Your conversation context is saved in `.researcherrag/context.json`
   - Claude Code knows which stage you're in
   - Can always check progress with `researcherrag status`

---

## 🚨 Troubleshooting

### "I'm not sure if my research question is specific enough"

Ask Claude: "Is my research question specific enough? Can you show me examples of too broad vs. well-scoped questions in my field?"

### "I don't know which databases to use"

No worries! Claude will recommend databases based on your field after understanding your research scope. Just answer the clarifying questions first.

### "I want to skip some stages"

This system follows PRISMA 2020 guidelines for systematic reviews. All 7 stages are necessary for reproducible, high-quality reviews. However, if you need quick exploratory search, this might not be the right tool—consider Google Scholar or Connected Papers instead.

### "Can I change my scope later?"

Yes! You can restart Stage 1 anytime with `researcherrag reset stage1`. However, you'll need to re-run subsequent stages if you significantly change your research question.

---

## 🎯 Stage 1 Success Criteria

You're ready to move to Stage 2 when:

✅ Research question is **clear and answerable**
✅ Scope is **realistic** (not too broad, not too narrow)
✅ Expected paper count is **20-500 papers**
✅ You understand the **time commitment** (~4-8 hours for all 7 stages)
✅ Data sources are **selected and approved**
✅ Project has been **initialized** with `config.yaml`

---

## 📍 Your Progress

```
[●○○○○○○] Stage 1/7: Research Domain Setup
```

**Next**: Stage 2 - Query Strategy Design (20-30 min)
**After That**: Stage 3 - PRISMA Configuration (10-15 min)

**Total Pipeline**: ~4-8 hours across all stages
**Your Commitment Today**: Just this 15-20 minute conversation

---

**Ready to start?** Copy the prompt template above, fill in your research details, and paste it to Claude Code!
