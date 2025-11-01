<!-- METADATA
stage: 2
stage_name: "Query Strategy Design"
stage_goal: "Design effective search queries with optimal precision/recall trade-off"
expected_duration: "20-30 minutes"
conversation_mode: "interactive"
prerequisites:
  - stage: 1
    requirement: "Research scope and data sources confirmed"
outputs:
  - query_strategies: "2-3 query options (broad/focused/narrow)"
  - estimated_counts: "Expected paper count for each query"
  - selected_query: "Final query choice with rationale"
  - database_mapping: "Query syntax adapted for each database"
validation_rules:
  query_completeness:
    required: true
    validation: "Query must include core concepts, domain context, and scope constraints"
  synonym_coverage:
    required: true
    validation: "Must use OR for synonyms (e.g., 'chatbot OR conversational agent')"
  estimated_papers:
    required: true
    range: [20, 5000]
    validation: "Realistic paper count between 20-5000"
  boolean_syntax:
    required: true
    validation: "Proper use of AND, OR, NOT, parentheses"
cli_commands:
  - command: "scholarag test-query --query '[QUERY]' --database semantic_scholar"
    when: "User wants to preview results before committing"
    auto_execute: false
scripts_triggered:
  - none (query design only, execution happens in Stage 5)
next_stage:
  stage: 3
  condition: "User confirms query strategy and estimated counts are acceptable"
  prompt_file: "03_prisma_configuration.md"
divergence_handling:
  common_divergences:
    - pattern: "User wants to start fetching papers immediately"
      response: "Great enthusiasm! But we need to complete Stage 3 (PRISMA configuration) first to set up inclusion/exclusion criteria. This ensures we screen papers systematically."
    - pattern: "User asks about API keys or technical setup"
      response: "API setup happens in Stage 5 (Execution). Right now in Stage 2, let's focus on designing the best possible queries. We'll handle technical setup later."
    - pattern: "User asks about screening or deduplication"
      response: "Excellent question! That's Stage 3 (PRISMA configuration). Let's finalize your queries first in Stage 2, then we'll design screening criteria."
    - pattern: "User wants only 1 query option"
      response: "I recommend seeing 2-3 options to understand precision/recall trade-offs. We can always adjust later if the initial query isn't working well."
    - pattern: "User unsure about boolean operators"
      response: "No problem! I'll design the queries for you and explain each component simply. You can also choose 'Just give me the final query' if you prefer not to understand the syntax."
conversation_flow:
  expected_turns: 5-10
  typical_pattern:
    - turn: 1
      user_action: "Provides confirmed research focus and preferences (broad/focused/narrow)"
      claude_action: "Ask about must-include/must-exclude keywords, technical comfort level"
    - turn: 2-3
      user_action: "Specifies additional constraints (keywords, exclusions)"
      claude_action: "Design 2-3 query options with different breadth levels"
    - turn: 4-6
      user_action: "Reviews queries, asks for adjustments (add/remove keywords)"
      claude_action: "Refine queries, explain trade-offs, estimate paper counts"
    - turn: 7-8
      user_action: "Tests query preview or requests narrow/broad variants"
      claude_action: "Show top 10 paper titles, adjust query based on feedback"
    - turn: "final"
      user_action: "Confirms final query choice"
      claude_action: "Save query to config.yaml, summarize decisions, show Stage 3 prompt"
validation_checklist:
  - "Query includes all core concepts (using OR for synonyms)"
  - "Query has proper boolean syntax (AND, OR, NOT, parentheses)"
  - "Estimated paper count is realistic (20-5000 papers)"
  - "User understands precision/recall trade-off"
  - "Query has been tested or previewed with sample results"
  - "Final query choice is confirmed and saved to config.yaml"
-->

# Stage 2: Query Strategy Design

**🎯 Your Current Stage**: Stage 2 of 7
**⏱️ Expected Time**: 20-30 minutes
**💬 Format**: Interactive conversation with Claude Code
**📋 Prerequisites**: Stage 1 completed (research scope defined)

