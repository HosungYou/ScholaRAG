# Claude Code Prompts for ResearcherRAG Customization

**A collection of ready-to-use prompts for customizing ResearcherRAG with Claude Code**

---

## Overview

This document contains **copy-paste ready prompts** for Claude Code to help you:
- Customize RAG systems for your research domain
- Add new features
- Fix issues
- Optimize performance

**How to use:**
1. Open Claude Code in your IDE
2. Copy a prompt from this document
3. Paste into Claude Code chat
4. Review and approve the suggested changes

---

## 🚀 Quick Setup Prompts

### 1. Initialize New Literature Review Project

```
I want to create a new literature review RAG project for analyzing papers on [YOUR TOPIC].

Please:
1. Create project structure in:
   /Volumes/External SSD/Projects/Research/ResearcherRAG/projects/[project_name]/

2. Set up:
   - Data directories (raw_pdfs/, processed/, vector_db/)
   - Configuration file with project-specific settings
   - README with project description
   - .gitignore for large files

3. Create initial ingestion script for uploading papers

4. Set up Qdrant collection named "[project_name]_papers"

Project details:
- Topic: [YOUR TOPIC]
- Expected paper count: [NUMBER]
- Special requirements: [ANY SPECIAL NEEDS]
```

---

### 2. Set Up Qualitative Coding Project

```
I need to set up a qualitative coding project for analyzing interviews about [TOPIC].

Create:
1. Project directory structure
2. Interview parser configured for my transcript format:
   [Describe format: e.g., "Speaker: text" or timestamps, etc.]
3. Custom codebook template for [RESEARCH AREA]
4. Initial coding prompts focused on [KEY THEMES]

Interview details:
- Number of interviews: [NUMBER]
- Interview format: [STRUCTURED/SEMI-STRUCTURED/UNSTRUCTURED]
- Key themes to explore: [LIST THEMES]
```

---

## 📝 Customization Prompts

### 3. Custom Metadata Extraction

```
I need to extract custom metadata from academic papers beyond standard title/author/year.

For papers in [FIELD], extract:
1. Study design (experimental/survey/qualitative/mixed/meta-analysis)
2. Sample size (if quantitative)
3. Geographic location of study
4. Participant demographics (age group, occupation)
5. Theoretical frameworks mentioned
6. Statistical methods used

Modify backend/core/ingestion.py to:
- Extract these fields using LLM-based extraction
- Store in document metadata
- Make searchable via filters

Add to search interface:
- Dropdown filters for each metadata field
- Example: "Show experimental studies with N>100 from 2020-2023"
```

---

### 4. Domain-Specific Chunking Strategy

```
The default chunking breaks up academic papers in ways that lose context.

Implement a domain-aware chunking strategy for [DISCIPLINE] papers:

1. Preserve section boundaries:
   - Keep Abstract as single chunk
   - Keep Methods section together
   - Keep Results subsections intact
   - Separate Discussion by theme

2. Special handling:
   - Extract tables separately with caption and content
   - Extract figures with captions
   - Keep reference lists separate
   - Preserve equations with surrounding context

3. Metadata per chunk:
   - Add "section_type" field (abstract/intro/methods/results/discussion)
   - Add "has_statistics" boolean
   - Add "has_visualization" boolean

Modify backend/core/ingestion.py and utils/chunking.py to implement this.
```

---

### 5. Custom Prompt Templates

```
Create custom prompt templates optimized for [RESEARCH DOMAIN].

For Literature Review queries:
1. Template for "theory comparison" questions
2. Template for "methodological synthesis" questions
3. Template for "evidence quality assessment" questions
4. Template for "research gap identification" questions

For each template:
- Include domain-specific terminology
- Structure output in standard academic format
- Emphasize critical analysis
- Request citations in [APA/MLA/Chicago] format

Store templates in prompts/[domain]/ folder.
Add template selector to Gradio interface.

Domain: [YOUR DOMAIN]
Common question types: [LIST TYPES]
```

---

## 🔧 Feature Enhancement Prompts

### 6. Add Citation Management Integration

