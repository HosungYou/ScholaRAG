# Stage 2: Query Strategy Design

**Load this file when**: Researcher provides Stage 2 prompt (after completing Stage 1)

**Expected duration**: 20-30 minutes (5-10 conversational turns)

**Goal**: Design optimal search queries with precision/recall trade-off

---

## Quick Overview

**What happens in this stage**:
1. Understand must-include/exclude keywords from research question
2. Design 2-3 query options (broad, focused, narrow)
3. Explain Boolean operators and synonym grouping
4. Estimate paper counts for each query option
5. Iterate based on feedback (2-4 rounds typical)
6. User selects final query
7. Save to config.yaml

**What you'll execute**:
```python
# Update config.yaml with selected query
import yaml

with open('projects/YYYY-MM-DD_ProjectName/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

config['search_query'] = "(chatbot OR agent) AND (language learning OR L2) AND (speaking OR oral)"

with open('projects/YYYY-MM-DD_ProjectName/config.yaml', 'w') as f:
    yaml.dump(config, f)
```

---

## API Query Syntax Reference

**Load full reference if needed**: [skills/reference/api_reference.md](../reference/api_reference.md)

### Quick Syntax Table

| API | Boolean Operators | Wildcards | Phrase Search | Proximity |
|-----|-------------------|-----------|---------------|-----------|
| **Semantic Scholar** | AND, OR, NOT | ❌ No | "exact phrase" | ❌ No |
| **OpenAlex** | AND, OR, NOT | ❌ No | "exact phrase" | ❌ No |
| **arXiv** | AND, OR, ANDNOT | ❌ No | "exact phrase" | ❌ No |

**Example queries**:
```
# Broad
"chatbot AND language"

# Focused (with synonyms)
"(chatbot OR agent OR conversational) AND (language OR L2 OR foreign)"

# Narrow (with specific outcomes)
"(chatbot OR agent) AND (language learning OR L2 acquisition) AND (speaking OR oral OR pronunciation) AND (proficiency OR improvement)"
```

---

## Conversation Flow (5-10 Turns)

### Turn 1: Extract Core Concepts

**From Stage 1 research question**: "How do AI chatbots improve speaking proficiency in university language learners?"

**Your action**: Identify 3-4 core concepts, ask about must-include keywords

**Example**:
```
YOU: "From your research question, I've identified these core concepts:

**Concept 1: Intervention**
- Primary: chatbot
- Synonyms: conversational agent, dialogue system, virtual tutor

**Concept 2: Domain**
- Primary: language learning
- Synonyms: L2 acquisition, foreign language, second language

**Concept 3: Outcome**
- Primary: speaking proficiency
- Synonyms: oral skills, speaking ability, pronunciation, fluency

**Concept 4: Context** (optional)
- Primary: university
- Synonyms: higher education, college, tertiary

**Questions**:
1. Are there any MUST-INCLUDE keywords? (e.g., must have 'chatbot', can't be just 'virtual tutor')
2. Any MUST-EXCLUDE keywords? (e.g., exclude 'writing', exclude 'K-12')
3. Should we include broader terms like 'AI' or stick to 'chatbot' only?

This will help me design queries with the right precision/recall balance."
```

### Turn 2-3: Design 3 Query Options

**User provides**: Keyword preferences, constraints

**Your action**: Design 3 queries (broad, focused, narrow), estimate paper counts

