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
- ✅ **Run commands in sequence** without waiting for approval (unless API costs involved)
- ✅ **Show results** after execution (e.g., "✅ Project initialized successfully!")

**DON'T:**
- ❌ Say "You'll need to run: `python script.py`" (run it for them instead!)
- ❌ Stop at interactive prompts (use automation techniques)
- ❌ Assume users can debug Python/shell errors
- ❌ Provide manual workarounds (automate the fix)

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
echo -e "Test-Project\nHow does AI improve learning?\neducation\nsystematic_review" | python scholarag_cli.py init

# Or use CLI arguments (recommended):
python scholarag_cli.py init \
  --name "Test-Project" \
  --question "How does AI improve learning?" \
  --domain education \
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
- Suggests project_type based on researcher goals
- Validates scope is realistic
- Recommends databases

**Researcher** confirms scope is good

**Claude Code** (validates against checklist):
- ✅ Research question is specific
- ✅ Project type chosen (knowledge_repository or systematic_review)
- ✅ Scope constraints realistic
- ✅ Paper count aligned with project_type
- ✅ Databases selected

**Claude Code** (auto-executes):
```bash
python scholarag_cli.py init \
  --name "AI-Chatbots-Language-Learning" \
  --question "How do AI chatbots improve speaking skills?" \
  --domain education \
  --project-type knowledge_repository
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
- 50% threshold (lenient, removes only spam)
- 15,000-20,000 papers output
- For: Teaching, exploration, AI assistant

**systematic_review**:
- 90% threshold (strict, PRISMA 2020)
- 50-300 papers output
- For: Meta-analysis, publication

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

**Primary Databases** (chosen for API access and PDF availability):
1. **Semantic Scholar** (~40% open access PDF URLs)
2. **OpenAlex** (~50% open access)
3. **arXiv** (100% PDF access)

**Why These Databases?**
- Traditional databases (PubMed, Scopus, ERIC) don't provide automated PDF access
- Semantic Scholar + OpenAlex + arXiv = ~50-60% overall PDF retrieval success
- All three provide REST APIs with generous rate limits
- No institutional subscriptions required

## CLI Tool

**IMPORTANT**: Always use echo pipes or CLI arguments to avoid interactive prompts.

```bash
# ✅ CORRECT: Auto-execute with echo pipe
echo -e "Test-Project\nHow does AI improve learning?\neducation\nsystematic_review" | python scholarag_cli.py init

# ✅ CORRECT: Use CLI arguments (recommended)
python scholarag_cli.py init \
  --name "AI-Chatbots-Learning" \
  --question "How do AI chatbots improve language learning?" \
  --domain education \
  --project-type systematic_review

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

**When to choose which:**
- Publishing systematic review? → `systematic_review` ✅
- Comprehensive domain coverage? → `knowledge_repository` ✅

## Environment Variables

Projects require these API keys:
- `ANTHROPIC_API_KEY`: Claude API for screening (Stage 3)
- `OPENAI_API_KEY`: OpenAI embeddings (optional, can use local models)

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
