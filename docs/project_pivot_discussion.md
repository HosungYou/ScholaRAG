# Project Pivot Discussion: From Web Service to Workshop Materials

**Date**: 2025-10-11
**Participants**: Project Lead, Claude Code
**Outcome**: Major pivot from web-based RAG service to VS Code + Claude Code workshop materials

---

## Initial Misunderstanding

### What Claude Initially Thought (❌ Wrong)
```
연구자 → 웹 UI → Backend API → 자동 코드 생성 → 다운로드 → 로컬 실행
         (별도 웹사이트)
```

**Assumed Features**:
- Web frontend (Next.js) with chat interface
- Backend API (FastAPI) that generates code
- Pre-populated RAG system that answers "10 topics, 1,234 papers"
- GitHub auto-repository creation
- Cloud execution of PDF downloads

**Problem**: This approach doesn't make sense because:
1. PDF downloads require local file system access
2. Python script execution needs terminal/IDE
3. Vector DB storage is local
4. Researchers work in IDE environments, not web browsers

---

## Actual Project Intent (✅ Correct)

### What the Project Really Is
```
연구자 → VS Code → Claude Code → 대화형 구축 → 터미널 실행 → RAG 완성
         (IDE 내에서 모든 것 해결)
```

**Core Purpose**:
> "Help researchers build their own RAG systems through conversational interaction with Claude Code in VS Code"

**Not a Service, but an Assistant**:
- **Not**: "RAG-as-a-Service" (AI provides answers from pre-built system)
- **Is**: "RAG Setup Assistant" (AI helps researcher build their own system)

**Analogy**:
- ❌ Restaurant (AI serves food)
- ✅ Cooking instructor (AI teaches you to cook)

---

## Key Insights from Discussion

### 1. Workflow Sequence Correction

