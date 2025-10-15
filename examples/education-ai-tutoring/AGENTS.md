# Agent Instructions for Education AI Tutoring Example

**Project**: AI-Powered Personalized Tutoring Systems in K-12 Education
**Purpose**: Guide AI agents (Claude Code, ChatGPT, etc.) working on this systematic review

---

## 🎯 Project Context

You are assisting with a **systematic literature review** examining the effectiveness of AI-powered personalized tutoring systems in K-12 education (grades K-12, ages 5-18).

### Research Question
> What is the effectiveness of AI-powered personalized tutoring systems on student learning outcomes in K-12 education, and what factors contribute to their success or failure?

### Key Objectives
1. **Quantify effectiveness**: Meta-analyze effect sizes on learning outcomes
2. **Identify moderators**: Subject domain, grade level, intervention duration, socioeconomic factors
3. **Implementation insights**: Teacher perspectives, challenges, best practices
4. **Policy recommendations**: Evidence-based guidance for school districts

---

## 📚 Domain Knowledge Required

### Education Research Terminology

**Effect Sizes**:
- **Cohen's d**: Standardized mean difference (small: 0.2, medium: 0.5, large: 0.8)
- **Hedge's g**: Bias-corrected Cohen's d for small samples
- **Odds ratio**: For binary outcomes (pass/fail, dropout)

**Study Designs** (hierarchy of evidence):
1. **Randomized Controlled Trials (RCTs)**: Gold standard
2. **Quasi-experimental**: Matched control groups
3. **Pre-post designs**: Single group before/after
4. **Observational/correlational**: Weakest causal inference

**Outcome Measures**:
- **Standardized tests**: SAT, ACT, state assessments (high stakes)
- **Curriculum-based measures**: Unit tests, quizzes
- **Engagement metrics**: Time on task, login frequency
- **Affective outcomes**: Motivation, self-efficacy, anxiety

### AI Tutoring System Types

1. **Intelligent Tutoring Systems (ITS)**
   - Rule-based expert systems
   - Student modeling + pedagogical module
   - Examples: Carnegie Learning MATHia, AutoTutor

2. **Adaptive Learning Platforms**
   - Machine learning for personalization
   - Continuous difficulty adjustment
   - Examples: DreamBox, ALEKS, Khan Academy

3. **Conversational Agents / Chatbots**
   - Natural language interaction
   - Socratic tutoring style
   - Examples: Duolingo, Khanmigo (GPT-4)

4. **Hybrid Systems**
   - AI + human tutor collaboration
   - AI handles routine, human handles complex

### K-12 Education Context

**Grade Levels**:
- Elementary: K-5 (ages 5-11)
- Middle School: 6-8 (ages 11-14)
- High School: 9-12 (ages 14-18)

**Subject Domains** (in priority order for this review):
1. **Mathematics**: Most researched, clearest outcomes
2. **Reading/Literacy**: Comprehension, fluency, vocabulary
3. **Science**: Physics, chemistry, biology
4. **Computer Science**: Programming, computational thinking
5. **Foreign Languages**: Vocabulary, grammar, speaking

**Equity Considerations**:
- **Title I schools**: High-poverty schools (>40% low-income students)
- **English Language Learners (ELL)**: Non-native English speakers
- **Special education**: Students with IEPs (Individualized Education Programs)
- **Digital divide**: Access to devices, internet

---

## 🔍 Search and Screening Guidance

### Stage 1: Paper Identification

**High-Value Databases**:
- **Semantic Scholar**: Best for CS/Education interdisciplinary research
- **OpenAlex**: Open access, broad coverage
- **ERIC (Education Resources Information Center)**: Education-specific
- **arXiv**: Preprints (bleeding edge, not peer-reviewed yet)

**Search Query Tips**:
- **Include synonyms**: "AI tutoring" = "intelligent tutoring" = "adaptive learning" = "personalized instruction"
- **Boolean operators**: `(AI OR "artificial intelligence") AND (tutoring OR personalized) AND (K-12 OR elementary OR "middle school")`
- **Wildcards**: `tutor*` captures "tutor", "tutoring", "tutors"

**Date Range Rationale (2018-2025)**:
- 2018: Deep learning became mainstream in EdTech
- 2020-2021: COVID-19 accelerated adoption
- 2023+: GPT-4 era (large language models in education)

### Stage 2: PRISMA Screening

**Inclusion Criteria Operationalization**:

✅ **"AI-powered system"**:
- Must use machine learning, neural networks, or natural language processing
- NOT simple if-then rules (exclude traditional CAI)
- NOT just digitized worksheets

