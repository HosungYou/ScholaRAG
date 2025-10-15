# 3-Tier Configuration Architecture

**Decision Document**
**Created**: 2025-10-14
**Status**: Approved - Implementation in Progress
**Version**: v1.0.6

---

## 📋 Executive Summary

This document outlines the **3-Tier Configuration Architecture** for ResearcherRAG, designed to enable **prompt-driven research automation** while maintaining a single source of truth and avoiding configuration duplication.

**Key Decision**: Use a hierarchical configuration system with clear separation of concerns:
- **Tier 1**: Prompt Metadata (researcher-facing)
- **Tier 2**: `.claude/` Configuration (execution-facing)
- **Tier 3**: CLAUDE.md (behavior-facing)

---

## 🎯 Problem Statement

### The Challenge

ResearcherRAG aims to provide a **conversation-first research experience** where researchers:
1. Read prompts from `prompts/*.md`
2. Talk to Claude Code
3. **Scripts execute automatically** based on conversation context
4. Never touch the terminal or write code

### Current Gaps

**Before v1.0.6**:
```
❌ Claude Code doesn't know which stage researcher is in
❌ No automatic script execution based on conversation
❌ No prerequisite validation (can skip stages accidentally)
❌ No divergence detection ("Can you help me download PDFs?" in Stage 1)
❌ Manual command execution required
```

**Example Pain Point**:
```
Researcher (Stage 1): "I want to research AI chatbots"
Claude Code: [Generates config.yaml] ✅

Researcher: "What's next?"
Claude Code: "Run: python scripts/01_fetch_papers.py --project ..." ❌
              ^^^ Researcher must copy-paste terminal command
```

**Goal**:
```
Researcher (Stage 1): "I want to research AI chatbots"
Claude Code: [Generates config.yaml] ✅
             [Auto-runs: researcherrag init] ✅
             "✅ Stage 1 complete! Ready for Stage 2?" ✅
```

---

## 🏗️ Architecture Design

### Overview Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    ResearcherRAG                        │
└─────────────────────────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │  Tier 1  │    │  Tier 2  │    │  Tier 3  │
    │ Prompts  │    │ .claude/ │    │CLAUDE.md │
    └──────────┘    └──────────┘    └──────────┘
         │               │               │
         │               │               │
         ▼               ▼               ▼
    Researcher      CLI + Claude      Behavior
      Reads           Executes         Guidelines
```

---

## 📊 Tier 1: Prompt Metadata

### Purpose
Human-readable documentation with machine-parseable metadata for stage definition.

### Location
```
prompts/
├── 01_research_domain_setup.md
├── 02_query_strategy.md
├── ...
└── 07_documentation_writing.md
```

### Example
```markdown
<!-- METADATA
stage: 1
stage_name: "Research Domain Setup"
stage_goal: "Define research scope and validate feasibility"
expected_duration: "15-20 minutes"
cli_commands:
  - command: "researcherrag init"
    when: "After conversation completes"
    auto_execute: true
validation_rules:
  research_question:
    required: true
    min_length: 20
-->

# Stage 1: Research Domain Setup

[Prompt content for researchers...]
```

### Responsibilities
- ✅ Document expected conversation flow
- ✅ Define validation rules
- ✅ Specify stage outputs
- ✅ Provide divergence handling patterns
- ❌ **NOT** for runtime state tracking
- ❌ **NOT** for CLI execution logic

### Current Status
**✅ Already exists** - prompts have complete metadata blocks (as of v1.0.4+)

---

## 📊 Tier 2: `.claude/` Configuration

### Purpose
Machine-first configuration for CLI automation and Claude Code integration.

### Location
```
.claude/
├── stages.yaml       # Stage definitions + commands
└── context.json      # Runtime state tracking
```

### File 1: `stages.yaml`

**Purpose**: Stage execution configuration (single source of truth)

```yaml
# ResearcherRAG Stage Configuration
version: "1.0"

