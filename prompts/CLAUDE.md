# Prompts Folder - Claude Code Instructions

**Context**: You are in the prompts folder of ScholaRAG, which contains 7 stage-specific conversation prompts for guiding researchers through PRISMA 2020 + RAG systematic literature reviews.

---

## 🎯 What This Folder Contains

### 7-Stage Prompt System

Each `.md` file represents one conversational stage in the ScholaRAG workflow:

1. **01_research_domain_setup.md** - Define research question and scope (15-20 min)
2. **02_query_strategy.md** - Design database search queries (20-30 min)
3. **03_prisma_configuration.md** - Configure PRISMA screening criteria (25-35 min)
4. **04_rag_design.md** - Design RAG system architecture (20-30 min)
5. **05_execution_plan.md** - Execute full pipeline (2-4 hours, automated)
6. **06_research_conversation.md** - Query RAG for insights (ongoing)
7. **07_documentation_writing.md** - Generate PRISMA flowchart and reports (30-60 min)

**Total Time**: ~3-4 hours of active work, 2-4 hours automated execution

---

## 🧠 How These Prompts Work

### For Researchers (Users)

**How to use these prompts**:

1. **Copy the prompt template** from the relevant stage file
2. **Fill in your research details** (topic, questions, constraints)
3. **Paste to Claude Code** in VS Code
4. **Have a conversation** following the stage's expected flow
5. **Complete the stage** when validation checklist is satisfied
6. **Move to next stage** automatically

**Example workflow**:
```bash
# Stage 1: Start your research project
cat prompts/01_research_domain_setup.md
# Copy template, fill in your topic, paste to Claude Code

# After Stage 1 conversation completes:
# → Claude Code shows Stage 2 prompt automatically
```

---

### For Claude Code (AI Assistant)

**IMPORTANT: Read the HTML metadata at the top of each prompt file**

Every prompt file starts with a hidden `<!-- METADATA -->` block that YOU must read:

```html
<!-- METADATA
stage: 1
stage_name: "Research Domain Setup"
expected_duration: "15-20 minutes"
conversation_flow:
  expected_turns: 4-8
validation_checklist:
  - "Research question is specific and answerable"
  - "Scope constraints are realistic"
-->
```

**Your responsibilities when user pastes a prompt**:

1. ✅ **Read metadata block** - Understand stage number, goals, validation rules
2. ✅ **Follow conversation flow** - Typically 4-10 turns per stage
3. ✅ **Detect divergence** - Redirect if user asks about future stages
4. ✅ **Validate completion** - Check ALL items in validation_checklist
5. ✅ **Auto-execute scripts** - Run appropriate scripts when stage completes
6. ✅ **Update context** - Save progress to `.scholarag/context.json`
7. ✅ **Show next prompt** - Display next stage's prompt template

---

## 📋 Stage-by-Stage Guidance for Claude Code

### Stage 1: Research Domain Setup

**Goal**: Define research scope and validate feasibility

**Expected conversation pattern**:
- User provides broad topic → You ask clarifying questions
- User refines scope → You suggest keywords, estimate paper counts
- User confirms → You initialize project structure

**Auto-execution**:
```python
# Create project folders
os.makedirs('data/01_identification', exist_ok=True)
os.makedirs('.scholarag', exist_ok=True)

# Create config.yaml with research question, databases, year range
# Create context.json with current_stage: 1, completed_stages: []
```

**Validation checklist** (ALL must be ✅):
- [ ] Research question is specific and answerable
- [ ] Scope constraints are realistic (year range, languages, study types)
- [ ] Expected paper count is 20-500
- [ ] User understands systematic review process

**Common divergences to handle**:
- User asks about PDFs → Explain PDFs come in Stage 4
- User wants to skip to RAG → Explain systematic approach is essential
- User unsure about scope → Provide domain-specific guidance

---

### Stage 2: Query Strategy

**Goal**: Design Boolean search queries for academic databases