✅ **"K-12 education"**:
- Students aged 5-18 in formal schooling
- Include: Public schools, private schools, homeschool programs
- Exclude: Preschool (ages 0-4), higher education (university), adult learning

✅ **"Reports learning outcomes"**:
- Must have quantitative data (test scores, completion rates) OR rich qualitative data (interviews, observations)
- Exclude: Opinion pieces, theoretical frameworks without empirical validation

**Exclusion Criteria Edge Cases**:

❌ **"Higher education only"** - BUT:
- Allow if includes K-12 + university comparison
- Allow if methodology transferable (e.g., algorithm development)

❌ **"Non-AI system"** - BUT:
- Allow if comparing AI vs. non-AI (to establish effect)

❌ **"No full text"** - BUT:
- Allow if open access preprint available (arXiv, EdArXiv, PsyArXiv)

### Stage 3: Quality Assessment

**Appraisal Criteria** (score 0-2 each):
1. **Clear research question**: Explicit, testable hypothesis
2. **Appropriate methodology**: Matches research question (RCT for causal claims)
3. **Valid outcome measures**: Standardized tests > teacher-created tests
4. **Adequate sample size**: n > 30 per group (power analysis ideal)
5. **Statistical analysis**: Effect sizes + confidence intervals reported
6. **Limitations discussed**: Acknowledges threats to validity

**Minimum threshold**: 8/12 points to include in synthesis

---

## 🤖 RAG Query Guidance

### Effective Query Patterns

**Pattern 1: Quantitative Synthesis**
```
Template: What are the [effect sizes / outcomes] of [intervention]
          on [outcome variable] in [population]? Include [sample sizes / CIs].

Example: What are the average effect sizes of AI tutoring on reading
         comprehension in elementary schools? Include sample sizes and
         confidence intervals.
```

**Pattern 2: Comparative Analysis**
```
Template: How does [intervention A] compare to [intervention B]
          on [outcome variable]? What are the [relative advantages]?

Example: How does AI tutoring compare to human tutoring on math
         achievement in middle schools? What are the cost-effectiveness
         tradeoffs?
```

**Pattern 3: Moderator Analysis**
```
Template: How does [intervention effectiveness] vary by [moderator variable]?
          Are there [differential effects]?

Example: How does AI tutoring effectiveness vary by student socioeconomic
         status? Are there equity concerns?
```

**Pattern 4: Implementation Research**
```
Template: What are the [barriers / facilitators] to implementing
          [intervention] in [setting]? What do [stakeholders] report?

Example: What are the most common barriers to implementing AI tutoring
         in Title I schools? What do teachers and administrators report?
```

**Pattern 5: Mechanism Exploration**
```
Template: What [mechanisms / processes] explain why [intervention]
          affects [outcome]? Which [components] are most important?

Example: What pedagogical mechanisms explain why AI tutoring improves
         math learning? Which system features are most important?
```

### Query Refinement Tips

**If response is too general**:
- Add specificity: grade level, subject, outcome type
- Request tables: "Summarize in a table with columns for [study, sample size, effect size]"
- Ask for citations: "List the top 5 studies by sample size"

**If response lacks citations**:
- Explicitly request: "Include paper citations (author, year) for each claim"
- Use verification query: "Which papers provide evidence for [specific claim]?"

**If response contradicts domain knowledge**:
- Challenge: "This conflicts with meta-analysis by VanLehn (2011). Reconcile."
- Request primary sources: "What are the original papers reporting [surprising finding]?"

---

## 📊 Data Extraction Guidance

### Key Variables to Extract

**Study Characteristics**:
- Authors, year, journal/conference
- Study design (RCT, quasi-experimental, pre-post)
- Sample size (total, by group)
- Setting (urban, suburban, rural; public, private; Title I status)

**Participant Characteristics**:
- Grade level (K-5, 6-8, 9-12)
- Age range
- Subject domain
- Demographics (% low-income, % ELL, % special education)

**Intervention Characteristics**:
- AI system name and type (ITS, adaptive, chatbot)
- Duration (weeks)
- Dosage (minutes per week)
- Implementation fidelity (% of planned sessions completed)

**Outcome Measures**:
- Test type (standardized, curriculum-based)
- Outcome domain (math, reading, etc.)
- Effect sizes (Cohen's d, Hedge's g, odds ratio)
- Statistical significance (p-values, confidence intervals)

**Qualitative Findings** (if applicable):
- Themes (motivation, engagement, challenges)
- Stakeholder perspectives (students, teachers, parents)

---

## ⚠️ Common Pitfalls to Avoid

### 1. Mixing K-12 with Higher Education
**Problem**: University studies often report larger effects due to self-selection bias
**Solution**: Explicitly filter by educational level in screening stage

