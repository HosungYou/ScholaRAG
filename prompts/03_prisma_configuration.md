<!-- METADATA
stage: 3
stage_name: "PRISMA Configuration"
stage_goal: "Design inclusion/exclusion criteria and screening thresholds"
expected_duration: "20-30 minutes"
conversation_mode: "interactive"
prerequisites:
  - stage: 2
    requirement: "Search query designed and saved to config.yaml"
outputs:
  - prisma_criteria: "Inclusion/exclusion keyword lists with weights"
  - thresholds: "Screening, eligibility, and review queue cutoffs"
  - research_profile: "YAML configuration for automated screening"
validation_rules:
  domain_keywords:
    required: true
    min_count: 3
    validation: "Must cover core research domain"
  exclusion_keywords:
    required: false
    validation: "Should include hard exclusions (e.g., animal studies, K-12 if irrelevant)"
  screening_threshold:
    required: true
    range: [15, 35]
    default: 25
    validation: "Should result in 50-70% pass rate"
  eligibility_threshold:
    required: true
    range: [35, 55]
    default: 45
    validation: "Should result in 20-40% final inclusion rate"
cli_commands:
  - command: "scholarag test-prisma --profile config/research_profile.yaml"
    when: "User wants to preview PRISMA results before committing"
    auto_execute: false
scripts_triggered:
  - none (configuration only, PRISMA runs in Stage 5)
next_stage:
  stage: 4
  condition: "User confirms PRISMA profile and thresholds are appropriate"
  prompt_file: "04_rag_design.md"
divergence_handling:
  common_divergences:
    - pattern: "User wants to run PRISMA screening immediately"
      response: "PRISMA execution happens in Stage 5. Right now in Stage 3, let's design the criteria. We'll run all scripts together in Stage 5."
    - pattern: "User asks about PDF downloading"
      response: "PDF downloading is part of Stage 5 execution. Let's first finish designing PRISMA criteria in Stage 3, then RAG design in Stage 4."
    - pattern: "User confused about scoring system"
      response: "The scoring system is multi-dimensional (domain, method, topic, context, exclusion, title). Each dimension contributes points, total range -20 to 50. Papers scoring ≥screening threshold pass to next stage."
    - pattern: "User wants to skip PRISMA and manually select papers"
      response: "Manual selection is fine for exploratory research, but ScholaRAG is designed for PRISMA 2020 systematic reviews. If you prefer manual selection, this might not be the right tool."
conversation_flow:
  expected_turns: 6-12
  typical_pattern:
    - turn: 1
      user_action: "Provides paper collection details (count, sources)"
      claude_action: "Analyze metadata if available, ask about preferred methodologies"
    - turn: 2-4
      user_action: "Specifies inclusion preferences (methods, contexts, exclusions)"
      claude_action: "Design keyword lists across 6 dimensions with weights"
    - turn: 5-7
      user_action: "Reviews keyword lists, requests adjustments"
      claude_action: "Refine weights, add synonyms, adjust exclusions"
    - turn: 8-10
      user_action: "Tests preview or adjusts thresholds"
      claude_action: "Estimate pass rates, explain trade-offs, show sample scores"
    - turn: "final"
      user_action: "Confirms PRISMA profile"
      claude_action: "Save research_profile.yaml to config/, show Stage 4 prompt"
validation_checklist:
  - "Domain keywords cover core research area (3+ keywords)"
  - "Method keywords reflect preferred study designs"
  - "Exclusion keywords prevent irrelevant papers"
  - "Thresholds are realistic (screening: 50-70% pass, eligibility: 20-40% pass)"
  - "User understands multi-dimensional scoring system"
  - "Research profile saved to config/research_profile.yaml"
-->

# Stage 3: PRISMA Configuration

**🎯 Your Current Stage**: Stage 3 of 7
**⏱️ Expected Time**: 20-30 minutes
**💬 Format**: Interactive conversation with Claude Code
**📋 Prerequisites**: Stages 1-2 completed (research scope + query designed)

---

## 🚀 Quick Start

After completing Stages 1-2, copy this prompt to Claude Code:

---

Now that we have our search queries, I need help configuring PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) screening criteria.

**My Project Type** (from Stage 1):
[knowledge_repository OR systematic_review]

**Research Focus**: [Brief summary from Stage 1]

**Search Query**: [Your selected query from Stage 2]

**Expected Paper Count**: [Estimated from Stage 2]

---

## 📊 PRISMA Configuration by Project Type

### If Knowledge Repository 🗂️

Please help me design **minimal filtering criteria**:
1. **Technical criteria only**: Language, publication format, duplicates
2. **Spam/noise detection**: Remove clearly irrelevant papers (not domain-related)
3. **Lenient thresholds**: 80-90% retention rate (AI screening only, no human review)

**My Preferences**:
- Languages: [e.g., English only, or multilingual]
- Exclude formats: [e.g., patents, posters, editorials]
- Domain boundaries: [e.g., exclude papers completely unrelated to X field]

### If Systematic Review 📄

Please help me design **strict PRISMA criteria**:
1. **Inclusion criteria**: Domain, method, population, intervention, outcomes (with keyword weights)
2. **Exclusion criteria**: Specific exclusions (animal studies, age groups, study designs)
3. **Strict thresholds**: 2-10% final retention rate (human review required)
4. **Research profile**: Detailed YAML configuration for multi-stage screening

**My Preferences**:
- Preferred study designs: [e.g., RCT only, experimental + quasi-experimental, include qualitative]
- Must include: [e.g., specific outcomes, populations, interventions]
- Must exclude: [e.g., animal studies, K-12 if focusing on higher ed, specific contexts]

---

## 📋 What Happens in This Stage

### For Knowledge Repository 🗂️

**Claude Code Will**:

1. **Explain Minimal Filtering Approach** (Turn 1)
   - Goal: Maximize coverage, minimize false negatives
   - AI screening only (no human review required)
   - Technical filters: Language, format, duplicates

2. **Design Simple Criteria** (Turn 2-3)
   - **Language filter**: English only or multilingual
   - **Format exclusions**: Patents, posters, editorials (if desired)
   - **Domain relevance**: Broad keywords to catch spam/noise only
   - **No strict thresholds**: Accept 80-90% of papers

3. **Configure AI Screening** (Turn 4)
   - Lenient confidence thresholds (auto_include: 50, auto_exclude: 20)
   - No human validation required
   - Focus: Remove spam, duplicates, clearly irrelevant papers

4. **Save Minimal Profile** (automatic)
   - Update `config.yaml` with lenient settings
   - Expected retention: 80-90% of initial papers
   - Ready for Stage 5 execution

---

### For Systematic Review 📄

**Claude Code Will**:

1. **Explain PRISMA 2020 Workflow** (Turn 1)
   - 4 stages: Identification → Screening → Eligibility → Inclusion
   - Multi-dimensional scoring system (6 dimensions)
   - Threshold-based filtering with human review

2. **Design Detailed Keyword Lists** (Turn 2-5)
   - **Domain keywords** (0-10 points): Core research area
   - **Method keywords** (0-5 points): Study designs (RCT, experimental, etc.)
   - **Population keywords** (0-5 points): Target groups (age, setting, etc.)
   - **Intervention keywords** (0-10 points): Specific interventions tested
   - **Outcome keywords** (0-10 points): Measured outcomes
   - **Exclusion keywords** (-20 to 0 points): Hard exclusions

3. **Set Strict Thresholds** (Turn 6-8)
   - Screening threshold (recommended: 25 points, expect 50-70% pass)
   - Eligibility threshold (recommended: 45 points, expect 20-40% final)
   - Review queue range (35-44 points, manual review needed)
   - Final retention: 2-10% of initial papers

4. **Configure Human Review** (Turn 9)
   - Require human validation (review sample papers)
   - Set confidence thresholds (auto_include: 90, auto_exclude: 10)
   - Flag borderline cases for manual decision

5. **Preview and Test** (if requested)
   - Estimate pass rates based on keyword analysis
   - Show sample papers from each score range
   - Adjust thresholds if needed