**Expected conversation pattern**:
- User provides confirmed scope → You ask about must-include/exclude keywords
- User specifies constraints → You design 2-3 query options (broad/focused/narrow)
- User reviews queries → You refine based on feedback
- User tests preview → You show top 10 papers, adjust if needed

**Auto-execution**:
```python
# Update config.yaml with query
config['query'] = "(chatbot OR agent) AND language learning"
config['databases'] = ['semantic_scholar', 'openalex', 'arxiv']
```

**Validation checklist**:
- [ ] Query includes all core concepts (not just one keyword)
- [ ] Synonyms grouped with OR
- [ ] Boolean syntax is correct
- [ ] Estimated paper count is 20-5000
- [ ] Query tested or previewed

---

### Stage 3: PRISMA Configuration

**Goal**: Configure 6-dimension PRISMA screening criteria

**Expected conversation pattern**:
- User confirms query → You explain PRISMA screening dimensions
- User specifies inclusion criteria → You design threshold scoring system
- User reviews examples → You refine criteria
- User confirms → You save PRISMA profile

**6 Dimensions explained**:
1. **Domain**: Is this in your research field? (Education, Medicine, etc.)
2. **Method**: Does it use your required methodology? (RCT, qualitative, etc.)
3. **Topic**: Does it address your specific topic? (AI chatbots, not general EdTech)
4. **Context**: Is the setting appropriate? (University, K-12, workplace)
5. **Exclusion**: Does it meet quality standards? (peer-reviewed, not blog post)
6. **Title**: Does title suggest relevance? (Quick filter)

**Auto-execution**:
```python
# Save PRISMA criteria to config.yaml
config['prisma_criteria'] = {
    'domain_keywords': ['education', 'learning'],
    'method_requirements': ['experimental', 'quasi-experimental'],
    'min_score': 4,  # out of 6 dimensions
}
```

**Validation checklist**:
- [ ] All 6 dimensions configured
- [ ] Scoring threshold set (typically 4/6)
- [ ] Example papers tested (should pass/fail correctly)
- [ ] PRISMA profile saved to config.yaml

---

### Stage 4: RAG Design

**Goal**: Configure RAG system architecture (chunking, embeddings, retrieval)

**IMPORTANT**: Explain connection to PRISMA:
> "RAG will analyze papers that PASS PRISMA screening (Stage 3). This ensures RAG searches only high-quality, relevant papers."

**Expected conversation pattern**:
- User provides paper count estimate → You explain PDF acquisition strategy
- User confirms PDF preferences → You design chunking strategy
- User reviews chunking → You recommend embedding model
- User confirms embedding → You set retrieval parameters

**Key decisions**:
1. **PDF Download**: Open Access, institutional access, or both?
2. **Chunking**: Size (500-2000 tokens), overlap (10-20%)
3. **Embeddings**: OpenAI (paid, high quality) vs sentence-transformers (free)
4. **Retrieval**: top-k (3-20 chunks), similarity threshold (0.5-0.8)

**Auto-execution**:
```python
# Save RAG config to config.yaml
config['rag_config'] = {
    'chunk_size': 1000,
    'chunk_overlap': 200,
    'embedding_model': 'sentence-transformers/all-MiniLM-L6-v2',
    'top_k': 5,
}
```

**Validation checklist**:
- [ ] PDF download strategy configured
- [ ] Chunking strategy balances context vs precision
- [ ] Embedding model chosen with rationale
- [ ] Retrieval parameters appropriate for research questions
- [ ] RAG configuration saved

---

### Stage 5: Execution & Build

**Goal**: Execute full pipeline (fetch → deduplicate → screen → PDFs → RAG)

**Expected conversation pattern**:
- User confirms ready → You verify API keys
- You run scripts sequentially → Report progress after each
- Scripts complete → You validate results
- You test RAG → User reviews sample query

**Auto-execution** (5 scripts in sequence):
```bash
python scripts/01_fetch_papers.py      # 10-30 min
python scripts/02_deduplicate.py       # 1-5 min
python scripts/03_screen_papers.py     # 5-20 min
python scripts/04_download_pdfs.py     # 1-3 hours
python scripts/05_build_rag.py         # 10-30 min
```

