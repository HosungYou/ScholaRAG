<!-- METADATA
stage: 3
stage_name: "AI-PRISMA Calibration"
stage_goal: "Calibrate template-free AI-PRISMA rubric and document screening rules"
expected_duration: "5-10 minutes"
conversation_mode: "interactive"
prerequisites:
  - stage: 2
    requirement: "Query strategy finalized and saved to config.yaml"
outputs:
  - ai_prisma_rubric: "Updated template-free rubric notes & thresholds in config.yaml"
  - inclusion_brief: "Plain-language inclusion/exclusion rationale saved under ai_prisma_rubric"
  - validation_plan: "Decision on human validation (required, sample size, reviewer notes)"
validation_rules:
  research_question:
    required: true
    validation: "Matches config.project.research_question"
  ai_prisma_guidance:
    required: true
    validation: "ai_prisma_rubric.notes or guidance fields populated with domain-specific cues"
  decision_confidence:
    required: true
    validation: "auto_include > auto_exclude and aligned with project_type defaults unless justified"
cli_commands:
  - command: "python scripts/validate_config.py --config config.yaml"
    when: "After editing config.yaml to confirm schema compliance"
    auto_execute: false
scripts_triggered:
  - none (rubric calibration; screening runs later in Stage 5)
next_stage:
  stage: 4
  condition: "Rubric guidance captured, thresholds confirmed, human validation plan agreed"
  prompt_file: "04_rag_design.md"
divergence_handling:
  common_divergences:
    - pattern: "User asks for keyword lists or templates"
      response: "v1.1.4 is template-free—Claude now infers signals directly from your research question. We'll describe inclusion/exclusion expectations in plain language instead of maintaining keyword YAML."
    - pattern: "User wants to run screening immediately"
      response: "We'll capture the rubric now; actual screening happens during Stage 5 execution after PDFs are ready."
    - pattern: "User unsure about thresholds"
      response: "Thresholds come from project_type: 50/20 for knowledge repositories, 90/10 with optional human validation for systematic reviews. We can document any adjustments here."
conversation_flow:
  expected_turns: 6-10
  typical_pattern:
    - turn: 1
      user_action: "Shares research question summary and project_type confirmation"
      claude_action: "Explain template-free AI-PRISMA rubric and verify research question matches config"
    - turn: 2-4
      user_action: "Clarifies desired inclusion/exclusion signals (population, intervention, outcomes, study types)"
      claude_action: "Drafts narrative guidance for each of the six scoring dimensions and highlights automatic thresholds"
    - turn: 5-7
      user_action: "Reviews guidance, decides on human validation requirements"
      claude_action: "Adjusts ai_prisma_rubric.notes/guidance, documents human validation plan"
    - turn: final
      user_action: "Approves rubric summary"
      claude_action: "Writes config snippet under ai_prisma_rubric, restates next steps, surfaces Stage 4 prompt"
validation_checklist:
  - "Research question in config.project.research_question confirmed and echoed in rubric notes"
  - "ai_prisma_rubric.notes (or guidance) captures population, intervention, outcomes, and exclusion cues in plain language"
  - "decision_confidence.auto_include / auto_exclude align with project_type defaults or have justification documented"
  - "Human validation expectations recorded (required?, sample size, reviewer role)"
  - "User understands 6-dimension scoring (domain, intervention, method, outcomes, exclusion, title bonus) and evidence requirements"
-->

# Stage 3: AI-PRISMA Calibration

**🎯 Current Stage**: 3 of 7
**⏱️ Time**: 5-10 minutes
**💬 Format**: Interactive conversation with Claude Code
**📋 Prerequisite**: Stage 2 query strategy saved to `config.yaml`

---

## 🚀 Quick Start

Copy the prompt below into Claude Code once Stage 2 is complete:

---

We finished Stage 2, and I'm ready to calibrate AI-PRISMA screening for Stage 3.

**Project Snapshot**
- Project type: [knowledge_repository | systematic_review]
- Research question: "[Paste from config.project.research_question]"
- Query scope: "[Short summary of the Stage 2 query and expected paper count]"

**What I need now**
1. Summarize how the template-free AI-PRISMA rubric works in v1.1.4 (no keyword templates).
2. Confirm thresholds (auto_include / auto_exclude) and whether human validation is required for my project type.
3. Draft plain-language guidance for the six scoring dimensions (domain, intervention, method, outcomes, exclusion, title bonus) based on my research question.
4. List clear inclusion signals and exclusion triggers the AI should look for in titles/abstracts.
5. Document any human validation plan (sample size, reviewer role) inside `ai_prisma_rubric`.
6. Provide the YAML edits I should append to `config.yaml` under `ai_prisma_rubric`.

