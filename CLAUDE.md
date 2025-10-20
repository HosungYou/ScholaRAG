# ScholaRAG: Prompt-Driven Systematic Review Assistant

**You are helping a researcher conduct a PRISMA 2020 systematic literature review enhanced with RAG-powered analysis using ScholaRAG's conversation-first automation approach.**

## 🧠 What is ScholaRAG?

ScholaRAG combines two powerful methodologies:

1. **PRISMA 2020 Protocol** (Stages 1-4): Systematic paper identification, screening, and selection
2. **RAG (Retrieval-Augmented Generation)** (Stages 5-6): AI-powered data extraction and synthesis from selected papers

**Why this combination?**
- **PRISMA ensures rigor**: Transparent, reproducible paper selection following academic standards
- **RAG enables depth**: Extract specific data (correlations, effect sizes, themes) from hundreds of pages automatically
- **Together**: Systematic rigor + AI-powered analysis = Comprehensive literature reviews in days, not months

---

## 📁 Hierarchical Context System

ScholaRAG uses **multi-level CLAUDE.md files** for optimal context:

```
ScholaRAG/
├── CLAUDE.md (THIS FILE - system-level behavior)
├── AGENTS.md (for OpenAI Codex compatibility)
└── examples/ai-chatbots-language-learning/
    ├── CLAUDE.md (project-specific context)
    ├── AGENTS.md (project-specific Codex instructions)
    └── .scholarag/context.json (runtime state)
```

**Precedence**: Project-specific > System-level > Default behavior

**IMPORTANT**: When working in a project folder (`examples/*/`):
1. **ALWAYS check for project-specific CLAUDE.md FIRST**
2. Use project CLAUDE.md for expected results, domain terminology
3. Use THIS file for general ScholaRAG workflow behavior

---

## 🎯 Core Philosophy

**IMPORTANT**: ScholaRAG is designed for **conversation-first research automation**.

1. **Prompts are the primary interface** - Researchers interact ONLY through prompts
2. **You (Claude Code) execute scripts automatically** - Based on conversation completion
3. **You are stage-aware** - Track which stage (1-7) researcher is currently in
4. **You enforce protocol** - Use divergence detection to keep conversations on track

**The researcher should NEVER touch terminal.** You handle all script execution behind the scenes.

---

## 🚀 How This Works

### When Researcher Provides a Stage Prompt

The researcher will copy/paste prompts from the ScholaRAG website. Each prompt has:

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
  - command: "scholarag init"
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

Check if `.scholarag/context.json` exists:

```python
import os
import json

if os.path.exists('.scholarag/context.json'):
    with open('.scholarag/context.json', 'r') as f:
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
os.makedirs('.scholarag', exist_ok=True)

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

**Stage 4 completion (PDF Download):**
```bash
# Download PDFs for screened papers
cd /path/to/project
python scripts/04_download_pdfs.py

# Expected: 30-80% success rate (paywalls are normal)
```

**Stage 5 completion (Build RAG - Core AI Analysis):**
```bash
# Build RAG system from downloaded PDFs
cd /path/to/project
python scripts/05_build_rag.py

# What this does:
# 1. Extract text from PDFs
# 2. Chunk into semantic units (~500 tokens)
# 3. Generate embeddings (OpenAI/local model)
# 4. Store in ChromaDB vector database
# 5. Enable semantic search across all papers
```

**Stage 6 (Query RAG - Interactive Analysis):**
```python
# Launch interactive RAG query interface
import subprocess

subprocess.run([
    'python', 'scripts/06_query_rag.py',
    '--project', 'current_project',
    '--interactive'
])

# User can now ask questions like:
# - "What methodologies were used to measure speaking skills?"
# - "Extract all correlation coefficients"
# - "Summarize main findings across papers"
#
# RAG returns: Citation-backed answers (no hallucination)
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

os.makedirs('.scholarag', exist_ok=True)
with open('.scholarag/context.json', 'w') as f:
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
8. Update `.scholarag/context.json`
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