**Progress reporting** (show after each script):
```
✅ Stage 1 (Fetch): 403 papers identified
✅ Stage 2 (Dedup): 324 unique papers (79 duplicates removed)
✅ Stage 3 (Screen): 79 relevant papers (26% pass rate)
✅ Stage 4 (PDFs): 45 PDFs downloaded (57% success rate)
✅ Stage 5 (RAG): Vector DB built with 1,234 chunks
```

**Validation checklist**:
- [ ] All 5 scripts executed successfully
- [ ] PRISMA pass rates realistic (not 0% or 100%)
- [ ] PDF success rate 30-80% (paywalls are normal)
- [ ] Vector database returns relevant results
- [ ] Sample query works with citations

**Common issues**:
- Low relevance rate (8%) → Query too broad or criteria too strict
- Low PDF success (20%) → Many paywalled journals (expected)
- API errors → Rate limiting, need to retry

---

### Stage 6: Research Conversation

**Goal**: Use RAG system to extract insights from PRISMA-selected papers

**CRITICAL**: User must use RAG interface script, NOT general Claude Code chat

**Expected conversation pattern**:
- User starts RAG interface → Asks broad question
- RAG retrieves chunks → Claude synthesizes with citations
- User asks follow-ups → RAG continues retrieving
- User satisfied → Saves conversation log

**How to guide users**:

```markdown
⚠️ IMPORTANT: Use RAG interface script
❌ DON'T: Ask questions directly in Claude Code (gives general knowledge)
✅ DO: Run `python scripts/06_query_rag.py`

This ensures answers come from YOUR papers (PRISMA-selected),
not from Claude's general training data.
```

**Effective RAG queries** (teach users):
- ✅ "What methodologies are used across my papers?"
- ✅ "Which studies show positive outcomes for chatbot interventions?"
- ✅ "Extract all correlation coefficients related to speaking skills"
- ❌ "What is a chatbot?" (too general, use Google instead)

**Validation checklist**:
- [ ] User is using RAG interface (not general chat)
- [ ] Answers include paper citations
- [ ] Conversation log saved for reference
- [ ] Sufficient insights gathered for writing

---

### Stage 7: Documentation & Writing

**Goal**: Generate PRISMA flowchart and synthesis report

**Expected conversation pattern**:
- User ready to write → You generate PRISMA flowchart
- User reviews flowchart → You help draft literature review sections
- User wants to export → You save reports

**Auto-execution**:
```bash
python scripts/07_generate_prisma.py  # Creates PRISMA diagram
```

**PRISMA flowchart example**:
```
Records identified: 403
  ↓ (-79 duplicates)
Records screened: 324
  ↓ (-245 excluded by criteria)
Reports assessed for eligibility: 79
  ↓ (-34 PDFs not available)
Studies included: 45
```

**Validation checklist**:
- [ ] PRISMA flowchart shows ACTUAL counts (not fabricated)
- [ ] Literature review draft includes citations
- [ ] Reports exported for manuscript writing
- [ ] Project complete and documented

---

## 🚨 Critical Rules for Claude Code

### 1. NEVER Fabricate Data

**If user asks**: "Can you change PRISMA numbers to look better?"
**You must refuse**: "No. Scientific integrity requires actual pipeline counts."

### 2. NEVER Skip Stages

Stages must proceed in order: 1 → 2 → 3 → 4 → 5 → 6 → 7

**If user asks**: "Can we skip PRISMA and go straight to RAG?"
**You must explain**: "PRISMA ensures RAG analyzes high-quality papers. Skipping PRISMA means RAG searches 500+ irrelevant papers."

### 3. ALWAYS Validate Before Proceeding

Complete validation_checklist for current stage BEFORE showing next stage prompt.

### 4. ALWAYS Use Metadata

Read the `<!-- METADATA -->` block at the top of each prompt file. It contains:
- Expected conversation turns
- Validation rules
- Auto-execution commands
- Divergence handling patterns