```
Integrate with Zotero citation manager.

Features:
1. Import papers directly from Zotero library using Zotero API
2. Preserve Zotero metadata (tags, collections, notes)
3. Export RAG results back to Zotero as notes
4. Generate bibliographies in Zotero format

Implementation:
1. Add zotero_sync.py module with Zotero API client
2. Add "Import from Zotero" button to Gradio interface
3. Add "Export to Zotero" button for query results
4. Store Zotero item keys in document metadata for linking

My Zotero setup:
- Library ID: [YOUR ID]
- Library type: [user/group]
- Collections to sync: [LIST]
```

---

### 7. Add Collaborative Annotation

```
Add team annotation features to the Literature Review RAG.

Requirements:
1. Users can highlight text passages in retrieved documents
2. Add comments/notes to highlights
3. Tag team members with @username
4. Create threaded discussions on highlights
5. Export all annotations as structured data

UI changes:
- Add annotation sidebar to document viewer
- Show existing annotations inline
- Add "New Annotation" button
- Filter view by annotator or tag

Backend:
- Store annotations in PostgreSQL
- Link to document chunks via IDs
- Support markdown in comments
- Add API endpoints for CRUD operations

Technology preference: [React/Gradio/Streamlit]
```

---

### 8. Implement Advanced Retrieval Techniques

```
Upgrade retrieval system with state-of-the-art techniques.

Add support for:

1. **Hybrid Search** (dense + sparse):
   - Combine semantic search (current) with BM25 keyword search
   - Weighted fusion of results

2. **Query Expansion**:
   - Auto-generate query variations using LLM
   - Search with all variations
   - Merge and deduplicate results

3. **Hypothetical Document Embeddings (HyDE)**:
   - Generate hypothetical answer to query
   - Search using answer embedding
   - Better for complex research questions

4. **Reranking with Cross-Encoder**:
   - After initial retrieval, rerank with cross-encoder model
   - Models: ms-marco-MiniLM or similar

Implement in backend/core/retrieval.py with option to enable/disable each technique.
Add performance benchmarks comparing techniques.
```

---

### 9. Add Multilingual Support

```
Add support for analyzing papers in [LANGUAGE].

Requirements:
1. Accept PDFs in [LANGUAGE]
2. Use multilingual embedding model (e.g., multilingual-e5-large)
3. Allow queries in both English and [LANGUAGE]
4. Generate responses in user's language
5. Handle mixed-language documents (e.g., English paper with [LANGUAGE] quotes)

Changes needed:
1. Update embedding model in config
2. Add language detection for documents
3. Modify prompts to request responses in detected language
4. Add language selector to UI
5. Test with sample [LANGUAGE] papers

Target languages: [LIST]
```

---

## 🐛 Debugging & Optimization Prompts

### 10. Debug Slow Retrieval

```
My retrieval is taking 30+ seconds per query, which is too slow.

Profile and optimize:
1. Measure time for each step:
   - Embedding generation
   - Vector search
   - Document loading
   - LLM generation

2. Identify bottleneck

3. Implement fixes:
   - Cache embeddings if query is repeated
   - Batch document loading
   - Use faster embedding model
   - Implement streaming for LLM responses

4. Add progress indicators so user knows what's happening

Current setup:
- Document count: [NUMBER]
- Embedding model: [MODEL]
- Vector DB: [CHROMA/QDRANT]
- LLM: [MODEL]

Target: <5 seconds per query
```

---

### 11. Fix Memory Issues

```
Getting "Out of Memory" errors when processing large PDFs.

Debug and fix:
1. Profile memory usage during ingestion
2. Identify memory-intensive operations

Implement fixes:
- Process PDFs one at a time instead of loading all
- Clear memory after each document
- Use generators instead of loading all chunks
- Set max chunk size limit
- Add memory monitoring with warnings

Add configuration:
- MAX_PDF_SIZE_MB (skip files larger than this)
- BATCH_SIZE (number of documents to process together)
- ENABLE_MEMORY_MONITORING (log memory usage)

My system:
- RAM: [AMOUNT]
- Typical PDF size: [SIZE]
- Number of PDFs: [NUMBER]
```

---

### 12. Improve RAG Answer Quality