## 🗂️ Project Creation and Switching Protocol

### When to Create a New Project

ScholaRAG supports **multiple independent projects** (e.g., "AI in Healthcare" and "Chatbots for Learning" are separate systematic reviews). You must detect when the user wants to create a **new project** vs. continue an **existing project**.

#### Triggers for Creating a New Project

Create a **new project** when:

1. **Explicit keyword trigger**:
   - User says: "new project", "start a new systematic review", "create another project", "second project", "different research topic"

2. **Topic mismatch detection**:
   - User mentions a research topic DIFFERENT from existing `.scholarag/context.json` metadata
   - Example: Existing project = "AI Healthcare Adoption", User says = "I want to study chatbots for language learning"

3. **No existing project detected**:
   - Working directory = `ScholaRAG/` (repository root)
   - No `.scholarag/context.json` file found
   - This is the user's FIRST project

4. **User confirmation required**:
   - ALWAYS ask user before creating a new project:
     ```
     "This looks like a new research topic (different from your current project 'AI Healthcare').
     Create a new project 'Chatbot-Learning'? [y/n]"
     ```

#### Decision Tree for Project Management

```
User message received
    ↓
Is working directory ScholaRAG/ (root)?
    ├─ Yes → Check for .scholarag/context.json
    │         ├─ Exists → ⚠️  ERROR: .scholarag should NOT be in root
    │         │           (Should be in projects/*/ subfolder)
    │         │           Ask: "Move this to projects/ folder?"
    │         │
    │         └─ Not exists → This is FIRST project or need to create NEW project
    │                         ├─ Check: Does projects/ folder exist?
    │                         │   ├─ Yes → List existing projects
    │                         │   │         Ask: "Continue existing or create new?"
    │                         │   └─ No → First project ever
    │                         │            Run: python scholarag_cli.py init
    │                         │            Creates: projects/2025-10-18_Project-Name/
    │                         └─ Run: python scholarag_cli.py init
    │
    └─ No → Check: Is working directory projects/*/ (project subfolder)?
              ├─ Yes → Check for .scholarag/context.json
              │         ├─ Exists → Load context, check topic match
              │         │             ├─ Topic MATCHES user message → Continue project
              │         │             │   Load current_stage, show progress
              │         │             │
              │         │             └─ Topic MISMATCH → Ask user
              │         │                 "Your current project is 'AI Healthcare'.
              │         │                  You mentioned 'chatbots'. Create new project?"
              │         │
              │         └─ Not exists → ⚠️  WARNING: Project folder without metadata
              │                         Ask: "Initialize this folder as ScholaRAG project?"
              │
              └─ No → ❌ ERROR: Must work inside ScholaRAG/ or projects/*/
                      Show: "Please navigate to ScholaRAG directory"
```

### Example Conversation Flows

#### Scenario 1: First Project Ever

```
Working directory: /path/to/ScholaRAG/
User: "I want to build a RAG for AI adoption in healthcare"

Claude Code:
1. Check: .scholarag/context.json exists? → No
2. Check: projects/ folder exists? → No
3. Conclusion: This is the FIRST project
4. Action: "I'll create your first ScholaRAG project.
            Running: python scholarag_cli.py init"
5. Prompt user for project details:
   - Project name: "AI-Healthcare-Adoption"
   - Research question: "What factors influence AI adoption in hospitals?"
   - Domain: "medicine"
6. Execute: python scholarag_cli.py init \
              --name "AI-Healthcare-Adoption" \
              --question "What factors influence AI adoption in hospitals?" \
              --domain medicine
7. Result: projects/2025-10-18_AI-Healthcare-Adoption/ created
8. Navigate: cd projects/2025-10-18_AI-Healthcare-Adoption/
9. Continue: Begin Stage 1 conversation
```

#### Scenario 2: Second Project (NEW Topic)

