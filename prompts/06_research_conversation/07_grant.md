### Scenario 7: Future Research Design - Grant Proposal Support

**Research Goal**: Design follow-up studies based on identified gaps

**Optimal Prompt**:
```
Based on the research gaps identified in my database, propose a follow-up study design.

Include:
1. Research question and hypotheses
2. Study design (methodology, sample, measures)
3. Analysis plan
4. Expected contributions to the field
5. Budget estimate and timeline
```

**Optimal AI Response Structure**:
```
🔬 FUTURE RESEARCH PROPOSAL: Grant-Ready Study Design

**Based on**: Systematic review of 45 papers revealing critical research gaps

---

## 🎯 Research Question

**Primary RQ**:
What is the minimum effective duration and frequency of AI chatbot practice required to produce sustained speaking proficiency gains in university-level language learners?

**Secondary RQs**:
1. Do gains persist after chatbot access is removed (3-month and 6-month follow-ups)?
2. Does the effect differ for beginner vs. intermediate learners (proficiency moderator)?
3. What is the optimal dosage (sessions/week × minutes/session × weeks)?

---

## 💡 Hypotheses

**H1**: Minimum threshold exists at 8 weeks of practice (consistent with gap analysis)
- H1a: 4-week intervention will show d<0.20 (non-significant)
- H1b: 8-week intervention will show d≥0.50 (medium effect)
- H1c: 12-week intervention will show d≥0.65 (medium-large effect)

**H2**: Frequency matters more than total duration
- H2a: Daily practice (5×/week) will outperform twice-weekly (2×/week) even with equivalent total minutes

**H3**: Gains will decay without continued practice
- H3a: 50% of gains lost by 3-month follow-up (no continued access)
- H3b: 80% of gains retained if optional continued access provided

**H4**: Proficiency level moderates effect
- H4a: Beginners (A2) will show larger gains (d≥0.70)
- H4b: Intermediates (B1-B2) will show moderate gains (d≥0.45)

**Rationale**: Based on gap analysis showing:
- Lack of dosage studies (only 2 studies manipulated duration)
- No retention studies beyond 3 months (0 studies with 6-month follow-up)
- Proficiency rarely tested as moderator (only 3 studies)

---

## 📐 Study Design

### Design Type: Factorial Randomized Controlled Trial (RCT)

**Factorial Structure**: 3×2×2 mixed design
- Factor 1 (Between-subjects): Duration (4 weeks vs. 8 weeks vs. 12 weeks)
- Factor 2 (Between-subjects): Frequency (2×/week vs. 5×/week)
- Factor 3 (Within-subjects): Proficiency Level (Beginner A2 vs. Intermediate B1-B2)

**Total Conditions**: 6 between-subjects groups
1. 4 weeks, 2×/week (control dose)
2. 4 weeks, 5×/week
3. 8 weeks, 2×/week
4. 8 weeks, 5×/week
5. 12 weeks, 2×/week
6. 12 weeks, 5×/week (maximum dose)

---

### Sample

**Target N**: 360 participants (60 per condition × 6 conditions)

**Recruitment**:
- University language learners (ages 18-30)
- Studying English as L2
- Proficiency: A2 (beginner) or B1-B2 (intermediate) on CEFR scale
- No prior chatbot experience

**Inclusion Criteria**:
- ✅ Enrolled in university language program
- ✅ Native speaker of languages other than English
- ✅ Age 18-30
- ✅ Proficiency A2-B2 (verified by placement test)
- ✅ Access to smartphone/computer + internet
- ✅ Willing to commit 12 weeks + 6-month follow-up

**Exclusion Criteria**:
- ❌ Native English speakers
- ❌ Previous chatbot experience (>2 hours)
- ❌ Speech/hearing impairments
- ❌ Planning to study abroad during study period

**Power Analysis**:
- Expected effect size: d=0.50 (medium)
- Alpha: 0.05
- Power: 0.80
- Required n per group: 51
- Recruit 60 per group (assuming 15% attrition)

---

### Measures

#### Primary Outcome: Speaking Proficiency

**Instrument**: IELTS Speaking Test (standardized, widely validated)

**Subscales**:
- Fluency and Coherence (0-9)
- Lexical Resource (0-9)
- Grammatical Range and Accuracy (0-9)
- Pronunciation (0-9)
- Overall Band Score (0-9)

**Administration**:
- Trained raters (certified IELTS examiners)
- Video-recorded for inter-rater reliability (20% double-scored)
- Target IRR: Kappa ≥ 0.80

**Timing**:
- Baseline (Week 0)
- Immediate post-test (Week 4, 8, or 12 depending on condition)
- 3-month follow-up
- 6-month follow-up

---

#### Secondary Outcomes

**1. Objective Fluency Metrics** (automated analysis):
- Speech rate (words per minute)
- Pause frequency and duration
- Mean length of utterance (MLU)
- **Tool**: PRAAT speech analysis software

**2. Learner Self-Assessment**:
- Perceived speaking proficiency (7-point Likert)
- Speaking anxiety (Foreign Language Classroom Anxiety Scale)
- Chatbot usability (System Usability Scale)

**3. Engagement Metrics** (from chatbot logs):
- Total practice time (minutes)
- Number of chatbot conversations
- Average session length
- Adherence rate (% of prescribed sessions completed)

**4. Implementation Fidelity**:
- Dosage received (actual vs. prescribed)
- Technical issues log
- Participant satisfaction ratings

---

### Intervention

**Chatbot Platform**: LLM-based conversational AI (Claude 3.5 Sonnet)

**Conversation Topics**: Aligned with IELTS Speaking Part 1-3
- Personal topics (hobbies, family, work)
- Abstract topics (environment, technology, culture)
- Opinion discussions (agree/disagree, advantages/disadvantages)

**Session Structure** (30 minutes):
1. Warm-up (5 min): Greeting, topic selection
2. Conversation (20 min): Back-and-forth dialogue
3. Feedback (5 min): Chatbot provides pronunciation, grammar, vocabulary feedback

**Scaffolding**:
- Adaptive difficulty (chatbot adjusts to proficiency level)
- Vocabulary hints available on request
- Option to repeat/rephrase if misunderstood

---

### Control Group

**Modified Control**: All participants receive intervention (dosage varies)
- No "no treatment" control (unethical to withhold beneficial intervention)
- 4-week, 2×/week group serves as "minimal dose" control

**Justification**: Compare dosage levels rather than intervention vs. nothing

---

## 📊 Analysis Plan

### Primary Analysis: Mixed-Effects ANOVA

**Model**:
```
Speaking Proficiency ~ Duration × Frequency × Proficiency Level × Time + (1|Participant)
```

**Fixed Effects**:
- Duration (4, 8, 12 weeks)
- Frequency (2×, 5× per week)
- Proficiency Level (A2, B1-B2)
- Time (baseline, post, 3mo, 6mo)
- All interactions

**Random Effect**:
- Participant (repeated measures)

**Contrasts**:
- Compare each duration level (4 vs. 8, 8 vs. 12)
- Compare frequencies within each duration
- Test proficiency moderator

---

### Secondary Analyses

**1. Dose-Response Curve**:
- Total practice time (minutes) as continuous predictor
- Non-linear models (quadratic, piecewise regression) to identify threshold

**2. Retention Analysis**:
- Decay rate from post-test to 3-month and 6-month follow-ups
- Compare participants with vs. without continued access (exploratory)

**3. Mediation Analysis**:
- Test whether engagement (time spent) mediates duration effect
- Use structural equation modeling (SEM)

**4. Moderated Mediation**:
- Does proficiency level moderate mediation pathway?

**5. Implementation Fidelity Analysis**:
- Adherence as predictor of outcomes
- Per-protocol analysis (only participants with ≥80% adherence)

---

### Sample Size Justification

**Power Calculation Details**:
- Main effect of duration: f=0.25 (medium)
- Duration × Frequency interaction: f=0.20 (small-medium)
- Power: 0.80, Alpha: 0.05
- Required N=360 (G*Power 3.1)

**Sensitivity Analysis**:
- Minimum detectable effect size with N=360: d=0.35

---

## 📅 Timeline (24 months)

### Year 1

**Months 1-3**: Preparation
- Finalize study protocol, IRB approval
- Recruit and train research assistants (2 RAs)
- Develop chatbot conversation scripts
- Pilot test with 20 participants
- Refine based on pilot feedback

**Months 4-6**: Wave 1 Recruitment & Baseline
- Recruit 180 participants (Wave 1)
- Administer baseline IELTS
- Randomize to 6 conditions
- Begin interventions

**Months 7-9**: Wave 1 Intervention
- 4-week group completes (Month 7)
- 8-week group completes (Month 8)
- 12-week group completes (Month 9)
- Immediate post-tests administered

**Months 10-12**: Wave 2 Recruitment & Baseline
- Recruit 180 participants (Wave 2)
- Administer baseline IELTS
- Randomize to 6 conditions
- Begin interventions

### Year 2

**Months 13-15**: Wave 2 Intervention
- 4-week, 8-week, 12-week groups complete
- Immediate post-tests

**Months 16-18**: Follow-up Testing
- Wave 1: 6-month follow-ups (Months 13-15)
- Wave 2: 3-month follow-ups (Months 16-18)

**Months 19-21**: Data Analysis
- Clean and organize data
- Run statistical analyses (ANOVA, SEM)
- Prepare figures and tables

**Months 22-24**: Dissemination
- Write journal manuscripts (2-3 papers)
- Present at conferences (AAAL, TESOL, CALICO)
- Submit grant final report

---

## 💰 Budget Estimate

### Personnel (Total: $180,000)

| Role | Salary | Effort | Cost |
|------|--------|--------|------|
| Principal Investigator | $120K/year | 20% × 2 years | $48,000 |
| Co-Investigator | $90K/year | 10% × 2 years | $18,000 |
| Research Coordinator | $55K/year | 100% × 2 years | $110,000 |
| Graduate Research Assistant | $30K/year | 25% × 2 years | $15,000 (tuition waiver: $18K additional) |

**Personnel Subtotal**: $191,000 (including benefits at 20% = $38,200)
**Total Personnel**: $229,200

---

### Participant Compensation (Total: $39,600)

| Item | Rate | Quantity | Cost |
|------|------|----------|------|
| Baseline assessment | $20 | 360 | $7,200 |
| Post-test | $30 | 360 | $10,800 |
| 3-month follow-up | $30 | 324 (10% attrition) | $9,720 |
| 6-month follow-up | $40 | 306 (15% attrition) | $12,240 |

**Compensation Subtotal**: $39,960

---

### Technology & Software (Total: $25,000)

| Item | Cost |
|------|------|
| Chatbot API credits (Claude API) | $15,000 (360 participants × 12 weeks × 2.5 sessions/week avg × $0.05/session) |
| PRAAT licenses | $0 (free) |
| SPSS/R licenses | $1,500 |
| Video recording equipment | $3,000 |
| Zoom/teleconference subscriptions | $500/year × 2 = $1,000 |
| Server/cloud storage | $2,000 |
| Survey platform (Qualtrics) | $2,500 |

**Technology Subtotal**: $25,000

---

### Assessment & Materials (Total: $12,000)

| Item | Cost |
|------|------|
| IELTS examiner training & certification | $3,000 |
| Scoring honoraria (10 hours × 1,080 tests × $25/hour) | $27,000 → use trained grad students at $15/hour = $16,200 → reduce to $8,000 with efficiency |
| Test materials & rubrics | $2,000 |
| Participant recruitment ads | $2,000 |

**Assessment Subtotal**: $15,000

---

### Travel & Dissemination (Total: $8,000)

| Item | Cost |
|------|------|
| Conference registration (2 conferences × $500) | $1,000 |
| Conference travel (airfare, hotel) (2 conferences × $2,000) | $4,000 |
| Open-access publication fees (2 articles × $1,500) | $3,000 |

**Travel Subtotal**: $8,000

---

### Indirect Costs (Total: $70,000)

- University overhead (30% of direct costs)
- Calculated on modified total direct costs

---

### TOTAL BUDGET: $387,160 over 24 months

---

## 🎯 Expected Contributions

### Theoretical Contributions

1. **Threshold Model of Chatbot Effectiveness**:
   - First study to systematically test dosage (duration × frequency)
   - Establish evidence-based minimum effective dose
   - Inform SLA theory (quantity vs. quality of input)

2. **Skill Retention in Technology-Enhanced Learning**:
   - Address gap: no studies beyond 3 months
   - Test "tool dependency" hypothesis
   - Contribute to implementation science

3. **Proficiency-Differentiated Effects**:
   - Clarify for whom chatbots work best
   - Refine aptitude-treatment interaction theories

---

### Practical Contributions

1. **Evidence-Based Guidelines for Practitioners**:
   - Clear dosage recommendations (X weeks, Y sessions/week, Z minutes/session)
   - Cost-benefit analysis (longer duration worth the investment?)
   - Implementation fidelity benchmarks

2. **Policy Implications**:
   - Inform education policy on chatbot integration
   - Justify funding requests with ROI data
   - Set quality standards for edtech vendors

3. **Chatbot Design Recommendations**:
   - Optimal session length and frequency
   - Features needed for long-term engagement
   - Retention-enhancing design patterns

---

### Methodological Contributions

1. **Factorial RCT Design**:
   - Rare in SLA research (most studies single-factor)
   - Demonstrates interaction effects
   - Model for future dosage studies

2. **Long-Term Follow-Up**:
   - 6-month retention data (unprecedented in chatbot research)
   - Establish new standard for longitudinal SLA research

3. **Implementation Fidelity Measurement**:
   - Track and report fidelity (often ignored)
   - Link fidelity to outcomes (causal chain)

---

## 📄 Grant Fit & Funding Opportunities

### Recommended Funding Sources

**1. National Science Foundation (NSF)**
- **Program**: Cyberlearning and Future Learning Technologies (DRL)
- **Typical Award**: $300K-600K over 3 years
- **Fit**: Technology-enhanced learning, design-based research
- **Deadline**: Annual (typically June/July)

**2. Institute of Education Sciences (IES)**
- **Program**: Education Research Grants - Exploration
- **Typical Award**: $400K over 3-4 years
- **Fit**: RCT design, dosage research, implementation science
- **Deadline**: Annual (typically June)

**3. Spencer Foundation**
- **Program**: Large Research Grants
- **Typical Award**: $125K-500K over 1-3 years
- **Fit**: Education research, international students, language learning
- **Deadline**: Annual (typically August)

**4. Digital Promise Global**
- **Program**: Learner Variability Project
- **Typical Award**: $50K-200K over 1-2 years
- **Fit**: Personalized learning, technology integration
- **Deadline**: Rolling

---

## 📊 Preliminary Data (if needed for grant)

### Pilot Study Results (n=20)

**Design**: Single-arm pilot (all received 8-week, 5×/week intervention)

**Results**:
- Pre-test IELTS: M=5.2 (SD=0.8)
- Post-test IELTS: M=6.4 (SD=0.9)
- Effect size: d=1.36 (large)
- Adherence rate: 82% (good feasibility)
- Technical issues: 8% of sessions (acceptable)

**Conclusion**: Intervention is feasible, acceptable, and shows promising effect size. Full RCT warranted.

---

## 📝 Next Steps for Grant Submission

1. **Finalize Protocol** (2-4 weeks):
   - Refine based on feedback
   - Add assessor blinding procedures
   - Detail data management plan

2. **Secure Institutional Support** (2-4 weeks):
   - Letter from department chair
   - Letter from university language center
   - Confirm IRB timelines

3. **Recruit Collaborators** (ongoing):
   - Co-PI with SLA expertise
   - Statistician for analysis plan
   - International partners (if applicable)

4. **Write Proposal** (4-6 weeks):
   - Specific Aims (1 page)
   - Research Strategy (12 pages)
   - Budget & Justification (5 pages)
   - Biosketches & References

5. **Submit** (target deadline: NSF June 2026)

---

## 📖 References Supporting This Design

**Gap Analysis**:
- 35 studies reviewed: only 2 manipulated duration (Smith 2023, Martinez 2023)
- 0 studies with 6-month follow-up (longest: Wang 2024 at 4 months)
- 3 studies tested proficiency moderator (Lee 2023, Chen 2024, Kim 2023)

**Methodological Precedents**:
- Factorial RCT in SLA: Garcia et al. (2022) - similar design in vocabulary learning
- Dosage research: Suzuki & DeKeyser (2017) - established precedent for threshold models
- Retention studies: Kasprowicz et al. (2019) - documented decay patterns

**Measurement Tools**:
- IELTS: Used in 8/45 papers, validated extensively (Taylor & Wigglesworth 2009)
- PRAAT: Gold standard for fluency analysis (Bosker et al. 2013)

---

**Proposal Prepared By**: ResearcherRAG System
**Evidence Base**: 45 PRISMA-selected papers, systematic gap analysis
**Confidence Level**: HIGH (gaps clearly identified, design addresses gaps directly)

**Next Action**: Export this proposal to Word document for grant writing
```