### 2. Ignoring Publication Bias
**Problem**: Studies with null/negative results less likely to be published
**Solution**: Search for dissertations, preprints, technical reports; conduct funnel plot analysis

### 3. Apples-to-Oranges Comparisons
**Problem**: Comparing 1-week pilot (d=0.2) with 2-year implementation (d=0.8)
**Solution**: Stratify by intervention duration or use meta-regression

### 4. Confusing Engagement with Learning
**Problem**: High login rates ≠ learning gains
**Solution**: Prioritize validated outcome measures (standardized tests) over proxies

### 5. Overgeneralizing from Single Subject Domain
**Problem**: Math tutoring results may not transfer to reading
**Solution**: Report effect sizes separately by subject domain

---

## 📝 Writing and Reporting Guidance

### PRISMA 2020 Compliance

**Required Sections**:
1. **Title**: "Effectiveness of AI-Powered Personalized Tutoring Systems in K-12 Education: A Systematic Review"
2. **Abstract**: Structured (Background, Methods, Results, Conclusions)
3. **Introduction**: Research question, PICO framework
4. **Methods**: Search strategy, selection criteria, data extraction, synthesis
5. **Results**: PRISMA flow diagram, study characteristics table, effect sizes
6. **Discussion**: Summary, limitations, implications, future research

**PRISMA Flow Diagram** (required checkpoints):
```
Identification:
  ├─ Records identified from databases (n=800)
  └─ Records removed before screening (n=50 duplicates)

Screening:
  ├─ Records screened (n=750)
  └─ Records excluded (n=630)

Included:
  ├─ Reports sought for retrieval (n=120)
  ├─ Reports not retrieved (n=0)
  ├─ Reports assessed for eligibility (n=120)
  ├─ Reports excluded (n=45, no full text)
  └─ Studies included in review (n=75)
```

### Citation Style

**APA 7th Edition** (education standard):
```
Smith, J. A., Johnson, B. C., & Lee, D. (2023). Effects of AI tutoring
  on elementary math achievement: A randomized controlled trial.
  *Journal of Educational Psychology, 115*(3), 456-472.
  https://doi.org/10.1037/edu0000789
```

**In-Text**: (Smith et al., 2023)

---

## 🎓 Domain-Specific Best Practices

### For Education Researchers

1. **Always report equity analyses**: Disaggregate by race, SES, ELL status
2. **Include effect size confidence intervals**: Point estimates alone are insufficient
3. **Discuss practical significance**: Is d=0.3 worth $50/student?
4. **Acknowledge limitations**: Teacher effects, implementation variability
5. **Connect to theory**: Cognitive load, spaced repetition, mastery learning

### For Policy Audiences

1. **Lead with actionable findings**: "AI tutoring shows moderate effects (d=0.52)"
2. **Use plain language**: "Students gained 3 months of learning" > "Effect size = 0.45"
3. **Include cost-benefit analysis**: $/student, scalability
4. **Highlight equity implications**: "Effects similar across income levels"
5. **Provide implementation recommendations**: Minimum duration, training needs

---

## 🔗 Resources

**Key Organizations**:
- [Institute of Education Sciences (IES)](https://ies.ed.gov/) - U.S. education research
- [What Works Clearinghouse](https://ies.ed.gov/ncee/wwc/) - Evidence reviews
- [UNESCO AI and Education](https://www.unesco.org/en/digital-education/artificial-intelligence) - Global policy

**Meta-Analyses to Reference**:
- VanLehn, K. (2011). Relative effectiveness of tutoring systems. *Educational Psychologist*.
- Kulik, J. A., & Fletcher, J. D. (2016). Effectiveness of intelligent tutoring systems. *Review of Educational Research*.

**Reporting Guidelines**:
- [PRISMA 2020](http://www.prisma-statement.org/) - Systematic review reporting
- [CONSORT](https://www.consort-statement.org/) - RCT reporting

---

## 🤝 Collaboration with Human Researchers

As an AI agent, you should:

✅ **Propose, don't impose**: "Would you like me to extract effect sizes from these 15 papers?"
✅ **Explain reasoning**: "I prioritized Semantic Scholar because it indexes education journals"
✅ **Flag uncertainties**: "This paper reports Hedge's g, not Cohen's d. Should I convert?"
✅ **Defer to expertise**: "You mentioned equity is a priority. Should I prioritize Title I school studies?"

❌ **Don't make unilateral decisions** on:
- Final inclusion/exclusion (human must review)
- Quality assessment cutoffs (subjective judgment)
- Interpretation of contradictory findings (requires domain expertise)

---

**This guide is a living document. Update as you learn more about the project's specific needs.**

*Compatible with ResearcherRAG v1.0.5+*
