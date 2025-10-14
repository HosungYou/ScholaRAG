<!-- METADATA
stage: 7
stage_name: "Documentation & Writing"
stage_goal: "Generate PRISMA diagram, write methods section, create bibliography"
expected_duration: "1-3 hours"
conversation_mode: "documentation_generation"
prerequisites:
  - stage: 6
    requirement: "Research insights gathered, conversation logs saved"
outputs:
  - prisma_diagram: "PRISMA 2020 flow diagram (PNG, Mermaid)"
  - methods_section: "Systematic review methods documentation"
  - bibliography: "Formatted citations (APA, Harvard, BibTeX)"
  - supplementary_materials: "Search strategies, screening criteria"
validation_rules:
  prisma_counts_accurate:
    required: true
    validation: "PRISMA diagram numbers must match pipeline outputs"
  citations_formatted:
    required: true
    validation: "Bibliography follows selected citation style"
cli_commands:
  - command: "python scripts/07_generate_prisma.py"
    when: "User ready to create PRISMA diagram"
    auto_execute: true
scripts_triggered:
  - scripts/07_generate_prisma.py
next_stage:
  stage: null
  condition: "All 7 stages complete - systematic review documented"
  prompt_file: null
divergence_handling:
  common_divergences:
    - pattern: "User wants to change PRISMA numbers manually"
      response: "PRISMA numbers must reflect actual pipeline results for reproducibility. If you need different numbers, re-run pipeline with adjusted thresholds."
conversation_flow:
  expected_turns: 3-6
  typical_pattern:
    - turn: 1
      user_action: "Requests PRISMA diagram generation"
      claude_action: "Generate diagram with pipeline statistics"
    - turn: 2-3
      user_action: "Requests methods section draft"
      claude_action: "Generate methods following PRISMA guidelines"
    - turn: 4-5
      user_action: "Requests bibliography formatting"
      claude_action: "Format citations in requested style"
    - turn: "final"
      user_action: "Reviews all documentation"
      claude_action: "Confirm all 7 stages complete, systematic review ready"
validation_checklist:
  - "PRISMA diagram generated with accurate counts"
  - "Methods section drafted following PRISMA 2020"
  - "Bibliography formatted correctly"
  - "Search strategies documented"
  - "Screening criteria clearly stated"
  - "All 7 stages complete"
-->

# Stage 7: Documentation & Writing

**🎯 Your Current Stage**: Stage 7 of 7
**⏱️ Expected Time**: 1-3 hours
**💬 Format**: Documentation generation
**📋 Prerequisites**: Stage 6 completed (research insights gathered)

---

## 🚀 Generate Documentation

Let's document your systematic review:

1. PRISMA flow diagram
2. Methods section
3. Bibliography
4. Search strategies

```bash
python scripts/07_generate_prisma.py
```

---

## 🎯 Stage 7 Success Criteria

✅ PRISMA diagram generated
✅ Methods section drafted
✅ Bibliography formatted
✅ Supplementary materials created
✅ All 7 stages complete

---

## 📍 Your Progress

```
[●●●●●●●] Stage 7/7: Documentation & Writing - COMPLETE!
```

**Congratulations!** Your systematic literature review is complete.

---

**Ready to finish?** Generate your PRISMA diagram and documentation!
