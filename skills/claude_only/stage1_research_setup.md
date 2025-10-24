# Stage 1: Research Domain Setup

**Load this file when**: Researcher provides Stage 1 prompt or asks to initialize new project

**Expected duration**: 15-20 minutes (6-10 conversational turns)

**Goal**: Define research scope, choose project_type, validate feasibility

---

## Quick Overview

**What happens in this stage**:
1. Researcher provides research topic
2. You ask clarifying questions (2-4 rounds)
3. Together decide between `knowledge_repository` vs `systematic_review`
4. Define scope constraints (years, publication types, etc.)
5. Estimate paper counts and recommend databases
6. Validate feasibility
7. Create project structure and config.yaml

**What you'll execute**:
```bash
python scholarag_cli.py init \
  --name "Project-Name" \
  --question "Research question?" \
  --field "domain" \
  --project-type "knowledge_repository or systematic_review"
```

---

## Conversation Flow (6-10 Turns)

### Turn 1: Initial Topic Exploration

**User provides**: Research topic (often vague)

**Your action**: Ask clarifying questions to understand domain, population, intervention, outcome

**Example**:
```
USER: "I want to study AI in education"

YOU: "Great topic! Let me help you refine this into a systematic review scope:

1. **Domain specificity**: Are you interested in:
   - AI chatbots specifically?
   - Intelligent tutoring systems?
   - All AI applications in education?

2. **Educational context**: Which level?
   - K-12?
   - Higher education?
   - Corporate training?
   - All levels?

3. **Outcome of interest**: What impact are you measuring?
   - Learning outcomes (test scores)?
   - Engagement/motivation?
   - Teacher workload reduction?
   - All outcomes?

4. **Publication scope**: Any constraints?
   - Peer-reviewed only?
   - Include grey literature?
   - Language constraints (English only)?

Let's narrow this down to create a focused, answerable research question."
```

### Turn 2-3: Research Question Refinement

**User answers**: Provides more specificity

**Your action**: Draft 2-3 research question options, explain differences

**Example**:
```
USER: "I'm interested in AI chatbots for language learning, specifically speaking skills in university students"

YOU: "Excellent! Based on that, here are 3 potential research questions:

**Option 1 (Broad - Knowledge Repository)**:
'What is the current state of AI chatbot research in language learning?'
- Captures all chatbot studies
- Estimated 5,000-10,000 papers
- Good for: Comprehensive overview, teaching material, future research directions

**Option 2 (Focused - Systematic Review)**:
'How do AI chatbots improve speaking proficiency in university-level language learners?'
- Focused on speaking outcomes
- Estimated 50-200 papers
- Good for: Meta-analysis, dissertation, journal publication

**Option 3 (Narrow - Systematic Review)**:
'What is the effectiveness of AI chatbots in improving English speaking proficiency among non-native university students, measured by standardized tests?'
- Very specific population + outcome + measurement
- Estimated 20-50 papers
- Good for: High-rigor systematic review, causal claims

Which scope aligns with your research goals?"
```

### Turn 4-5: project_type Decision

**User indicates**: Research goals (publication, teaching, exploration)

**Your action**: Recommend `project_type` based on goals, explain implications

**Critical decision point**: Use [skills/reference/project_type_decision_tree.md](../reference/project_type_decision_tree.md)

**2-Question Decision Tree**:

1. **Will you publish this as a systematic review in an academic journal?**
   - Yes → `systematic_review` ✅
   - No → Go to Question 2

2. **Do you need comprehensive domain coverage (15,000+ papers)?**
   - Yes → `knowledge_repository` ✅ (For teaching, AI assistant, exploration)
   - No → `systematic_review` ✅ (Focused high-quality subset)

**Example**:
```
USER: "This is for my dissertation, I need a publishable systematic review"

YOU: "Perfect! Based on that goal, I recommend **systematic_review** mode:

**Why systematic_review**:
- ✅ PRISMA 2020 compliant (journal requirement)
- ✅ 90% AI confidence threshold → High-quality papers only
- ✅ Manageable paper count (50-200) for deep analysis
- ✅ Suitable for meta-analysis, effect size extraction

**What this means for your pipeline**:
- Stage 3 screening: 90% threshold (strict) vs 50% (lenient)
- Expected output: ~50-200 highly relevant papers
- PRISMA diagram title: 'Systematic Review: [Your Topic]'

**Year range recommendation**:
For AI chatbot research, I suggest 2015-2024 (captures recent deep learning era).

Shall we proceed with:
- **project_type**: systematic_review
- **Research question**: 'How do AI chatbots improve speaking proficiency in university-level language learners?'
- **Year range**: 2015-2024"
```