stages:
  1:
    name: "Research Domain Setup"
    prompt_file: "prompts/01_research_domain_setup.md"
    duration: "15-20 min"
    cli_command: "researcherrag init"
    auto_execute: true
    prerequisites: []
    outputs:
      - "config.yaml"
      - "projects/{project_name}/README.md"
    validation:
      - research_question: "required, min 20 chars"

  2:
    name: "Query Strategy Design"
    prompt_file: "prompts/02_query_strategy.md"
    cli_command: "python scripts/01_fetch_papers.py --project {project_name}"
    auto_execute: false  # Requires approval
    prerequisites:
      - stage: 1
        files: ["config.yaml"]
    # ... rest

# Divergence rules
divergence_rules:
  - pattern: "pdf|download"
    current_stage: [1, 2, 3]
    redirect: "PDF download happens in Stage 4"
```

**Design Rationale**:
- ✅ Single file (70 lines) vs. 7 prompt files (2,000+ lines)
- ✅ Easy for CLI to parse (YAML)
- ✅ Easy to maintain (one place to update commands)
- ✅ Version-controlled alongside code

### File 2: `context.json`

**Purpose**: Runtime state tracking (auto-generated, not version-controlled)

```json
{
  "project": {
    "name": "AI-Chatbots-Language-Learning",
    "created": "2025-10-14T10:30:00Z"
  },
  "current_stage": {
    "stage": 2,
    "name": "Query Strategy Design",
    "status": "in_progress"
  },
  "completed_stages": [
    {
      "stage": 1,
      "completed_at": "2025-10-14T10:42:00Z",
      "outputs": ["config.yaml"]
    }
  ],
  "checkpoints": {
    "last_command": "researcherrag init",
    "ready_for_next_stage": true
  }
}
```

**Design Rationale**:
- ✅ Lightweight (JSON, ~100 lines max)
- ✅ Auto-updated by CLI after each stage
- ✅ Claude Code reads to know current state
- ✅ Enables "Where am I?" queries

### Responsibilities
- ✅ Define stage execution order
- ✅ Map stages to CLI commands
- ✅ Track current progress
- ✅ Validate prerequisites
- ✅ Detect divergence patterns
- ❌ **NOT** for human-readable documentation (use Tier 1)
- ❌ **NOT** for Claude behavior guidelines (use Tier 3)

---

## 📊 Tier 3: CLAUDE.md

### Purpose
Behavior guidelines for Claude Code (how to act, not what to execute).

### Location
```
CLAUDE.md  (repository root)
```

### Example
```markdown
# ResearcherRAG: Prompt-Driven Systematic Review Assistant

## Core Philosophy

1. **You are stage-aware**: Read `.claude/context.json` to know current stage
2. **You auto-execute**: Run commands from `.claude/stages.yaml` when appropriate
3. **You enforce protocol**: Use divergence rules to keep conversations on track

## Stage-Aware Behavior

When researcher pastes a prompt:

1. **Detect stage** from prompt metadata or `.claude/context.json`
2. **Load stage config** from `.claude/stages.yaml`
3. **Follow conversation flow** from `prompts/{stage}.md`
4. **Validate outputs** against stage validation rules
5. **Auto-execute** if `auto_execute: true`
6. **Update context** after completion

## Divergence Handling

IF user asks about PDFs in Stage 1-3:
  → "PDF download happens in Stage 4. Let's complete current stage first."

IF user asks off-topic:
  → Check `.claude/stages.yaml` divergence_rules
  → Redirect gracefully

## Auto-Execution Rules

**Safe to auto-execute** (no approval needed):
- Stage 1: `researcherrag init` (creates folders only)

**Requires approval** (API costs or external calls):
- Stage 2: `scripts/01_fetch_papers.py` (API calls)
- Stage 3: `scripts/02_screen_papers.py` (Claude API)
- Stage 4+: All other scripts

ALWAYS ask: "Ready to execute? This will [cost/time estimate]"
```

### Responsibilities
- ✅ Define Claude Code's personality
- ✅ Explain stage-awareness logic
- ✅ Provide conversation patterns
- ✅ Set auto-execution policies
- ❌ **NOT** for stage definitions (use Tier 2)
- ❌ **NOT** for researcher documentation (use Tier 1)

---

## 🔄 How Tiers Interact

### Example: Stage 1 → Stage 2 Transition

**Step 1: Researcher Pastes Prompt**
```
USER: [Pastes content from prompts/01_research_domain_setup.md]
```

**Step 2: Claude Reads Tier 1 (Prompt)**
```python
# Claude parses prompt metadata
metadata = parse_prompt_metadata("prompts/01_research_domain_setup.md")
# metadata.stage = 1
# metadata.expected_duration = "15-20 min"
```

**Step 3: Claude Reads Tier 2 (Config)**
```python
# Claude loads execution config
stage_config = load_stages_yaml(".claude/stages.yaml")
# stage_config[1].cli_command = "researcherrag init"
# stage_config[1].auto_execute = true

