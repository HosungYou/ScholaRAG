# Stage 7: Documentation & Writing

**Purpose**: Transform your RAG-assisted research into publishable documentation, including literature reviews, systematic review papers, and supplementary materials.

**Prerequisites**:
- Completed Stage 6 (Research conversations and analysis)
- Research notes with verified citations
- Key findings and evidence organized

---

## Overview

This final stage helps you:
1. Structure your literature review or systematic review paper
2. Generate properly formatted citations and bibliography
3. Create PRISMA flow diagrams and supplementary materials
4. Ensure reproducibility and transparency
5. Prepare for publication or submission

---

## Part 1: Structuring Your Literature Review

### Systematic Review Structure (PRISMA Format)

```markdown
# Standard Systematic Review Outline

## 1. Title
- Descriptive and specific
- Includes "systematic review" or "literature review"

## 2. Abstract (250-300 words)
- **Background**: Why is this review needed?
- **Objective**: What is your research question?
- **Methods**: How did you conduct the review? (PRISMA, databases, criteria)
- **Results**: How many papers? What were the main findings?
- **Conclusions**: What do the findings mean?

## 3. Introduction
### 3.1 Rationale
- What gap does this review address?
- Why is it important?

### 3.2 Objectives
- Specific research questions (PICO/SPIDER format)

## 4. Methods
### 4.1 Protocol and Registration
- State if pre-registered (PROSPERO, OSF)

### 4.2 Eligibility Criteria
- Inclusion/exclusion criteria
- PICO framework

### 4.3 Information Sources
- Databases searched (with dates)
- Other sources (reference lists, citations)

### 4.4 Search Strategy
- Full Boolean queries for each database
- Keywords and synonyms

### 4.5 Study Selection
- Screening process (title/abstract → full-text)
- Number of reviewers
- Conflict resolution

### 4.6 Data Collection Process
- What data were extracted?
- Tools used (your RAG system!)

### 4.7 Risk of Bias Assessment
- Quality assessment method used

## 5. Results
### 5.1 Study Selection
- PRISMA flow diagram
- Numbers at each stage

### 5.2 Study Characteristics
- Table of included studies
- Geographic distribution, date range

### 5.3 Findings
- Organized by theme or research question
- Evidence tables
- Synthesis of key findings

### 5.4 Synthesis of Results
- Meta-analysis (if applicable)
- Narrative synthesis
- Subgroup analyses

## 6. Discussion
### 6.1 Summary of Evidence
- Answer your research questions
- Key patterns and themes

### 6.2 Limitations
- Limitations of included studies
- Limitations of your review process

### 6.3 Implications
- For practice
- For policy
- For future research

## 7. Conclusions
- Main takeaways
- Future directions

## 8. References
- All cited papers in chosen format

## 9. Supplementary Materials
- Full search strategies
- Excluded studies with reasons
- Data extraction forms
- PRISMA checklist
```

---

## Part 2: Writing with RAG Assistance

### Using Your RAG System to Draft Sections

**Methods Section**:
```
Prompt your RAG system:

"Generate a Methods section for my systematic review. Include:
- Databases: [list databases you searched]
- Search dates: [dates]
- Search strategy: [Boolean queries from Stage 2]
- Inclusion criteria: [from Stage 3]
- Number of papers at each stage: Identification (n=1247), Screening (n=289), Eligible (n=156), Included (n=137)
- Data extraction: Used ResearcherRAG with Claude API for screening and LangChain for vector search
- Analysis: Thematic synthesis using conversational AI analysis"
```

**Results - Study Characteristics**:
```
"Create a summary table of the 137 included studies with these columns:
- Author, Year
- Study Design
- Sample Size
- Setting (country/context)
- Main Findings

Group by study design and sort by year."
```

**Results - Thematic Synthesis**:
```
"Synthesize all findings related to [your theme]. Structure as:
1. Overview paragraph
2. Sub-theme 1 with supporting citations
3. Sub-theme 2 with supporting citations
4. Summary paragraph

Use APA citation format [Author, Year]"
```

**Discussion**:
```
"Help me write a discussion section that:
1. Summarizes the main findings from my results
2. Compares my findings to [cite relevant reviews]
3. Discusses implications for [your field]
4. Acknowledges limitations
5. Suggests future research directions"
```

---

## Part 3: Citation & Bibliography Management

### Generating Your Bibliography

**Step 1: Export All Cited Papers**