### Turn 6-7: Scope Constraints Definition

**User confirms**: project_type and research question

**Your action**: Define scope constraints (years, languages, study designs, etc.)

**Example**:
```
YOU: "Great! Now let's define scope constraints for systematic screening:

**Inclusion criteria** (papers we WANT):
1. **Population**: University students (18-30 years)
2. **Intervention**: AI chatbot (conversational agent, dialogue system)
3. **Outcome**: Speaking proficiency (oral fluency, pronunciation, accuracy)
4. **Study design**: RCT, quasi-experimental, pre-post test

**Exclusion criteria** (papers we DON'T want):
1. Non-AI chatbots (rule-based only)
2. Non-speaking outcomes (writing, reading, listening only)
3. K-12 students or corporate training
4. Opinion pieces, editorials, proposals

**Language constraint**: English only (for consistency)

**Publication type**: Peer-reviewed journal articles + conference proceedings

Does this scope accurately capture what you're looking for?"
```

### Turn 8: Database Recommendation

**User confirms**: Scope constraints

**Your action**: Recommend databases based on domain + availability

**Example**:
```
YOU: "Based on your education + linguistics domain, I recommend:

**Recommended databases** (3):
1. **Semantic Scholar** (~40% open access PDF)
   - Strong coverage of education + CS interdisciplinary work
   - Good for: AI + language learning intersection

2. **OpenAlex** (~50% open access PDF)
   - Broad academic coverage
   - Good for: Capturing papers Semantic Scholar might miss

3. **arXiv** (100% PDF access)
   - Preprints + conference papers
   - Good for: Cutting-edge AI research

**Estimated combined coverage**: 20,000-30,000 papers initially
**After screening (90% threshold)**: ~50-200 highly relevant

**Not using**:
- ❌ PubMed (medicine-focused, low AI coverage)
- ❌ ERIC (education-focused but weak on AI)
- ❌ Scopus/Web of Science (require institutional access, no API automation)

Ready to initialize your project?"
```

### Turn 9-10: Final Validation & Initialization

**User confirms**: Ready to initialize

**Your action**: Validate all criteria, execute `scholarag init`, create project structure

**Validation checklist**:
```python
# Check all required fields present
✅ project_name: "AI-Chatbots-Speaking-Proficiency"
✅ research_question: "How do AI chatbots improve speaking proficiency in university-level language learners?"
✅ research_field: "Education"
✅ project_type: "systematic_review"
✅ year_range: [2015, 2024]
✅ databases: ["semantic_scholar", "openalex", "arxiv"]
✅ target_papers: "50-200 (final, after screening)"

# Validate constraints
✅ Research question length: 20-500 chars
✅ project_type: Valid value (knowledge_repository or systematic_review)
✅ Year range: Realistic (9 years, appropriate for AI research)
✅ Databases: At least 1 selected
```

**Execute**:
```bash
cd "/Volumes/External SSD/Projects/Research/ScholaRAG"

python scholarag_cli.py init \
  --name "AI-Chatbots-Speaking-Proficiency" \
  --question "How do AI chatbots improve speaking proficiency in university-level language learners?" \
  --field "Education" \
  --project-type "systematic_review" \
  --year-start 2015 \
  --year-end 2024 \
  --databases semantic_scholar openalex arxiv
```

**Expected output**:
```
✅ Project created: projects/2025-10-24_AI-Chatbots-Speaking-Proficiency/
✅ config.yaml initialized
✅ Folder structure created:
   - data/01_identification/
   - data/02_screening/
   - data/pdfs/
   - rag/
   - outputs/
   - .scholarag/

Next: Stage 2 - Query Strategy Design
```

**Show Stage 2 prompt**:
```python
# Read next stage prompt
with open('prompts/02_query_strategy.md', 'r') as f:
    stage2_prompt = f.read()

# Remove metadata block
import re
stage2_clean = re.sub(r'<!--.*?-->', '', stage2_prompt, flags=re.DOTALL)

print(f"""
✅ **Stage 1 Complete!**

Your project is initialized. Here's your Stage 2 prompt:

---

{stage2_clean}

---

**Copy the Stage 2 prompt template above and paste it back to me when you're ready!**
""")
```

---

## Divergence Handling

### Divergence 1: User asks about downloading PDFs

**Pattern**: "Can you help me download PDFs now?"