Please keep everything template-free—the model should infer keywords dynamically from the research question rather than maintaining static lists.

---

## 🔍 How Stage 3 Works in v1.1.4

### 🆕 Template-Free AI-PRISMA v2.0

v1.1.4 eliminates manual keyword configuration. Claude now interprets your research question directly using the PICO framework.

**Key Changes from v1.1.3:**
- ❌ No `domain_keywords` lists
- ❌ No `method_keywords` lists
- ❌ No `exclusion_keywords` lists
- ❌ No `templates/research_profiles/` files
- ✅ Plain-language guidance in `ai_prisma_rubric.notes`
- ✅ Automatic keyword inference from research question

### 📊 Six Scoring Dimensions

Papers are scored across **6 dimensions** (total range: **-20 to 50 points**):

1. **Domain** (0-10 points) - Core research domain/population
2. **Intervention** (0-10 points) - Technology/treatment being studied
3. **Method** (0-5 points) - Study design rigor (RCT=5, Survey=3, Case study=2)
4. **Outcomes** (0-10 points) - Measured results relevant to research question
5. **Exclusion** (-20 to 0 points) - Hard exclusions (animal studies, editorials, etc.)
6. **Title Bonus** (+10 points) - Domain + intervention keywords in title

### 🎯 Decision Logic

Three decision thresholds based on **confidence** (0-100%) and **total score**:

```
IF confidence ≥ auto_include AND total_score ≥ 30:
    → AUTO-INCLUDE ✅
ELIF confidence ≤ auto_exclude OR total_score < 0:
    → AUTO-EXCLUDE ❌
ELSE:
    → HUMAN-REVIEW 👤
```

### 📐 Project Type Thresholds

| Project Type | auto_include | auto_exclude | Human Validation |
|--------------|--------------|--------------|------------------|
| `knowledge_repository` | 50% | 20% | Optional (default: false) |
| `systematic_review` | 90% | 10% | Required (default: true) |

### 📝 Evidence-Based Scoring

Every score must include **direct quotes** from the abstract:

```json
{
  "scores": {
    "domain": 10,
    "intervention": 10,
    "method": 4,
    "outcomes": 9
  },
  "evidence_quotes": [
    "ChatGPT was integrated into three undergraduate courses",
    "Student engagement increased by 23% (p<0.05)",
    "Quasi-experimental design with pre-test/post-test"
  ],
  "confidence": 87
}
```

If evidence is missing, confidence decreases automatically.

---

## 🧭 Conversation Outline

### Turn 1 – Recap & Reality Check

Claude restates the research question and confirms it matches `config.project.research_question`.

**Example:**
```
Your research question is: "How do AI chatbots improve speaking proficiency in EFL learners?"

This is a systematic_review project, so I'll use:
- auto_include threshold: 90%
- auto_exclude threshold: 10%
- Human validation: Required (sample size: 50, κ ≥ 0.61)

The AI-PRISMA rubric will interpret this question using PICO framework:
- Population: EFL learners (likely university/adult)
- Intervention: AI chatbots
- Outcomes: Speaking proficiency improvements
- Comparison: Any study design (RCT, quasi-experimental, survey)

Does this align with your intent?
```

### Turn 2-3 – Inclusion Signals

Discuss populations, interventions, outcomes, and study designs that **must** appear.

**Example Questions:**
- "Should I include K-12 students, or only university/adult learners?"
- "Are rule-based chatbots acceptable, or only AI/LLM-powered bots?"
- "Must the paper measure speaking proficiency directly, or are indirect measures (engagement, confidence) acceptable?"

**Claude drafts narrative guidance:**
```yaml
notes: |
  Population: University or adult EFL learners (18+). Exclude K-12 only studies.
  Intervention: AI-enabled conversational agents (ChatGPT, GPT-4, Claude, custom LLMs).
    Exclude rule-based bots without AI/NLP.
  Outcomes: Speaking proficiency metrics (fluency, pronunciation, oral exams).
    Accept: Pre-test/post-test, standardized tests (TOEFL speaking, IELTS oral).
    Exclude: Only self-reported confidence without objective measures.
  Study designs: Accept experimental, quasi-experimental, survey, mixed methods.
    Prefer RCT/experimental but don't exclude surveys.
```

### Turn 4 – Exclusion Logic

Gather "red flag" conditions that trigger penalties.

**Example Exclusions:**
- **Hard exclusions (-20 points)**: Animal studies, in vitro research, K-12 only populations, editorials/opinion pieces
- **Soft exclusions (-5 to -10)**: Purely theoretical papers, literature-only reviews, rule-based (non-AI) chatbots

**Claude documents:**
```yaml
guidance:
  exclusion_signals:
    - "Editorial/commentary only"
    - "Non-AI rule-based bot"
    - "Primary outcome unrelated to speaking"
    - "K-12 only population (if adult focus)"
    - "Animal study"
```

