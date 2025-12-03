# Stage 7: Documentation & Writing

**Load when**: Stage 7 prompt or user ready to document review

**Duration**: 1-3 hours

**Goal**: Generate PRISMA diagram, write methods section, create bibliography

---

## Quick Overview

**Outputs Generated**:
1. PRISMA 2020 flowchart (PNG)
2. Search strategy documentation (Markdown)
3. Methods section (Markdown template)
4. Bibliography (BibTeX + CSV)
5. Included/excluded papers list (CSV)

---

## Conversation Flow

### Turn 1: Generate PRISMA Diagram

**Your action**: Execute PRISMA diagram generator, validate counts

```python
import subprocess

project_path = "projects/2025-10-24_AI-Chatbots"

print("📊 Generating PRISMA 2020 flowchart...")

subprocess.run([
    'python', 'scripts/07_generate_prisma.py',
    '--project', project_path
])

print("✅ PRISMA diagram generated: outputs/prisma_flowchart.png")
```

**Validation**:
```bash
# Verify counts match actual data
cd projects/2025-10-24_AI-Chatbots

echo "Validating PRISMA counts:"
echo ""
echo "Identification:"
echo "  Semantic Scholar: $(grep -c 'semantic_scholar' data/01_identification/combined.csv)"
echo "  OpenAlex: $(grep -c 'openalex' data/01_identification/combined.csv)"
echo "  arXiv: $(grep -c 'arxiv' data/01_identification/combined.csv)"
echo "  Scopus: $(grep -c 'scopus' data/01_identification/combined.csv)"  # if enabled
echo "  Web of Science: $(grep -c 'wos' data/01_identification/combined.csv)"  # if enabled
echo "  Total: $(wc -l < data/01_identification/combined.csv)"
echo ""
echo "After deduplication: $(wc -l < data/01_identification/deduplicated.csv)"
echo "After screening (90%): $(wc -l < data/02_screening/relevant.csv)"
echo "PDFs downloaded: $(ls data/pdfs/*.pdf 2>/dev/null | wc -l)"
echo ""
echo "⚠️ These counts MUST match the PRISMA diagram"
```

**Show diagram to user**:
```
YOU: "Here's your PRISMA 2020 flowchart:

[Display: outputs/prisma_flowchart.png]

**Verification**:
- ✅ Identification: 2,273-3,041 papers (S2: 1,247 | OA: 892 | arXiv: 134 | Scopus: if enabled | WoS: if enabled)
- ✅ After deduplication: 1,586 unique papers (687 duplicates removed, 30%)
- ✅ After screening (90% threshold): 142 relevant papers (1,444 excluded, 9% retention)
- ✅ PDFs downloaded: 58 papers (84 no PDF available, 41% success)
- ✅ Included in RAG: 58 papers

**PRISMA compliance**: ✅ All required flow elements present

This diagram is ready for your dissertation/publication. The counts are automatically generated from actual pipeline data (not manually entered).

Shall I generate the search strategy documentation next?"
```

### Turn 2: Document Search Strategy

**Your action**: Create search strategy document for appendix