**Response**:
```
"PDF downloading happens in Stage 4 (after we've designed queries and screened papers).

Right now in Stage 1, we're defining your research scope. Once we have a clear question and scope, we'll:
- Stage 2: Design optimal search queries
- Stage 3: Configure PRISMA screening criteria
- Stage 4: Download PDFs (only for papers that pass screening)

This systematic approach prevents downloading thousands of irrelevant PDFs. Let's continue refining your research question first!"
```

### Divergence 2: User asks about RAG implementation

**Pattern**: "How will the RAG system work?"

**Response**:
```
"RAG design happens in Stage 4, after we know which papers we're analyzing.

Right now in Stage 1, let's focus on:
1. Defining your research question (what do you want to know?)
2. Scoping the literature (which papers are relevant?)
3. Estimating feasibility (can we find enough papers?)

Once we know your exact papers (Stage 3 screening), we'll design the RAG system in Stage 4 to match your research needs. For example, if you're extracting correlations, we'll configure chunking differently than if you're doing thematic analysis.

What's your research domain?"
```

### Divergence 3: User wants to skip systematic review

**Pattern**: "Can I just search Google Scholar instead?"

**Response**:
```
"Google Scholar is great for exploratory search, but ScholaRAG is designed for PRISMA 2020 systematic reviews with these advantages:

**ScholaRAG advantages**:
1. ✅ **Reproducible**: Exact search queries saved, anyone can re-run
2. ✅ **Comprehensive**: 3 databases simultaneously (Semantic Scholar, OpenAlex, arXiv)
3. ✅ **AI-powered screening**: Claude screens 10,000+ papers in 30 minutes
4. ✅ **RAG analysis**: Extract specific data (correlations, effect sizes) from 100+ PDFs automatically
5. ✅ **PRISMA compliant**: Generate PRISMA diagram for publication

**Google Scholar limitations**:
1. ❌ No API (manual searching)
2. ❌ Results not reproducible (personalized, changes over time)
3. ❌ No systematic screening (manual, time-consuming)
4. ❌ No automated PDF download
5. ❌ No RAG-powered analysis

**If you need**:
- **Quick exploratory search**: Use Google Scholar or Connected Papers
- **Rigorous systematic review**: Use ScholaRAG (we're here!)
- **Meta-analysis for publication**: Definitely use ScholaRAG

Which matches your goal?"
```

### Divergence 4: User unsure about project_type

**Pattern**: "I don't know if I should choose knowledge_repository or systematic_review"

**Response**:
```
"Great question! Let me help you decide with 2 questions:

**Question 1**: Will you publish this as a systematic review in an academic journal?
- ✅ Yes → Choose **systematic_review** (skip to initialization)
- ❌ No → Go to Question 2

**Question 2**: Do you need comprehensive domain coverage (15,000+ final papers)?
- ✅ Yes → Choose **knowledge_repository** (for teaching, AI chatbot, exploration)
- ❌ No → Choose **systematic_review** (focused high-quality subset, 50-300 papers)

**Examples**:

- **PhD dissertation** → systematic_review (need publishable rigor)
- **Teaching material for course** → knowledge_repository (want comprehensive coverage)
- **Meta-analysis** → systematic_review (need precise effect sizes)
- **Domain exploration** → knowledge_repository (breadth over depth)
- **Building AI research assistant** → knowledge_repository (large dataset for RAG)

What's your end goal for this literature review?"
```

---

## Common Issues

### Issue 1: Research question too broad

**Symptom**: Estimated 50,000+ papers, user overwhelmed

**Solution**:
```
"Your research question is very broad. Let's narrow it using PICO framework:

**Current**: 'What is the impact of AI in education?'
**Too broad because**: AI (many types) + education (many levels) + impact (many outcomes)

**PICO refinement**:
- **P**opulation: University students (not K-12, not corporate)
- **I**ntervention: AI chatbots (not all AI)
- **C**omparison: Traditional instruction (optional)
- **O**utcome: Speaking proficiency (not all skills)

**Refined**: 'How do AI chatbots improve speaking proficiency in university language learners compared to traditional instruction?'

**Result**: 50,000 → 500 papers (manageable!)

Shall we refine your question using PICO?"
```

### Issue 2: Research question too narrow

**Symptom**: Estimated <20 papers, not enough for systematic review

