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

### Example Research Session

**Query 1: Exploratory Overview**
```
> What methodologies are most commonly used in my papers?

🔍 Retrieving relevant chunks... (5 chunks found)
📝 Generating answer...

Based on the 45 PRISMA-selected papers, three main methodologies emerge:

1. **Randomized Controlled Trials (RCTs)** - 60%
   Most studies employ experimental designs with control groups:
   - Smith et al. (2023): 120 participants, pre-post design
   - Chen et al. (2023): 85 students, treatment vs. control
   - Lee et al. (2024): 200 learners, 3-arm RCT

2. **Qualitative Studies** - 25%
   Interview and observation-based approaches:
   - Jones et al. (2022): Semi-structured interviews (n=30)
   - Kim et al. (2023): Ethnographic study in classrooms

3. **Mixed Methods** - 15%
   Combining quantitative and qualitative data:
   - Wang et al. (2024): RCT + follow-up interviews

📖 Citations:
[1] Smith, J. et al. (2023). AI Chatbots in Language Learning. p.3-5
[2] Chen, L. et al. (2023). Experimental Study of... p.8
[3] Lee, M. et al. (2024). Three-arm RCT... p.2-4
[4] Jones, A. et al. (2022). Qualitative Analysis... p.5-7
[5] Kim, S. et al. (2023). Ethnographic Exploration... p.3

⏱️  Response time: 4.2 seconds
```

**Query 2: Specific Outcomes**
```
> Which studies show positive learning outcomes?

🔍 Retrieving relevant chunks... (8 chunks found)
📝 Generating answer...

Of the 45 papers, 31 studies (69%) reported positive learning outcomes
for chatbot interventions:

**Strong Evidence (Effect Size > 0.5)**:
1. Smith et al. (2023): d=0.72
   - Vocabulary acquisition improved by 18%
   - Speaking fluency gains: +2.1 on IELTS scale

2. Martinez et al. (2023): d=0.68
   - Grammar test scores: +15% vs. control
   - Retention after 3 months: 85%

**Moderate Evidence (Effect Size 0.3-0.5)**:
3. Lee et al. (2024): d=0.42
   - Writing scores improved (+12%)
   - Student engagement: +25%

**Mixed or No Effect**:
- 8 studies (18%) showed no significant difference
- 6 studies (13%) had methodological limitations

**Key Success Factors** identified across positive studies:
✓ Personalized feedback mechanisms
✓ Integration with curriculum (not standalone)
✓ Teacher guidance + chatbot support
✓ Duration: minimum 8 weeks for measurable effects

📖 Citations: [Full list of 31 studies with page numbers]

💡 Research Gap: No long-term studies (>6 months) found.

⏱️  Response time: 5.8 seconds
```

**Query 3: Research Gaps**
```
> What are the research gaps in this PRISMA-vetted literature?

🔍 Retrieving relevant chunks... (12 chunks found)
📝 Generating answer...

Analysis of the 45 PRISMA-selected papers reveals 7 major research gaps:

1. **Lack of Long-term Studies** (CRITICAL GAP)
   - Longest study duration: 16 weeks (Wang 2024)
   - No studies examining effects beyond 6 months
   - Retention and sustained benefits unknown

2. **Limited Diversity in Contexts** (HIGH PRIORITY)
   - 82% focus on higher education
   - Only 3 studies (7%) examine K-12 settings
   - Corporate training: 2 studies (4%)

3. **Methodological Weaknesses** (MEDIUM PRIORITY)
   - Small sample sizes: avg n=78 (range 20-200)
   - 67% lack statistical power analysis
   - Control for teacher effects: only 5 studies (11%)

4. **Technology-Specific Gaps**
   - Most use rule-based chatbots (60%)
   - LLM-based chatbots: only 8 studies (18%)
   - Multimodal chatbots (voice+text): 2 studies (4%)

5. **Outcome Measurement Issues**
   - Standardized tests: 31 studies (69%)
   - Authentic communication tasks: only 9 studies (20%)
   - Affective outcomes underexplored

6. **Theoretical Frameworks**
   - 58% atheoretical (no explicit theory)
   - SLA theories: 12 studies (27%)
   - Learning sciences frameworks: 7 studies (16%)

7. **Equity and Access**
   - Socioeconomic diversity: rarely reported
   - Special education needs: 0 studies
   - Non-English languages: 6 studies (13%)

**Recommended Future Research Directions**:
→ Longitudinal RCTs (12+ months)
→ K-12 and workplace contexts
→ LLM-based chatbot interventions
→ Authentic assessment measures
→ Theory-driven designs

📖 Based on comprehensive analysis of all 45 papers

⏱️  Response time: 7.3 seconds
```

### Example Workflow

**Your Pipeline Journey**:
```
PRISMA identified:    403 papers
↓ Screening
PRISMA selected:      79 papers (20%)
↓ PDF Download
Successfully downloaded: 45 PDFs (57%)
↓ RAG Building
Vector database:      2,250 chunks

✅ NOW QUERYING: Those 45 PRISMA-vetted papers only
```

**Result**: Every answer comes from high-quality, domain-relevant, systematically-selected literature.

### Advanced Query Techniques

**1. Comparative Queries**
```
> Compare chatbot effectiveness in K-12 vs. higher education
> How do rule-based chatbots differ from LLM-based ones?
```

**2. Methodological Queries**
```
> What sample sizes are typical in RCT studies?
> Which assessment tools are most commonly used?
```

**3. Temporal Queries**
```
> How have chatbot designs evolved from 2018 to 2024?
> What are the emerging trends in recent papers (2023-2024)?
```

**4. Gap Identification**
```
> What contexts are underrepresented in this literature?
> Which theoretical frameworks are rarely used?
```

**5. Citation Extraction**
```
> List all studies that use vocabulary acquisition as primary outcome
> Which papers cite Krashen's Input Hypothesis?
```

---

## 📍 Your Progress

```
[●●●●●●○] Stage 6/7: Research Conversation
```

**Next**: Stage 7 - Documentation & Writing
**Current**: Ongoing research analysis

---

**Ready to start?** Run the RAG interface and begin exploring your literature!
