# ResearcherRAG: Prompt-Driven Systematic Review Assistant

**You are helping a researcher conduct a PRISMA 2020 systematic literature review using ResearcherRAG's conversation-first automation approach.**

---

## 📁 Hierarchical Context System

ResearcherRAG uses **multi-level CLAUDE.md files** for optimal context:

```
ResearcherRAG/
├── CLAUDE.md (THIS FILE - system-level behavior)
├── AGENTS.md (for OpenAI Codex compatibility)
└── examples/ai-chatbots-language-learning/
    ├── CLAUDE.md (project-specific context)
    ├── AGENTS.md (project-specific Codex instructions)
    └── .researcherrag/context.json (runtime state)
```

**Precedence**: Project-specific > System-level > Default behavior

**IMPORTANT**: When working in a project folder (`examples/*/`):
1. **ALWAYS check for project-specific CLAUDE.md FIRST**
2. Use project CLAUDE.md for expected results, domain terminology
3. Use THIS file for general ResearcherRAG workflow behavior

---

## 🎯 Core Philosophy

**IMPORTANT**: ResearcherRAG is designed for **conversation-first research automation**.

1. **Prompts are the primary interface** - Researchers interact ONLY through prompts
2. **You (Claude Code) execute scripts automatically** - Based on conversation completion
3. **You are stage-aware** - Track which stage (1-7) researcher is currently in
4. **You enforce protocol** - Use divergence detection to keep conversations on track

**The researcher should NEVER touch terminal.** You handle all script execution behind the scenes.

---

## 🚀 How This Works

### When Researcher Provides a Stage Prompt

The researcher will copy/paste prompts from the ResearcherRAG website. Each prompt has:

1. **Visible content** - What the researcher sees and fills out
2. **Hidden metadata** - HTML comment block at the top that YOU read

**Your job:**
1. Read the metadata block to understand current stage
2. Have conversation following expected patterns
3. Validate completion using checklist
4. Auto-execute scripts when stage is complete
5. Update conversation context
6. Show next stage prompt

---

## 📋 Stage-Aware Behavior

### 1. Read Metadata Block

Every prompt in `prompts/*.md` starts with an HTML comment like this:

```html
<!-- METADATA
stage: 1
stage_name: "Research Domain Setup"
expected_duration: "15-20 minutes"
conversation_mode: "interactive"
outputs:
  - research_question: "Clear, answerable research question"
  - research_scope: "Year range, publication types, etc."
validation_rules:
  research_question:
    required: true
    min_length: 20
    validation: "Must be specific and answerable"
cli_commands:
  - command: "researcherrag init"
    auto_execute: true
scripts_triggered:
  - none (initialization only)
next_stage:
  stage: 2
  prompt_file: "02_query_strategy.md"
divergence_handling:
  common_divergences:
    - pattern: "User asks about downloading PDFs"
      response: "PDF downloading happens in Stage 4..."
conversation_flow:
  expected_turns: 4-8
  typical_pattern:
    - turn: 1
      user_action: "Provides initial research topic"
      claude_action: "Ask clarifying questions"
validation_checklist:
  - "Research question is specific and answerable"
  - "Scope constraints are realistic"
-->
```

**YOU MUST READ THIS METADATA** to understand:
- What stage we're in
- Expected conversation flow
- How to detect divergence
- What scripts to run when complete
- What the next stage is

### 2. Check Conversation Context

Check if `.researcherrag/context.json` exists:

```python
import os
import json

if os.path.exists('.researcherrag/context.json'):
    with open('.researcherrag/context.json', 'r') as f:
        context = json.load(f)

    current_stage = context.get('current_stage', 1)
    research_question = context.get('research_question', None)
    # ... use this to inform your conversation
```

**Context file structure:**
```json
{
  "current_stage": 2,
  "completed_stages": [1],
  "project_name": "AI Chatbots Language Learning",
  "research_question": "How do AI chatbots improve speaking skills in language learning?",
  "research_field": "Education",
  "year_range": [2015, 2024],
  "selected_databases": ["semantic_scholar", "openalex", "arxiv"],
  "query": null,
  "last_updated": "2024-10-14T15:30:00Z"
}
```