**Why This Response is Optimal**:
- Grant-ready structure (follows NIH/NSF format)
- Specific hypotheses with rationale
- Detailed methodology (replicable)
- Power analysis and sample size justification
- Realistic timeline and budget
- Expected contributions (theory, practice, methodology)
- Funding source recommendations
- Direct connection to identified gaps

---

## 🎯 AI Response Quality Standards

To ensure all RAG-based answers meet high professional standards, follow this **3-tier response structure**:

### Tier 1: Summary (Top of Response)
- **3-5 sentence executive summary**
- Direct answer to the question
- Key statistics or findings
- Example: "Based on 27 RCTs, chatbots show moderate effectiveness (d=0.53). Success requires 8+ weeks, teacher integration, and technical reliability."

### Tier 2: Detailed Evidence (Body of Response)
- **Tables, lists, or structured breakdowns**
- Citations with page numbers
- Direct quotes from papers (when relevant)
- Statistical values (effect sizes, p-values, confidence intervals)
- Example: See tables in Scenario 3 (Statistical Extraction)

### Tier 3: References & Next Actions (Bottom of Response)
- **Complete citation list** (APA format)
- **Suggested follow-up queries** ("To explore further, ask...")
- **Export options** ("Save this analysis: `outputs/analysis.md`")
- **RAG transparency** ("Based on 12 chunks from 8 papers")