**Example**:
```
YOU: "Based on your preferences, here are 3 query options:

**Query 1: BROAD (Maximum Recall)**
```
(chatbot OR agent) AND language
```
**Estimated papers**: 15,000-20,000
**Precision**: Low (~10-20% relevant)
**Recall**: High (~95% of relevant papers captured)
**Good for**: knowledge_repository mode, exploratory research
**Risk**: Many irrelevant papers (chatbot + programming languages, non-learning contexts)

---

**Query 2: FOCUSED (Balanced) ✅ RECOMMENDED**
```
(chatbot OR "conversational agent" OR "dialogue system") AND ("language learning" OR "L2 acquisition" OR "foreign language") AND (speaking OR oral OR pronunciation)
```
**Estimated papers**: 500-1,500
**Precision**: Medium (~40-60% relevant)
**Recall**: Medium (~70-80% of relevant papers)
**Good for**: systematic_review mode, dissertation
**Advantage**: Captures most relevant papers, manageable screening workload

---

**Query 3: NARROW (Maximum Precision)**
```
(chatbot OR "conversational agent") AND ("language learning" OR "L2") AND (speaking OR oral) AND (proficiency OR improvement OR effectiveness) AND (university OR college OR "higher education")
```
**Estimated papers**: 200-500
**Precision**: High (~70-90% relevant)
**Recall**: Lower (~50-60% of relevant papers)
**Good for**: Very specific systematic review, tight timeline
**Risk**: May miss relevant papers that use different terminology

---

**My recommendation**: Query 2 (Focused)
- Balanced precision/recall
- Appropriate for systematic_review (your project_type)
- Estimated ~50-200 final papers after 90% screening (matches your target)

Which query aligns with your goals? Or shall I refine any of these?"
```

### Turn 4-6: Iteration and Refinement

**User provides**: Feedback (too broad/narrow, missing terms, etc.)

**Your action**: Refine query, explain trade-offs

**Example iteration 1**:
```
USER: "Query 2 looks good, but I'm also interested in 'fluency', not just 'pronunciation'"

YOU: "Great catch! Let's add 'fluency' to the outcome terms:

**Query 2 REVISED**:
```
(chatbot OR "conversational agent" OR "dialogue system") AND ("language learning" OR "L2 acquisition") AND (speaking OR oral OR pronunciation OR fluency)
```

**Impact**:
- **Before**: ~500-1,500 papers
- **After**: ~800-2,000 papers (+60% papers)
- **Precision**: ~40-60% (unchanged, still relevant)

**Analysis**: Adding 'fluency' captures papers that focus on fluency metrics (words per minute, hesitation, natural flow) rather than just pronunciation accuracy. This broadens your outcome scope appropriately.

Shall we test this query with a preview?"
```

**Example iteration 2**:
```
USER: "Can we exclude papers about writing or reading?"

YOU: "Yes! We can add exclusion terms using NOT/ANDNOT:

**Query 2 with Exclusions**:
```
(chatbot OR "conversational agent") AND ("language learning" OR "L2") AND (speaking OR oral OR fluency) NOT (writing OR reading OR literacy)
```

**Impact**:
- Excludes papers focused only on writing/reading skills
- Estimated reduction: -30% papers (many multimodal studies)
- **New estimate**: ~600-1,400 papers

**Warning**: This might exclude papers that study ALL four skills (listening, speaking, reading, writing) but include speaking outcomes. Those papers could still be valuable.

**Alternative approach**: Include those papers in fetching, then exclude during Stage 3 screening based on 'primary outcome must be speaking'. This gives you more control.

Which approach do you prefer?"
```

### Turn 7-8: Dry Run Preview

**User confirms**: Query looks good

**Your action**: Run dry-run to show top 10 papers, validate relevance

**Example**:
```
YOU: "Let me run a quick dry-run to show you the top 10 papers this query would fetch:

```python
# Dry run (doesn't save results)
python scripts/01_fetch_papers.py \
  --project projects/2025-10-24_AI-Chatbots/ \
  --query '(chatbot OR "conversational agent") AND "language learning" AND speaking' \
  --dry-run \
  --limit 10