**Solution**:
```
"Your research question might be too narrow. We found only ~15 papers, which is below the typical threshold for systematic review (20-50 minimum).

**Current**: 'Impact of GPT-4 chatbots on English pronunciation in Korean university students aged 20-22'

**Too narrow because**:
- Specific model (GPT-4) limits to 2023-2024
- Specific skill (pronunciation only)
- Specific population (Korean, 20-22 only)

**Broadening options**:

**Option 1**: Broaden model
- 'AI chatbots' instead of 'GPT-4 chatbots'
- **Impact**: +150 papers (includes all LLM-based chatbots)

**Option 2**: Broaden outcome
- 'Speaking skills' instead of 'pronunciation only'
- **Impact**: +80 papers (includes fluency, accuracy, speaking confidence)

**Option 3**: Broaden population
- 'University students' instead of 'Korean 20-22'
- **Impact**: +200 papers (includes all university-age learners)

**Recommended**: Option 1 + Option 2
- **New question**: 'How do AI chatbots improve speaking skills in university language learners?'
- **Estimated papers**: ~150-300 (good for systematic review!)

Which broadening approach fits your research goals?"
```

### Issue 3: User confused about year range

**Symptom**: Asks "Should I go back to 1990 for comprehensive coverage?"

**Solution**:
```
"Year range depends on your research domain and project_type:

**For AI/ML topics** (deep learning era):
- ✅ **Recommended**: 2015-2024 (transformer models, modern LLMs)
- ❌ **Too early**: 1990-2024 (includes outdated rule-based systems, dilutes findings)

**For established medical topics**:
- ✅ **Recommended**: 2000-2024 (captures evidence-based medicine era)
- ⚠️ **Consider**: 2010-2024 if methodology has changed significantly

**For your topic (AI chatbots + language learning)**:
- **Recommended**: 2015-2024
- **Rationale**:
  - 2015: AlexNet + deep learning becomes mainstream
  - 2017: Transformer models (BERT, GPT)
  - 2020+: GPT-3, ChatGPT, modern conversational AI
  - Pre-2015 chatbots: Mostly rule-based, not relevant to modern AI

**Rule of thumb**:
- **systematic_review**: Narrower time range (5-10 years) for consistency
- **knowledge_repository**: Broader time range (10-20 years) for comprehensive coverage

For your systematic review, shall we use 2015-2024 (9 years)?"
```

---

## Completion Checklist

Before moving to Stage 2, verify:

- [ ] **project_name**: Descriptive, unique, no spaces (use hyphens)
- [ ] **research_question**: 20-500 chars, specific, answerable
- [ ] **research_field**: Valid domain (Education, Medicine, CS, etc.)
- [ ] **project_type**: Chosen with understanding
  - [ ] User knows: knowledge_repository = 50% threshold, broad coverage
  - [ ] User knows: systematic_review = 90% threshold, publication-ready
- [ ] **year_range**: Realistic for domain (not too broad, not too narrow)
- [ ] **databases**: At least 1 selected (recommended: all 3)
- [ ] **target_papers**: User understands expected outcome
  - [ ] knowledge_repository: 10,000-20,000 final
  - [ ] systematic_review: 50-300 final
- [ ] **scope constraints**: Inclusion/exclusion criteria discussed
- [ ] **feasibility validated**: Estimated paper count is reasonable
- [ ] **User understanding**: Researcher knows next 6 stages

**If all checked**: ✅ Execute `scholarag init` and show Stage 2 prompt

**If any unchecked**: ❌ Continue conversation, clarify remaining points

---

## Example Complete Conversation

See [skills/example_conversations/stage1_example.md](../example_conversations/stage1_example.md) for full conversation example.

**Summary**:
- User starts with vague topic: "AI in education"
- 6 turns of refinement
- Final question: "How do AI chatbots improve speaking proficiency in university language learners?"
- project_type: systematic_review (publication goal)
- Year range: 2015-2024
- Databases: All 3 (Semantic Scholar, OpenAlex, arXiv)
- Estimated: 50-200 final papers
- Duration: 18 minutes

---

## Integration Points

**Load on-demand from SKILL.md**:
- When researcher provides Stage 1 prompt
- When researcher asks: "How do I start a new project?"

**Reference files to load if needed**:
- [skills/reference/project_type_decision_tree.md](../reference/project_type_decision_tree.md) - If user asks "Which project_type?"
- [skills/reference/api_reference.md](../reference/api_reference.md) - If user asks "Which databases?"

**Next stage**:
- [skills/claude_only/stage2_query_strategy.md](stage2_query_strategy.md)

---

**Last Updated**: 2025-10-24
**Version**: 2.0
**Token Budget**: ~300 lines