```
Working directory: /path/to/ScholaRAG/projects/2025-10-18_AI-Healthcare/
Current project context loaded:
  - project_name: "AI Healthcare Adoption"
  - research_question: "What factors influence AI adoption in hospitals?"
  - current_stage: 3

User: "NEW project: I want to study chatbots for language learning"

Claude Code:
1. Detect keyword: "NEW project"
2. Check current .scholarag/context.json:
   - Topic: "AI Healthcare" ≠ "chatbots for language learning"
3. Conclusion: User wants a DIFFERENT systematic review
4. Ask confirmation:
   ┌─────────────────────────────────────────────────────────┐
   │ 🔍 New Project Detection                                │
   ├─────────────────────────────────────────────────────────┤
   │ Current project: "AI Healthcare Adoption" (Stage 3/7)   │
   │ Your message mentions: "chatbots for language learning" │
   │                                                          │
   │ This looks like a DIFFERENT research topic.             │
   │                                                          │
   │ Options:                                                │
   │ 1️⃣  Create NEW project "Chatbot-Learning"              │
   │    → New folder: projects/2025-10-18_Chatbot-Learning/ │
   │    → Separate database, separate RAG system            │
   │                                                          │
   │ 2️⃣  Continue current project "AI Healthcare"           │
   │    → Stay in current folder, resume Stage 3            │
   │                                                          │
   │ Which option? [1/2]                                     │
   └─────────────────────────────────────────────────────────┘

User: "1"

Claude Code:
5. Navigate to root: cd ../../
6. Execute: python scholarag_cli.py init \
              --name "Chatbot-Learning" \
              --question "How do chatbots improve language learning outcomes?" \
              --domain education
7. Result: projects/2025-10-18_Chatbot-Learning/ created
8. Navigate: cd projects/2025-10-18_Chatbot-Learning/
9. Continue: Begin Stage 1 for NEW project
10. Note: Original project remains intact at:
    projects/2025-10-18_AI-Healthcare/ (can resume later)
```

#### Scenario 3: Switch Between Existing Projects

```
Working directory: /path/to/ScholaRAG/projects/2025-10-18_Chatbot-Learning/
User: "Switch to my AI Healthcare project"

Claude Code:
1. Detect keyword: "Switch to"
2. Run: python scholarag_cli.py list
   Output:
   ✅ 2025-10-18_AI-Healthcare-Adoption
      📊 Stage 3/6 • Domain: medicine

   🆕 2025-10-18_Chatbot-Learning
      📊 Stage 1/6 • Domain: education
3. Find match: "AI Healthcare" → "2025-10-18_AI-Healthcare-Adoption"
4. Navigate: cd ../2025-10-18_AI-Healthcare-Adoption/
5. Load context: .scholarag/context.json
   {
     "current_stage": 3,
     "project_name": "AI Healthcare Adoption",
     "research_question": "What factors influence AI adoption?"
   }
6. Inform user:
   "✅ Switched to project: AI Healthcare Adoption
    📍 Currently on Stage 3/7: PRISMA Configuration
    📅 Last updated: 2025-10-15

    Ready to continue where you left off!"
7. Show Stage 3 prompt or ask: "Continue with Stage 3 or jump to different stage?"
```

#### Scenario 4: User Confused About Multiple Projects

```
Working directory: /path/to/ScholaRAG/
User: "I want to continue my chatbot project"

Claude Code:
1. Check: .scholarag/context.json in current directory? → No
2. Check: projects/ folder exists? → Yes
3. Run: python scholarag_cli.py list
4. Show user:
   ┌─────────────────────────────────────────────────────────┐
   │ 📚 Your ScholaRAG Projects                          │
   ├─────────────────────────────────────────────────────────┤
   │ 1. AI-Healthcare-Adoption (Stage 3/7)                   │
   │    Research: "What factors influence AI adoption?"      │
   │    Last active: 2025-10-15                              │
   │                                                          │
   │ 2. Chatbot-Learning (Stage 1/7)                         │
   │    Research: "How do chatbots improve learning?"        │
   │    Last active: 2025-10-18                              │
   │                                                          │
   │ Which project? [1/2]                                    │
   └─────────────────────────────────────────────────────────┘

User: "2"

Claude Code:
5. Navigate: cd projects/2025-10-18_Chatbot-Learning/
6. Load context and continue
```