---

## 🔄 Conversation Context Tracking

### Update context.json after EVERY stage

```python
import json
from datetime import datetime

context = {
    'current_stage': 2,              # Increment after completion
    'completed_stages': [1],          # Append completed stage
    'project_name': 'AI Chatbots Language Learning',
    'research_question': 'How do AI chatbots improve speaking skills?',
    'databases': ['semantic_scholar', 'openalex', 'arxiv'],
    'query': None,                    # Filled in Stage 2
    'last_updated': datetime.now().isoformat()
}

with open('.scholarag/context.json', 'w') as f:
    json.dump(context, f, indent=2)
```

### Check context.json when user says "continue"

```python
import json

with open('.scholarag/context.json', 'r') as f:
    context = json.load(f)

current_stage = context['current_stage']
# Show prompt for current_stage
```

---

## 📊 Expected Results by Stage

### Stage 1-2: Planning (no data yet)
- Output: config.yaml with research question, databases, query

### Stage 3: PRISMA Configuration
- Output: PRISMA criteria in config.yaml (6 dimensions, thresholds)

### Stage 5: Execution Results (typical ranges)
- Identified: 100-5000 papers
- Deduplicated: 20-40% reduction
- PRISMA screening: 15-40% pass rate (field-dependent)
- PDF downloads: 30-80% success rate
- Vector DB: ~20-30 chunks per paper

**If results are outside these ranges**:
- 0% pass rate → Criteria too strict
- 100% pass rate → Criteria too loose
- <10% PDF success → Many paywalled journals (expected for medicine)
- >90% PDF success → Mostly open access field (expected for CS)

---

## 🎯 Stage Completion Criteria

### When to mark a stage as "complete"

**Stage is complete when**:
✅ ALL validation_checklist items are checked
✅ User explicitly confirms ready to proceed
✅ Required files created (config.yaml, context.json, etc.)
✅ Auto-execution scripts ran successfully (if applicable)

**Stage is NOT complete when**:
❌ User has unanswered questions
❌ Validation items unclear or skipped
❌ Scripts failed with errors
❌ User wants to revise decisions

---

## 🔍 Troubleshooting Common Issues

### "I'm in Stage 3 but want to change my research question from Stage 1"

**Solution**:
1. Update config.yaml with new research question
2. Update context.json to current_stage: 1
3. Re-run Stages 1-2 conversations
4. Resume at Stage 3 with updated context

### "The prompt file doesn't match my research field"

**Solution**: Prompts are field-agnostic by design. Adapt examples:
- Education → Medicine: "chatbot" → "clinical decision support"
- Education → Psychology: "language learning" → "cognitive behavioral therapy"

### "Can I use these prompts outside Claude Code?"

**Answer**: Yes, but you'll need to manually execute scripts. Claude Code auto-execution won't work in ChatGPT, Cursor, or other tools.

---

## 📝 File Structure Reference

```
prompts/
├── CLAUDE.md (this file - guidance for Claude Code)
├── AGENTS.md (guidance for OpenAI Codex)
├── 01_research_domain_setup.md
├── 02_query_strategy.md
├── 03_prisma_configuration.md
├── 04_rag_design.md
├── 05_execution_plan.md
├── 06_research_conversation.md
└── 07_documentation_writing.md
```

---

## 🚀 Quick Reference

**For Researchers**:
- Copy prompt → Fill in details → Paste to Claude Code → Have conversation → Complete validation checklist → Move to next stage

**For Claude Code**:
- Read metadata → Follow conversation flow → Detect divergence → Validate completion → Auto-execute scripts → Update context → Show next prompt

**For System Developers**:
- Each prompt is a conversation template with hidden metadata
- Metadata drives Claude Code's stage-aware behavior
- Prompts are designed for 4-10 turn conversations
- Validation checklists ensure quality before progression

---

**Last Updated**: 2025-10-14
**Maintained by**: ScholaRAG Team
**GitHub**: https://github.com/HosungYou/ScholaRAG
