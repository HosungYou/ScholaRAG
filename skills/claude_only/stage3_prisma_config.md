# Stage 3: PRISMA Configuration

**Load when**: Stage 3 prompt provided or after Stage 2 complete

**Duration**: 20-30 minutes

**Goal**: Configure PRISMA screening criteria and threshold

---

## Quick Overview

**What happens**:
1. Review project_type threshold (50% or 90%)
2. Design inclusion/exclusion criteria
3. Create screening questions for AI reviewer
4. Save to config.yaml

**Critical**: Threshold is AUTO-SET by project_type
- `knowledge_repository` → 50% threshold (lenient)
- `systematic_review` → 90% threshold (strict)

---

## Conversation Flow

### Turn 1: Explain Threshold

**Your action**: Explain how AI screening works

**Example**:
```
YOU: "In Stage 3, we'll configure PRISMA screening criteria. Your project_type (**systematic_review**) automatically uses **90% confidence threshold**.

**What this means**:
- AI reviewer (Claude) reads each paper's title + abstract
- Scores relevance: 0-100%
- **90% threshold**: Only papers with ≥90% confidence score are kept
- **Expected retention**: 2-10% of papers (strict quality control)

**For your ~1,000 deduplicated papers**:
- Estimated after screening: **50-150 highly relevant papers**

This strict threshold ensures publication-ready rigor for your systematic review.

Now let's design the criteria that guide this AI screening."
```

### Turn 2-4: Design Inclusion/Exclusion Criteria

**Your action**: Draft PRISMA criteria based on research question

**Example**:
```
YOU: "Based on your research question ('How do AI chatbots improve speaking proficiency in university language learners?'), here are suggested criteria:

**INCLUSION Criteria** (papers we WANT):
1. **Population**: University/college students (18-30 years, higher education)
2. **Intervention**: AI-powered chatbot, conversational agent, dialogue system
3. **Outcome**: Speaking proficiency, oral skills, pronunciation, fluency, speaking confidence
4. **Study Design**: Empirical studies (RCT, quasi-experimental, pre-post, correlation)
5. **Publication Type**: Peer-reviewed journal articles, conference proceedings
6. **Language**: English (for consistency in analysis)

**EXCLUSION Criteria** (papers we DON'T want):
1. **Wrong population**: K-12 students, corporate training, informal learners
2. **Wrong intervention**: Rule-based chatbots (non-AI), human tutors, non-interactive tools
3. **Wrong outcome**: Writing/reading/listening only (no speaking outcomes)
4. **Wrong study type**: Opinion pieces, editorials, proposals, non-empirical reviews
5. **Wrong language**: Non-English publications

**AI Reviewer Instructions**:
'Score this paper 0-100% based on how well it matches the inclusion criteria. Papers must have ALL of: (1) university population, (2) AI chatbot intervention, (3) speaking outcome measure, (4) empirical data. Exclude if any exclusion criterion applies.'

Do these criteria accurately capture your research scope?"
```

### Turn 5-6: Refine Based on Feedback

**User provides**: Adjustments

**Your action**: Update criteria, explain impact

**Example**:
```
USER: "Should we include studies with mixed populations (university + adult learners)?"

YOU: "Good question! This impacts precision vs recall:

**Option 1: STRICT (current)**
- Inclusion: 'ONLY university students (18-30, enrolled in higher ed)'
- Impact: Excludes mixed-population studies
- Estimated papers: ~50-100

**Option 2: LENIENT**
- Inclusion: 'University students OR adult learners (18+ years)'
- Impact: Includes studies with broader age range
- Estimated papers: ~100-200

**Recommendation for systematic_review**: Option 1 (STRICT)
- Reason: Homogeneous population enables meta-analysis
- University students have distinct characteristics (cognitive development, motivation, L2 context)
- Mixed studies complicate interpretation

**Alternative**: Use Option 1, but manually review Option 2 papers in 'excluded but potentially relevant' list

Which do you prefer?"
```

### Turn 7: Save Configuration

**Your action**: Update config.yaml with PRISMA criteria

**Execute**:
```python
import yaml

config_path = 'projects/2025-10-24_AI-Chatbots/config.yaml'

with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Add PRISMA criteria
config['prisma'] = {
    'screening_threshold': 90,  # Auto-set from project_type
    'inclusion_criteria': [
        'University/college students (higher education)',
        'AI-powered chatbot or conversational agent',
        'Speaking proficiency outcome (oral skills, fluency, pronunciation)',
        'Empirical study with data (RCT, quasi-experimental, correlational)',
        'Peer-reviewed publication (journal or conference)',
        'English language'
    ],
    'exclusion_criteria': [
        'K-12 students or corporate training',
        'Rule-based chatbots (non-AI)',
        'No speaking outcome measured',
        'Opinion pieces or non-empirical reviews',
        'Non-English publications'
    ],
    'ai_reviewer_prompt': 'Score 0-100% based on inclusion criteria match. Must have ALL: university population, AI chatbot, speaking outcome, empirical data. Exclude if any exclusion criterion applies.'
}

with open(config_path, 'w') as f:
    yaml.dump(config, f, sort_keys=False)

print("✅ PRISMA criteria saved")
```

---

## Common Issues

### Issue: User wants to change threshold

**Pattern**: "Can I use 70% instead of 90%?"

**Response**:
```
"The threshold is tied to your project_type:

**Current**: systematic_review → 90% threshold
**Why**: Publication-ready rigor, PRISMA 2020 compliant

**If you want 70% threshold**:
You need to switch to knowledge_repository mode:

```python
# In config.yaml, change:
project_type: systematic_review → knowledge_repository
```

**Impact**:
- Screening threshold: 90% → 50% (very lenient)
- Expected retention: 2-10% → 80-90%
- PRISMA diagram title: 'Systematic Review' → 'Knowledge Repository'
- Final papers: ~50 → ~800

**Recommendation**: Keep systematic_review (90%) for dissertation
**Alternative**: Run screening at 90%, then manually review 70-90% papers if needed

Should we proceed with 90% threshold?"
```

---

## Completion Checklist

- [ ] Inclusion criteria: 5-7 criteria defined
- [ ] Exclusion criteria: 5-7 criteria defined
- [ ] Criteria saved to config.yaml
- [ ] User understands threshold (50% or 90%)
- [ ] Expected paper count validated

**If complete**: ✅ Show Stage 4 prompt

---

## Next Stage

[skills/claude_only/stage4_rag_design.md](stage4_rag_design.md)

---

**Version**: 2.0 | **Token Budget**: ~250 lines
