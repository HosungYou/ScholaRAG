<!-- METADATA
stage: 6
stage_name: "Research Conversation"
stage_goal: "Use RAG system to conduct literature analysis and extract insights"
expected_duration: "Ongoing (hours to weeks)"
conversation_mode: "research_analysis"
prerequisites:
  - stage: 5
    requirement: "Vector database built and validated"
outputs:
  - research_insights: "Answers to research questions with citations"
  - literature_patterns: "Themes, gaps, methodological trends"
  - conversation_logs: "Saved to conversations/*.md for reference"
validation_rules:
  rag_interface_used:
    required: true
    validation: "Must use RAG interface, not general Claude knowledge"
  citations_present:
    required: true
    validation: "All answers must include paper citations"
cli_commands:
  - command: "python scripts/06_query_rag.py --query 'your research question'"
    when: "User wants to query RAG system"
    auto_execute: false
  - command: "researcherrag stage6-examples"
    when: "User wants to see available prompt scenarios"
    auto_execute: false
  - command: "researcherrag stage6-prompt <scenario>"
    when: "User wants to copy a specific scenario prompt"
    auto_execute: false
scripts_triggered:
  - scripts/06_query_rag.py (interactive mode)
next_stage:
  stage: 7
  condition: "User has gathered sufficient insights and is ready to write"
  prompt_file: "07_documentation_writing.md"
divergence_handling:
  common_divergences:
    - pattern: "User asks question without using RAG interface"
      response: "IMPORTANT: I'm answering from general knowledge, NOT your database. Please use the RAG interface: python scripts/06_query_rag.py"
    - pattern: "User unsure how to formulate research questions"
      response: "Effective RAG queries: Start broad ('What methodologies are used?'), then narrow ('Which RCT studies show positive outcomes?'). Use iterative refinement."
conversation_flow:
  expected_turns: "Unlimited (ongoing research)"
  typical_pattern:
    - turn: 1
      user_action: "Starts RAG interface, asks broad question"
      claude_action: "Retrieve relevant papers, synthesize with citations"
    - turn: "2-N"
      user_action: "Asks follow-up questions, explores themes"
      claude_action: "Continue retrieving and synthesizing"
    - turn: "final"
      user_action: "Satisfied with insights, ready to write"
      claude_action: "Save conversation log, show Stage 7 prompt"
validation_checklist:
  - "Using RAG interface (not general Claude knowledge)"
  - "Answers include paper citations"
  - "Conversation logs saved for reference"
  - "Sufficient insights gathered for writing"
-->

# Stage 6: Research Conversation

**🎯 Your Current Stage**: Stage 6 of 7
**⏱️ Expected Time**: Ongoing (hours to weeks)
**💬 Format**: Research analysis with RAG interface
**📋 Prerequisites**: Stage 5 completed (vector database ready)

---

## ⚠️ CRITICAL: Use RAG Interface

**DON'T**: Ask questions directly in Claude Code (gives general knowledge, NOT your database)

**DO**: Use the RAG interface script

```bash
python scripts/06_query_rag.py
```

---

## 🚀 Start Research Conversations

Now that RAG is built from your **PRISMA-selected papers**, query your curated literature:

**What you're querying**: Only the ~50-150 papers that **passed PRISMA screening** (not the original 500+).
This ensures high-quality, relevant answers backed by rigorous paper selection.

### Starting the RAG Interface

```bash
python scripts/06_query_rag.py --project /path/to/project

╔═══════════════════════════════════════════════════════════╗
║           ResearcherRAG - Research Conversation            ║
║                                                           ║
║  📚 Database: 45 PRISMA-selected papers                   ║
║  🔢 Chunks: 2,250 semantic units                          ║
║  🤖 Model: Claude 3.5 Sonnet + text-embedding-3-small    ║
╚═══════════════════════════════════════════════════════════╝

Type your research question (or 'quit' to exit):
>
```

---

## 📚 7 Research Conversation Scenarios

This directory contains **specialized prompt templates** for different research goals. Each scenario includes:
- Optimal prompt structure
- Expected AI response format
- Best practices and tips

### Quick Access (CLI)

```bash
# List all available scenarios
researcherrag stage6-examples

# Copy a specific scenario prompt
researcherrag stage6-prompt overview
researcherrag stage6-prompt hypothesis
researcherrag stage6-prompt statistics
```

### Scenario Files

| # | Scenario | File | Use Case |
|---|----------|------|----------|
| 1 | **Context Scanning** | [01_overview.md](01_overview.md) | Get high-level overview of literature themes, methods, findings |
| 2 | **Hypothesis Validation** | [02_hypothesis.md](02_hypothesis.md) | Test hypothesis with supporting/refuting evidence + effect sizes |
| 3 | **Statistical Extraction** | [03_statistics.md](03_statistics.md) | Extract quantitative data (effect sizes, sample sizes, measurement tools) |
| 4 | **Methodology Comparison** | [04_methods.md](04_methods.md) | Compare RCT vs quasi-experimental vs mixed methods approaches |
| 5 | **Contradiction Detection** | [05_contradictions.md](05_contradictions.md) | Identify conflicting results and analyze potential reasons |
| 6 | **Policy Translation** | [06_policy.md](06_policy.md) | Convert research findings into actionable policy recommendations |
| 7 | **Future Research Design** | [07_grant.md](07_grant.md) | Design follow-up studies based on identified research gaps |