```

**Top 10 Results**:

1. ✅ **Smith et al. (2023)** - 'Effectiveness of AI chatbots for improving L2 speaking proficiency'
   - Relevance: HIGH (perfect match)

2. ✅ **Chen & Wang (2022)** - 'Conversational agents in language learning: Impact on oral fluency'
   - Relevance: HIGH (good match)

3. ✅ **Garcia (2023)** - 'Chatbot-assisted speaking practice for university ESL students'
   - Relevance: HIGH (exact population)

4. ⚠️ **Lee et al. (2021)** - 'Dialogue systems for language learning across four skills'
   - Relevance: MEDIUM (includes speaking but not primary focus)

5. ❌ **Johnson (2020)** - 'Chatbots for programming language education'
   - Relevance: LOW (wrong domain, 'language' = programming)

6. ✅ **Rodriguez (2022)** - 'AI tutors for pronunciation training in L2 Spanish'
   - Relevance: HIGH

7. ✅ **Kim & Park (2023)** - 'Speaking confidence improvement via chatbot interaction'
   - Relevance: HIGH

8. ⚠️ **Taylor (2021)** - 'Conversational AI for language assessment'
   - Relevance: MEDIUM (assessment focus, not intervention)

9. ✅ **Zhang (2022)** - 'Chatbot-mediated speaking practice: An experimental study'
   - Relevance: HIGH

10. ❌ **Brown (2019)** - 'Natural language processing for chatbot development'
    - Relevance: LOW (technical NLP paper, not learning study)

**Analysis**:
- **HIGH relevance**: 6/10 (60%)
- **MEDIUM relevance**: 2/10 (20%)
- **LOW relevance**: 2/10 (20%)

**Precision**: 60% (good for balanced query!)
**Next step**: Stage 3 screening will filter MEDIUM/LOW papers using 90% AI confidence threshold

Is this relevance distribution acceptable? Or shall we adjust the query to increase precision?"
```

### Turn 9-10: Final Confirmation

**User approves**: Query is good

**Your action**: Save to config.yaml, explain next stage, show Stage 3 prompt

**Example**:
```
YOU: "Perfect! I'll save this query to your project config.

```python
import yaml

