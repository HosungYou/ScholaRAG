<!-- METADATA
stage: 4
stage_name: "RAG Design"
stage_goal: "Configure RAG system architecture (chunking, embeddings, retrieval)"
expected_duration: "20-30 minutes"
conversation_mode: "interactive"
prerequisites:
  - stage: 3
    requirement: "PRISMA profile saved, ready to process papers"
outputs:
  - pdf_strategy: "Download plan with fallback options"
  - chunking_config: "Chunk size, overlap, metadata preservation"
  - embedding_model: "Selected model (OpenAI, sentence-transformers, etc.)"
  - vector_db_config: "ChromaDB collection settings"
  - rag_prompts: "System prompt and citation format"
  - retrieval_params: "Top-k, similarity threshold, reranking"
validation_rules:
  chunk_size:
    required: true
    range: [500, 2000]
    default: 1000
    validation: "Should balance context preservation with retrieval precision"
  chunk_overlap:
    required: true
    range: [50, 500]
    default: 200
    validation: "Typically 10-20% of chunk size"
  top_k:
    required: true
    range: [3, 20]
    default: 5
    validation: "Number of chunks to retrieve per query"
cli_commands:
  - command: "researcherrag test-rag --query 'sample question'"
    when: "User wants to preview RAG retrieval before full execution"
    auto_execute: false
scripts_triggered:
  - none (configuration only, RAG builds in Stage 5)
next_stage:
  stage: 5
  condition: "User confirms RAG configuration and is ready to execute"
  prompt_file: "05_execution_plan.md"
divergence_handling:
  common_divergences:
    - pattern: "User wants to start downloading PDFs immediately"
      response: "PDF downloading is part of Stage 5 execution. Right now in Stage 4, let's finalize RAG design configuration. We'll run everything in Stage 5."
    - pattern: "User asks about querying the RAG system"
      response: "Querying happens in Stage 6. Stage 4 is about designing the RAG architecture. Stage 5 builds it, Stage 6 uses it."
    - pattern: "User confused about chunking strategy"
      response: "Chunking splits documents into smaller pieces. Larger chunks (1500-2000) preserve context but may reduce precision. Smaller chunks (500-800) increase precision but may lose context. Default 1000 with 200 overlap is recommended."
conversation_flow:
  expected_turns: 5-10
  typical_pattern:
    - turn: 1
      user_action: "Provides paper count and research questions"
      claude_action: "Explain PDF acquisition strategy, estimate success rate"
    - turn: 2-3
      user_action: "Confirms PDF strategy preferences"
      claude_action: "Design chunking strategy based on research questions"
    - turn: 4-6
      user_action: "Reviews chunking, asks about embeddings"
      claude_action: "Recommend embedding model, explain trade-offs"
    - turn: 7-8
      user_action: "Confirms embedding choice"
      claude_action: "Set retrieval parameters, design system prompts"
    - turn: "final"
      user_action: "Ready to execute"
      claude_action: "Save RAG config to config.yaml, show Stage 5 prompt"
validation_checklist:
  - "PDF download strategy configured (Open Access / Institutional / Both)"
  - "Chunking strategy set (size 500-2000, overlap 10-20%)"
  - "Embedding model selected (OpenAI / sentence-transformers / other)"
  - "Retrieval parameters configured (top-k 3-20, threshold 0.5-0.8)"
  - "System prompt designed for academic rigor and citation"
  - "RAG configuration saved to config.yaml"
-->

# Stage 4: RAG Design

**🎯 Your Current Stage**: Stage 4 of 7
**⏱️ Expected Time**: 20-30 minutes
**💬 Format**: Interactive conversation with Claude Code
**📋 Prerequisites**: Stages 1-3 completed (PRISMA profile ready)

---

## 🚀 Quick Start

After completing Stage 3 (PRISMA Configuration), copy this prompt to Claude Code:

---

Now that we have our PRISMA criteria, I need help designing a RAG system to query the final papers effectively.

**Expected Papers**: [Estimated from Stage 3]

**Research Questions**:
1. [Your primary research question]
2. [Secondary questions, if any]

**Goals for RAG System**:
- [e.g., "Generate evidence-based answers with citations"]
- [e.g., "Compare findings across studies"]
- [e.g., "Identify research gaps"]

Please help me configure:
1. **PDF download strategy** (Open Access, institutional access, fallbacks)
2. **Text extraction** (PyMuPDF, OCR for scanned papers)
3. **Chunking strategy** (chunk size, overlap, metadata)
4. **Embedding model** (OpenAI, sentence-transformers, trade-offs)
5. **Vector database** (ChromaDB configuration)
6. **RAG prompts** (system prompt, citation format)
7. **Retrieval parameters** (top-k, similarity threshold)

**My Constraints** (if any):
- Budget: [e.g., "Free only", "Can pay for OpenAI embeddings"]
- Speed: [e.g., "Fast retrieval important", "Quality over speed"]
- Infrastructure: [e.g., "Local only", "Cloud OK"]

---

## 📋 What Happens in This Stage

### Claude Code Will:

1. **Design PDF Acquisition Plan** (Turn 1-2)
   - Estimate success rate (target: 50-60%)
   - Configure Open Access sources
   - Set up institutional access (if available)
   - Plan fallback strategies

2. **Configure Chunking Strategy** (Turn 3-4)
   - Choose chunk size based on research questions
   - Set overlap to preserve context
   - Decide metadata to preserve (citations, page numbers)

3. **Select Embedding Model** (Turn 5-6)
   - Recommend model based on budget/speed/quality trade-offs
   - Options: OpenAI, sentence-transformers, local models
   - Explain embedding dimension implications

4. **Set Retrieval Parameters** (Turn 7-8)
   - Configure top-k (how many chunks per query)
   - Set similarity threshold
   - Design reranking strategy (if needed)

5. **Design System Prompts** (Turn 9)
   - Create academic-rigorous system prompt
   - Define citation format
   - Set response structure

6. **Save Configuration** (automatic)
   - Update `config.yaml` with RAG settings
   - Ready for Stage 5 execution

### ✅ Stage Completion Checklist

Before moving to Stage 5, ensure:

- [ ] **PDF strategy** configured (Open Access / Institutional / Both)
- [ ] **Chunking** set (size 500-2000, overlap 10-20%)
- [ ] **Embedding model** selected with rationale
- [ ] **Retrieval params** configured (top-k 3-20, threshold 0.5-0.8)
- [ ] **System prompt** designed for citations and academic rigor
- [ ] **RAG config saved** to `config.yaml`

---

## 🎯 Stage 4 Success Criteria

You're ready to move to Stage 5 when:

✅ PDF download strategy configured
✅ Chunking strategy balances context vs precision
✅ Embedding model chosen based on needs
✅ Retrieval parameters set appropriately
✅ System prompt ensures academic rigor
✅ RAG configuration saved to config.yaml

---

## 📍 Your Progress

```
[●●●●○○○] Stage 4/7: RAG Design
```

**Next**: Stage 5 - Execution & Build (2-4 hours)
**After That**: Stage 6 - Research Conversation (ongoing)

**Progress So Far**: ~75-110 minutes
**Remaining Time**: ~2-6 hours across stages 5-7

---

**Ready to continue?** Copy the prompt template above, fill in your details, and paste it to Claude Code!