```python
# If using claude_code_interface.py

# Track citations during research
cited_papers = set()

# After each query, extract citations
import re
citations = re.findall(r'\[([^\]]+)\]', llm_response)
cited_papers.update(citations)

# At the end
print(f"Total papers cited: {len(cited_papers)}")
with open('cited_papers.txt', 'w') as f:
    for paper_id in sorted(cited_papers):
        f.write(f"{paper_id}\n")
```

**Step 2: Generate Bibliography**

```
Ask your RAG system:

"For each of these paper IDs, generate a full citation in APA format:
[list of paper_ids from your research]

Include: Author(s), Year, Title, Journal, Volume(Issue), Pages, DOI"
```

**Step 3: Verify and Format**

```python
# bibliography_generator.py

import bibtexparser

def generate_bibliography(cited_papers, metadata_file, format='apa'):
    """
    Generate bibliography from cited papers

    Args:
        cited_papers: list of paper IDs cited
        metadata_file: CSV/JSON with paper metadata
        format: 'apa', 'chicago', 'ieee', 'bibtex'
    """

    import pandas as pd
    metadata = pd.read_csv(metadata_file)

    bibliography = []
    for paper_id in sorted(cited_papers):
        paper = metadata[metadata['paper_id'] == paper_id].iloc[0]

        if format == 'apa':
            citation = format_apa(paper)
        elif format == 'bibtex':
            citation = format_bibtex(paper)
        # ... other formats

        bibliography.append(citation)

    return '\n\n'.join(bibliography)

def format_apa(paper):
    """Format single paper in APA style"""
    authors = paper['authors']  # "Smith, J., & Johnson, M."
    year = paper['year']
    title = paper['title']
    journal = paper['journal']
    volume = paper['volume']
    issue = paper['issue']
    pages = paper['pages']
    doi = paper['doi']

    citation = f"{authors} ({year}). {title}. *{journal}*, *{volume}*({issue}), {pages}. https://doi.org/{doi}"

    return citation
```

---

## Part 4: PRISMA Flow Diagram

### Generating Your PRISMA Diagram

**Option 1: Using Your Data**

```python
# generate_prisma.py

def create_prisma_diagram(stats):
    """
    Create PRISMA 2020 flow diagram

    stats = {
        'identification': {
            'databases': 1247,
            'registers': 0,
            'other_sources': 15
        },
        'screening': {
            'duplicates_removed': 158,
            'records_screened': 1089,
            'records_excluded': 825
        },
        'eligibility': {
            'reports_sought': 264,
            'reports_not_retrieved': 7,
            'reports_assessed': 257,
            'reports_excluded': 120,
            'exclusion_reasons': {
                'wrong_population': 45,
                'wrong_intervention': 32,
                'wrong_methodology': 28,
                'no_full_text': 15
            }
        },
        'included': {
            'studies': 137,
            'reports': 137
        }
    }
    """

    # Use matplotlib or plotly to create diagram
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    fig, ax = plt.subplots(figsize=(12, 14))

    # ... (PRISMA box layout code)
    # ... (arrows and connections)

    plt.savefig('prisma_flow_diagram.png', dpi=300, bbox_inches='tight')
    print("PRISMA diagram saved!")
```

**Option 2: Using Online Tools**

- PRISMA Flow Diagram Generator: http://prisma.thetacollaborative.ca/
- Input your numbers from Stage 3
- Export as PNG or PDF

---

## Part 5: Supplementary Materials

### What to Include

**1. Complete Search Strategies**

```markdown
# Supplementary File 1: Search Strategies

## PubMed Search (Conducted: 2024-01-10)

```
("technology adoption"[Title/Abstract] OR "technology implementation"[Title/Abstract] OR "technology integration"[Title/Abstract])
AND
("healthcare"[Title/Abstract] OR "hospital"[Title/Abstract] OR "clinic"[Title/Abstract])
AND
("barrier"[Title/Abstract] OR "facilitator"[Title/Abstract] OR "factor"[Title/Abstract])
AND
("2010"[Date - Publication] : "2024"[Date - Publication])
```

Results: 487 papers
```

**2. Excluded Studies List**

```markdown
# Supplementary File 2: Excluded Studies with Reasons

| Author, Year | Exclusion Reason | Stage Excluded |
|-------------|------------------|----------------|
| Williams, 2019 | Not healthcare setting | Full-text review |
| Garcia, 2020 | No empirical data | Full-text review |
| ...
```

**3. Data Extraction Form**

