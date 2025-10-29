# ScholaRAG v1.1.6 Release Notes

**Release Date**: 2025-10-29
**Type**: Academic Positioning (Documentation Update)
**Status**: Stable

---

## 🎯 What's New: Scholarly-Grounded Framework Positioning

ScholaRAG v1.1.6 provides **comprehensive academic justification** for our 6-dimension rubric by mapping it to established evidence-synthesis frameworks. This release positions ScholaRAG as a **PICOC+S-derived, automation-aware framework** with full scholarly citations.

---

## 📚 Academic Lineage of ScholaRAG's 6-Dimension Rubric

### Framework Positioning

**Previous (v1.1.5):** "PICO-inspired 6-dimension rubric"
**Current (v1.1.6):** "PICOC+S-derived relevance scoring with automation-aware prioritisation"

**What this means:**
- **PICOC**: Context-sensitive variant for social sciences (Booth et al., 2012)
- **+S**: Study design rigor from PICOS (Higgins et al., 2022)
- **Automation-aware**: Text-mining insights from systematic review automation (O'Mara-Eves et al., 2015)

### Complete Academic Lineage Table

| ScholaRAG Dimension | Established Framework Elements | Key Citations | Scholarly Precedent |
|---------------------|--------------------------------|---------------|---------------------|
| **Domain** (0-10) | • PICOC: Context<br>• SPICE: Setting/Perspective<br>• PICo: Context | Booth et al., 2012<br>Lockwood et al., 2015 | ✅ **Direct precedent**: Context-enriched formulations require articulating setting and stakeholder perspective alongside population |
| **Intervention** (0-10) | • PICO: Intervention<br>• SPIDER: Phenomenon<br>• PICo: Interest | Richardson et al., 1995<br>Cooke et al., 2012 | ✅ **Direct precedent**: Intervention remains lynchpin of clinical and social inquiry across all variants |
| **Method** (0-5) | • PICOS: Study design<br>• SPIDER: Design<br>• Cochrane: Risk-of-bias | Higgins et al., 2022<br>Cooke et al., 2012 | ✅ **Direct precedent**: PICOS adds study design to prevent mixing incompatible evidence; prioritizes higher-rigor studies |
| **Outcomes** (0-10) | • PICO: Outcomes<br>• PICOT: Outcomes<br>• PEO: Outcomes | Richardson et al., 1995<br>Stillwell et al., 2010 | ✅ **Direct precedent**: Outcomes define actionable endpoint in every variant; measurable effects required |
| **Exclusion** (-20 to 0) | • PRISMA 2020: Eligibility exclusions<br>• Cochrane: Predefined criteria | Page et al., 2021<br>Higgins et al., 2022 | ✅ **Direct precedent**: Systematic review standards require prespecified exclusions; Cochrane emphasizes documenting exclusions for reproducibility |
| **Title Bonus** (+10) | • Text-mining automation:<br>  Title/abstract relevance weighting | O'Mara-Eves et al., 2015<br>Wallace et al., 2010 | ⚠️ **Novel synthesis**: No question framework analogue, but aligns with validated machine-learning triage practices |

### Key Academic Justifications

#### 1. Domain (Population → Context)

**Scholarly precedent:**
- **PICOC** (Booth et al., 2012): Adds contextual/setting constraints to capture organizational conditions
- **SPICE** (Booth et al., 2012): Anchors question in setting and stakeholder viewpoint
- **PICo** (Lockwood et al., 2015): Integrates phenomenon and context for qualitative syntheses
- **CIMO logic** (Denyer & Tranfield, 2009): Organizational reviews extend population to domain-wide considerations

**ScholaRAG application:**
> "ScholaRAG's domain scoring reflects established practice of coupling population with contextual qualifiers" (Codex analysis, 2025)

**Example:**
- Standard PICO: "undergraduate students aged 18-22" (specific demographics)
- ScholaRAG Domain: "higher education" (field) + "adult learners" (context)

#### 2. Method (Comparison → Study Design Rigor)

**Scholarly precedent:**
- **PICOS** (Higgins et al., 2022, Cochrane Handbook): "Requires specifying eligible study designs to safeguard methodological rigor"
- **SPIDER** (Cooke et al., 2012): "Design component ensures method-sensitive retrieval for qualitative questions"

**ScholaRAG application:**
> "ScholaRAG's explicit scoring of design quality mirrors these standards by prioritising higher-rigor studies" (Codex analysis, 2025)

**Justification for replacing Comparison:**
- Many education/social science papers don't explicitly state control groups in 250-word abstracts
- Study design rigor (RCT > Survey > Case study) captures methodological quality regardless of comparison structure
- Trade-off: Broader applicability vs. strict PICO Comparison compliance

#### 3. Exclusion (Negative Scoring)

**Scholarly precedent:**
- **PRISMA 2020** (Page et al., 2021): "Systematic review standards require prespecified exclusions alongside inclusions"
- **Cochrane Handbook** (Higgins et al., 2022): "Emphasises documenting exclusions to preserve reproducibility"

**ScholaRAG innovation:**
> "While classical acronyms encode only positive criteria, Cochrane guidance emphasises documenting exclusions. ScholaRAG's negative weighting operationalises this by demoting records that violate hard exclusions" (Codex analysis, 2025)

**Novel contribution:**
- **Quantitative exclusion scoring** (-20 to 0) is not found in any PICO variant
- But **conceptually grounded** in mandatory systematic review exclusion criteria

#### 4. Title Bonus (Novel Dimension)

**Scholarly precedent:**
- **Text-mining automation** (O'Mara-Eves et al., 2015): "Title/abstract term weighting improves prioritisation accuracy"
- **Semi-automated screening** (Wallace et al., 2010): "Title/abstract features predict inclusion decisions"

**ScholaRAG innovation:**
> "Although not part of PICO variants, integrating a title bonus aligns with validated machine-learning triage practices without altering question structure" (Codex analysis, 2025)

**Academic positioning:**
- Not a PICO extension
- Derived from **systematic review automation research**
- Operationalizes text-mining insights for relevance scoring

---

## 📊 Comparison: ScholaRAG vs. Established Frameworks

### How ScholaRAG Relates to 10 Academic Variants

| Framework | Full Expansion | Source | Domain | ScholaRAG Alignment |
|-----------|---------------|--------|--------|---------------------|
| **PICO** | Population, Intervention, Comparison, Outcome | Richardson et al., 1995 | Clinical therapy | 2/4 dimensions match (I, O) |
| **PICOT** | PICO + Time | Stillwell et al., 2010 | Nursing, longitudinal | Could add Time dimension (v1.2.0?) |
| **PICOS** | PICO + Study design | Higgins et al., 2022 | Systematic reviews | ✅ **Method dimension directly inspired** |
| **PICOC** | PICO + Context | Booth et al., 2012 | Social policy, education | ✅ **Domain dimension directly inspired** |
| **PICo** | Population, Interest, Context | Lockwood et al., 2015 | Qualitative syntheses | Context → Domain mapping |
| **SPIDER** | Sample, Phenomenon, Design, Evaluation, Research type | Cooke et al., 2012 | Qualitative/mixed-methods | Design → Method mapping |
| **SPICE** | Setting, Perspective, Intervention, Comparison, Evaluation | Booth et al., 2012 | Social sciences | ✅ **Setting → Domain mapping** |
| **PECO** | Population, Exposure, Comparator, Outcome | Morgan et al., 2018 | Environmental health | Not applicable |
| **PEO** | Population, Exposure, Outcome | Bettany-Saltikov, 2016 | Etiology research | Not applicable |
| **ECLIPSE** | Expectation, Client, Location, Impact, Professionals, Service | Wildridge & Bell, 2002 | Health policy | Not applicable |

**Conclusion:** ScholaRAG synthesizes **PICOC** (context/setting), **PICOS** (study design), and **automation research** (title weighting).

---

## 🎓 Academic Positioning Statement

### For Researchers Citing ScholaRAG

**Recommended citation language:**

> "We used ScholaRAG's PICOC+S-derived 6-dimension rubric for automated screening (ScholaRAG v1.1.6, 2025). The framework synthesizes context-sensitive PICOC (Booth et al., 2012) and methodological rigor-focused PICOS (Higgins et al., 2022) frameworks, supplemented by text-mining automation insights (O'Mara-Eves et al., 2015). ScholaRAG extends standard PICO by: (1) incorporating contextual domain alongside population (PICOC), (2) prioritizing study design rigor over explicit comparison groups (PICOS), (3) operationalizing PRISMA 2020 exclusion criteria as negative scoring (Page et al., 2021), and (4) integrating title-abstract alignment as a relevance signal from systematic review automation research (Wallace et al., 2010)."

### For Academic Papers

**Methodology section template:**

```latex
\subsection{Screening Framework}
Paper screening employed ScholaRAG v1.1.6's six-dimensional relevance scoring
framework \citep{scholarag2025}, which synthesizes established evidence-synthesis
frameworks. The rubric operationalizes PICOC's context-sensitive population
definition \citep{booth2012} and PICOS's study design quality emphasis
\citep{higgins2022}. Six dimensions were scored:

\begin{enumerate}
    \item \textbf{Domain} (0-10 points): Research field and participant context,
          extending PICOC's context dimension \citep{booth2012, lockwood2015}
    \item \textbf{Intervention} (0-10 points): Technology/tool alignment
          \citep{richardson1995}
    \item \textbf{Method} (0-5 points): Study design rigor (RCT=5, Survey=3,
          Case study=2), following PICOS guidance \citep{higgins2022}
    \item \textbf{Outcomes} (0-10 points): Measurable results \citep{richardson1995}
    \item \textbf{Exclusion} (-20 to 0 points): PRISMA-derived hard filters
          \citep{page2021}
    \item \textbf{Title Bonus} (+10 points): Title-abstract alignment, based on
          automation research \citep{omara2015, wallace2010}
\end{enumerate}

Papers scoring $\geq X$ were included (threshold based on project type:
systematic review=90\%, knowledge repository=50\%).
```

---

## 📖 Complete Reference List

### Primary Framework Sources

1. **Richardson, W. S., Wilson, M. C., Nishikawa, J., & Hayward, R. S. (1995).** The well-built clinical question: a key to evidence-based decisions. *ACP Journal Club*, 123(3), A12–A13.
   - **Original PICO framework** for clinical questions

2. **Booth, A., Papaioannou, D., & Sutton, A. (2012).** *Systematic Approaches to a Successful Literature Review*. SAGE Publications.
   - **PICOC and SPICE frameworks** for social science/education reviews
   - **Citation count**: 5,000+ (Google Scholar)

3. **Higgins, J. P. T., Thomas, J., Chandler, J., Cumpston, M., Li, T., Page, M. J., & Welch, V. A. (Eds.). (2022).** *Cochrane Handbook for Systematic Reviews of Interventions* (Version 6.3). Cochrane.
   - **PICOS framework** for systematic reviews
   - **Authoritative source**: Cochrane Collaboration (gold standard)

4. **Lockwood, C., Munn, Z., & Porritt, K. (2015).** Qualitative research synthesis: methodological guidance for systematic reviewers utilizing the Joanna Briggs Institute approach. *International Journal of Evidence-Based Healthcare*, 13(3), 179–187.
   - **PICo framework** for qualitative syntheses
   - DOI: 10.1097/XEB.0000000000000062

5. **Cooke, A., Smith, D., & Booth, A. (2012).** Beyond PICO: The SPIDER tool for qualitative evidence synthesis. *Qualitative Health Research*, 22(10), 1435–1443.
   - **SPIDER framework** for qualitative/mixed-methods reviews
   - DOI: 10.1177/1049732312452938

### Systematic Review Standards

6. **Page, M. J., McKenzie, J. E., Bossuyt, P. M., et al. (2021).** The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*, 372, n71.
   - **PRISMA 2020 guidelines** (exclusion criteria)
   - DOI: 10.1136/bmj.n71
   - **Citation count**: 20,000+ (highly influential)

### Automation Research

7. **O'Mara-Eves, A., Thomas, J., McNaught, J., Miwa, M., & Ananiadou, S. (2015).** Using text mining for study identification in systematic reviews: a systematic review of current approaches. *Systematic Reviews*, 4, 5.
   - **Text-mining automation** (title/abstract weighting)
   - DOI: 10.1186/2046-4053-4-5

8. **Wallace, B. C., Trikalinos, T. A., Lau, J., Brodley, C., & Schmid, C. H. (2010).** Semi-automated screening of biomedical citations for systematic reviews. *BMC Bioinformatics*, 11, 55.
   - **Semi-automated screening** (relevance prediction)
   - DOI: 10.1186/1471-2105-11-55

### Additional Variants

9. **Stillwell, S. B., Fineout-Overholt, E., Melnyk, B. M., & Williamson, K. M. (2010).** Evidence-based practice: Step by step: Asking the clinical question: A key step in evidence-based practice. *American Journal of Nursing*, 110(3), 58–61.
   - **PICOT framework** (time dimension)

10. **Denyer, D., & Tranfield, D. (2009).** Producing a systematic review. In D. Buchanan & A. Bryman (Eds.), *The SAGE Handbook of Organizational Research Methods* (pp. 671–689). SAGE.
    - **CIMO logic** for organizational reviews

11. **Morgan, R. L., Whaley, P., Thayer, K. A., & Schünemann, H. J. (2018).** Identifying the PECO components to answer environmental health questions. *Environment International*, 121, 1027–1031.
    - **PECO framework** for environmental health

12. **Bettany-Saltikov, J. (2016).** *How to Do a Systematic Literature Review in Nursing and Healthcare* (2nd ed.). Wiley-Blackwell.
    - **PEO framework** for etiology research

13. **Wildridge, V., & Bell, L. (2002).** How CLIP became ECLIPSE: a mnemonic to assist in searching for health policy/management information. *Health Information & Libraries Journal*, 19(2), 113–115.
    - **ECLIPSE framework** for health policy

---

## 🔄 What Changed from v1.1.5 → v1.1.6

### Code Changes
- **None** - Algorithm, scoring logic unchanged

### Documentation Changes
- ✅ Added **complete academic lineage** with 13 primary citations
- ✅ Updated terminology: "PICO-inspired" → "PICOC+S-derived"
- ✅ Mapped each dimension to established frameworks
- ✅ Provided citation templates for researchers
- ✅ Created comprehensive reference list

### Terminology Updates

| v1.1.5 | v1.1.6 |
|--------|--------|
| "PICO-inspired" | "PICOC+S-derived with automation-aware prioritisation" |
| "Intentional adaptations" | "Synthesizes PICOC (context), PICOS (study design), automation research" |
| No citations | 13 primary academic citations |

---

## 💡 Key Takeaways

### 1. Honest Academic Positioning
- ✅ Every dimension has scholarly precedent (except Title Bonus, which has automation research justification)
- ✅ Clear lineage from established frameworks
- ✅ Transparent about novel contributions

### 2. ScholaRAG is NOT...
- ❌ "Another PICO variant"
- ❌ A replacement for PICO
- ❌ Overclaiming framework compliance

### 3. ScholaRAG IS...
- ✅ **PICOC+S synthesis** for multidisciplinary research
- ✅ **Automation-aware** (text-mining insights)
- ✅ **Scholarly grounded** (13 primary citations)

---

## 🚀 Future Directions (v1.2.0+)

### Potential Framework Extensions

Based on Codex analysis, future versions could:

1. **Add Time dimension** (→ PICOC+S+T)
   - Following PICOT (Stillwell et al., 2010)
   - Useful for longitudinal systematic reviews

2. **Add Comparison dimension** (→ 7-dimension)
   - Detect explicit control groups (when stated)
   - Keep Method (study rigor) as separate dimension
   - User option: 6D (flexible) vs 7D (PICO-strict)

3. **Domain-specific rubrics**
   - Education: PICOC+SPIDER synthesis
   - Medicine: PICO+PICOS synthesis
   - Social science: SPICE+SPIDER synthesis

4. **User-customizable weights**
   - Allow researchers to adjust dimension importance
   - Maintain scholarly precedent citations

---

## 📞 For Researchers

### Need Academic Justification?
See complete academic lineage: [ACADEMIC_LINEAGE.md](docs/ACADEMIC_LINEAGE.md)

### Questions about Citations?
Discussion: https://github.com/HosungYou/ScholaRAG/discussions

### Found Issues?
Issues: https://github.com/HosungYou/ScholaRAG/issues

---

**Bottom Line:** v1.1.6 provides **full scholarly grounding** for ScholaRAG's 6-dimension rubric. Every dimension maps to established frameworks or automation research. This is honest, transparent, academically credible positioning.