---

## 🔍 RAG Quality Indicators

Every RAG response should include:

✅ **Citation Transparency**:
- "Based on analysis of 45 PRISMA-selected papers"
- "8 relevant chunks retrieved"
- "Top 5 papers cited below"

✅ **Statistical Rigor**:
- Report original values (not just interpretations)
- Include confidence intervals (when available)
- Specify measurement tools

✅ **Distinguishing Fact from Inference**:
- Mark inferences: "⚠️ **Inference** (not directly stated in papers): ..."
- Mark extrapolations: "🔮 **Speculation** (RAG knowledge base incomplete): ..."
- Mark consensus: "✅ **Strong Consensus** (18/20 studies agree): ..."

✅ **Actionable Next Steps**:
- Suggest follow-up queries
- Recommend analysis scripts: `python scripts/06_query_rag.py --preset methodology_comparison`
- Export options: `outputs/summary.xlsx`

---

## 🚀 Advanced RAG Query Presets

To implement these scenarios, consider adding **preset queries** to `scripts/06_query_rag.py`:

```bash
# Scenario 1: Context Scanning
python scripts/06_query_rag.py --preset overview

# Scenario 2: Hypothesis Testing
python scripts/06_query_rag.py --preset hypothesis --arg "chatbots improve speaking"

# Scenario 3: Statistical Extraction
python scripts/06_query_rag.py --preset extract_stats --output outputs/effect_sizes.csv

# Scenario 4: Methodology Comparison
python scripts/06_query_rag.py --preset compare_methods

# Scenario 5: Contradiction Detection
python scripts/06_query_rag.py --preset contradictions

# Scenario 6: Policy Translation
python scripts/06_query_rag.py --preset policy_memo --output outputs/policy.md

# Scenario 7: Future Research
python scripts/06_query_rag.py --preset research_gaps --output outputs/grant_proposal.md
```

These presets can be implemented in the RAG script with predefined prompt templates and output formats.

---

## 📊 Response Quality Checklist

Before sending any RAG response, verify:

- [ ] **3-tier structure** (Summary → Evidence → References)?
- [ ] **Citations included** with page numbers?
- [ ] **Statistical values** reported (effect sizes, p-values, CIs)?
- [ ] **Direct quotes** for key claims (when applicable)?
- [ ] **Tables or structured data** for complex information?
- [ ] **RAG transparency** (number of chunks, papers cited)?
- [ ] **Inference vs. fact** clearly distinguished?
- [ ] **Follow-up actions** suggested?
- [ ] **Export options** provided (when relevant)?
- [ ] **No hallucination** (all claims grounded in retrieved text)?

---

**These 7 scenarios and quality standards transform Stage 6 from basic Q&A into professional research analysis.**

---

## 📍 Your Progress

```
[●●●●●●○] Stage 6/7: Research Conversation
```

**Next**: Stage 7 - Documentation & Writing
**Current**: Ongoing research analysis

---

**Ready to start?** Run the RAG interface and begin exploring your literature!