### Topic Mismatch Detection Algorithm

Use this logic to detect when user wants a NEW project vs. continue existing:

```python
import json
import os

def should_create_new_project(user_message: str, context_file: str = '.scholarag/context.json') -> bool:
    """
    Determine if user wants a new project or continue existing.

    Returns:
        True: Create new project
        False: Continue existing project
    """
    # Check for explicit keywords
    new_project_keywords = [
        "new project", "start a new", "create another",
        "second project", "different topic", "different research"
    ]

    if any(keyword in user_message.lower() for keyword in new_project_keywords):
        return True

    # Check if context file exists
    if not os.path.exists(context_file):
        # No existing project
        return True

    # Load existing project context
    with open(context_file, 'r') as f:
        context = json.load(f)

    existing_topic = context.get('project_name', '').lower()
    existing_question = context.get('research_question', '').lower()

    # Extract key terms from user message (simple approach)
    user_message_lower = user_message.lower()

    # Check if user message contains terms from existing project
    topic_overlap = (
        existing_topic in user_message_lower or
        any(word in user_message_lower for word in existing_question.split() if len(word) > 4)
    )

    # If NO overlap and user is describing a research topic → likely NEW project
    research_indicators = ["study", "research", "review", "investigate", "analyze"]
    mentions_research = any(indicator in user_message_lower for indicator in research_indicators)

    if mentions_research and not topic_overlap:
        # User is describing research, but doesn't match existing project
        return True  # Probably wants new project (but ASK for confirmation)

    return False  # Continue existing project
```

### Critical Rules for Project Management

**DO:**
- ✅ Always check working directory before creating projects
- ✅ Detect topic mismatch and ASK user for confirmation
- ✅ Use `python scholarag_cli.py list` to show existing projects
- ✅ Navigate to correct project folder before starting work
- ✅ Keep projects isolated (separate folders, separate databases)

**DON'T:**
- ❌ Create new project without asking when existing project detected
- ❌ Overwrite existing .scholarag/context.json
- ❌ Mix data from different projects in same folder
- ❌ Assume user wants to continue if topic looks different

### Project Folder Structure (Multiple Projects)

```
ScholaRAG/                                  # Framework repository (root)
├── scholarag_cli.py                        # Project manager CLI
├── scripts/                                    # Shared scripts (all projects use these)
│   ├── 01_fetch_papers.py
│   ├── 02_deduplicate.py
│   └── ...
├── prompts/                                    # Shared prompts
│   ├── 01_research_domain_setup.md
│   └── ...
└── projects/                                   # All user projects (gitignored)
    ├── 2025-10-18_AI-Healthcare-Adoption/      # Project 1
    │   ├── .scholarag/
    │   │   └── context.json                    # Project 1 state
    │   ├── config.yaml                         # Project 1 config
    │   ├── data/
    │   │   ├── 01_identification/
    │   │   │   └── semantic_scholar.csv        # Project 1 papers
    │   │   └── pdfs/                           # Project 1 PDFs
    │   └── rag/
    │       └── chroma_db/                      # Project 1 vector DB
    │
    └── 2025-10-18_Chatbot-Learning/            # Project 2
        ├── .scholarag/
        │   └── context.json                    # Project 2 state (independent)
        ├── config.yaml                         # Project 2 config (different)
        ├── data/
        │   ├── 01_identification/
        │   │   └── semantic_scholar.csv        # Project 2 papers (separate)
        │   └── pdfs/                           # Project 2 PDFs (separate)
        └── rag/
            └── chroma_db/                      # Project 2 vector DB (separate)
```

**Key principle**: Each project is COMPLETELY ISOLATED:
- Different research questions
- Different papers fetched
- Different PDFs downloaded
- Different vector databases
- Different RAG systems
- Independent conversation contexts

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

### "I don't see .scholarag/context.json"

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
- `.scholarag/context.json` - Conversation state

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
