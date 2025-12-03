# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with ScholaRAG.

## 🎓 User Profile: Researchers with Limited Coding Experience

**CRITICAL UNDERSTANDING**: Users of ScholaRAG are **researchers, not developers**. They have:
- **Limited coding experience**: May not know how to use terminal, run commands, or debug errors
- **Domain expertise**: Strong in their research field (education, medicine, psychology) but not in software engineering
- **Time constraints**: Need automated workflows, not manual step-by-step instructions
- **Expectation of assistance**: Assume Claude Code will handle technical details automatically

### How Claude Code Should Behave

**DO:**
- ✅ **Auto-execute commands** whenever possible (don't ask "would you like me to run X?")
- ✅ **Handle interactive inputs** automatically using echo pipes or CLI arguments
- ✅ **Provide default values** for test/demo scenarios
- ✅ **Run commands in sequence** without waiting for approval
- ✅ **Show results** after execution (e.g., "✅ Project initialized successfully!")
- ✅ **ALWAYS ask user to choose `project_type`** before initialization (critical branching point)

**DON'T:**
- ❌ Say "You'll need to run: `python script.py`" (run it for them instead!)
- ❌ Stop at interactive prompts (use automation techniques)
- ❌ Assume users can debug Python/shell errors
- ❌ Provide manual workarounds (automate the fix)
- ❌ **Auto-select `project_type` without explicit user confirmation**

### Example: Auto-Executing Interactive Commands

**Bad approach** (manual, requires user action):
```bash
# Don't do this:
python scholarag_cli.py init
# Then wait for user to type inputs manually
```

**Good approach** (automated, researcher-friendly):
```bash
# Do this instead:
echo -e "Test-Project\nHow does AI improve learning?\nsystematic_review" | python scholarag_cli.py init

# Or use CLI arguments (recommended):
python scholarag_cli.py init \
  --name "Test-Project" \
  --question "How does AI improve learning?" \
  --project-type systematic_review
```

## ScholaRAG: Production Systematic Review Automation

**IMPORTANT**: ScholaRAG is designed for **conversation-first research automation**. Researchers interact ONLY through prompts - Claude Code reads prompt metadata and auto-executes scripts behind the scenes.

### When to Activate This Workflow

**This behavior activates when:**
1. Working directory is inside `ScholaRAG/`
2. User provides a message that contains ScholaRAG prompt structure (starts with Stage number, has metadata comment)
3. OR user explicitly says they're doing a systematic literature review

**Detection pattern:**
- User message contains: "I want to conduct a PRISMA 2020 systematic literature review"
- OR user message starts with: "I want to build a RAG system for my research project"
- OR user asks: "Help me with Stage X of ScholaRAG"
- OR working directory contains `prompts/*.md` files with metadata blocks

### Core Philosophy

1. **Prompts are the primary interface** - Researchers never touch terminal
2. **Scripts execute automatically** - Based on conversation completion and metadata triggers
3. **Stage awareness** - Claude Code tracks which stage (1-7) researcher is currently in
4. **Protocol enforcement** - Divergence detection keeps conversations on track

### How It Works

When a researcher copies a stage prompt and pastes it to Claude Code:

1. **Claude Code reads HTML comment metadata** at the top of the prompt
2. **Understands current stage**, expected outputs, validation rules, next steps
3. **Has conversation** with researcher following expected patterns
4. **Validates completion** using checklist criteria
5. **Auto-executes scripts** when stage is complete
6. **Updates conversation context** (`.claude/context.json`)
7. **Shows next stage prompt** for researcher to continue

### Stage-Aware Behavior

**When user provides a ScholaRAG prompt, Claude Code should:**

1. **Read metadata block** (HTML comment at top of prompt file)
   - Current stage number and name
   - Expected conversation duration
   - Validation rules for outputs
   - Divergence handling patterns
   - Next stage transition conditions

2. **Check conversation context** (`.claude/context.json` if exists)
   - What stage is the researcher currently in?
   - What decisions have been made in previous stages?
   - Is there configuration data to reference?

3. **Follow conversation flow** (from metadata `conversation_flow.typical_pattern`)
   - Expected number of turns (e.g., 4-8 for Stage 1, 5-10 for Stage 2)
   - User action → Claude action patterns
   - Validate each turn against expected pattern

4. **Detect divergence** (from metadata `divergence_handling.common_divergences`)
   - Pattern: "User asks about downloading PDFs" in Stage 1
   - Response: Redirect with "PDF downloading happens in Stage 4..."
   - Pattern: "User wants to skip systematic review"
   - Response: Explain PRISMA requirements or suggest alternatives

5. **Validate stage completion** (from metadata `validation_checklist`)
   - Check all required fields are complete
   - Verify outputs meet validation rules
   - Confirm user understands next steps

6. **Execute scripts automatically** (from metadata `scripts_triggered`, `cli_commands`)
   - Stage 1 complete → Create `config.yaml`, initialize project structure
   - Stage 2 complete → Save query to `config.yaml`
   - Stage 5 complete → Execute `scripts/01_fetch_papers.py`, then `02_deduplicate.py`, etc.

7. **Update conversation context**
   ```json
   {
     "current_stage": 2,
     "completed_stages": [1],
     "research_question": "How do AI chatbots improve speaking skills?",
     "selected_databases": ["semantic_scholar", "openalex", "arxiv"],
     "query": "(chatbot OR agent) AND language learning",
     "last_updated": "2024-10-14T15:30:00Z"
   }
   ```

8. **Show next stage prompt**
   - Read from metadata `next_stage.prompt_file`
   - Display the full prompt for researcher to copy/paste
   - Explain what will happen in next stage

### Prompt Metadata Structure

All prompts in `prompts/*.md` have this metadata block:

```markdown
<!-- METADATA
stage: 1
stage_name: "Research Domain Setup"
expected_duration: "15-20 minutes"
conversation_mode: "interactive"
outputs:
  - research_question: "Clear, answerable research question"
  - project_type: "knowledge_repository or systematic_review"
validation_rules:
  research_question:
    required: true
    min_length: 20
  project_type:
    required: true
    allowed_values: ["knowledge_repository", "systematic_review"]
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
      user_action: "Provides research topic"
      claude_action: "Ask clarifying questions"
-->
```

### Example: Stage 1 Conversation Flow

**Researcher** (copies from website):
```
I want to build a RAG system for my research project.

**My Research Topic**: AI chatbots for language learning
**Research Field**: Education
...
```

**Claude Code** (reads metadata, knows this is Stage 1):
- Asks clarifying questions (2-3 rounds)
- Validates scope is realistic
- Recommends databases

**Claude Code** (MANDATORY: Present project_type options):
"I need to know which project type to use. ScholaRAG offers two modes:

**Option 1: knowledge_repository**
- Stage 1-2: Fetch & deduplicate ~10,000-20,000 papers (same for both modes)
- Stage 3 PRISMA screening: 50% confidence threshold (lenient)
- Typical result: ~5,000-15,000 papers pass screening
- Best for: Domain exploration, teaching materials, AI research assistant

**Option 2: systematic_review**
- Stage 1-2: Fetch & deduplicate ~10,000-20,000 papers (same for both modes)
- Stage 3 PRISMA screening: 90% confidence threshold (strict)
- Typical result: ~50-300 papers pass screening
- Best for: Meta-analysis, journal publication, clinical guidelines

⚠️  IMPORTANT: Both modes fetch the SAME papers in Stage 1.
The difference is Stage 3 PRISMA screening threshold, which naturally filters papers.

Which option matches your research goals?"

**Researcher** selects project_type

**Claude Code** (validates against checklist):
- ✅ Research question is specific
- ✅ Project type explicitly chosen by user
- ✅ Scope constraints realistic
- ✅ Expected paper count explained
- ✅ Databases selected

**Claude Code** (auto-executes with user-chosen project_type):
```bash
python scholarag_cli.py init \
  --name "AI-Chatbots-Language-Learning" \
  --question "How do AI chatbots improve speaking skills?" \
  --project-type knowledge_repository  # ← USER CHOICE
```

**Claude Code** (shows next prompt):
"Stage 1 complete! Here's your Stage 2 prompt for query design:
[Shows full prompt from 02_query_strategy.md]"

### Divergence Handling Examples

**Scenario 1: User jumps ahead**
```
USER (in Stage 1): "Can you help me download PDFs?"
CLAUDE: "PDF downloading happens in Stage 4. Right now in Stage 1,
let's first define your research scope, then design queries (Stage 2-3)."
```

**Scenario 2: User confused about project types**
```
USER (in Stage 1): "What's the difference between the two modes?"
CLAUDE: "ScholaRAG offers two project types:

**knowledge_repository**:
- Stage 1-2: Fetch & deduplicate ~10,000-20,000 papers (same for both)
- Stage 3 PRISMA: 50% confidence threshold → naturally retains ~5K-15K papers
- Lenient filtering (removes only spam/clearly off-topic)
- Best for: Teaching materials, AI research assistant, domain exploration

**systematic_review**:
- Stage 1-2: Fetch & deduplicate ~10,000-20,000 papers (same for both)
- Stage 3 PRISMA: 90% confidence threshold → naturally retains ~50-300 papers
- Strict PRISMA 2020 filtering (rigorous inclusion criteria)
- Best for: Meta-analysis, journal publication, clinical guidelines

⚠️  CRITICAL: Both modes fetch IDENTICAL papers in Stage 1-2.
Stage 3 PRISMA screening naturally filters based on confidence threshold.
NO manual paper count limits in Stage 1!

Which best matches your research goals?"
```

**Scenario 3: User confused about stage**
```
USER: "Wait, what stage am I in?"
CLAUDE: "You're in Stage 2 of 7: Query Strategy Design.
[●●○○○○○] Progress: ~35-50 minutes spent, ~3-7 hours remaining"
```

## 7-Stage Pipeline

ScholaRAG implements a 7-stage automated systematic literature review pipeline following PRISMA 2020 guidelines:

1. **Research Domain Setup** (`scholarag init`): Define scope, choose project_type
2. **Query Strategy** (`01_fetch_papers.py`): Fetch papers from databases
3. **Deduplication** (`02_deduplicate.py`): Remove duplicates
4. **Screening** (`03_screen_papers.py`): AI-assisted PRISMA screening
5. **PDF Download & RAG Building** (`04_download_pdfs.py`, `05_build_rag.py`): Build vector database
6. **Research Conversation** (`06_query_rag.py`): Interactive queries
7. **Documentation** (`07_generate_prisma.py`): Generate PRISMA flowchart

### Database Strategy

ScholaRAG supports **5 databases** across two categories:

**Open Access Databases** (PDF URLs available):
1. **Semantic Scholar** (~40% open access PDF URLs)
2. **OpenAlex** (~50% open access)
3. **arXiv** (100% PDF access)

**Institutional Databases** (metadata only - NO PDF URLs):
4. **Scopus** (Elsevier) - Requires `SCOPUS_API_KEY`
5. **Web of Science** (Clarivate) - Requires `WOS_API_KEY`

**Database Selection Protocol** (Stage 1, Turn 3):
```
Claude MUST ask: "Do you have institutional access to Scopus or Web of Science?"
- If Yes → Enable scopus/wos in config, show API key requirements
- If No → Use default open access databases only
```

**Why This Strategy?**
- Open access: Provides automated PDF retrieval for RAG
- Institutional: Provides comprehensive metadata coverage
- Best of both worlds when institutional access available

## CLI Tool

**IMPORTANT**: Always use echo pipes or CLI arguments to avoid interactive prompts.

```bash
# ✅ CORRECT: Auto-execute with echo pipe
echo -e "Test-Project\nHow does AI improve learning?\nsystematic_review" | python scholarag_cli.py init

# ✅ CORRECT: Use CLI arguments (recommended)
python scholarag_cli.py init \
  --name "AI-Chatbots-Learning" \
  --question "How do AI chatbots improve language learning?" \
  --project-type systematic_review

# ✅ With institutional databases (v1.2.6+)
python scholarag_cli.py init \
  --name "AI-Healthcare" \
  --question "How does AI improve clinical decision-making?" \
  --project-type systematic_review \
  --databases semantic_scholar openalex arxiv scopus wos

# ❌ WRONG: Interactive mode (blocks automation)
python scholarag_cli.py init  # Don't do this

# Check project status
python scholarag_cli.py status projects/2025-01-12_ProjectName

# List all projects
python scholarag_cli.py list

# Show current stage
python scholarag_cli.py stage-status

# Show next action
python scholarag_cli.py next
```

## Project Types

ScholaRAG supports **two project types** to serve different research goals:

### 📊 knowledge_repository (Comprehensive Domain Coverage)
- **Threshold**: 50% (lenient AI screening)
- **Output**: 15,000-20,000 papers
- **Use cases**: Teaching materials, AI research assistant, exploratory research, domain mapping
- **Filtering**: Minimal - removes only spam/duplicates

### 📄 systematic_review (Publication-Quality Review)
- **Threshold**: 90% (strict PRISMA 2020)
- **Output**: 50-300 papers
- **Use cases**: Meta-analysis, systematic review publication, clinical guidelines, dissertation
- **Filtering**: Strict - detailed inclusion/exclusion criteria

### Project Type Selection Protocol (v1.2.5.3+)

**CRITICAL: Claude MUST explicitly ask for project type selection in Stage 1, Turn 2:**

```
Claude MUST ask:
"Which project type matches your research goals?

**Option A: Knowledge Repository**
- 50% confidence threshold (lenient)
- Retains 15,000-20,000 papers
- Best for: Teaching, exploration, AI assistant

**Option B: Systematic Review**
- 90% confidence threshold (strict)
- Retains 50-300 papers
- Best for: Publication, meta-analysis, dissertation

Please choose Option A or Option B."
```

**Rules:**
- ❌ NEVER auto-infer project_type from user description
- ❌ NEVER skip this question
- ✅ ALWAYS present both options explicitly
- ✅ ALWAYS wait for user's explicit choice

**When to choose which:**
- Publishing systematic review? → `systematic_review` ✅
- Comprehensive domain coverage? → `knowledge_repository` ✅

## Environment Variables

Projects require these API keys:

**Required:**
- `ANTHROPIC_API_KEY`: Claude API for screening (Stage 3)

**Optional:**
- `OPENAI_API_KEY`: OpenAI embeddings (optional, can use local models)
- `SEMANTIC_SCHOLAR_API_KEY`: Higher rate limits for Semantic Scholar

**Institutional (if enabled):**
- `SCOPUS_API_KEY`: Scopus API access (requires institutional affiliation)
- `SCOPUS_INST_TOKEN`: Scopus institutional token (optional, for full access)
- `WOS_API_KEY`: Web of Science API access

## Testing and Development

```bash
# Run full pipeline test
python scripts/test_full_pipeline.py

# Validate config
python scripts/validate_config.py

# Run validation workflow
python scripts/run_validation_workflow.py
```

## Documentation

- **Main README**: [README.md](README.md)
- **SKILL.md**: Detailed implementation guide for AI assistants
- **Stage Prompts**: [prompts/](prompts/) - All 7 stage conversation templates
- **Website**: https://researcher-rag-helper.vercel.app/