**Wrong Sequence** (Claude's initial assumption):
```
User: "AI in education"
  ↓
AI: "Found 10 topics with 1,234 papers" ← Where did this data come from?!
  ↓
[Magic happens]
  ↓
RAG system ready
```

**Correct Sequence**:
```
1. User: "I want to study AI in education"
2. AI: "Let's design search queries together" [Conversation]
3. Semantic Scholar API call → Collect 568 papers
4. AI: "Let's build PRISMA profile" [Conversation]
5. research_profile.yaml generated
6. PDF download + text extraction
7. Vector DB created
8. Now RAG queries are possible
```

**Key Difference**: No data exists until User and AI work together to collect it.

---

### 2. Workshop Context

**Target Audience**: Academic researchers (not developers)
- Education, Medicine, Psychology, Economics, Social Sciences
- May have limited programming experience
- Need step-by-step guidance
- Want to learn, not just receive results

**Workshop Format** (3 hours):
1. Introduction (30 min): Demo of complete RAG workflow
2. Hands-on (90 min): Build your own RAG with guidance
3. Advanced Topics (30 min): Troubleshooting, multi-project management
4. Wrap-up (30 min): Resources, homework, Q&A

**Deliverables for Participants**:
- Functional RAG system for their research topic
- Understanding of PRISMA systematic review
- Ability to adapt the system for future projects
- Templates and documentation for self-study

---

### 3. Frontend Role Clarification

**Question**: "그런데 웹으로 가능한가? IDE 등을 통해서만 가능하지 않니?"

**Answer**: Correct! Web frontend is **optional demo only**.

**What's NOT Possible in Web Browser**:
- File system access for PDF downloads
- Terminal command execution
- Local vector DB storage (ChromaDB files)
- Git operations
- Python script execution

**What Web Can Do** (limited scope):
- Show demo of completed RAG system
- Preview PRISMA flow diagrams
- Display sample queries and answers
- Visualize knowledge graphs

**Conclusion**:
- Primary workflow = VS Code + Claude Code
- Web frontend = Optional demo for workshop introduction only

---

## Project Goals (Clarified)

### Primary Goal
Build comprehensive **educational materials** that enable researchers to:
1. Learn RAG concepts through conversation
2. Build customized RAG systems for their research
3. Understand PRISMA systematic review methodology
4. Troubleshoot and adapt systems independently

### Secondary Goal
Create **reusable templates** that:
1. Work across different research domains (Education, Medicine, etc.)
2. Can be customized through simple YAML configs
3. Don't require deep programming knowledge
4. Follow academic research best practices

### Non-Goal
- Building a commercial RAG service
- Providing pre-built RAG systems
- Automating the entire research process
- Replacing human research judgment

---

## Key Design Decisions

### Decision 1: Conversation-Driven Setup

**Rationale**: Researchers don't know how to configure RAG systems upfront.

**Approach**: 5-stage conversational workflow
1. Research Domain Setup (define scope)
2. Query Strategy Design (build search queries)
3. PRISMA Configuration (screen papers)
4. RAG System Design (configure retrieval/generation)
5. Execution & Deployment (run scripts)

**Implementation**: Prompt templates that researchers copy-paste to Claude Code

---

### Decision 2: YAML Over Code

**Rationale**: Researchers are more comfortable with configuration files than Python.

**Approach**:
```yaml
# research_profile.yaml (readable, editable)
domain_keywords:
  - language learning: 10
  - higher education: 7

thresholds:
  screening: 25
  eligibility: 45
```

vs.

```python
# config.py (intimidating for non-programmers)
DOMAIN_WEIGHTS = {"language learning": 10, "higher education": 7}
SCREENING_THRESHOLD = 25
```

**Benefit**: Researchers can adjust configs without touching code.

---

### Decision 3: Realistic Expectations

**PDF Download Reality** (from AI failure_HR):
- Target: 592 papers
- Success: 316 PDFs (53.4%)
- Reasons: Paywalls, institutional access, broken links

**Our Approach**:
1. **Warn upfront** about realistic success rates
2. **Provide fallbacks**: Unpaywall, OpenAlex, abstracts
3. **Offer alternatives**: Author contact templates, preprints
4. **Accept incompleteness**: 50-60% is normal and acceptable

**Anti-pattern**: Overpromising "we'll download everything automatically"

---

### Decision 4: Multi-Source Data Collection

**Single Source (e.g., Semantic Scholar only)**:
- Pros: Simpler, consistent API
- Cons: Limited coverage, single point of failure

**Multi-Source Waterfall**:
```
Tier 1: Semantic Scholar (primary, 60% coverage)
  ↓
Tier 2: OpenAlex (metadata backup, 30% coverage)
  ↓
Tier 3: arXiv (full-text preprints, 10% coverage)
```

**Implementation**: Scripts try sources sequentially, merge results

---

## What Changed in v1.1.0

### Added
1. **CLAUDE_FOR_RESEARCHERS.md**: Comprehensive guide for Claude Code (18,000 words)
2. **Prompt Templates** (5 stages): Copy-paste prompts for each workflow stage
3. **Workshop Guide**: 3-hour hands-on workshop structure with exercises
4. **Conversation Examples**: Sample dialogues showing how to interact with Claude
5. **Troubleshooting Section**: Common issues and solutions
6. **Multi-Project Management**: Guide for handling multiple research projects

### Changed
1. **Project Focus**: Web service → Educational materials for VS Code + Claude Code
2. **User Journey**: API calls → Conversational setup with AI guidance
3. **Deliverable**: Hosted RAG → Local RAG built by researcher
4. **Documentation**: Technical API docs → Step-by-step learning materials

### Removed
1. Web frontend plans (Next.js, tRPC) - moved to "optional demo" status
2. Backend API for code generation - replaced with Claude Code conversation
3. GitHub auto-repository creation - researchers manage their own repos
4. Cloud execution - all execution is local in terminal

---

## Open Questions & Future Decisions

### Q1: Sample Data for Workshop
**Question**: Should we provide pre-downloaded PDFs for workshop participants?
**Options**:
- A: Yes, 50 sample papers per domain (faster, no download issues)
- B: No, participants download their own (realistic but slow)
- C: Hybrid: Demo uses samples, homework uses real downloads

**Decision**: TBD (depends on workshop duration and internet reliability)

---

### Q2: Web Frontend Scope
**Question**: How much web frontend should we build?
**Options**:
- A: None (pure VS Code workflow)
- B: Demo only (show completed RAG, read-only)
- C: Setup wizard (help design configs, then export to VS Code)

**Current Stance**: B (demo only) is sufficient for workshop introduction

---

### Q3: Advanced Features Priority
**Question**: Which advanced features to include in v1.1.0?
**Candidates**:
1. Citation graph analysis
2. Temporal trend analysis
3. Multi-lingual RAG (Korean, Chinese, Spanish)
4. Automated effect size extraction
5. Cross-project comparative queries

**Decision**: Document in "Future Enhancements" section, don't implement yet

---

### Q4: Code Template Complexity
**Question**: How much customization should templates support?
**Options**:
- A: Minimal (3 templates: Education, Medicine, Social Science)
- B: Moderate (10 templates covering major fields)
- C: Maximum (Template generator that creates custom templates)

**Decision**: Start with A (minimal), expand based on user feedback

---

## Success Metrics for v1.1.0

### Workshop Success
- ✅ 80%+ participants complete hands-on exercises
- ✅ 60%+ participants build working RAG system
- ✅ Positive feedback on clarity of instructions

### Post-Workshop Success
- ✅ 50%+ participants complete homework (full RAG with their data)
- ✅ Active forum discussions (troubleshooting, tips)
- ✅ <5 critical bugs reported in first month

### Long-Term Success
- ✅ 10+ published papers using this methodology
- ✅ Adoption by other research groups
- ✅ Community contributions (new templates, scripts)

---

## Next Steps (Immediate)

1. ✅ Document this discussion (this file)
2. ⏳ Restructure repository (new folder organization)
3. ⏳ Complete remaining prompt templates (Stage 3-5)
4. ⏳ Create code templates (Education, Medicine, Social Science)
5. ⏳ Write Release Note v1.1.0
6. ⏳ Update README.md with new project focus
7. ⏳ Create TODO management system
8. ⏳ Clean up obsolete files

---

## Lessons Learned

### Communication
- Always clarify **user environment** (web vs. IDE) early
- Ask about **intended use case** (service vs. tool vs. education)
- Verify **technical constraints** (file system, API access, execution)

### Design
- **Start with user workflow**, not technical architecture
- **Realistic expectations** beat overpromising
- **Conversation-driven** beats form-based for complex tasks

### Education
- **Show, then teach** (demo first, theory second)
- **Hands-on immediately** (don't lecture for 1 hour)
- **Celebrate small wins** (each stage completion)

---

**Document Version**: 1.0
**Last Updated**: 2025-10-11
**Status**: Approved, proceeding with v1.1.0 development