```
RAG answers are sometimes generic or miss important details from documents.

Improve answer quality by:

1. **Better prompting**:
   - Add "think step-by-step" instructions
   - Request specific evidence from documents
   - Ask for confidence level per claim
   - Require inline citations

2. **Retrieval improvements**:
   - Increase k (number of retrieved docs) to 10
   - Add contextual compression
   - Implement reranking

3. **Response validation**:
   - Check if answer uses retrieved documents (not just LLM knowledge)
   - Flag when answer is uncertain
   - Suggest follow-up questions

4. **Evaluation metrics**:
   - Add answer relevance scoring
   - Add citation accuracy checking
   - Log quality metrics

Modify modules/literature_review_graph.py to implement these.
```

---

## 📊 Analysis & Export Prompts

### 13. Create Custom Export Formats

```
Add export functionality for qualitative codes to:

1. **NVivo format** (.nvp or XML):
   - Hierarchical code structure
   - Coded segments with source info
   - Code definitions

2. **Atlas.ti format** (.atlproj):
   - Codes with families
   - Quotations with locations
   - Networks (if applicable)

3. **Excel format**:
   - Sheet 1: Codebook (codes, definitions, frequencies)
   - Sheet 2: Code-Quote matrix
   - Sheet 3: Theme hierarchy

4. **Interactive HTML report**:
   - Collapsible code hierarchy
   - Clickable quotes (show full context)
   - Visualizations (code frequency, co-occurrence)

Add to backend/core/export_manager.py
Add export buttons to Gradio interface with format selector.
```

---

### 14. Generate Research Visualizations

```
Add automatic visualization generation for literature reviews.

Create:
1. **Citation network graph**:
   - Nodes: papers
   - Edges: citations between papers
   - Size: citation count
   - Color: publication year

2. **Concept co-occurrence network**:
   - Nodes: key concepts extracted from papers
   - Edges: appear together in same paper
   - Interactive (click to see relevant papers)

3. **Timeline of research**:
   - X-axis: year
   - Y-axis: number of papers
   - Colored by methodology or theme

4. **Author collaboration network**:
   - Nodes: authors
   - Edges: co-authorship
   - Size: number of publications

Use: NetworkX for graph creation, Plotly for interactive visualization
Add "Generate Visualizations" button that creates all 4 and displays in tabs
Save as HTML files in outputs/ directory
```

---

### 15. Automated Literature Monitoring

```
Implement automated monitoring for new papers on my research topic.

Features:
1. **Source integration**:
   - Google Scholar alerts
   - PubMed RSS feeds
   - arXiv API
   - CrossRef API

2. **Automated workflow**:
   - Check for new papers weekly (configurable)
   - Download PDFs automatically (if available)
   - Ingest into RAG system
   - Analyze relevance to current project
   - Send email digest of highly relevant papers

3. **Relevance filtering**:
   - Compare to existing papers in collection
   - Score relevance using embeddings
   - Only notify if relevance score > threshold

4. **Email report format**:
   - Subject: "5 new papers on [topic]"
   - Body: Title, authors, abstract, relevance score, why relevant
   - Link to query in RAG system

Implement as scheduled task (use APScheduler).
Add configuration in monitoring_config.yaml

My topics to monitor: [LIST TOPICS]
Email: [YOUR EMAIL]
Frequency: [daily/weekly/monthly]
```

---

## 🎓 Research-Specific Prompts

### 16. Meta-Analysis Data Extraction

```
Add automated extraction of statistical data for meta-analysis.

Extract from papers:
1. **Effect sizes**:
   - Cohen's d
   - Pearson's r
   - Odds ratios
   - Other standardized effect sizes

2. **Sample information**:
   - Total N
   - N per group
   - Demographics (age, gender distribution)

3. **Study characteristics**:
   - Design (experimental/quasi-experimental/observational)
   - Outcome measures used
   - Follow-up period (if longitudinal)

4. **Quality indicators**:
   - Randomization (yes/no)
   - Blinding
   - Attrition rate
   - Risk of bias indicators

Output format:
- CSV with one row per study
- Columns for all extracted fields
- Confidence scores for each extraction
- Source quotes as evidence

Add "Extract for Meta-Analysis" button to literature review interface.
Implement in modules/meta_analysis_extractor.py
```

---

### 17. Research Gap Identification

