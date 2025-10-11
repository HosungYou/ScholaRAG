# Stage 2: Query Strategy Design Prompt

After completing Stage 1 (Research Domain Setup), use this prompt to design your search queries:

---

Now that we've defined my research scope, please help me design effective search queries for academic databases.

**Confirmed Research Focus**:
[Summarize what you agreed on with Claude in Stage 1]

**My Preferences**:

1. **Query Breadth**:
   - [ ] Broad (high recall, more screening work) - I want comprehensive coverage
   - [ ] Balanced (recommended) - I want quality papers without too much noise
   - [ ] Narrow (high precision) - I want only the most relevant papers

2. **Data Sources**:
   - [ ] Semantic Scholar (good for CS, Engineering, General)
   - [ ] OpenAlex (comprehensive metadata, all fields)
   - [ ] arXiv (preprints in STEM)
   - [ ] PubMed (Medicine, Life Sciences)
   - [ ] ERIC (Education)
   - [ ] Let Claude recommend based on my field

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

## What Claude Code Will Do

Claude will:

1. Analyze your research domain and suggest relevant databases
2. Design 2-3 query strategies with different precision/recall trade-offs
3. Explain boolean operators and search syntax
4. Estimate paper counts for each query (using API preview if possible)
5. Recommend a starting point based on your goals
6. Offer to test queries before committing

## Understanding Query Trade-offs

| Query Type | Papers Found | Relevance Rate | Screening Time | Risk |
|------------|--------------|----------------|----------------|------|
| **Broad** | 2000+ | 20-30% relevant | High (days) | Miss nothing |
| **Focused** | 500-800 | 50-70% relevant | Medium (hours) | Balanced |
| **Narrow** | 100-200 | 80-90% relevant | Low (minutes) | May miss papers |

**Recommendation**: Start with **Focused**, then broaden if needed.

## Example Queries

### Education Research (AI Chatbots in Language Learning)

**Broad Query (~2000 papers)**:
```
AI chatbot language learning
```

**Focused Query (~600 papers, RECOMMENDED)**:
```
(conversational agent OR chatbot OR dialogue system) AND
(language learning OR second language acquisition OR L2 OR foreign language) AND
(university OR college OR higher education OR postsecondary)
```

**Narrow Query (~150 papers)**:
```
[Focused Query] AND
(experimental OR RCT OR randomized OR quasi-experimental OR controlled trial)
```

### Medical Research (EHR Alert Fatigue)

**Broad Query (~1500 papers)**:
```
alert fatigue electronic health record
```

**Focused Query (~400 papers, RECOMMENDED)**:
```
(alert fatigue OR alarm fatigue OR alert override) AND
(electronic health record OR EHR OR clinical decision support OR CDSS) AND
(physician OR clinician OR provider)
```

**Narrow Query (~80 papers)**:
```
[Focused Query] AND
(intervention OR trial OR cohort OR prospective) NOT
(editorial OR commentary OR letter)
```

## Boolean Operator Cheat Sheet

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| **AND** | Both terms must appear | chatbot AND learning | Papers with BOTH words |
| **OR** | Either term can appear | chatbot OR agent | Papers with EITHER word |
| **NOT** | Exclude term | learning NOT animal | Papers WITHOUT "animal" |
| **( )** | Group terms | (A OR B) AND C | A+C or B+C, not just A+B |
| **" "** | Exact phrase | "language learning" | Exact phrase only |

## Tips

### 1. Use Synonyms with OR
```
✅ Good: (chatbot OR conversational agent OR dialogue system)
❌ Bad: chatbot
```
Why: Different papers use different terms for the same concept.

### 2. Use AND to Narrow Scope
```
✅ Good: chatbot AND "language learning" AND university
❌ Bad: chatbot education
```
Why: Ensures all key concepts are present.

### 3. Exclude Irrelevant Areas with NOT
```
✅ Good: language learning NOT (animal OR mouse OR rat)
❌ Bad: (forgetting to exclude irrelevant contexts)
```
Why: Removes papers from completely different domains.

### 4. Test Queries Incrementally
```
Step 1: Start with core concept (e.g., "chatbot")
Step 2: Add domain (e.g., + "language learning")
Step 3: Add context (e.g., + "university")
Step 4: Refine with methods (e.g., + "experimental")
```

## Decision Tree

```
Do you want comprehensive coverage of the literature?
├─ YES → Use Broad query
│   └─ Expected: 1500+ papers, 3-5 days of screening
│
└─ NO → Do you know your research question precisely?
    ├─ YES → Use Narrow query
    │   └─ Expected: 100-200 papers, 2-3 hours of screening
    │
    └─ NO → Use Focused query (RECOMMENDED)
        └─ Expected: 500-800 papers, 1 day of screening
```

## After Claude Responds

Claude will provide you with:
- 2-3 query options
- Estimated paper counts
- Recommended starting point
- Explanation of each query component

**Your next actions**:
1. Review the queries - do they capture your research focus?
2. Ask Claude to adjust if needed:
   - "Can you add [keyword]?"
   - "This seems too broad, can you narrow it?"
   - "I'm worried about missing papers on [topic]"
3. Once satisfied, confirm: "Let's use Query 2"
4. Move to Stage 3: PRISMA Configuration

## Common Questions

### Q: How do I know if my query is too broad or too narrow?
A: Ask Claude: "Can you test this query and show me the top 10 paper titles?" This will give you a sense of relevance.

### Q: What if I want papers from multiple sub-topics?
A: Use OR to combine them:
```
(topic1 OR topic2 OR topic3) AND [rest of your query]
```

### Q: Can I search multiple databases?
A: Yes! Ask Claude: "Can you design queries for both Semantic Scholar and PubMed?" Claude will adapt syntax for each database.

### Q: What if the paper count is way off from my target?
A: Adjust iteratively:
- Too many papers (>1000)? Add more AND constraints
- Too few papers (<100)? Remove some constraints or add OR synonyms

---

## Next Steps

Once your query is finalized:
→ Proceed to [Stage 3: PRISMA Configuration](./03_prisma_configuration.md)
