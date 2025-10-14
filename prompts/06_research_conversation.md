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

Now that RAG is built, query your literature:

```bash
python scripts/06_query_rag.py

# Interactive mode starts
> What methodologies are most commonly used in my papers?
> Which studies show positive outcomes for chatbot interventions?
> What are the research gaps?
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