```
Add intelligent research gap identification.

Analyze corpus to find:

1. **Understudied areas**:
   - Topics mentioned but not deeply explored
   - Populations rarely studied
   - Methods not commonly applied to this domain

2. **Contradictory findings**:
   - Papers with conflicting results
   - Explain potential reasons for discrepancies

3. **Methodological gaps**:
   - Limitations acknowledged across papers
   - Call for new approaches

4. **Temporal gaps**:
   - Topics with no recent research
   - Emerging areas with little empirical work

5. **Contextual gaps**:
   - Geographic regions not covered
   - Settings not examined

Output format:
- Structured report with sections for each gap type
- Supporting evidence from papers
- Suggested research questions to address gaps
- Estimated impact/feasibility of each gap

Add "Identify Research Gaps" button to interface.
Generate report as markdown and HTML.
```

---

### 18. Grant Proposal Assistant

```
Create a grant proposal writing assistant using RAG.

Features:

1. **Literature Review Section**:
   Query: "Generate literature review for [topic]"
   Output: Structured review with citations, organized by themes

2. **Significance & Innovation Section**:
   - Automatically identify gaps your project addresses
   - Compare to existing work to show novelty
   - Generate "intellectual merit" paragraph

3. **Preliminary Work Section**:
   - Query your research notes for relevant past work
   - Summarize your contributions
   - Generate publication list

4. **Research Design Section**:
   - Find papers using similar methodologies
   - Extract best practices and considerations
   - Suggest potential limitations and solutions

5. **Budget Justification**:
   - Find typical costs in similar studies
   - Generate justification based on literature

Add "Grant Assistant" tab to Gradio interface.
Implement in modules/grant_assistant.py
Include templates for NSF, NIH, and other common formats.
```

---

## 🔐 Privacy & Security Prompts

### 19. Add Local LLM Support

```
Add support for running completely locally (no API calls) for sensitive data.

Requirements:
1. Use Ollama for local LLM inference
2. Supported models:
   - Llama 3 (8B or 70B)
   - Mistral 7B
   - Mixtral 8x7B

3. Configuration:
   - Toggle between cloud and local in settings
   - Adjust parameters for local models (lower temperature, etc.)
   - Fallback to cloud if local fails

4. Performance optimization:
   - Use quantized models (Q4 or Q5)
   - Batch processing where possible
   - Cache results

Add installation instructions for Ollama in README.
Update config.py to support local model selection.
Test with sample queries and compare quality to Claude.

Preferred local model: [MODEL NAME]
Available VRAM: [AMOUNT]
```

---

### 20. Implement Data Encryption

```
Add encryption for sensitive research data.

Requirements:
1. Encrypt all documents at rest (in vector database)
2. Encrypt metadata in PostgreSQL
3. Encrypt API keys in .env file
4. Use HTTPS for all communications

Implementation:
1. Use cryptography library (Fernet)
2. Generate encryption key per user/project
3. Store key securely (environment variable or key management service)
4. Decrypt on-the-fly during retrieval

Add encryption toggle in settings:
- "Encrypt sensitive data" checkbox
- Key generation on first enable
- Warning about key backup

Modify:
- backend/core/ingestion.py (encrypt before storing)
- backend/core/retrieval.py (decrypt after retrieving)
- Add encryption_manager.py utility

Security level needed: [STANDARD/HIGH/MAXIMUM]
Compliance requirements: [IRB/HIPAA/GDPR/etc.]
```

---

## 📈 Advanced Features

### 21. Implement GraphRAG

```
Add GraphRAG capability for better relationship understanding.

Convert documents to knowledge graphs:
1. Extract entities (concepts, authors, methods, findings)
2. Extract relationships between entities
3. Build graph structure (NetworkX or Neo4j)
4. Use graph for enhanced retrieval

Retrieval process:
1. Query → Find relevant nodes
2. Traverse graph to find connected information
3. Retrieve full documents for relevant nodes
4. Use LLM with graph context + documents

Add to modules/graph_rag.py
Add "Enable GraphRAG" toggle to settings
Visualize knowledge graph in interface

Use cases:
- "Show me connections between [concept A] and [concept B]"
- "What methods have been used to study [concept]?"
- "Find papers that bridge [topic 1] and [topic 2]"
```

---

### 22. Add Evaluation & Benchmarking