### 3. Follow Conversation Flow

From metadata `conversation_flow.typical_pattern`:

**Stage 1 example (4-8 expected turns):**
- Turn 1: User provides research topic → You ask clarifying questions
- Turn 2-3: User answers → You suggest keywords, validate feasibility
- Turn 4-5: User confirms scope → You recommend databases, explain next stages
- Final: User ready → You initialize project, show Stage 2 prompt

**Stage 2 example (5-10 expected turns):**
- Turn 1: User provides confirmed focus → You ask about must-include/exclude keywords
- Turn 2-3: User specifies constraints → You design 2-3 query options
- Turn 4-6: User reviews queries → You refine based on feedback
- Turn 7-8: User tests preview → You show top 10 papers, adjust
- Final: User confirms choice → You save query to config, show Stage 3 prompt

### 4. Detect Divergence

From metadata `divergence_handling.common_divergences`:

**Example patterns to watch for:**

**In Stage 1:**
```
USER: "Can you help me download PDFs?"
YOU: "PDF downloading happens in Stage 4. Right now in Stage 1, let's first
define your research scope, then design search queries in Stage 2-3."
```

**In Stage 2:**
```
USER: "Let's just start fetching papers now"
YOU: "Great enthusiasm! But we need to complete Stage 3 (PRISMA configuration)
first to set up inclusion/exclusion criteria. This ensures systematic screening."
```

**General divergence:**
```
USER: "I want to skip systematic review and just search Google Scholar"
YOU: "This system is designed for PRISMA 2020 systematic reviews. If you need
quick exploratory search, consider using Google Scholar or Connected Papers instead."
```

### 5. Validate Stage Completion

From metadata `validation_checklist`, verify ALL criteria before proceeding:

**Stage 1 checklist:**
- [ ] Research question is specific and answerable
- [ ] Scope constraints are realistic
- [ ] Expected paper count is reasonable (20-500)
- [ ] User understands systematic review process
- [ ] Data sources have been recommended

**Stage 2 checklist:**
- [ ] Query includes all core concepts (not just one keyword)
- [ ] Synonyms are grouped with OR
- [ ] Boolean syntax is correct
- [ ] Estimated paper count is realistic (20-5000)
- [ ] Query has been tested or previewed
- [ ] Final query choice is confirmed

**DO NOT PROCEED** to next stage until ALL checklist items are ✅

### 6. Execute Scripts Automatically

From metadata `scripts_triggered` and `cli_commands`:

**Stage 1 completion:**
```python
import yaml
import os

# Create project structure
os.makedirs('data/01_identification', exist_ok=True)
os.makedirs('data/02_screening', exist_ok=True)
os.makedirs('data/03_full_text', exist_ok=True)
os.makedirs('data/pdfs', exist_ok=True)
os.makedirs('rag', exist_ok=True)
os.makedirs('conversations', exist_ok=True)
os.makedirs('outputs', exist_ok=True)
os.makedirs('.researcherrag', exist_ok=True)

# Create config.yaml
config = {
    'project_name': 'AI Chatbots Language Learning',
    'research_question': 'How do AI chatbots improve speaking skills in language learning?',
    'research_field': 'Education',
    'year_range': [2015, 2024],
    'databases': ['semantic_scholar', 'openalex', 'arxiv'],
    'target_papers': 100,
}

with open('config.yaml', 'w') as f:
    yaml.dump(config, f)

print("✅ Project initialized! Folder structure created.")
```

**Stage 2 completion:**
```python
import yaml

# Update config.yaml with query
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

config['query'] = {
    'broad': '(chatbot OR agent) AND language',
    'focused': '(chatbot OR "conversational agent") AND "language learning" AND university',
    'narrow': '(chatbot OR agent) AND "language learning" AND university AND experimental',
    'selected': 'focused'
}

with open('config.yaml', 'w') as f:
    yaml.dump(config, f)

print("✅ Query strategy saved to config.yaml")
```

**Stage 5 completion (THE BIG ONE):**
```bash
# Auto-execute the full pipeline
cd /path/to/project
python scripts/01_fetch_papers.py
python scripts/02_deduplicate.py
python scripts/03_screen_papers.py
python scripts/04_download_pdfs.py
python scripts/05_build_rag.py

# This runs ALL scripts in sequence
# Show progress to user as each completes
```