# Claude checks current state
context = load_context(".claude/context.json")
# context.current_stage = 1 (or None if first run)
```

**Step 4: Claude Follows Tier 3 (Behavior)**
```python
# CLAUDE.md says: "Conduct conversation, then auto-execute Stage 1"
conduct_conversation()  # 4-8 turns
generate_config_yaml()  # Output file
validate_outputs()      # Check requirements

if stage_config[1].auto_execute:
    run_command("researcherrag init")  # Auto-run!
    update_context(stage=1, status="completed")  # Save state
```

**Step 5: Claude Prompts Next Stage**
```
CLAUDE: ✅ Stage 1 complete!

        📁 Created:
        - config.yaml
        - projects/2025-10-14_AI-Chatbots/

        🎯 Next: Stage 2 (Query Strategy Design)
        Ready to continue? I can show you the Stage 2 prompt.
```

**Step 6: Researcher Continues**
```
USER: Yes, let's continue

CLAUDE: [Loads prompts/02_query_strategy.md]
        [Reads .claude/stages.yaml for Stage 2 config]
        [Sees Stage 1 is completed in context.json] ✅
        [Begins Stage 2 conversation...]
```

---

## ✅ Benefits of This Architecture

### 1. Single Source of Truth
```
Stage execution logic: .claude/stages.yaml (one file, 70 lines)
vs.
Old approach: Duplicate in each prompt (7 files × 50 lines = 350 lines)
```

### 2. Clear Separation of Concerns

| Tier | Audience | Purpose | Format |
|------|----------|---------|--------|
| Tier 1 (Prompts) | Researchers | What to discuss | Markdown |
| Tier 2 (.claude/) | CLI + Claude | What to execute | YAML/JSON |
| Tier 3 (CLAUDE.md) | Claude Code | How to behave | Markdown |

### 3. Maintenance Simplicity
```
Update CLI command:
  Before: Edit 7 prompt files
  After: Edit 1 line in stages.yaml
```

### 4. Stage Awareness
```python
# Claude can now answer:
USER: "Where am I?"
CLAUDE: [Reads .claude/context.json]
        "You're in Stage 2 (Query Strategy).
         Stage 1 completed ✅
         Next: Stage 3 (PRISMA Screening)"
```

### 5. Prerequisite Validation
```python
USER: "Can you run Stage 4?"
CLAUDE: [Checks .claude/stages.yaml]
        "❌ Cannot run Stage 4 yet.
         Missing: data/screened_papers.json from Stage 3"
```

### 6. Auto-Execution
```python
# Stage 1 (safe, no API calls)
→ Auto-executes: researcherrag init

# Stage 2 (API calls)
CLAUDE: "Ready to fetch papers from Semantic Scholar?
         This will make ~500 API requests (~5 min).
         Proceed? (yes/no)"
```

---

## 🚧 Implementation Plan

### Phase 1: Foundation (Week 1) ✅

**Deliverables**:
- ✅ `.claude/stages.yaml` created
- ✅ `.claude/context.json.example` template
- ⏳ CLI commands:
  - `researcherrag status`
  - `researcherrag run-stage <N>`
  - `researcherrag next`

**Code Changes**:
```python
# researcherrag_cli.py additions

@cli.command()
def status():
    """Show current stage and progress"""
    context = load_json(".claude/context.json")
    stages = load_yaml(".claude/stages.yaml")

    current = context["current_stage"]["stage"]
    completed = [s["stage"] for s in context["completed_stages"]]

    print(f"📍 Current Stage: {current} - {stages[current]['name']}")
    print(f"✅ Completed: {completed}")
    print(f"➡️  Next: {current + 1} - {stages[current + 1]['name']}")