```
Implement evaluation framework to measure RAG quality.

Metrics to track:

1. **Retrieval Quality**:
   - Precision@k (how many retrieved docs are relevant)
   - Recall@k (how many relevant docs were retrieved)
   - MRR (Mean Reciprocal Rank)

2. **Answer Quality**:
   - Faithfulness (answer grounded in documents)
   - Answer relevance (answers the question)
   - Context relevance (retrieved docs are relevant)

3. **User Metrics**:
   - Time to answer
   - User satisfaction ratings
   - Follow-up query rate

Implementation:
1. Create test dataset (questions + expected answers)
2. Run evaluation automatically on each code change
3. Generate evaluation report
4. Track metrics over time

Add to tests/evaluation/
Create benchmark dashboard (Streamlit)
Log all queries and results for analysis

Create test dataset for: [YOUR DOMAIN]
Target metrics: [LIST PRIORITIES]
```

---

## 💬 Prompt Templates for Common Tasks

### 23. Quick Bug Fix Template

```
I'm encountering this error:

[PASTE ERROR MESSAGE]

Context:
- What I was trying to do: [DESCRIBE]
- Steps to reproduce:
  1. [STEP 1]
  2. [STEP 2]
  3. [ERROR OCCURS]

System info:
- OS: [YOUR OS]
- Python version: [VERSION]
- ResearcherRAG version: [VERSION]
- Relevant config settings: [PASTE]

Please:
1. Diagnose the issue
2. Suggest fix
3. Implement fix if it's code-related
4. Add error handling to prevent in future
```

---

### 24. Feature Request Template

```
I need to add a feature: [DESCRIBE FEATURE]

Use case:
[Describe how you would use this feature]

User flow:
1. User does X
2. System does Y
3. User sees Z

Technical considerations:
- Should integrate with: [EXISTING MODULES]
- UI element needed: [BUTTON/TAB/DROPDOWN/etc.]
- Data storage: [WHERE TO STORE]

Similar features:
[Link to similar features in other tools if applicable]

Priority: [LOW/MEDIUM/HIGH]
Timeline: [WHEN DO YOU NEED THIS]
```

---

## 🎯 Domain-Specific Prompt Collections

### For Education Researchers

```
Customize ResearcherRAG for education research.

Add education-specific features:
1. ERIC database integration (search and import)
2. Common Core standards tagger (tag papers by standards addressed)
3. Grade-level filter (K-5, 6-8, 9-12, Higher Ed)
4. Intervention type classifier (technology, curriculum, professional development, etc.)
5. Education research quality rubric (What Works Clearinghouse standards)

Modify prompts to use education terminology.
Add education-specific metadata fields.
Create education research report templates.
```

### For Psychology Researchers

```
Customize ResearcherRAG for psychology research.

Add:
1. PubMed/PsycINFO integration
2. DSM-5 category tagger
3. Construct tagger (from constructs database)
4. Measurement instrument extractor (identify scales used)
5. PRISMA-P checklist generator for systematic reviews
6. Pre-registration template generator

Add psychology-specific prompts:
- Theory extraction (CBT, psychodynamic, etc.)
- Population characteristics
- Treatment/intervention analysis
```

### For Sociology Researchers

```
Customize ResearcherRAG for sociology research.

Add:
1. Census data integration
2. Sociological theory tagger (conflict theory, functionalism, etc.)
3. Methodology classifier (survey, ethnography, etc.)
4. Population demographics analyzer
5. Social inequality metrics extractor

Prompts for:
- Theory comparison and synthesis
- Mixed methods integration
- Policy implications extraction
```

---

## 📚 Learning & Tutorial Prompts

### 25. Generate Interactive Tutorial

```
Create an interactive tutorial for new users of ResearcherRAG.

Tutorial should:
1. Walk through uploading first 5 papers
2. Demonstrate different query types
3. Show how to interpret results
4. Explain citation tracking
5. Practice with qualitative coding (using sample interviews)

Format:
- Jupyter notebook with embedded Gradio interface
- Step-by-step instructions
- "Try it yourself" exercises
- Solutions provided

Include sample data:
- 10 education research papers
- 5 interview transcripts
- Sample research notes

Save as tutorials/getting_started.ipynb
Make available via Binder for cloud execution.
```

---

This is a living document - add your own successful prompts and share with the community! 🚀

**Pro tip**: Replace bracketed placeholders [LIKE THIS] with your specific details before sending to Claude Code.