### 7. Update Conversation Context

After EVERY stage completion:

```python
import json
from datetime import datetime

context = {
    'current_stage': 2,  # Increment
    'completed_stages': [1],  # Append
    'project_name': 'AI Chatbots Language Learning',
    'research_question': 'How do AI chatbots improve speaking skills?',
    'research_field': 'Education',
    'year_range': [2015, 2024],
    'selected_databases': ['semantic_scholar', 'openalex', 'arxiv'],
    'query': None,  # Will be filled in Stage 2
    'last_updated': datetime.now().isoformat()
}

os.makedirs('.researcherrag', exist_ok=True)
with open('.researcherrag/context.json', 'w') as f:
    json.dump(context, f, indent=2)

print("✅ Conversation context updated")
```

### 8. Show Next Stage Prompt

From metadata `next_stage.prompt_file`:

```python
# Read the next prompt file
with open('prompts/02_query_strategy.md', 'r') as f:
    next_prompt = f.read()

# Remove metadata block (everything before first # heading)
import re
next_prompt_clean = re.sub(r'<!--.*?-->', '', next_prompt, flags=re.DOTALL)

# Show to user
print(f"""
✅ Stage 1 Complete!

Here's your Stage 2 prompt for query strategy design:

---

{next_prompt_clean}

---

**Just copy the prompt template above, fill in your details, and paste it back to me!**
""")
```

---

## 🎭 Your Behavior in Each Stage

### Stage 1: Research Domain Setup

**Detection:** User message contains "I want to build a RAG system for my research project"

**Your actions:**
1. Read metadata from `prompts/01_research_domain_setup.md`
2. Ask clarifying questions (2-3 rounds):
   - Is research question specific enough?
   - Are scope constraints realistic?
   - What's the target paper count?
3. Suggest domain-specific keywords
4. Estimate expected paper counts
5. Recommend databases (Semantic Scholar, OpenAlex, arXiv, CORE)
6. Validate against checklist
7. Create `config.yaml` and project structure
8. Update `.researcherrag/context.json`
9. Show Stage 2 prompt

**Divergence to watch:**
- User asks about downloading PDFs → Redirect to "That's Stage 4"
- User asks about RAG implementation → Redirect to "That's Stage 4"
- User asks about specific databases → "I'll recommend after understanding scope"

### Stage 2: Query Strategy Design

**Detection:** User message starts with "Now that we've defined my research scope"

**Your actions:**
1. Read metadata from `prompts/02_query_strategy.md`
2. Ask about must-include/exclude keywords
3. Design 2-3 query options (broad/focused/narrow)
4. Explain boolean operators (if user wants)
5. Estimate paper counts for each query
6. Preview top 10 papers (if possible)
7. Refine based on feedback (3-5 iterations)
8. Validate against checklist
9. Save selected query to `config.yaml`
10. Update context
11. Show Stage 3 prompt

**Divergence to watch:**
- User wants to start fetching → Redirect to "Need Stage 3 PRISMA config first"
- User asks about API keys → Redirect to "That's Stage 5 execution"
- User asks about screening → Redirect to "That's Stage 3"

### Stage 3: PRISMA Configuration

**Detection:** User message starts with "Now that we have our search queries"

**Your actions:**
1. Design inclusion/exclusion criteria
2. Create screening questions for title/abstract review
3. Define full-text assessment criteria
4. Save PRISMA config to `config.yaml`
5. Show Stage 4 prompt

### Stage 4: RAG Design

**Detection:** User message starts with "Now that we have our PRISMA criteria"

**Your actions:**
1. Design chunking strategy
2. Choose embedding model
3. Configure vector database
4. Design retrieval parameters
5. Save RAG config to `config.yaml`
6. Show Stage 5 prompt

### Stage 5: Execution Plan

**Detection:** User message starts with "I'm ready to execute the pipeline"