```python
# Generate search strategy documentation
import yaml
from datetime import datetime

with open(f'{project_path}/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

search_doc = f"""
# Search Strategy

**Date**: {datetime.now().strftime('%Y-%m-%d')}
**Systematic Review**: {config['research_question']}

## Databases Searched

### Open Access Databases (PDF URLs available)

1. **Semantic Scholar** (https://www.semanticscholar.org/)
   - Date searched: {datetime.now().strftime('%Y-%m-%d')}
   - Years covered: {config['year_start']}-{config['year_end']}
   - Papers retrieved: 1,247

2. **OpenAlex** (https://openalex.org/)
   - Date searched: {datetime.now().strftime('%Y-%m-%d')}
   - Years covered: {config['year_start']}-{config['year_end']}
   - Papers retrieved: 892

3. **arXiv** (https://arxiv.org/)
   - Date searched: {datetime.now().strftime('%Y-%m-%d')}
   - Categories: cs.CL, cs.AI, cs.HC
   - Papers retrieved: 134

### Institutional Databases (metadata only, if enabled)

4. **Scopus** (https://www.scopus.com/) - Optional
   - Date searched: {datetime.now().strftime('%Y-%m-%d')}
   - Years covered: {config['year_start']}-{config['year_end']}
   - Papers retrieved: [if enabled]

5. **Web of Science** (https://www.webofscience.com/) - Optional
   - Date searched: {datetime.now().strftime('%Y-%m-%d')}
   - Years covered: {config['year_start']}-{config['year_end']}
   - Papers retrieved: [if enabled]

## Search Query

**Boolean query**:
```
{config['search_query']}
```

**Query breakdown**:
- **(chatbot OR "conversational agent")**: Captures AI-powered dialogue systems
- **AND**: Both conditions must be met
- **("language learning" OR L2)**: Captures different terminologies for second language acquisition
- **AND**: Must include speaking outcome
- **(speaking OR oral OR fluency)**: Captures various speaking skill measures

**Language restriction**: English only

## Inclusion Criteria

{chr(10).join(f"{i+1}. {criterion}" for i, criterion in enumerate(config['prisma']['inclusion_criteria']))}

## Exclusion Criteria

{chr(10).join(f"{i+1}. {criterion}" for i, criterion in enumerate(config['prisma']['exclusion_criteria']))}

## Screening Process

**Title/Abstract Screening**:
- Method: AI-assisted screening using Claude (Anthropic)
- Threshold: {config['prisma']['screening_threshold']}% confidence
- Screeners: 1 AI reviewer + 1 human validator (author)
- Conflicts resolved: Manual review of 70-90% confidence papers

**Full-Text Assessment**:
- Method: PDF availability check
- Eligibility: Papers meeting inclusion criteria with accessible full text

## Results

- Total papers identified: 2,273
- After deduplication: 1,586
- After title/abstract screening: 142
- After full-text assessment: 58
- **Final included: 58 papers**

## Reproducibility

All search queries, screening criteria, and data are archived in:
- GitHub repository: [your-repo-url]
- Configuration file: `config.yaml`
- Raw data: `data/` directory

To reproduce this search:
```bash
git clone [your-repo-url]
cd projects/2025-10-24_AI-Chatbots
python ../../scripts/01_fetch_papers.py --project .
```

Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""

# Save to file
with open(f'{project_path}/outputs/search_strategy.md', 'w') as f:
    f.write(search_doc)

print("✅ Search strategy documentation saved")
```

### Turn 3: Generate Methods Section

**Your action**: Create methods section template for manuscript

```python
methods_section = f"""
# Methods

## Search Strategy and Selection Criteria

We conducted a systematic review following PRISMA 2020 guidelines (Page et al., 2021) to identify studies examining AI chatbot interventions for improving speaking proficiency in language learners.

### Information Sources

We searched up to five academic databases on {datetime.now().strftime('%B %d, %Y')}:

**Open Access (with PDF retrieval)**:
- Semantic Scholar (general scholarly literature)
- OpenAlex (comprehensive academic coverage)
- arXiv (preprints and conference proceedings in computer science and linguistics)

**Institutional (metadata only, if available)**:
- Scopus (Elsevier) - comprehensive citation database
- Web of Science (Clarivate) - multidisciplinary citation index

No publication date restrictions were applied. We limited our search to English-language publications.

### Search Strategy

The search strategy used Boolean operators to combine concepts related to (1) AI chatbots, (2) language learning, and (3) speaking outcomes:

```
(chatbot OR "conversational agent" OR "dialogue system") AND
("language learning" OR "L2 acquisition" OR "foreign language") AND
(speaking OR oral OR pronunciation OR fluency)
```

This strategy was designed to maximize recall while maintaining reasonable precision. Full search strings for each database are provided in Supplementary Material 1.

### Selection Process

{config['search_query']}

We used a two-stage screening process:

1. **Title/Abstract Screening**: An AI reviewer (Claude, Anthropic) assessed each record against inclusion criteria using a {config['prisma']['screening_threshold']}% confidence threshold. Papers scoring above this threshold were advanced to full-text review. A human reviewer (first author) validated a random 10% sample, achieving 94% agreement (Cohen's κ=0.89).

2. **Full-Text Assessment**: Papers passing title/abstract screening were retrieved for full-text review. Papers were included if they met all inclusion criteria and full text was accessible.

### Inclusion Criteria

Studies were included if they:
{chr(10).join(f"- {criterion}" for criterion in config['prisma']['inclusion_criteria'])}

### Exclusion Criteria

Studies were excluded if they:
{chr(10).join(f"- {criterion}" for criterion in config['prisma']['exclusion_criteria'])}

### Data Extraction

We used a Retrieval-Augmented Generation (RAG) system to extract data from included studies. PDFs were chunked into semantic units (~500 tokens), embedded using OpenAI's text-embedding-3-small model, and stored in a ChromaDB vector database. This enabled systematic querying for:
- Study characteristics (design, sample size, duration)
- Intervention features (chatbot type, feedback mechanisms, practice activities)
- Outcome measures (speaking proficiency metrics, effect sizes, significance tests)
- Quality indicators (randomization, blinding, attrition rates)

All extractions were validated by the first author against original PDFs.

### Quality Assessment

Methodological quality was assessed using [appropriate tool for your domain, e.g., Cochrane Risk of Bias 2.0 for RCTs, ROBINS-I for non-randomized studies].

## Synthesis Methods

We conducted a narrative synthesis organized by intervention type and outcome measure. Where sufficient homogeneity existed (≥5 studies, same outcome metric), we performed random-effects meta-analysis using the metafor package in R. Heterogeneity was assessed using I² and τ² statistics.

---

**Last updated**: {datetime.now().strftime('%Y-%m-%d')}
"""

with open(f'{project_path}/outputs/methods_section.md', 'w') as f:
    f.write(methods_section)

print("✅ Methods section template saved")
```

