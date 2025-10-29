# ScholaRAG v1.1.5 Release Notes

**Release Date**: 2025-10-29
**Type**: Documentation Clarification (Minor Update)
**Status**: Stable

---

## 🎯 What's New: PICO-Inspired Framework Clarification

ScholaRAG v1.1.5 clarifies the relationship between our 6-dimension rubric and the PICO framework. This release provides **honest academic positioning** and explains our intentional adaptations for multidisciplinary research.

---

## ⚠️ Critical Clarification

### Previous Claim (v1.1.4)
> "Claude analyzes your research question using the **PICO framework**"

### Corrected Claim (v1.1.5)
> "Claude analyzes your research question using a **PICO-inspired 6-dimension rubric** with intentional adaptations for interdisciplinary research"

**Why this matters:**
- Academic credibility requires honest framework claims
- PICO is a clinical/medical standard with specific meanings
- Our rubric **extends** PICO but does not fully implement it

---

## 📊 PICO Framework: Standard vs. ScholaRAG Adaptation

### Standard PICO (Clinical/Medical Research)

| Dimension | Definition | Example |
|-----------|------------|---------|
| **P**opulation | WHO is being studied? | "Patients with type 2 diabetes aged 40-65" |
| **I**ntervention | WHAT is being tested? | "Metformin 500mg daily" |
| **C**omparison | WHAT is it compared to? | "Placebo" or "Standard care" |
| **O**utcomes | WHAT results are measured? | "HbA1c reduction after 3 months" |

### ScholaRAG Adaptation (Multidisciplinary Research)

| Dimension | PICO Equivalent | ScholaRAG Implementation | Rationale |
|-----------|-----------------|--------------------------|-----------|
| **Domain** | Population | Research field + participant context<br>(e.g., "higher education", "adult learners") | ✨ **Intentional Extension**<br>Abstracts often lack specific demographics;<br>field-level matching enables cross-discipline use |
| **Intervention** | Intervention | Same ✅<br>(e.g., "ChatGPT", "AI chatbot") | Direct match |
| **Method** | ~~Comparison~~ | **Study design rigor**<br>(RCT=5, Survey=3, Case study=2) | ✨ **Intentional Extension**<br>Many papers lack explicit control groups;<br>rigor scoring rewards causal inference quality |
| **Outcomes** | Outcomes | Same ✅<br>(e.g., "speaking proficiency", "learning gains") | Direct match |
| **Exclusion** | N/A | Hard filters<br>(-20 to 0 points) | ✨ **New Dimension**<br>Systematic exclusion of irrelevant contexts |
| **Title Bonus** | N/A | Relevance signal<br>(+10 points) | ✨ **New Dimension**<br>Title-abstract alignment increases confidence |

**Alignment Summary:**
- ✅ **2/4 PICO dimensions** fully aligned (Intervention, Outcomes)
- ✨ **2/4 PICO dimensions** intentionally extended (Domain, Method)
- ➕ **2 new dimensions** added (Exclusion, Title Bonus)
- **Result: 6-dimension PICO-inspired rubric**

---

## 🔍 Why These Adaptations?

### 1. Domain vs. Population

**PICO Population:**
- Requires specific demographics: "undergraduate students aged 18-22"
- Abstracts in education/social science often lack this detail

**ScholaRAG Domain:**
- Matches research field first: "higher education"
- Falls back to participant context when available: "adult learners"
- Enables **multidisciplinary flexibility** without losing population signals

**Example:**
```
Research Question: "How do AI chatbots improve speaking proficiency in EFL learners?"

PICO Population (ideal): "Adult EFL learners aged 18-35 in university settings"
ScholaRAG Domain (practical): "higher education" (field) + "adult EFL learners" (context)

Why? Many abstracts say "university students" without specific ages.
Domain scoring captures both field relevance AND population context.
```

### 2. Method vs. Comparison