---

## 🚀 Quick Start

After completing Stage 1 (Research Domain Setup), copy this prompt to Claude Code:

---

Now that we've defined my research scope, please help me design effective search queries for academic databases.

**Confirmed Research Focus**:
[Summarize what you agreed on with Claude in Stage 1]

**My Project Type** (from Stage 1):
[knowledge_repository OR systematic_review]

**My Preferences**:

1. **Query Breadth** (depends on your project type):

   **If Knowledge Repository**:
   - [ ] Comprehensive (recommended for knowledge repository) - Maximize domain coverage (20,000+ papers)
   - [ ] Moderate - Balance coverage and relevance (5,000-10,000 papers)

   **If Systematic Review**:
   - [ ] Broad (high recall) - Comprehensive coverage for publication (1,000-5,000 papers)
   - [ ] Balanced (recommended for SLR) - Quality papers without too much noise (500-800 papers)
   - [ ] Narrow (high precision) - Only the most relevant papers (100-300 papers)

2. **Data Sources**:
   - [ ] Semantic Scholar (CS, Engineering, Sciences - 40% open access PDFs)

     ⚠️  **Performance Tip**: Get a free API key for 10x faster retrieval
     - Without key: 100 requests/5 min (slower, may take 30-60 minutes)
     - With key: 1,000 requests/5 min (faster, ~5-10 minutes)
     - Get free key: https://www.semanticscholar.org/product/api#api-key
     - You'll be prompted to enter it when fetching papers (optional)

   - [ ] OpenAlex (All fields, comprehensive - 50% open access)
   - [ ] arXiv (STEM preprints - 100% PDF access)
   - [ ] Let Claude recommend the best combination for my field