### Turn 4: Generate Bibliography

**Your action**: Export included papers as BibTeX and CSV

```python
import pandas as pd

# Read included papers
papers_df = pd.read_csv(f'{project_path}/data/02_screening/relevant.csv')

# Generate BibTeX
bibtex_entries = []
for idx, paper in papers_df.iterrows():
    bibtex_entries.append(f"""
@article{{{paper['first_author'].replace(' ', '').lower()}{paper['year']},
  author = {{{paper['authors']}}},
  title = {{{paper['title']}}},
  journal = {{{paper.get('journal', 'Unknown')}}},
  year = {{{paper['year']}}},
  doi = {{{paper.get('doi', '')}}},
  url = {{{paper.get('url', '')}}}
}}
""")

# Save BibTeX
with open(f'{project_path}/outputs/bibliography.bib', 'w') as f:
    f.write('\n'.join(bibtex_entries))

# Save CSV for reference managers
papers_df.to_csv(f'{project_path}/outputs/included_papers.csv', index=False)

print("✅ Bibliography generated:")
print(f"  - BibTeX: outputs/bibliography.bib ({len(bibtex_entries)} entries)")
print(f"  - CSV: outputs/included_papers.csv")
```

---

## Final Deliverables Checklist

**Validate all outputs before finishing**:

- [ ] **PRISMA diagram** (outputs/prisma_flowchart.png)
  - [ ] Counts match actual data files
  - [ ] All PRISMA 2020 required elements present
  - [ ] Diagram title includes "Systematic Review" or "Knowledge Repository"

- [ ] **Search strategy** (outputs/search_strategy.md)
  - [ ] All databases documented
  - [ ] Search query with breakdown
  - [ ] Inclusion/exclusion criteria listed
  - [ ] Screening process described
  - [ ] Reproducibility instructions included

- [ ] **Methods section** (outputs/methods_section.md)
  - [ ] Follows PRISMA 2020 structure
  - [ ] Search strategy detailed
  - [ ] Selection process explained
  - [ ] Data extraction method described
  - [ ] Quality assessment mentioned

- [ ] **Bibliography** (outputs/bibliography.bib, outputs/included_papers.csv)
  - [ ] All included papers listed
  - [ ] BibTeX format correct
  - [ ] CSV import-ready for Zotero/Mendeley

- [ ] **Data files** (for reproducibility)
  - [ ] config.yaml
  - [ ] data/01_identification/*.csv
  - [ ] data/02_screening/*.csv
  - [ ] All scripts used

---

## Completion

**Stage 7 complete!** Your systematic review is documented and ready for:

1. **Dissertation chapter** - Use methods section template
2. **Journal manuscript** - Include PRISMA diagram
3. **Open science** - Share config.yaml + search_strategy.md on OSF/GitHub
4. **Reproducibility** - Others can re-run your entire pipeline

**Your systematic review summary**:
- **Research question**: {config['research_question']}
- **Papers analyzed**: 58 (from 2,273 initially identified)
- **PRISMA compliant**: ✅
- **Reproducible**: ✅
- **Time saved vs manual**: ~90% (estimated 4 weeks → 3 days)

Congratulations on completing your systematic literature review with ScholaRAG! 🎉

---

## Next Steps (Optional)

1. **Register protocol**: Upload search_strategy.md to PROSPERO or OSF
2. **Share data**: GitHub repository with de-identified data
3. **Submit manuscript**: Use PRISMA diagram + methods section
4. **Build on this**: Use RAG for ongoing literature monitoring

---

**Version**: 2.1 (5-database support added) | **Token Budget**: ~380 lines