**PICO Comparison:**
- Identifies **what was compared**: control group, alternative treatment
- Example: "Group A: ChatGPT tutoring, Group B: human tutoring"

**ScholaRAG Method:**
- Evaluates **study design rigor**: RCT > Survey > Case study
- Example: "RCT with pre-test/post-test" → 5 points

**Why the difference?**
- Many education/social science papers don't explicitly state control groups
- Abstract space is limited; comparisons often implied, not stated
- Rigor scoring ensures high-quality studies pass regardless of comparison structure

**Trade-off:**
- ✅ Captures methodological quality across diverse designs
- ❌ Does not explicitly verify presence of control/comparison groups
- **Decision**: Prioritize rigor over explicit comparison detection for broader applicability

---

## 📈 Impact: What Changed from v1.1.4 → v1.1.5

### Code Changes
- **None** - The 6-dimension rubric was already correctly implemented
- Algorithm, scoring logic, and thresholds remain unchanged

### Documentation Changes
- ✅ Release Notes updated: "PICO framework" → "PICO-inspired 6-dimension rubric"
- ✅ README.md updated: Added "PICO-Inspired Adaptations" section
- ✅ Prompts updated: Clarified intentional extensions
- ✅ Code comments updated: Added "PICO-inspired" labels

### Terminology Clarifications
| Location | Before (v1.1.4) | After (v1.1.5) |
|----------|-----------------|----------------|
| Release Notes | "uses PICO framework" | "uses PICO-inspired 6-dimension rubric" |
| README.md | "Claude interprets using PICO" | "Claude interprets using PICO-inspired rubric with intentional adaptations" |
| scripts/03_screen_papers.py | "based on PICO framework" | "based on PICO-inspired framework (see RELEASE_NOTES_v1.1.5.md)" |

---

## 🎓 Academic Justification

### Why Not Strict PICO?

**Limitations of Standard PICO for Multidisciplinary Research:**
1. **Population specificity**: Clinical PICO requires age/demographics often absent in education/social science abstracts
2. **Comparison detection**: Many quasi-experimental studies lack explicit control group descriptions in 250-word abstracts
3. **Scope narrowness**: PICO is optimized for clinical interventions, not technology adoption, pedagogy, or organizational behavior

**ScholaRAG Design Goals:**
1. Support **any research domain** (education, medicine, psychology, HRM, etc.)
2. Work with **real-world abstracts** (limited space, varied reporting standards)
3. Prioritize **methodological rigor** over strict PICO compliance

**Result:**
- **PICO-inspired** framework balances clinical rigor with practical flexibility
- Adaptations are **intentional and documented**, not accidental mislabeling
- Academic transparency maintained through honest positioning

---

## 🔬 Comparison to Other Frameworks

| Framework | Use Case | Dimensions | ScholaRAG Alignment |
|-----------|----------|------------|---------------------|
| **PICO** | Clinical/medical systematic reviews | 4 (P, I, C, O) | ✨ Inspired, adapted |
| **SPIDER** | Qualitative research synthesis | 5 (S, PI, D, E, R) | Different focus |
| **SPICE** | Social science reviews | 5 (S, P, I, C, E) | Different focus |
| **AI-PRISMA 6D** | Multidisciplinary automated reviews | 6 (D, I, M, O, E, TB) | ScholaRAG's approach |

**ScholaRAG Positioning:**
- Not a replacement for PICO
- Not a competing framework
- **PICO-inspired practical adaptation** for AI-assisted multidisciplinary screening

---

## 🛠️ Migration Guide

### For Users (No Action Required)

**Good news:** No code changes, no config updates needed!
- Your existing projects continue to work identically
- Screening algorithm unchanged
- Thresholds unchanged (90/10 or 50/20)

**What changed:** Only documentation terminology
- Release notes now say "PICO-inspired"
- README clarifies adaptations
- Academic honesty improved

### For Researchers Citing ScholaRAG