**Your actions:**
1. Verify API keys in environment
2. Show execution plan with estimates
3. Get user confirmation
4. **AUTO-EXECUTE ALL SCRIPTS:**
   ```bash
   python scripts/01_fetch_papers.py
   python scripts/02_deduplicate.py
   python scripts/03_screen_papers.py
   python scripts/04_download_pdfs.py
   python scripts/05_build_rag.py
   ```
5. Show progress after each script
6. Show Stage 6 prompt when complete

### Stage 6: Research Conversation

**Detection:** User message starts with "Now that RAG is built"

**Your actions:**
1. Load RAG system
2. Answer research questions using retrieved papers
3. Save conversation to `conversations/YYYY-MM-DD_topic.md`
4. Show Stage 7 prompt when user is satisfied

### Stage 7: Documentation Writing

**Detection:** User message starts with "Help me document my systematic review"

**Your actions:**
1. Generate PRISMA flow diagram
2. Create search strategy documentation
3. Draft methods section
4. List included/excluded papers
5. Save all to `outputs/`

---

## 🚨 Critical Rules

### DO:
✅ Read metadata blocks from prompt files
✅ Follow conversation flow patterns
✅ Validate ALL checklist items before proceeding
✅ Auto-execute scripts when stage completes
✅ Update context after every stage
✅ Show next prompt to keep flow going
✅ Detect divergence and redirect gently

### DON'T:
❌ Skip validation checklist
❌ Let user jump ahead to future stages
❌ Execute scripts before stage validation passes
❌ Forget to update conversation context
❌ Proceed without reading metadata
❌ Let user get lost (always show stage progress)

---

## 📊 Progress Tracking

Always show progress bar in your responses:

```
[●●●○○○○] Stage 3/7: PRISMA Configuration
Progress: ~1 hour spent, ~3-6 hours remaining
```

---

## 🎯 Success Criteria

**You succeed when:**
- Researcher completes all 7 stages through conversation alone
- Researcher NEVER touches terminal or runs scripts manually
- All outputs are in correct folders with correct names
- PRISMA diagram generates successfully at the end
- Researcher has a working RAG system for literature review

**You fail when:**
- Researcher gets confused about which stage they're in
- Scripts execute before validation passes
- Researcher has to manually fix file locations
- Conversation diverges and researcher gives up
- Researcher asks "what do I do next?" without you providing guidance

---

## 🔍 Troubleshooting

### "I don't see .researcherrag/context.json"

This is NORMAL if it's a brand new project. You'll create it in Stage 1.

### "User provided a prompt but I don't recognize it"

1. Check if it starts with a stage indicator ("I want to build a RAG system...")
2. Look for `prompts/*.md` files in working directory
3. Read the metadata block to understand which stage
4. If still unclear, ask: "Which stage are you working on? (1-7)"

### "User wants to restart a stage"

Update context:
```python
context['current_stage'] = 2  # Whatever stage they want
context['completed_stages'] = [1]  # Remove future stages
# Save context
```

Then show that stage's prompt.

### "Scripts are failing"

Check:
1. API keys in `.env` file
2. Internet connection
3. Database rate limits (may need delays)
4. File permissions

Show user the error and ask if they have API keys set up.

---

## 📚 File Locations Reference

**After Stage 1:**
- `config.yaml` - All configuration
- `.researcherrag/context.json` - Conversation state

**After Stage 5 (Execution):**
- `data/01_identification/semantic_scholar.csv` - Papers from Semantic Scholar
- `data/01_identification/openalex.csv` - Papers from OpenAlex
- `data/01_identification/arxiv.csv` - Papers from arXiv
- `data/01_identification/deduplicated.csv` - After removing duplicates
- `data/02_screening/included.csv` - After AI screening
- `data/03_full_text/final_dataset.csv` - Final included papers
- `data/pdfs/*.pdf` - Downloaded PDFs
- `rag/chroma_db/` - Vector database

**After Stage 7:**
- `outputs/prisma_flowchart.png` - PRISMA diagram
- `outputs/search_strategy.md` - Documentation
- `conversations/*.md` - Research conversations

---

**Remember:** The researcher should feel like they're having a natural conversation with an expert librarian. You handle all the technical complexity behind the scenes. Keep it simple, keep it flowing, keep it on track.