6. **Save Detailed Profile** (automatic)
   - Create `config/research_profile.yaml`
   - Include all keyword lists and thresholds
   - Ready for Stage 5 execution

### ✅ Stage Completion Checklist

Before moving to Stage 4, ensure:

- [ ] **Domain keywords** cover core research area (3+ keywords)
- [ ] **Method keywords** reflect preferred study designs
- [ ] **Exclusion keywords** filter out irrelevant papers
- [ ] **Thresholds** are realistic (screening: 50-70% pass, eligibility: 20-40% final)
- [ ] You **understand scoring system** (6 dimensions, -20 to 50 range)
- [ ] **Research profile saved** to `config/research_profile.yaml`

---

## 🔍 PRISMA 2020 Workflow

```
Stage 1: Identification
├─ Papers fetched from databases (X papers)
└─ Duplicates removed (Y papers)
    ↓
Stage 2: Screening (Title/Abstract)
├─ Score ≥25 points → PASS (50-70% of Y)
└─ Score <25 points → EXCLUDE
    ↓
Stage 3: Eligibility (Detailed Assessment)
├─ Score ≥45 points → INCLUDE (20-40% of Y)
├─ Score 35-44 points → MANUAL REVIEW (10-15% of Y)
└─ Score <35 points → EXCLUDE
    ↓
Stage 4: Inclusion
└─ Final papers for RAG system (W papers)
```

---

## 📊 Multi-Dimensional Scoring System

Papers are scored across **6 dimensions** (total range: **-20 to 50 points**):

### 1. Domain Match (0-10 points)

Core research domain keywords

**Example (Education):**
```yaml
domain_keywords:
  - "language learning": 10
  - "education": 9
  - "pedagogy": 8
```

**Example (Medicine):**
```yaml
domain_keywords:
  - "clinical": 10
  - "patient": 9
  - "treatment": 8
```

**Scoring:**
- 10 points: Perfect match (3+ domain keywords)
- 7-9 points: Good match (2 domain keywords)
- 4-6 points: Moderate match (1 domain keyword)
- 0-3 points: Poor match (no domain keywords)

---

### 2. Method Match (0-5 points)

Research methodology preferences

**Example:**
```yaml
method_keywords:
  - "RCT": 5
  - "experimental": 5
  - "quasi-experimental": 4
  - "survey": 3
  - "case study": 2
```

**Scoring:**
- 5 points: Preferred method (RCT, experimental)
- 3-4 points: Acceptable method (survey, quasi-experimental)
- 1-2 points: Weak method (case study, descriptive)
- 0 points: No method mentioned

---

### 3. Topic Match (0-5 points)

Specific research focus

**Example:**
```yaml
topic_keywords:
  - "chatbot": 5
  - "conversational agent": 5
  - "learning outcomes": 4
  - "engagement": 3
```

**Scoring:**
- 5 points: Highly relevant (3+ topic keywords)
- 3-4 points: Relevant (2 topic keywords)
- 1-2 points: Somewhat relevant (1 topic keyword)
- 0 points: Not relevant

---

### 4. Context Match (0-10 points)

Research context and outcomes

**Example:**
```yaml
context_keywords:
  - "effectiveness": 10
  - "impact": 9
  - "speaking proficiency": 8
  - "higher education": 7
```

**Scoring:**
- 10 points: Perfect context (strong outcomes + setting)
- 7-9 points: Good context
- 4-6 points: Moderate context
- 0-3 points: Poor context

---

### 5. Exclusion Penalty (-20 to 0 points)

Papers to filter out

**Example:**
```yaml
exclusion_keywords:
  - "animal study": -20  # Hard exclusion (auto-fail)
  - "K-12": -10          # Strong exclusion
  - "children": -5       # Soft exclusion (penalty)
```

**Scoring:**
- -20 points: Hard exclusion (paper automatically fails)
- -10 points: Strong exclusion (very hard to recover)
- -5 points: Soft exclusion (penalty, not elimination)
- 0 points: No exclusion keywords

---

### 6. Title Bonus (0 or 10 points)