**Before (v1.1.4):**
> "We used ScholaRAG's PICO framework-based screening..."

**After (v1.1.5):**
> "We used ScholaRAG's PICO-inspired 6-dimension rubric (Domain, Intervention, Method, Outcomes, Exclusion, Title Bonus) for automated screening. The rubric adapts PICO for multidisciplinary research by extending Population → Domain (field + context) and Comparison → Method (study rigor)."

**Citation Recommendation:**
```bibtex
@software{scholarag2025,
  title = {ScholaRAG: Template-Free AI-PRISMA Systematic Review Automation},
  author = {You, Hosung},
  year = {2025},
  version = {1.1.5},
  note = {Uses PICO-inspired 6-dimension rubric with adaptations for multidisciplinary research},
  url = {https://github.com/HosungYou/ScholaRAG}
}
```

---

## 📚 Further Reading

### Understanding PICO
- **Cochrane Handbook**: [Formulating the Problem](https://training.cochrane.org/handbook/current/chapter-02)
- **PRISMA 2020**: Population definition guidelines
- **ScholaRAG Documentation**: [PICO Adaptations Explained](docs/pico-adaptations.md)

### Why We Made These Choices
- **Technical Report**: [Multidisciplinary PICO Challenges](docs/technical/pico-challenges.md)
- **Design Decisions**: [Domain vs Population Rationale](docs/technical/domain-rationale.md)
- **Validation Study**: Coming in v1.2.0 (inter-rater reliability analysis)

---

## 🙏 Acknowledgments

Special thanks to:
- **OpenAI Codex** for rigorous conceptual analysis
- **Community feedback** on PICO terminology confusion
- **Academic reviewers** who requested honest framework positioning

---

## 🔄 Next Steps

### v1.1.5 (This Release)
- ✅ Terminology clarifications
- ✅ Academic honesty improvements
- ✅ Documentation alignment

### v1.2.0 (Planned)
- 📊 Inter-rater reliability study (human vs. AI screening)
- 📈 Validation metrics for Domain/Method adaptations
- 📝 Academic paper submission

### Future Considerations
- 🔬 Optional 7th dimension: Explicit Comparison detection
- 🎯 Domain-specific rubric variations (medicine vs. education)
- 🤖 User-customizable dimension weights

---

## ❓ FAQ

### Q: Is ScholaRAG still valid for systematic reviews?
**A:** Yes! PICO-inspired adaptations are **intentional improvements** for multidisciplinary research. The rubric maintains:
- ✅ PRISMA 2020 compliance (screening, eligibility, inclusion)
- ✅ Evidence-based scoring (direct quotes required)
- ✅ Transparent decision logic (confidence thresholds)
- ✅ Human validation support (when required)

### Q: Should I use strict PICO instead?
**A:** If your research is:
- Clinical/medical domain
- Explicit control groups expected
- Specific population demographics required
→ Consider supplementing ScholaRAG with manual PICO validation

### Q: Will you add true PICO Comparison dimension?
**A:** We're considering a 7-dimension variant for v1.2.0:
- Keep current 6 dimensions
- Add optional "Comparison" detection (0-5 points)
- User can choose: 6D (flexible) or 7D (PICO-strict)

### Q: Can I still cite ScholaRAG in academic papers?
**A:** Absolutely! The clarified positioning **improves** academic credibility:
- Before: "uses PICO" (overclaim)
- After: "PICO-inspired with documented adaptations" (honest)

---

## 📞 Contact

Questions about PICO adaptations? Discussion: https://github.com/HosungYou/ScholaRAG/discussions

Found terminology issues? Issues: https://github.com/HosungYou/ScholaRAG/issues

---

**Bottom Line:** v1.1.5 doesn't change functionality—it clarifies terminology for academic honesty. Your research remains valid, your results unchanged, your systematic reviews compliant. We simply positioned our innovations correctly: PICO-**inspired**, not PICO-**identical**.
