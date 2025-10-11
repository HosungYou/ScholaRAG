# ResearcherRAG TODO List

**Last Updated**: 2025-10-11
**Current Version**: v1.1.0 (in development)

---

## 🔥 High Priority (Complete for v1.1.0 Release)

### Documentation
- [ ] Write Release Note v1.1.0 (major pivot to workshop focus)
- [ ] Update README.md (workshop-centric overview)
- [ ] Update QUICK_START.md (workshop workflow)
- [ ] Create docs/FAQ.md (common researcher questions)
- [ ] Create docs/workshop_planning.md (logistics, timeline)

### Prompt Templates (Stage 3-5)
- [ ] `prompts/03_prisma_configuration.md` - PRISMA setup guide
- [ ] `prompts/04_rag_design.md` - RAG configuration guide
- [ ] `prompts/05_execution_plan.md` - Execution and troubleshooting

### Code Templates
- [ ] `templates/scripts/1_collect_papers_template.py`
- [ ] `templates/scripts/2_run_prisma_template.py`
- [ ] `templates/scripts/3_download_pdfs_template.py`
- [ ] `templates/scripts/4_extract_text_template.py`
- [ ] `templates/scripts/5_build_vectordb_template.py`
- [ ] `templates/scripts/6_query_rag_template.py`

### Research Profile Templates
- [ ] `templates/research_profiles/education_template.yaml`
- [ ] `templates/research_profiles/medicine_template.yaml`
- [ ] `templates/research_profiles/social_science_template.yaml`

### Example Project
- [ ] `examples/ai_education_chatbot/README.md`
- [ ] `examples/ai_education_chatbot/conversation_log.md`
- [ ] `examples/ai_education_chatbot/config/research_profile.yaml`
- [ ] `examples/ai_education_chatbot/scripts/*.py` (all 6 scripts)

---

## 📅 Medium Priority (v1.2.0 or later)

### Bookdown Documentation Site 📚 NEW!
- [ ] Set up Bookdown project structure (docs_site/)
- [ ] Convert Chapters 1-5 (Getting Started, RAG Fundamentals, PRISMA, Research Scope, Search Queries)
- [ ] Convert Chapters 6-8 (PRISMA Config, Vector DB, RAG Prompts)
- [ ] Convert Chapters 9-14 (Troubleshooting, Multi-project, Advanced, Workshop, Templates, Community)
- [ ] Add diagrams and screenshots
- [ ] Custom CSS styling (match reference: https://bookdown.org/MathiasHarrer/Doing_Meta_Analysis_in_R/)
- [ ] Set up GitHub Pages deployment
- [ ] Test all code examples in documentation
- [ ] PDF export functionality

**Estimate**: 2.5 weeks (20-25 hours)
**Target**: v1.2.0 release (2025-11-15)
**Reference**: See `docs/bookdown_documentation_plan.md`

### Workshop Materials
- [ ] `workshop/slides.pdf` - Presentation slides
- [ ] `workshop/sample_data/50_sample_papers.zip` - Demo dataset
- [ ] `workshop/exercises/exercise_1_query_design.md`
- [ ] `workshop/exercises/exercise_2_prisma_config.md`
- [ ] `workshop/exercises/exercise_3_rag_query.md`

### Additional Examples
- [ ] `examples/medical_ehr_workflow/` - Complete medical research example
- [ ] `examples/psychology_intervention/` - Psychology research example
- [ ] `examples/economics_policy/` - Economics research example

### Advanced Features
- [ ] Citation graph analysis module
- [ ] Temporal trend analysis
- [ ] Cross-lingual RAG (Korean, Chinese, Spanish)
- [ ] Automated effect size extraction
- [ ] Multi-project comparative queries

---

## 🔮 Low Priority (Future Enhancements)

### Web Frontend (Optional Demo)
- [ ] Simple Gradio interface for workshop demo
- [ ] Read-only query interface (pre-built RAG)
- [ ] PRISMA flow diagram visualizer
- [ ] Knowledge graph interactive viewer

### Advanced Documentation
- [ ] Video tutorial series (YouTube)
- [ ] Research methodology best practices guide
- [ ] Integration with reference managers (Zotero, Mendeley)
- [ ] API documentation (for programmatic access)

### Community Features
- [ ] Template contribution guidelines
- [ ] Community forum setup (Discord/Slack)
- [ ] User showcase (published papers using this tool)
- [ ] Certification program for workshop completion

---

## ✅ Completed (v1.1.0)

- [x] Document project pivot discussion
- [x] Create new folder structure plan
- [x] Archive obsolete files (frontend plans, old modules, duplicate docs)
- [x] Reorganize core code into `/backend/` structure
- [x] Move research profiles to `/templates/`
- [x] Rename `CLAUDE_FOR_RESEARCHERS.md` to `CLAUDE.md`
- [x] Create CLAUDE.md (comprehensive guide for Claude Code)
- [x] Create `prompts/01_research_domain_setup.md`
- [x] Create `prompts/02_query_strategy.md`
- [x] Create `workshop/hands_on_guide.md` (3-hour workshop structure)
- [x] Create project management structure (this file)

---

## 📝 Notes

### v1.1.0 Release Criteria
**Must have before release**:
- All High Priority items completed
- At least 1 complete example project
- Release note written and reviewed
- README and QUICK_START updated

**Can defer to v1.2.0**:
- Workshop slides (can use simple bullet points initially)
- Sample data (can use AI failure_HR subset)
- Additional example projects (1 is sufficient for launch)

### Workshop Schedule
- **Target Date**: TBD (to be determined by project lead)
- **Duration**: 3 hours
- **Format**: Hands-on (bring your own research topic)
- **Prerequisites**: VS Code + Claude Code installed

### Known Issues
- Need to test all templates with actual researchers
- PDF download success rate varies by institution
- Some academic databases require VPN access

### Questions to Resolve
1. ~~Should web frontend be included in v1.1.0, or defer to v1.2.0?~~ **RESOLVED**: Defer to v1.2.0 as Bookdown documentation site
2. How many example projects are sufficient (1, 3, or 5)? **Current stance**: 1 for v1.1.0, expand to 3 in v1.2.0
3. What format for workshop slides (PDF, Google Slides, reveal.js)? **Resolved for now**: Simple PDF, enhance in v1.2.0
4. Should we create video tutorials before or after first workshop? **Resolved**: After first workshop (capture live workshop as recordings)
5. **NEW**: Bookdown vs. MkDocs vs. Quarto? **Resolved**: Bookdown (R-based, matches reference site)

---

## 🤝 Contributing

If you're contributing to this project:
1. Pick an item from High Priority
2. Create a branch: `git checkout -b feature/[todo-item]`
3. Complete the task
4. Update this TODO.md (move item to "Completed")
5. Create pull request

---

**Document Version**: 1.0
**Maintained By**: Project Lead
**Review Frequency**: Weekly (every Friday)