```markdown
# Supplementary File 3: Data Extraction Form

For each included study, we extracted:

1. **Bibliographic Information**
   - Author(s)
   - Year
   - Title
   - Journal
   - DOI

2. **Study Characteristics**
   - Country/Region
   - Setting (hospital, clinic, etc.)
   - Study design
   - Sample size
   - Time period

3. **Technology Information**
   - Type of technology
   - Purpose/Application

4. **Key Findings**
   - Main results
   - Adoption rates (if reported)
   - Barriers identified
   - Facilitators identified
   - Recommendations

5. **Quality Assessment**
   - Study quality score
   - Risk of bias
   - Limitations noted
```

**4. PRISMA Checklist**

Download from: http://www.prisma-statement.org/PRISMAStatement/Checklist

Fill in page numbers for each item.

**5. Reproducibility Package**

```markdown
# Supplementary File 5: Reproducibility Package

## ResearcherRAG Configuration

This systematic review used ResearcherRAG v1.0 for automated screening and analysis.

### Software Versions
- Python: 3.11.5
- LangChain: 0.1.0
- ChromaDB: 0.4.18
- Claude API: claude-3-5-sonnet-20241022
- OpenAI Embeddings: text-embedding-3-small

### Vector Database Configuration
```yaml
embedding_model: text-embedding-3-small
chunk_size: 500
chunk_overlap: 50
similarity_threshold: 0.7
top_k: 5
```

### Prompt Templates
All prompt templates used are available at:
https://github.com/YourUsername/researcherRAG/tree/main/prompts

### Replication Instructions
1. Clone repository: `git clone https://github.com/YourUsername/researcherRAG`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure API keys in `.env`
4. Run Stages 1-7 following documentation
5. See `REPRODUCTION.md` for detailed instructions
```

---

## Part 6: Ensuring Transparency & Reproducibility

### Disclosure Statement

**Include in your Methods section:**

```markdown
## AI-Assisted Screening and Analysis

This systematic review utilized AI-assisted tools for literature screening and analysis:

1. **Initial Screening (Stage 3)**:
   - Claude 3.5 Sonnet was used to assess abstracts against inclusion criteria
   - Each decision was reviewed by a human researcher
   - Inter-rater reliability: κ = 0.89

2. **Data Extraction (Stage 4)**:
   - Papers were processed using OpenAI text-embedding-3-small for vector representation
   - Stored in ChromaDB vector database
   - Full text extraction performed with PyMuPDF

3. **Literature Analysis (Stage 6)**:
   - Claude 3.5 Sonnet was used to answer research questions based on retrieved paper chunks
   - All generated citations were manually verified against source papers
   - Critical findings were cross-referenced with original PDFs

4. **Validation**:
   - 10% of screening decisions were independently verified
   - All citations in final manuscript were validated
   - No AI-generated text appears in the manuscript without human review and editing

5. **Reproducibility**:
   - Complete code and configuration available at [GitHub URL]
   - Vector database snapshot available upon request
   - All prompts documented in supplementary materials
```

---

## Part 7: Writing Tips with RAG

### Effective Prompts for Writing Assistance

**For Each Section:**

```
"Based on my research notes, help me write the [section name] for my systematic review.

Context:
- Research question: [your question]
- Number of papers: 137
- Key findings: [bullet points]
- Citation style: APA

Requirements:
- Academic tone
- Include citations for all claims
- Follow PRISMA guidelines
- Length: ~500 words

Please draft the section."
```

**Refining Drafts:**

```
"Review this paragraph from my literature review. Improve it by:
1. Ensuring all claims have citations
2. Improving academic tone
3. Removing redundancy
4. Strengthening the argument
5. Adding transitional sentences

[paste your paragraph]"
```

**Creating Evidence Tables:**

```
"Create a table summarizing evidence for [your theme]:

Columns:
- Finding
- Supporting Papers (with citations)
- Sample Size (total)
- Study Designs
- Quality Assessment
- Notes