3. **Technical Comfort**:
   - [ ] I'm comfortable with boolean operators (AND, OR, NOT)
   - [ ] Please explain boolean operators simply
   - [ ] Just give me the final query (I don't need to understand the syntax)

**Additional Constraints**:
- Must include keywords: [e.g., "experimental", "RCT"]
- Must exclude keywords: [e.g., "animal study", "in vitro"]
- Year range: [e.g., 2015-2024]

Please design 2-3 query options (broad/focused/narrow) and estimate the expected paper count for each. I'd also like to understand the trade-offs.

---

## 📋 What Happens in This Stage

### Claude Code Will:

1. **Analyze Your Research Domain** (Turn 1-2)
   - Identify core concepts and their synonyms
   - Understand field-specific terminology
   - Map research questions to searchable terms

2. **Design Query Strategies Based on Project Type** (Turn 3-4)

   **For Knowledge Repository**:
   - **Comprehensive**: Maximum domain coverage (20,000-30,000 papers) ⭐ **RECOMMENDED**
   - **Moderate**: Balanced scope (5,000-10,000 papers)

   **For Systematic Review**:
   - **Broad**: High recall, comprehensive coverage (1,500-5,000 papers)
   - **Balanced**: Balanced precision/recall (500-800 papers) ⭐ **RECOMMENDED**
   - **Narrow**: High precision, minimal noise (100-300 papers)

3. **Explain Boolean Operators** (if requested)
   - How AND, OR, NOT work
   - Why parentheses matter
   - How to read complex queries

4. **Estimate Paper Counts** (Turn 5-6)
   - Preview results using database APIs
   - Show top 10 paper titles for validation
   - Adjust if counts are way off target

5. **Save Final Query** (automatic)
   - Update `config.yaml` with selected query
   - Save alternative queries as backups
   - Prepare for Stage 3 AI-PRISMA calibration

### ✅ Stage Completion Checklist

Before moving to Stage 3, ensure:

- [ ] Query includes **all core concepts** (not just one keyword)
- [ ] Synonyms are grouped with **OR** (e.g., "chatbot OR conversational agent")
- [ ] Boolean syntax is **correct** (proper use of AND, OR, NOT, parentheses)
- [ ] Estimated paper count is **realistic** (20-5000 papers, ideally 100-800)
- [ ] You've **tested or previewed** results (top 10 papers look relevant)
- [ ] Final query is **confirmed and saved** to config.yaml

---

## 📊 Understanding Query Trade-offs

### For Knowledge Repository Projects 🗂️

**Goal**: Maximize domain coverage for comprehensive knowledge base

| Query Type | Papers Found | Retention After Filtering | Screening Approach | Philosophy |
|------------|--------------|---------------------------|--------------------|--------------|
| **Comprehensive** ⭐ | 20,000-30,000 | 15,000-20,000 (80-90%) | AI-only, minimal filtering | Maximize coverage |
| **Moderate** | 5,000-10,000 | 4,000-8,000 (80-90%) | AI-only, minimal filtering | Balanced scope |

**💡 Recommendation**: Use **Comprehensive** for knowledge repositories - you want maximum coverage with minimal filtering.

**Trade-off Philosophy**:
- No human review required
- AI removes only spam/duplicates/clearly irrelevant
- Accept 10-20% noise for complete domain coverage
- Large dataset enables better semantic search

---

### For Systematic Review Projects 📄

**Goal**: Publication-quality PRISMA review with strict criteria

| Query Type | Papers Found | After PRISMA Filtering | Screening Time | Risk |
|------------|--------------|------------------------|----------------|------|
| **Broad** | 1,500-5,000 | 50-300 (2-10%) | High (3-5 days) | Miss nothing |
| **Balanced** ⭐ | 500-800 | 50-150 (5-20%) | Medium (1 day) | Good coverage |
| **Narrow** | 100-300 | 30-100 (20-40%) | Low (2-3 hours) | May miss papers |

**💡 Recommendation**: Use **Balanced**, then broaden if missing important papers after screening.

**Trade-off Philosophy**:
- Human review required for final decisions
- Strict inclusion/exclusion criteria (study design, population, intervention)
- High rejection rate (80-98%) is normal for systematic reviews
- Small final dataset for deep analysis

---

### When to Choose Each Strategy

```
What is your project type?
│
├─ Knowledge Repository 🗂️
│   └─ Use Comprehensive query (20,000+ papers)
│       └─ Trade-off: Large dataset, minimal filtering, no human review needed
│
└─ Systematic Review 📄
    │
    ├─ Do you want comprehensive coverage for publication?
    │   └─ YES → Use Broad query
    │       └─ Trade-off: 3-5 days screening, strict PRISMA filtering, 50-300 final papers
    │
    └─ Do you know exact research question with specific methods?
        ├─ YES → Use Narrow query
        │   └─ Trade-off: Fast screening (2-3 hours), may miss relevant papers, 30-100 final
        │
        └─ NO → Use Balanced query ⭐ RECOMMENDED
            └─ Trade-off: 1 day screening, good coverage, 50-150 final papers
```

---

## 🔍 Boolean Operator Guide

### Quick Reference

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| **AND** | Both terms must appear | `chatbot AND learning` | Papers with BOTH words |
| **OR** | Either term can appear | `chatbot OR agent` | Papers with EITHER word |
| **NOT** | Exclude term | `learning NOT animal` | Papers WITHOUT "animal" |
| **( )** | Group terms | `(A OR B) AND C` | A+C or B+C, not just A+B |
| **" "** | Exact phrase | `"language learning"` | Exact phrase only |

### Best Practices

#### ✅ DO: Use Synonyms with OR

```
✅ Good: (chatbot OR conversational agent OR dialogue system)
❌ Bad: chatbot
```
**Why**: Different papers use different terms for the same concept.

#### ✅ DO: Use AND to Narrow Scope

```
✅ Good: chatbot AND "language learning" AND university
❌ Bad: chatbot education
```
**Why**: Ensures all key concepts are present.

#### ✅ DO: Exclude Irrelevant Areas with NOT

```
✅ Good: language learning NOT (animal OR mouse OR rat)
❌ Bad: (forgetting to exclude irrelevant contexts)
```
**Why**: Removes papers from completely different domains.

#### ✅ DO: Test Queries Incrementally

```
Step 1: Start with core concept (e.g., "chatbot")
        → Check: ~50,000 papers (too broad)

Step 2: Add domain (e.g., + "language learning")
        → Check: ~2,000 papers (still broad)

Step 3: Add context (e.g., + "university")
        → Check: ~600 papers (good!)

Step 4: Refine with methods (e.g., + "experimental")
        → Check: ~150 papers (narrow option)
```

---

## 📚 Example: Education Research

### Research Focus
"Effectiveness of AI-powered chatbots in improving speaking proficiency for second language learners in higher education contexts"

### Query Option 1: Broad (~2000 papers)

```
(chatbot OR "conversational agent" OR "dialogue system" OR "virtual agent") AND
(language OR languages OR "second language" OR L2 OR "foreign language")
```

**Pros**: Won't miss any relevant papers
**Cons**: 3-5 days of screening, many irrelevant papers about general chatbots

---

### Query Option 2: Focused ⭐ (~600 papers, RECOMMENDED)

```
(chatbot OR "conversational agent" OR "dialogue system" OR "virtual agent") AND
("language learning" OR "second language acquisition" OR "L2 acquisition" OR "foreign language learning") AND
(university OR college OR "higher education" OR postsecondary OR undergraduate)
```

**Pros**: Balanced relevance (~60%), manageable screening (1 day)
**Cons**: Might miss a few papers that don't mention education level

---

### Query Option 3: Narrow (~150 papers)

```
(chatbot OR "conversational agent" OR "dialogue system") AND
("language learning" OR "second language acquisition") AND
(university OR college OR "higher education") AND
(speaking OR "oral proficiency" OR fluency OR pronunciation) AND
(experimental OR RCT OR "quasi-experimental" OR "controlled trial")
```

**Pros**: High relevance (~80%), fast screening (2-3 hours)
**Cons**: Will miss qualitative studies, surveys, non-experimental designs

---

### Expected Conversation Flow

**Claude**: "I've designed 3 query options for you. The Focused query (Option 2) with ~600 papers is recommended for your dissertation lit review. Would you like to see sample results from this query?"

**You**: "Yes, please show me the top 10 papers from Option 2."

**Claude**: "Here are the top 10 papers:
1. 'Chatbot-assisted language learning for Chinese EFL students...'
2. 'Effectiveness of AI conversational agents in improving speaking skills...'
[...shows 10 titles...]

These look highly relevant! About 70% directly address your research question. Shall we use Option 2?"

**You**: "Perfect! But can you also exclude papers about children (K-12)?"

**Claude**: "Absolutely! I'll add `NOT (children OR K-12 OR elementary OR secondary)`. New estimate: ~520 papers. Still a good range!"

---

## 📚 Example: Medical Research

### Research Focus
"Impact of electronic health record (EHR) alert fatigue on physician clinical decision-making and patient safety outcomes"

### Query Option 1: Broad (~1500 papers)

```
("alert fatigue" OR "alarm fatigue") AND
("electronic health record" OR EHR)
```

**Pros**: Comprehensive coverage
**Cons**: Includes many papers about technical alert systems without clinical outcomes

---

### Query Option 2: Focused ⭐ (~400 papers, RECOMMENDED)

```
("alert fatigue" OR "alarm fatigue" OR "alert override") AND
("electronic health record" OR EHR OR "clinical decision support" OR CDSS) AND
(physician OR clinician OR provider OR doctor)
```

**Pros**: Focused on clinical decision-making context
**Cons**: Might miss some nursing/pharmacist studies

---

### Query Option 3: Narrow (~80 papers)

```
("alert fatigue" OR "alarm fatigue") AND
("electronic health record" OR EHR OR "clinical decision support") AND
(physician OR clinician) AND
(intervention OR trial OR cohort OR prospective) NOT
(editorial OR commentary OR letter)
```

**Pros**: Only high-quality empirical studies
**Cons**: Will miss descriptive studies and qualitative research

---

## 🔄 What Happens Next

### After This Conversation

1. **Queries Saved** ✓
   - `config.yaml` updated with selected query
   - Alternative queries saved as backups
   - Database-specific syntax adaptations saved

2. **You Receive Stage 3 Prompt** ➡️
   - Copy/paste to continue conversation
   - Design PRISMA inclusion/exclusion criteria
   - Expected time: 10-15 minutes

3. **Progress Tracking**
   - Conversation context updated in `.scholarag/context.json`
   - Query preview results saved for reference
   - Can test query anytime with `scholarag test-query`

---

## 🚨 Troubleshooting

### "How do I know if my query is too broad or too narrow?"

Ask Claude: "Can you test this query and show me the top 10 paper titles?" This will give you a sense of relevance rate.

**Signs of too broad**:
- Paper count >2000
- Top 10 titles have <50% relevance to your research question
- Seeing papers from unrelated fields

**Signs of too narrow**:
- Paper count <50
- Missing obvious papers you know should be included
- Query has 5+ AND constraints

---

### "What if I want papers from multiple sub-topics?"

Use OR to combine them:

```
(topic1 OR topic2 OR topic3) AND [rest of your query]
```

Example: Studying chatbots in BOTH language learning AND mathematics?

```
(chatbot OR "conversational agent") AND
("language learning" OR "mathematics education") AND
(university OR college)
```

---

### "Can I search multiple databases with different syntax?"

Yes! Claude will adapt syntax for each database:

**Semantic Scholar / OpenAlex / arXiv**:
```
(chatbot OR agent) AND learning
```

**OpenAlex (supports field-specific search)**:
```
title.search:(chatbot OR "conversational agent") AND
abstract.search:(education OR learning)
```

Ask Claude: "Can you adapt this query for all three databases (Semantic Scholar, OpenAlex, arXiv)?"

---

### "What if the paper count is way off from my target?"

Adjust iteratively:

**Too many papers (>1000)?**
- Add more AND constraints (e.g., + "university")
- Make terms more specific (e.g., "chatbot" → "AI chatbot")
- Add NOT exclusions (e.g., NOT "children")

**Too few papers (<100)?**
- Remove some AND constraints
- Add more OR synonyms (e.g., "chatbot OR agent OR assistant")
- Broaden year range
- Remove method constraints (e.g., remove "experimental")

---

### "I'm not comfortable with boolean operators"

No problem! Choose this option in your prompt:
- [ ] Just give me the final query (I don't need to understand the syntax)

Claude will design optimized queries for you without explaining every detail. You can always ask "What does this query mean in plain English?" if you're curious.

---

## 🎯 Stage 2 Success Criteria

You're ready to move to Stage 3 when:

✅ Query includes **all core concepts** (not just 1-2 keywords)
✅ Synonyms are properly grouped with **OR**
✅ Boolean syntax is **correct** (parentheses balanced)
✅ Estimated paper count is **realistic** (20-5000, ideally 100-800)
✅ You've **previewed results** and they look relevant
✅ Query is **saved to config.yaml**

---

## 📍 Your Progress

```
[●●○○○○○] Stage 2/7: Query Strategy Design
```

**Next**: Stage 3 - PRISMA Configuration (10-15 min)
**After That**: Stage 4 - RAG Design (20-30 min)

**Progress So Far**: ~35-50 minutes
**Remaining Time**: ~3-7 hours across stages 3-7

---

**Ready to continue?** Copy the prompt template above, fill in your research focus and preferences, and paste it to Claude Code!
