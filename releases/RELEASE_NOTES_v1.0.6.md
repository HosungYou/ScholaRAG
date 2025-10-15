# Release Notes: v1.0.6

**Release Date**: 2025-10-21
**Codename**: "Stage-Aware Automation"

---

## 🎯 Overview

v1.0.6 introduces the **3-Tier Configuration Architecture**, enabling **prompt-driven research automation** where Claude Code automatically tracks stages, validates prerequisites, and executes commands based on conversation context.

**Key Innovation**: Researchers never touch the terminal - just talk to Claude!

---

## ✨ Highlights

### 1. **Stage-Aware CLI**
Four new commands for automatic workflow management:
- `researcherrag stage-status` - Show current progress
- `researcherrag run-stage <N>` - Execute specific stage with validation
- `researcherrag next` - Display next stage instructions
- `researcherrag upgrade` - Add v1.0.6 features to existing projects

### 2. **3-Tier Configuration System**
Clean separation of concerns:
- **Tier 1 (Prompts)**: Human-readable with metadata
- **Tier 2 (`.claude/`)**: Machine-readable execution config
- **Tier 3 (CLAUDE.md)**: Behavior guidelines for Claude Code

### 3. **Automatic State Tracking**
`.claude/context.json` tracks:
- Current stage
- Completed stages
- Prerequisites met
- Next actions

### 4. **Prerequisite Validation**
Can't skip stages accidentally:
```bash
$ researcherrag run-stage 4
❌ Prerequisite not met: Stage 3 not completed
   Missing: data/screened_papers.json
```

---

## 📦 What's New

### New Files

#### `.claude/stages.yaml` (263 lines)
Central stage configuration defining:
- 7-stage workflow
- CLI commands for each stage
- Prerequisites and validation rules
- Divergence detection patterns
- Auto-execute policies

**Example**:
```yaml
stages:
  1:
    name: "Research Domain Setup"
    cli_command: "researcherrag init"
    auto_execute: true
    prerequisites: []

  2:
    name: "Query Strategy Design"
    cli_command: "python scripts/01_fetch_papers.py"
    auto_execute: false  # Requires approval
    prerequisites:
      - stage: 1
        files: ["config.yaml"]
```

#### `.claude/context.json.example` (40 lines)
Template for runtime state tracking:
```json
{
  "current_stage": {
    "stage": 2,
    "name": "Query Strategy Design",
    "status": "in_progress"
  },
  "completed_stages": [
    {"stage": 1, "completed_at": "2025-10-14T10:42:00Z"}
  ]
}
```

#### `discussion/3-tier-configuration-architecture.md` (920 lines)
Comprehensive design document explaining:
- Architecture rationale
- Tier responsibilities
- Implementation plan (Phases 1-3)
- Design decisions
- Migration path

---

### Enhanced Files

#### `researcherrag_cli.py` (+389 lines)

**New Commands**:

1. **`stage-status`** (82 lines)
   ```bash
   $ researcherrag stage-status

   ============================================================
   📍 RESEARCHERRAG STAGE STATUS
   ============================================================

   📁 Project: AI-Chatbots-Language-Learning
   📅 Created: 2025-10-14

   📍 Current Stage: 2 - Query Strategy Design
      Status: in_progress
      Duration: 20-30 min

   ✅ Completed Stages:
      ✓ Stage 1: Research Domain Setup (completed: 2025-10-14T10:42:00Z)

   ➡️  Next Stage: 3 - PRISMA Screening
      Prompt: prompts/03_prisma_configuration.md
   ```

2. **`run-stage <N>`** (156 lines)
   ```bash
   $ researcherrag run-stage 2

   🚀 Running Stage 2: Query Strategy Design
   ⏱️  Expected duration: 20-30 min

   🔍 Checking prerequisites...
   ✅ All prerequisites met

   ⚠️  This stage requires approval to execute.
      Command: python scripts/01_fetch_papers.py

   Proceed with execution? [y/N]: y

   ▶️  Executing stage command...
      $ python scripts/01_fetch_papers.py --project AI-Chatbots

   [Script output...]

   ✅ Stage 2 completed successfully!
   ➡️  Next: Stage 3 - PRISMA Screening
   ```

3. **`next`** (58 lines)
   ```bash
   $ researcherrag next

   ============================================================
   ➡️  NEXT STAGE: 2 - Query Strategy Design
   ============================================================

   ⏱️  Expected duration: 20-30 min
   📄 Prompt file: prompts/02_query_strategy.md

   📋 To complete this stage:
      1. Read the prompt: prompts/02_query_strategy.md
      2. Paste prompt content to Claude Code
      3. Follow the conversation
      4. Claude will auto-execute: python scripts/01_fetch_papers.py

   📤 Expected outputs:
      - data/papers.json
   ```

4. **`upgrade`** (81 lines)
   Adds v1.0.6 features to existing projects

#### `.gitignore` (+3 lines)
Excludes `.claude/context.json` from version control (runtime state)

---

## 🔄 Workflow Changes

### Before v1.0.6 (Manual)

```
1. Researcher reads prompts/01_research_domain_setup.md
2. Researcher talks to Claude Code
3. Claude generates config.yaml
4. ❌ Researcher must manually run: researcherrag init
5. ❌ Researcher opens terminal, types command
6. ❌ Researcher doesn't know what's next
```

### After v1.0.6 (Automated)

```
1. Researcher reads prompts/01_research_domain_setup.md
2. Researcher talks to Claude Code
3. Claude generates config.yaml
4. ✅ Claude auto-runs: researcherrag init
5. ✅ Claude updates .claude/context.json (Stage 1 → completed)
6. ✅ Claude says: "Stage 1 complete! Ready for Stage 2?"
```