Make it publication-ready."
```

---

## Part 8: Quality Checklist

### Before Submission

- [ ] **PRISMA Checklist**: All 27 items completed
- [ ] **PRISMA Diagram**: Generated and included
- [ ] **Search Strategy**: Fully documented in supplementary materials
- [ ] **Citations**: All verified against source papers
- [ ] **Bibliography**: Complete and properly formatted
- [ ] **Supplementary Materials**: All files prepared
- [ ] **Reproducibility**: Code and data sharing plan in place
- [ ] **AI Disclosure**: Transparent about AI use
- [ ] **Quality Assessment**: Risk of bias assessed for all papers
- [ ] **Data Extraction**: Systematic and documented
- [ ] **Conflicts of Interest**: Declared
- [ ] **Funding**: Acknowledged

---

## Part 9: Publishing & Sharing

### Preparing for Submission

**1. Choose Target Journal**
- Check journal's systematic review guidelines
- Note required formats (PRISMA, MOOSE, etc.)
- Check citation style

**2. Prepare Submission Package**
```
submission_package/
├── manuscript.docx
├── cover_letter.docx
├── prisma_checklist.pdf
├── prisma_diagram.png
├── supplementary_materials/
│   ├── search_strategies.pdf
│   ├── excluded_studies.csv
│   ├── data_extraction_form.pdf
│   └── reproducibility_package.md
└── figures/
    └── figure_1_prisma.png
```

**3. Data & Code Sharing**

```markdown
# Data Availability Statement

The data supporting the findings of this study are available as follows:

1. **Included Studies**: Complete list available in Supplementary Table 1
2. **Extracted Data**: Available in structured format at [OSF/Zenodo URL]
3. **Code**: ResearcherRAG implementation available at [GitHub URL]
4. **Vector Database**: Snapshot available upon reasonable request
5. **Prompts**: All AI prompts documented in Supplementary File 5

The authors commit to making all materials available to support reproducibility.
```

---

## Part 10: Post-Publication

### Sharing Your Work

**1. Create Project Website**
- Summary of findings
- Interactive PRISMA diagram
- Download links for supplementary materials
- Links to code repository

**2. Social Media Summary**
```
Thread for Twitter/LinkedIn:

1/ We just published a systematic review of [topic]! 🧵

Analyzed 137 papers using AI-assisted ResearcherRAG. Here are the key findings:

2/ Main Finding 1: [brief summary]
📊 Evidence from [n] papers
🔗 Link: [paper URL]

3/ Main Finding 2: [brief summary]
...

Final/ All code, data, and materials are openly available:
📂 GitHub: [URL]
📄 Paper: [DOI]
✨ Fully reproducible!
```

**3. Present at Conferences**
- Poster highlighting method and findings
- Talk about AI-assisted systematic reviews
- Workshop on ResearcherRAG methodology

---

## Resources & Templates

### Useful Tools

1. **Citation Management**
   - Zotero: https://www.zotero.org/
   - Mendeley: https://www.mendeley.com/

2. **PRISMA Resources**
   - PRISMA Statement: http://www.prisma-statement.org/
   - PRISMA Flow Diagram: http://prisma.thetacollaborative.ca/

3. **Quality Assessment Tools**
   - CASP Checklists: https://casp-uk.net/casp-tools-checklists/
   - Newcastle-Ottawa Scale: http://www.ohri.ca/programs/clinical_epidemiology/oxford.asp

4. **Reporting Guidelines**
   - EQUATOR Network: https://www.equator-network.org/

5. **Pre-registration**
   - PROSPERO: https://www.crd.york.ac.uk/prospero/
   - OSF: https://osf.io/

---

## Completion Checklist

At the end of Stage 7, you should have:

✅ **Manuscript**
- [ ] Complete draft following PRISMA guidelines
- [ ] All sections written and reviewed
- [ ] Citations verified and formatted

✅ **Figures & Tables**
- [ ] PRISMA flow diagram
- [ ] Study characteristics table
- [ ] Evidence synthesis tables

✅ **Supplementary Materials**
- [ ] Complete search strategies
- [ ] Excluded studies list
- [ ] Data extraction forms
- [ ] PRISMA checklist
- [ ] Reproducibility package

✅ **Submission Ready**
- [ ] Formatted for target journal
- [ ] All co-authors reviewed
- [ ] Cover letter prepared
- [ ] Data sharing statement included

---

## Congratulations!

You have completed all 7 stages of ResearcherRAG! 🎉

You now have a complete, reproducible systematic review powered by AI-assisted literature analysis.

---

**Estimated Time for This Stage**: 20-40 hours (varies by complexity)

**Key Deliverable**: Publication-ready systematic review manuscript with complete supplementary materials

---

## Further Reading

- [Best Practices Guide](https://researcher-rag-helper.vercel.app/guide/06-best-practices)
- [Troubleshooting](https://researcher-rag-helper.vercel.app/guide/07-troubleshooting)
- [ResearcherRAG GitHub](https://github.com/HosungYou/researcherRAG)