### Turn 5 – Human Validation Plan

Decide if expert review is required.

**For systematic_review (default):**
```yaml
human_validation:
  required: true
  sample_size: 50  # Recommended: 50-100 papers
  kappa_threshold: 0.61  # Substantial agreement
  notes: "Dual screening by PI + senior RA; reconcile disagreements weekly."
```

**For knowledge_repository (default):**
```yaml
human_validation:
  required: false
  sample_size: 0
  notes: "AI-only review for comprehensive coverage."
```

### Turn 6 – YAML Patch

Claude produces the exact YAML snippet to paste into `config.yaml`:

```yaml
ai_prisma_rubric:
  enabled: true
  llm: claude-3-5-sonnet-20241022
  temperature: 0.1
  decision_confidence:
    auto_include: 90
    auto_exclude: 10
  human_validation:
    required: true
    sample_size: 50
    kappa_threshold: 0.61
    notes: "Dual screening by PI + senior RA; reconcile disagreements weekly."
  notes: |
    Population focus: University or adult L2 learners (18+).
    Interventions: AI-enabled conversational agents, large language-model chatbots.
    Outcomes: Speaking proficiency metrics (fluency, pronunciation, oral exams).
    Must exclude: K-12 only studies, purely theoretical papers, rule-based chatbots.
    Accept borderline: Mixed-methods studies if speaking outcomes are reported.
  guidance:
    domain_signals:
      - "Higher education or adult ESL/EFL learners"
      - "Language learning / speaking proficiency context"
    intervention_signals:
      - "AI chatbot, conversational agent, LLM tutor"
    outcomes_signals:
      - "Measured improvements in speaking, pronunciation, or fluency"
    exclusion_signals:
      - "Editorials, opinion pieces, literature-only reviews"
      - "Rule-based bot without AI"
      - "Primary outcome unrelated to speaking"
    evidence_requirements:
      - "Quote one sentence for each scoring dimension."
      - "If abstract lacks detail, assign lower scores and explain the uncertainty."
```

---

## ✅ Stage 3 Completion Checklist

You're ready for Stage 4 when:

- [ ] `config.project.research_question` is confirmed and referenced in `ai_prisma_rubric.notes`
- [ ] `ai_prisma_rubric.decision_confidence` uses `50/20` (knowledge repository) or `90/10` (systematic review) unless justified
- [ ] Plain-language guidance for inclusion and exclusion signals is documented (`notes` and/or `guidance` keys)
- [ ] Human validation requirements are explicit (`required`, `sample_size`, `kappa_threshold`, reviewer notes)
- [ ] No keyword lists, template paths, or `research_profile.yaml` references remain

---

## 🔄 Next Steps

1. **Save updates**
   Append Claude's YAML snippet to `config.yaml` under `ai_prisma_rubric`.

2. **Optional validation**
   Run `python scripts/validate_config.py --config config.yaml` to confirm structure.

3. **Preview Stage 5 usage**
   Screening will later be executed with:
   ```bash
   python scripts/03_screen_papers.py --project . --question "<research question>"
   ```

4. **Proceed to Stage 4**
   Copy `prompts/04_rag_design.md` once rubric calibration is signed off.

---

## 🚨 Troubleshooting

### "Do I still need to provide keyword lists?"

No. Template-based lists were removed in v1.1.4. Capture expectations as narrative guidance instead.

### "Why do I need a research question if it's already in config?"

Stage 3 ensures the research question is up-to-date and matches what the screening script requires. This becomes the single source of truth passed to `03_screen_papers.py`.

### "Can I change thresholds?"

Only if you switch project_type or have a documented rationale. Otherwise keep defaults:
- 90/10 for systematic review
- 50/20 for knowledge repository

### "How do I document edge cases?"

Add notes under `guidance` (e.g., "allow mixed populations if adult learners constitute >50% of sample").

### "What if I'm migrating from v1.1.3?"

Delete old keyword-based config:
```bash
# Remove old structure
vim config.yaml
# Delete these sections if they exist:
# - domain_keywords
# - method_keywords
# - topic_keywords
# - exclusion_keywords
# - templates/research_profiles/ references
```

Add new rubric guidance as shown in Turn 6 above.

---

## 📍 Progress Tracker

```
[●●●○○○○] Stage 3/7: AI-PRISMA Calibration
```

**Next**: Stage 4 – RAG Design (20-30 min)
**Later**: Stage 5 – Pipeline Execution (2-4 hours)
**Cumulative time so far**: ~40-60 minutes (down from ~70-110 in v1.1.3)

---

**Ready for Stage 4?** Paste the updated prompt and continue the pipeline with confidence in your template-free rubric.