Keywords in title are stronger signals

**Scoring:**
- +10 points: Domain keyword appears in title
- 0 points: No domain keyword in title

---

## 🎯 Total Score Calculation

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

**Example paper:**
- Domain: "language learning" + "education" in abstract (8 points)
- Method: "experimental" mentioned (5 points)
- Topic: "chatbot" + "engagement" (4 points)
- Context: "effectiveness" + "higher education" (8 points)
- Exclusion: No exclusion keywords (0 penalty)
- Title: "language learning" in title (+10 bonus)

**Total: 8 + 5 + 4 + 8 + 0 + 10 = 35 points** (Manual review queue)

---

## ⚙️ Threshold Settings

| Stage | Threshold | Expected Pass Rate | Purpose |
|-------|-----------|-------------------|---------|
| **Screening** | 25 points | 50-70% | Remove obviously irrelevant |
| **Eligibility** | 45 points | 20-40% | High-quality papers only |
| **Review Queue** | 35-44 points | 10-15% | Manual review needed |
| **Auto-include** | 50 points | 5-10% | Perfect matches |

### How to Adjust Thresholds

**Too many papers passing (>70%)?**
- Increase screening threshold (25 → 30 or 35)
- Add more exclusion keywords
- Increase method/topic weight requirements

**Too few papers passing (<20%)?**
- Decrease screening threshold (25 → 20 or 15)
- Remove or soften exclusion keywords
- Add more synonyms for domain/topic keywords
- Lower method requirements (allow surveys, case studies)

---

## 📚 Example: Education Research

### Research Focus
"Effectiveness of AI chatbots in improving speaking proficiency for language learners in higher education"

### Research Profile (YAML)

```yaml
name: "AI Chatbots for Language Learning Speaking Skills"
description: "Systematic review of chatbot interventions for speaking proficiency in higher education"

# Domain keywords (max weight: 10)
domain_keywords:
  - "language learning": 10
  - "second language acquisition": 10
  - "foreign language": 9
  - "L2": 8
  - "education": 7

# Method keywords (max weight: 5)
method_keywords:
  - "RCT": 5
  - "randomized": 5
  - "experimental": 5
  - "quasi-experimental": 4
  - "survey": 3
  - "mixed methods": 3

# Topic keywords (max weight: 5)
topic_keywords:
  - "chatbot": 5
  - "conversational agent": 5
  - "dialogue system": 4
  - "virtual agent": 4
  - "AI tutor": 4

# Context keywords (max weight: 10)
context_keywords:
  - "speaking proficiency": 10
  - "oral proficiency": 10
  - "fluency": 9
  - "pronunciation": 8
  - "higher education": 7
  - "university": 7
  - "college": 6
  - "effectiveness": 8
  - "learning outcomes": 7

# Exclusion keywords (negative weights)
exclusion_keywords:
  - "animal study": -20
  - "in vitro": -20
  - "K-12": -5              # Soft (some papers compare K-12 + university)
  - "children": -10
  - "elementary": -10
  - "secondary school": -5
  - "review article": -15  # Exclude meta-analyses/reviews
  - "opinion": -15

# Thresholds
thresholds:
  screening: 25        # Stage 2 cutoff (expect 60% pass)
  eligibility: 45      # Stage 3 cutoff (expect 30% final)
  review_queue: 35     # Manual review needed
  min_inclusion: 50    # Auto-include threshold (perfect matches)
```

### Expected Conversation Flow

**Claude**: "Based on your research focus, I've designed a PRISMA profile emphasizing:

1. **Domain**: Language learning + higher education contexts
2. **Methods**: Experimental studies preferred (RCT=5), but surveys allowed (3)
3. **Topics**: Chatbots and conversational agents (high weights)
4. **Contexts**: Speaking proficiency outcomes (10), university settings (7)
5. **Exclusions**: K-12 softly excluded (-5 to allow comparative studies)

With these settings, I estimate:
- Screening pass: ~60% (if you collect 500 papers → 300 pass)
- Eligibility pass: ~30% (500 → 150 final papers)
- Manual review: ~12% (500 → 60 borderline papers)