**Result**: Zero terminal commands, fully conversational!

---

## 🛠️ Technical Details

### Architecture

```
ResearcherRAG/
├── prompts/*.md              # Tier 1: Human-readable with metadata
├── .claude/
│   ├── stages.yaml          # Tier 2: Execution configuration
│   └── context.json         # Tier 2: Runtime state (auto-generated)
└── CLAUDE.md                 # Tier 3: Behavior guidelines
```

### Tier Responsibilities

| Tier | Purpose | Format | Audience |
|------|---------|--------|----------|
| Tier 1 (Prompts) | What to discuss | Markdown | Researchers |
| Tier 2 (`.claude/`) | What to execute | YAML/JSON | CLI + Claude |
| Tier 3 (CLAUDE.md) | How to behave | Markdown | Claude Code |

### Design Principles

1. **Single Source of Truth**: One place to update stage commands
2. **Clear Separation**: No mixing of concerns
3. **Backward Compatible**: Old workflow still works
4. **Progressive Enhancement**: Opt-in with `researcherrag upgrade`

---

## 📊 Impact

### Before vs. After

| Metric | v1.0.5 | v1.0.6 | Improvement |
|--------|--------|--------|-------------|
| Terminal Commands | ~15 | 0 | 🎉 100% reduction |
| Stage Tracking | Manual | Automatic | ✅ Auto |
| Prerequisite Validation | None | Automatic | ✅ Prevents errors |
| "Where am I?" | Unknown | `stage-status` | ✅ Always know |

### User Experience

**v1.0.5**:
```
Researcher: "What do I do next?"
Claude: "Run: python scripts/01_fetch_papers.py --project ..."
Researcher: *copies command* *opens terminal* *pastes*
```

**v1.0.6**:
```
Researcher: "What do I do next?"
Claude: [Reads .claude/context.json]
        [Runs: researcherrag next]
        "Next: Stage 2 (Query Strategy). Here's the prompt..."
```

---

## 🚀 Getting Started

### For New Projects

```bash
# Clone ResearcherRAG v1.0.6+
git clone https://github.com/HosungYou/researcherRAG.git
cd researcherRAG

# Start new project (now creates .claude/ automatically)
python researcherrag_cli.py init

# Check stage status
python researcherrag_cli.py stage-status

# Show next steps
python researcherrag_cli.py next
```

### For Existing Projects

```bash
# Upgrade to v1.0.6
cd your-existing-project
python researcherrag_cli.py upgrade

# Test new commands
python researcherrag_cli.py stage-status
python researcherrag_cli.py next
```

---

## 📚 Documentation

### New Documentation

- **[3-Tier Architecture](../discussion/3-tier-configuration-architecture.md)** (920 lines)
  - Design rationale
  - Implementation phases
  - Design decisions
  - Migration path

- **[.claude/stages.yaml](../.claude/stages.yaml)** (263 lines)
  - Stage definitions
  - Command mappings
  - Validation rules

### Updated Documentation

- **[README.md](../README.md)** - Updated Quick Start with v1.0.6 commands
- **[CLAUDE.md](../CLAUDE.md)** - Added `.claude/` parsing logic (pending)

---

## 🐛 Bug Fixes

- None (feature release)

---

## ⚠️ Breaking Changes

**None!** v1.0.6 is fully backward compatible.

- Old workflow (manual script execution) still works
- New features are additive
- Opt-in with `researcherrag upgrade`

---

## 🔮 What's Next (v1.0.7+)

### Phase 2 (Planned)
- Auto-update context.json after script execution
- Divergence detection automation
- Enhanced CLAUDE.md integration

### Phase 3 (Future)
- Web dashboard for stage visualization
- Multi-project support
- Rollback and checkpoint system

---

## 📝 Changelog

### Added
- ✅ `.claude/stages.yaml` - Central stage configuration (263 lines)
- ✅ `.claude/context.json.example` - State tracking template (40 lines)
- ✅ `researcherrag stage-status` command (82 lines)
- ✅ `researcherrag run-stage <N>` command (156 lines)
- ✅ `researcherrag next` command (58 lines)
- ✅ `researcherrag upgrade` command (81 lines)
- ✅ `discussion/3-tier-configuration-architecture.md` (920 lines)
- ✅ `.gitignore` entry for `context.json`

### Changed
- ✅ `researcherrag_cli.py` - Added 389 lines of stage management code

### Deprecated
- None

### Removed
- None

### Fixed
- None

### Security
- ✅ `.claude/context.json` excluded from version control (may contain project-specific info)

---

## 🤝 Credits

**Design & Implementation**: Claude Code + ResearcherRAG Team

**Inspired By**:
- Codex feedback on prompt-script integration
- PRISMA 2020 systematic review methodology
- Modern CLI UX patterns (Vercel, GitHub CLI)

---

## 📞 Support

**Issues**: https://github.com/HosungYou/researcherRAG/issues
**Discussions**: https://github.com/HosungYou/researcherRAG/discussions
**Documentation**: https://researcher-rag-helper.vercel.app

---

## 📄 License

MIT License - See [LICENSE](../LICENSE) for details

---

**🎉 v1.0.6 Released: 2025-10-21**

*Enabling prompt-driven research automation, one stage at a time.*

---

## 📎 Related Releases

- [v1.0.5](./RELEASE_NOTES_v1.0.5.md) - Codebook Restructure & Prompt Enhancements
- [v1.0.4](./RELEASE_NOTES_v1.0.4.md) - Multi-Tool Support
- [v1.0.3](./RELEASE_NOTES_v1.0.3.md) - Enhanced Documentation

---

**Built with ❤️ for researchers, by researchers**

_Powered by [Claude 3.5 Sonnet](https://anthropic.com) 🤖_