### Web Access

Browse scenarios with examples and customization options:
**[Prompt Library](https://researcher-rag-helper.vercel.app/guide/prompt-library)**

---

## 💡 Usage Workflow

### 1. Choose Your Scenario

Start with **Context Scanning** (Scenario 1) to understand your corpus, then move to specific scenarios based on your research needs.

### 2. Copy the Prompt

**Option A: Via CLI**
```bash
researcherrag stage6-prompt overview
# Copies prompt to terminal, you paste into RAG interface
```

**Option B: Via File**
```bash
cat prompts/06_research_conversation/01_overview.md
# Read the prompt, copy the template
```

**Option C: Via Web**
Visit [Prompt Library](https://researcher-rag-helper.vercel.app/guide/prompt-library) and click the scenario

### 3. Customize (Optional)

Modify placeholders in the prompt:
- Replace `[your hypothesis]` with your actual hypothesis
- Adjust focus areas (e.g., "Focus on studies from 2020-2024")
- Add constraints (e.g., "Only include RCT studies")

### 4. Run in RAG Interface

```bash
python scripts/06_query_rag.py
> [paste your customized prompt]
```

### 5. Iterate

Ask follow-up questions based on the response. Most research sessions involve 5-20 queries.

---

## 📖 Example Research Session

**Query 1: Exploratory Overview** (Scenario 1)
```
> Analyze the papers in my database and provide a structured overview of:
  1. Core themes and topics
  2. Methodological approaches
  3. Key findings and outcomes
```

**Response**: Overview with 3-5 themes, method distribution table, key findings synthesis (with citations)

**Query 2: Deep Dive** (Follow-up)
```
> For Theme 1 (Speaking Proficiency), which studies show the strongest evidence?
```

**Response**: 5-8 papers with effect sizes, sorted by evidence strength

**Query 3: Contradiction Analysis** (Scenario 5)
```
> Identify cases where studies report conflicting results on speaking outcomes
```

**Response**: 2-4 contradictions with analysis of methodological differences

**Query 4: Research Gap** (Leading to Scenario 7)
```
> Based on these contradictions, what follow-up study would you recommend?
```

**Response**: Study design proposal (can refine with Scenario 7 prompt)

---

## ✅ Best Practices

### Do This:
- ✓ Start broad (Scenario 1), then narrow down
- ✓ Always use RAG interface, not direct Claude chat
- ✓ Verify citations by spot-checking source papers
- ✓ Save conversation logs for reference
- ✓ Use multiple scenarios in sequence
- ✓ Ask follow-up questions to dig deeper

### Avoid This:
- ✗ Asking questions without RAG interface (gets general knowledge)
- ✗ Accepting answers without verifying citations
- ✗ Stopping at first answer (iterate!)
- ✗ Forgetting to document your findings
- ✗ Skipping Context Scanning (Scenario 1)

---

## 🔗 Navigation

- **Previous Stage**: [Stage 5: RAG Building](../05_rag_building.md)
- **Next Stage**: [Stage 7: Documentation Writing](../07_documentation_writing.md)
- **Main Documentation**: [README.md](../../README.md)

---

## 📝 Version History

- **v1.0.10** (2025-01-15): Split scenarios into individual files for better navigation
- **v1.0.8** (2025-01-13): Added 7 specialized scenarios with optimal response structures
- **v1.0.6** (2025-01-10): Initial Stage 6 prompt

---

## 🆘 Troubleshooting

**Problem**: "How do I know if I'm using RAG vs general knowledge?"

**Solution**: RAG interface shows:
```
🔍 Retrieving relevant chunks... (X chunks found)
📖 Citations: [Author, Year]
```

If you don't see these indicators, you're NOT using RAG.

**Problem**: "My queries return 'No relevant documents found'"

**Solution**:
1. Check your vector DB was built: `ls chroma_db/`
2. Broaden your query (less specific terms)
3. Verify papers were successfully embedded in Stage 5

**Problem**: "Which scenario should I use?"

**Solution**:
1. Start with Scenario 1 (Context Scanning) - always
2. For specific research questions → Scenario 2 or 3
3. For writing papers → Scenario 4, 5, or 6
4. For grant proposals → Scenario 7

---

## 📚 Additional Resources

- [ResearcherRAG Documentation](https://researcher-rag-helper.vercel.app)
- [Prompt Library (Web)](https://researcher-rag-helper.vercel.app/guide/prompt-library)
- [GitHub Issues](https://github.com/HosungYou/researcherRAG/issues)