# Load config
with open('projects/2025-10-24_AI-Chatbots/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Add search query
config['search_query'] = '(chatbot OR "conversational agent") AND ("language learning" OR "L2") AND (speaking OR oral OR fluency)'

# Save
with open('projects/2025-10-24_AI-Chatbots/config.yaml', 'w') as f:
    yaml.dump(config, f, sort_keys=False)

print("✅ Query saved to config.yaml")
```

**Output**:
```
✅ Query saved to config.yaml

**What's next (Stage 3 - PRISMA Configuration)**:
1. Define inclusion/exclusion criteria for screening
2. Configure screening threshold (50% or 90% based on your project_type: systematic_review → 90%)
3. Design screening questions for AI reviewer

**Preview**:
- Your query will fetch ~1,000 papers (estimated)
- After deduplication (Stage 2 script): ~800 unique papers
- After AI screening at 90% threshold (Stage 3): ~50-150 highly relevant papers
- After PDF download (Stage 4): ~30-100 papers with full text

This pipeline gets you from 1,000 papers → 30-100 high-quality papers automatically!

Ready for Stage 3? Here's your prompt:

[Shows Stage 3 prompt from prompts/03_prisma_configuration.md]
```

---

## Common Issues

### Issue 1: Query returns <100 papers

**Diagnosis**: Too narrow, missing synonyms

**Solution**:
```
"Your query is returning very few papers (<100). Let's broaden it:

**Current query**:
```
"GPT-4 chatbot" AND "pronunciation accuracy" AND "Korean university students"
```

**Problems**:
1. "GPT-4" limits to 2023-2024 only (~2 years of research)
2. "pronunciation accuracy" misses papers that say "pronunciation improvement", "accent reduction"
3. "Korean university students" excludes all other populations

**Recommended broadening**:
```
(chatbot OR "conversational AI" OR GPT) AND (pronunciation OR accent OR speaking) AND (university OR college OR "higher education")
```

**Changes**:
- ✅ "GPT-4" → "GPT" or "chatbot" (captures GPT-3, GPT-4, other models)
- ✅ "pronunciation accuracy" → "pronunciation OR accent OR speaking" (captures related terms)
- ✅ "Korean" removed (can filter by population in Stage 3 screening)

**Expected impact**: <100 → ~500-800 papers

Would you like to try this broader query?"
```

### Issue 2: Query returns >50,000 papers

**Diagnosis**: Too broad, missing specificity

**Solution**:
```
"Your query is very broad (>50,000 papers). This will create challenges:

**Current query**:
```
chatbot AND education
```

**Problems**:
1. 'chatbot' includes: customer service bots, mental health bots, tutoring bots (all domains)
2. 'education' includes: K-12, higher ed, corporate training, informal learning

**Recommended narrowing**:

**Option 1: Add domain specificity**
```
chatbot AND ("language learning" OR linguistics OR "second language")
```
**Impact**: 50,000 → 5,000 papers

**Option 2: Add outcome specificity**
```
chatbot AND education AND (speaking OR oral OR pronunciation OR fluency)
```
**Impact**: 50,000 → 8,000 papers

**Option 3: Combine both (RECOMMENDED)**
```
chatbot AND ("language learning" OR "L2 acquisition") AND (speaking OR oral)
```
**Impact**: 50,000 → 1,500 papers (manageable!)

**Rationale**: For systematic_review mode with 90% threshold, you want 1,000-5,000 initial papers. Your current 50,000 would take 10+ hours just for screening.

Shall we narrow to Option 3?"
```

### Issue 3: User confused about Boolean operators

**Pattern**: "What's the difference between AND vs OR?"

**Solution**:
```
"Great question! Boolean operators control how terms combine:

**AND**: Both terms MUST appear
```
chatbot AND education
```
- ✅ Matches: Papers with BOTH 'chatbot' AND 'education'
- ❌ Excludes: Papers with only 'chatbot' (no 'education')
- ❌ Excludes: Papers with only 'education' (no 'chatbot')
- **Effect**: Narrows results (fewer papers, higher precision)

**OR**: At least ONE term must appear
```
chatbot OR agent
```
- ✅ Matches: Papers with 'chatbot'
- ✅ Matches: Papers with 'agent'
- ✅ Matches: Papers with BOTH 'chatbot' AND 'agent'
- **Effect**: Broadens results (more papers, captures synonyms)

**NOT**: Excludes papers with this term
```
education NOT K-12
```
- ✅ Matches: Papers with 'education' but NOT 'K-12'
- ❌ Excludes: Papers with both 'education' AND 'K-12'
- **Effect**: Filters out unwanted papers

**Combining operators** (use parentheses for grouping):
```
(chatbot OR agent) AND (education OR learning) NOT K-12
```
- Matches: Papers with (chatbot OR agent) AND (education OR learning) but NOT K-12
- Example matches:
  - ✅ 'Chatbot for higher education learning'
  - ✅ 'Conversational agent in university education'
  - ❌ 'Chatbot for K-12 education' (excluded by NOT K-12)

**Your research question**: 'AI chatbots for language learning speaking skills'
**Suggested query**:
```
(chatbot OR "conversational agent") AND ("language learning" OR L2) AND (speaking OR oral)
```

**Breakdown**:
- (chatbot OR "conversational agent"): Captures synonyms
- AND: MUST have language learning term
- ("language learning" OR L2): Captures different ways authors describe domain
- AND: MUST have speaking term
- (speaking OR oral): Captures different outcome descriptions

Makes sense?"
```

---

## Completion Checklist

Before moving to Stage 3, verify:

- [ ] **Core concepts identified**: 3-4 concepts from research question
- [ ] **Synonyms included**: Each concept has OR-grouped synonyms
- [ ] **Boolean syntax correct**: Parentheses used for grouping
- [ ] **Query tested**: Dry run shows top 10 papers
- [ ] **Relevance validated**: User confirms top papers are relevant
- [ ] **Paper count realistic**:
  - [ ] knowledge_repository: 10,000-30,000 initial papers
  - [ ] systematic_review: 500-5,000 initial papers
- [ ] **Exclusions considered**: Discussed NOT terms if needed
- [ ] **Query saved**: Written to config.yaml
- [ ] **User understands**: Next stage is PRISMA screening

**If all checked**: ✅ Show Stage 3 prompt

**If any unchecked**: ❌ Continue iterating query

---

## Reference Integration

**Load on-demand**:
- [skills/reference/api_reference.md](../reference/api_reference.md) - If user asks about API syntax details

**Next stage**:
- [skills/claude_only/stage3_prisma_config.md](stage3_prisma_config.md)

---

**Last Updated**: 2025-10-24
**Version**: 2.0
**Token Budget**: ~350 lines