@cli.command()
@click.argument('stage', type=int)
def run_stage(stage):
    """Execute specific stage with prerequisite validation"""
    stages = load_yaml(".claude/stages.yaml")
    stage_info = stages[stage]

    # Check prerequisites
    for prereq in stage_info.get("prerequisites", []):
        if not check_prerequisite(prereq):
            print(f"❌ Missing: {prereq}")
            return

    # Execute command
    command = stage_info["cli_command"]
    run_command(command)

    # Update context
    update_context(stage, status="completed")
```

---

### Phase 2: Integration (Week 2-3)

**Deliverables**:
- Context auto-update after CLI runs
- CLAUDE.md integration (read `.claude/` files)
- Divergence detection automation
- Prerequisite validation

**CLAUDE.md Addition**:
```markdown
## Reading Configuration

When researcher starts conversation:

```python
# 1. Load stage config
stages = yaml.load(".claude/stages.yaml")

# 2. Check current state
context = json.load(".claude/context.json")
current_stage = context.get("current_stage", {}).get("stage", 1)

# 3. Load prompt
prompt = read_file(stages[current_stage]["prompt_file"])

# 4. Conduct conversation following prompt
# 5. Validate outputs
# 6. Auto-execute if configured
# 7. Update context
```

---

### Phase 3: Advanced Features (Week 4+)

**Deliverables**:
- Automatic checkpoint creation
- Rollback on errors
- Multi-project support
- Dashboard UI (optional)

---

## 📏 Design Decisions & Rationale

### Decision 1: YAML for stages, JSON for context

**Rationale**:
- YAML: Human-editable, comments allowed, better for static config
- JSON: Machine-friendly, standard library support, better for runtime state

**Alternative Considered**: All JSON
**Rejected Because**: YAML more readable for 70-line config file

---

### Decision 2: `.claude/` folder not `.researcherrag/`

**Rationale**:
- `.claude/` is becoming a standard (similar to `.github/`, `.vscode/`)
- Claude Code may auto-recognize `.claude/` in future
- Shorter path

**Alternative Considered**: `.researcherrag/`
**Rejected Because**: Longer, non-standard

---

### Decision 3: Single CLAUDE.md not per-stage files

**Rationale**:
- Codex feedback: Duplication = maintenance nightmare
- Single file = single source of truth
- Stage-specific behavior via `.claude/stages.yaml` lookup

**Alternative Considered**: `CLAUDE_STAGE_1.md`, `CLAUDE_STAGE_2.md`, etc.
**Rejected Because**: 7 files to maintain, version conflicts likely

---

### Decision 4: Metadata stays in prompts

**Rationale**:
- Prompts are primary interface for researchers
- Metadata provides context when reading prompts
- Backward compatibility (existing prompts already have metadata)

**Alternative Considered**: Remove metadata from prompts
**Rejected Because**: Breaks researcher experience

---

## 🔄 Migration Path

### For Existing Projects

**No Breaking Changes!**
- Old workflow still works (manual script execution)
- New features are additive

**To Opt-In**:
```bash
cd my-project
researcherrag upgrade  # Adds .claude/ folder
```

---

## 📊 Success Metrics

### Quantitative
- **Completion Rate**: 80% of users complete all 7 stages (vs. 40% before)
- **Time to Stage 3**: <2 hours (vs. 4+ hours before)
- **Terminal Usage**: <5% of users run scripts manually (vs. 100% before)

### Qualitative
- "I didn't touch the terminal once!"
- "Claude knew exactly where I was in the process"
- "Conversation stayed on track"

---

## 🔗 Related Documents

- [Prompt-Script Integration Plan](./prompt-script-integration-plan.md) - Original vision
- [CLAUDE.md](../CLAUDE.md) - Claude Code behavior guidelines
- [.claude/stages.yaml](../.claude/stages.yaml) - Stage configuration

---

## 📝 Changelog

### 2025-10-14: Initial Design (v1.0.6)
- Created 3-Tier Architecture
- Defined `.claude/` folder structure
- Specified Tier responsibilities
- Approved for implementation

---

**Status**: ✅ Approved - Implementation in Progress
**Target Release**: v1.0.6 (2025-10-21)
**Assigned**: Claude Code Implementation Team