Does this align with your research goals?"

**You**: "Yes, but I'm worried we're being too strict on methods. Some good qualitative studies might be excluded."

**Claude**: "Excellent point! Qualitative studies can provide rich insights. I'll add qualitative methods:

```yaml
method_keywords:
  - "RCT": 5
  - "experimental": 5
  - "quasi-experimental": 4
  - "survey": 3
  - "mixed methods": 3
  - "interview": 3         # Added
  - "case study": 2        # Added
  - "qualitative": 2       # Added
```

New estimates:
- Screening pass: ~65% (500 → 325 papers)
- Eligibility pass: ~35% (500 → 175 papers)

This allows strong qualitative studies to pass if they score well in other dimensions."

**You**: "Perfect! Let's proceed."

---

## 🔄 What Happens Next

### After This Conversation

1. **Research Profile Saved** ✓
   - `config/research_profile.yaml` created
   - All keyword lists and thresholds configured
   - Ready for Stage 5 automated screening

2. **You Receive Stage 4 Prompt** ➡️
   - Copy/paste to continue conversation
   - Design RAG system (chunking, embeddings, retrieval)
   - Expected time: 20-30 minutes

3. **Progress Tracking**
   - Conversation context updated in `.scholarag/context.json`
   - PRISMA configuration saved for execution in Stage 5

---

## 🚨 Troubleshooting

### "I don't understand the scoring system"

Think of it like a college application:
- **Domain** (0-10): Is this the right field? (like major fit)
- **Method** (0-5): Is the methodology rigorous? (like GPA)
- **Topic** (0-5): Is it about your specific interest? (like extracurriculars)
- **Context** (0-10): Is it the right setting/outcome? (like location preference)
- **Exclusion** (-20 to 0): Deal-breakers? (like "must not be X")
- **Title bonus** (+10): Keywords in title = stronger signal

Papers need to score well across MULTIPLE dimensions to pass.

### "How do I choose keyword weights?"

**High weight (8-10)**: Core to your research question
**Medium weight (5-7)**: Important but not essential
**Low weight (2-4)**: Nice to have, slightly relevant

**Example**: If studying "chatbot speaking proficiency in universities":
- "speaking proficiency" = 10 (core outcome)
- "university" = 7 (important context)
- "engagement" = 4 (nice to have, but not core)

### "Should I use hard exclusions (-20) or soft (-5)?"

**Hard exclusion (-20)**: Use for completely irrelevant contexts
- Animal studies (if human-only research)
- K-12 (if ONLY interested in higher education)
- Review articles (if want primary research only)

**Soft exclusion (-5 to -10)**: Use when context is mostly irrelevant but exceptions exist
- K-12 (if some papers compare K-12 + university)
- Specific diseases (if medical research with narrow focus)

**Test**: If you'd NEVER include a paper with this keyword, use -20. If exceptions are possible, use -5 or -10.

### "What if I want to test before committing?"

Ask Claude: "Can you show me example scores for these papers?" Provide 3-5 paper titles/abstracts, and Claude will calculate their PRISMA scores using your profile.

---

## 🎯 Stage 3 Success Criteria

You're ready to move to Stage 4 when:

✅ **Domain keywords** cover core research area (3+ keywords)
✅ **Method keywords** reflect preferred study designs
✅ **Exclusion keywords** filter out irrelevant contexts
✅ **Thresholds** are realistic (screening: 50-70% pass, eligibility: 20-40% final)
✅ You **understand the scoring system** (6 dimensions)
✅ **Research profile saved** to `config/research_profile.yaml`

---

## 📍 Your Progress

```
[●●●○○○○] Stage 3/7: PRISMA Configuration
```

**Next**: Stage 4 - RAG Design (20-30 min)
**After That**: Stage 5 - Execution Plan & Run (2-4 hours)

**Progress So Far**: ~55-80 minutes
**Remaining Time**: ~3-6 hours across stages 4-7

---

**Ready to continue?** Copy the prompt template above, fill in your research details, and paste it to Claude Code!
