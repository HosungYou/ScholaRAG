---
layout: default
title: Glossary
nav_order: 2
description: "Searchable glossary of key terms in ResearcherRAG"
---

# Glossary
{: .no_toc }

Searchable reference for all key terms, concepts, and components in ResearcherRAG.
{: .fs-6 .fw-300 }

---

## 🔍 Quick Search Tips

**Use the search box above to find terms instantly!**

**Popular searches**:
- `PRISMA` → PRISMA 2020, PRISMA Flowchart, 6-Dimension Criteria
- `RAG` → RAG System, Vector Database, Embeddings, Semantic Search
- `Stage` → Stage 1-6, Stage Mapping Table
- `Script` → 01-07 scripts, Execution, Query
- `Metrics` → Relevance Rate, PDF Success Rate, Chunks per Paper

[View full search guide]({{ site.baseurl }}{% link search-guide.md %}) for advanced search techniques.

---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Methodology & Frameworks

### PRISMA 2020
{: .d-inline-block }

Framework
{: .label .label-purple }

**Preferred Reporting Items for Systematic Reviews and Meta-Analyses** - An evidence-based methodology for conducting transparent, rigorous systematic literature reviews.

**Used in**: [Stages 1-4]({{ site.baseurl }}{% link stages/index.md %})

**Key components**:
- Identification: Database searching
- Screening: Applying inclusion/exclusion criteria
- Eligibility: Full-text assessment
- Inclusion: Final paper selection

**Related terms**: [PRISMA Flowchart](#prisma-flowchart), [Screening](#screening), [6-Dimension Criteria](#6-dimension-criteria)

**Learn more**: [PRISMA 2020 Official Site](http://www.prisma-statement.org/)

---

### RAG (Retrieval-Augmented Generation)
{: .d-inline-block }

Technology
{: .label .label-blue }

AI system that retrieves relevant document chunks from a vector database and uses an LLM to generate citation-backed answers.

**Components**:
1. **Vector Database** ([ChromaDB](#chromadb))
2. **Embeddings** (semantic representation of text)
3. **Retrieval** (semantic search for relevant chunks)
4. **Generation** (LLM synthesizes answer with citations)

**Used in**: [Stages 3-5]({{ site.baseurl }}{% link stages/index.md %})

**Related terms**: [Vector Database](#vector-database), [Embeddings](#embeddings), [Semantic Search](#semantic-search), [ChromaDB](#chromadb)

**Why paired with PRISMA**: RAG analyzes papers selected by PRISMA, ensuring high-quality, relevant answers.

---

### Systematic Literature Review
{: .d-inline-block }

Methodology
{: .label .label-purple }

A rigorous, transparent, and reproducible method for identifying, screening, and analyzing academic literature on a specific research question.

**Key characteristics**:
- Predefined search strategy
- Explicit inclusion/exclusion criteria
- Transparent reporting
- Reproducible process

**Traditional time**: 6-8 weeks
**With ResearcherRAG**: 2-3 weeks (67-75% time savings)

**Related terms**: [PRISMA 2020](#prisma-2020), [Meta-Analysis](#meta-analysis)

---

## Stages (User-Facing)

### Stage 1: Planning
{: .d-inline-block }

User Stage
{: .label .label-green }

**Duration**: 35-50 minutes (active conversation)

**What you do**:
- Define research question
- Set scope constraints (year range, languages, study types)
- Design Boolean search query

**Behind the scenes**:
- [Prompt 01]({{ site.baseurl }}{% link reference/prompts.md %}#01-research-domain-setup) guides research scope definition
- [Prompt 02]({{ site.baseurl }}{% link reference/prompts.md %}#02-query-strategy) guides query design
- Claude Code creates `config.yaml` automatically

**Expected outputs**:
- `config.yaml` with research question, databases, year range
- `.researcherrag/context.json` tracking progress

**Maps to prompts**: 01-02

---

### Stage 2: PRISMA Setup
{: .d-inline-block }

User Stage
{: .label .label-green }

**Duration**: 25-35 minutes

**What you do**:
- Configure [6-Dimension Criteria](#6-dimension-criteria)
- Set scoring threshold (typically 4/6)
- Review example papers to validate criteria

**Behind the scenes**:
- [Prompt 03]({{ site.baseurl }}{% link reference/prompts.md %}#03-prisma-configuration) guides PRISMA configuration
- PRISMA criteria saved to `config.yaml`

**Expected outputs**:
- PRISMA criteria in `config.yaml`
- Threshold configuration

**Maps to prompts**: 03

---

### Stage 3: RAG Design
{: .d-inline-block }

User Stage
{: .label .label-green }

**Duration**: 20-30 minutes

**What you do**:
- Choose [embedding model](#embeddings) (OpenAI vs sentence-transformers)
- Configure [chunking](#chunking) (size, overlap)
- Set retrieval parameters (top-k, similarity threshold)

**Behind the scenes**:
- [Prompt 04]({{ site.baseurl }}{% link reference/prompts.md %}#04-rag-design) guides RAG architecture
- RAG configuration saved to `config.yaml`

**Expected outputs**:
- RAG config in `config.yaml`
- Embedding model selection
- Chunking strategy

**Maps to prompts**: 04

---

### Stage 4: Execution
{: .d-inline-block }

User Stage
{: .label .label-green }

**Duration**: 2-4 hours (automated)

**What you do**:
- Click "Execute" in Claude Code
- Monitor progress (optional)

**Behind the scenes**:
- [Prompt 05]({{ site.baseurl }}{% link reference/prompts.md %}#05-execution-plan) triggers automated execution
- [Scripts 01-05]({{ site.baseurl }}{% link reference/scripts.md %}) run sequentially:
  1. Fetch papers (10-30 min)
  2. Deduplicate (1-5 min)
  3. Screen with PRISMA (5-20 min)
  4. Download PDFs (1-3 hours)
  5. Build RAG (10-30 min)

**Expected outputs**:
- `data/01_identification/deduplicated.csv` (~400 papers)
- `data/02_screening/relevant_papers.csv` (~75 papers, 26% relevance)
- `data/03_pdfs/*.pdf` (~45 PDFs, 60% success rate)
- `data/04_rag/chroma_db/` (vector database)

**Maps to prompts**: 05
**Maps to scripts**: 01-05

---

### Stage 5: Analysis
{: .d-inline-block }

User Stage
{: .label .label-green }

**Duration**: Ongoing

**What you do**:
- Run `python scripts/06_query_rag.py --interactive`
- Ask questions about your literature
- Extract insights with citations

**Behind the scenes**:
- [Prompt 06]({{ site.baseurl }}{% link reference/prompts.md %}#06-research-conversation) guides RAG querying
- [Script 06]({{ site.baseurl }}{% link reference/scripts.md %}#06-query-rag) provides interactive interface

**Example queries**:
```
"What methodologies are used across my papers?"
"Extract all correlation coefficients for speaking skills"
"Which studies used randomized controlled trials?"
```

**Expected outputs**:
- Answers with paper citations
- Conversation logs (optional)

**Maps to prompts**: 06
**Maps to scripts**: 06

---

### (Optional) Stage 6: Documentation
{: .d-inline-block }

User Stage
{: .label .label-green }

**Duration**: 30-60 minutes

**What you do**:
- Generate [PRISMA Flowchart](#prisma-flowchart)
- Export conversation logs
- Create synthesis report

**Behind the scenes**:
- [Prompt 07]({{ site.baseurl }}{% link reference/prompts.md %}#07-documentation-writing) guides documentation
- [Script 07]({{ site.baseurl }}{% link reference/scripts.md %}#07-generate-prisma) generates flowchart

**Expected outputs**:
- `outputs/prisma_flowchart.png`
- `outputs/prisma_stats.json`

**Maps to prompts**: 07
**Maps to scripts**: 07

---

## Technical Components

### ChromaDB
{: .d-inline-block }

Technology
{: .label .label-blue }

Open-source vector database for storing and querying document embeddings. ResearcherRAG's default vector store.

**Purpose**: Semantic search across PRISMA-selected papers

**Alternative**: FAISS, Pinecone, Weaviate

**Used in**: [Stage 5 (Build RAG)]({{ site.baseurl }}{% link stages/04-execution.md %}#stage-5-build-rag)

**File location**: `data/04_rag/chroma_db/`

**Related terms**: [Vector Database](#vector-database), [Embeddings](#embeddings)

---

### Vector Database
{: .d-inline-block }

Concept
{: .label .label-yellow }

A database that stores **embeddings** (numerical representations of text) and enables **semantic search** (finding similar meaning, not just keyword matching).

**In ResearcherRAG**: Stores chunks from PRISMA-selected papers

**Implementation**: [ChromaDB](#chromadb)

**Example**:
```
Query: "What are the benefits of chatbot interventions?"
Vector DB finds: Papers discussing "advantages", "positive outcomes",
                 "improvements" (semantic similarity, not just keyword "benefits")
```

**Related terms**: [ChromaDB](#chromadb), [Embeddings](#embeddings), [Semantic Search](#semantic-search)

---

### Embeddings
{: .d-inline-block }

Concept
{: .label .label-yellow }

Numerical representations of text that capture semantic meaning. Similar texts have similar embeddings.

**In ResearcherRAG**:
- Each paper chunk → 384-dimension vector (sentence-transformers) or 1536-dimension (OpenAI)
- Vectors stored in [ChromaDB](#chromadb)
- Semantic search uses vector similarity

**Model options**:
- `sentence-transformers/all-MiniLM-L6-v2` (free, fast, 384-dim)
- `text-embedding-ada-002` (OpenAI, paid, high-quality, 1536-dim)

**Related terms**: [Vector Database](#vector-database), [Semantic Search](#semantic-search)

---

### Chunking
{: .d-inline-block }

Process
{: .label .label-yellow }

Splitting long documents into smaller semantic units (~500-2000 tokens) for embedding and retrieval.

**Parameters**:
- **Chunk size**: Typically 1000 tokens (balances context vs precision)
- **Overlap**: Typically 200 tokens (10-20% of chunk size, preserves context)

**Example**:
```
Paper (10,000 tokens)
  ↓ Chunk with size=1000, overlap=200
30 chunks (some overlap between adjacent chunks)
```

**Trade-offs**:
- Larger chunks: More context, but less precise retrieval
- Smaller chunks: More precise, but may lose context

**Related terms**: [Embeddings](#embeddings), [RAG](#rag-retrieval-augmented-generation)

---

### Semantic Search
{: .d-inline-block }

Concept
{: .label .label-yellow }

Search based on **meaning** rather than keywords. Uses [embeddings](#embeddings) to find similar concepts.

**Example**:
```
Keyword search: "chatbot" only finds exact word "chatbot"
Semantic search: "chatbot" also finds "conversational agent",
                 "virtual assistant", "dialogue system"
```

**How it works**:
1. Query → Embedding
2. Find chunks with similar embeddings (cosine similarity)
3. Retrieve top-k most similar chunks

**Related terms**: [Vector Database](#vector-database), [Embeddings](#embeddings)

---

## PRISMA-Specific Terms

### 6-Dimension Criteria
{: .d-inline-block }

PRISMA
{: .label .label-purple }

ResearcherRAG's PRISMA screening system uses 6 dimensions to score paper relevance:

1. **Domain**: Correct research field? (e.g., Education, Medicine)
2. **Method**: Right methodology? (e.g., Experimental, Qualitative)
3. **Topic**: Specific topic match? (e.g., AI chatbots, not general EdTech)
4. **Context**: Appropriate setting? (e.g., University, K-12)
5. **Exclusion**: Quality standards met? (e.g., Peer-reviewed, not blog post)
6. **Title**: Title suggests relevance? (Quick filter)

**Scoring**:
- Each dimension: 0 (not met) or 1 (met)
- Total score: 0-6
- Threshold: Typically 4/6 to pass

**Example**:
```
Paper: "AI Chatbots for ESL Speaking Practice in Universities"
- Domain: Education ✅ (1)
- Method: Experimental ✅ (1)
- Topic: AI chatbots for speaking ✅ (1)
- Context: University ✅ (1)
- Exclusion: Peer-reviewed ✅ (1)
- Title: Highly relevant ✅ (1)
Total: 6/6 → PASS
```

**Used in**: [Stage 2 (PRISMA Setup)]({{ site.baseurl }}{% link stages/02-prisma.md %})

---

### PRISMA Flowchart
{: .d-inline-block }

Output
{: .label .label-purple }

Visual diagram showing paper flow through PRISMA stages, with counts at each step.

**Standard structure**:
```
Records identified (n=500)
  ↓ (-100 duplicates removed)
Records screened (n=400)
  ↓ (-325 excluded by criteria)
Reports assessed for eligibility (n=75)
  ↓ (-30 PDFs not available)
Studies included in review (n=45)
```

**Generated by**: [Script 07]({{ site.baseurl }}{% link reference/scripts.md %}#07-generate-prisma)

**Output file**: `outputs/prisma_flowchart.png`

**Critical rule**: Numbers MUST be actual counts from pipeline (never fabricated)

---

### Screening
{: .d-inline-block }

Process
{: .label .label-purple }

Applying [6-Dimension Criteria](#6-dimension-criteria) to determine if papers are relevant.

**Execution**: [Script 03 (screen_papers.py)]({{ site.baseurl }}{% link reference/scripts.md %}#03-screen-papers)

**Method**: LLM-powered (Claude) reads abstracts and scores each dimension

**Typical results**:
- Relevance rate: 15-40% (field-dependent)
- Education: ~25-30%
- Medicine: ~15-25% (more specific)

**Input**: `data/01_identification/deduplicated.csv`
**Output**: `data/02_screening/relevant_papers.csv`

---

## Process Terms

### Configure
{: .d-inline-block }

Action
{: .label .label-green }

Set up criteria, parameters, or settings **before execution**.

**Used in**: Stages 1-3

**Examples**:
- Configure research question (Stage 1)
- Configure PRISMA criteria (Stage 2)
- Configure RAG architecture (Stage 3)

**Opposite**: [Execute](#execute)

---

### Execute
{: .d-inline-block }

Action
{: .label .label-green }

**Run scripts** to perform automated tasks.

**Used in**: Stage 4

**What executes**:
- Fetch papers
- Deduplicate
- Screen with PRISMA
- Download PDFs
- Build RAG

**Opposite**: [Configure](#configure)

---

### Query
{: .d-inline-block }

Action
{: .label .label-green }

**Ask questions** to the RAG system.

**Used in**: Stage 5

**Examples**:
```
"What methodologies are used?"
"Extract all correlation coefficients"
"Which studies show positive outcomes?"
```

**Interface**: [Script 06 (query_rag.py)]({{ site.baseurl }}{% link reference/scripts.md %}#06-query-rag)

---

## Statistical Terms

### Relevance Rate
{: .d-inline-block }

Metric
{: .label .label-yellow }

Percentage of papers that pass PRISMA screening.

**Formula**: `Relevant papers / Total papers screened`

**Typical ranges**:
- 15-40% (varies by field and query specificity)
- Education: 25-30%
- Medicine: 15-25%

**Example**:
```
400 papers screened → 75 relevant
Relevance rate = 75/400 = 18.75%
```

**Interpretation**:
- <10%: Criteria may be too strict or query too broad
- >70%: Criteria may be too loose or query too specific

---

### PDF Success Rate
{: .d-inline-block }

Metric
{: .label .label-yellow }

Percentage of papers for which PDFs are successfully downloaded.

**Formula**: `Downloaded PDFs / Papers to download`

**Typical ranges**:
- 30-80% (highly variable)
- Open Access fields (CS, preprints): 60-80%
- Paywalled fields (Medicine, journals): 30-50%

**Why low is normal**:
- Many papers behind paywalls
- Broken DOI links
- Publisher restrictions

**Example**:
```
75 papers to download → 45 PDFs downloaded
Success rate = 45/75 = 60%
```

---

### Chunks per Paper
{: .d-inline-block }

Metric
{: .label .label-yellow }

Average number of chunks created from each paper during RAG building.

**Formula**: `Total chunks / Total papers`

**Typical range**: 5-100 (depends on paper length and chunk size)

**Example**:
```
45 papers → 1,350 chunks
Chunks per paper = 1,350/45 = 30 chunks/paper
```

**Interpretation**:
- <5: Papers very short or chunk size too large
- >100: Papers very long or chunk size too small

---

## File Types

### config.yaml
{: .d-inline-block }

File
{: .label .label-blue }

YAML file storing all project configuration (research question, databases, PRISMA criteria, RAG settings).

**Created**: Stage 1 (Planning)
**Updated**: Stages 1-3 (as configuration evolves)

**Example structure**:
```yaml
project_name: "AI Chatbots Language Learning"
research_question: "How do AI chatbots improve speaking skills?"
databases: ["semantic_scholar", "openalex", "arxiv"]
query: "(chatbot OR agent) AND language learning"
prisma_criteria:
  domain_keywords: ["education", "learning"]
  min_score: 4
rag_config:
  chunk_size: 1000
  chunk_overlap: 200
  embedding_model: "sentence-transformers/all-MiniLM-L6-v2"
```

---

### context.json
{: .d-inline-block }

File
{: .label .label-blue }

JSON file tracking current stage, completed stages, and project metadata.

**Location**: `.researcherrag/context.json`

**Purpose**: Enables "continue my research" functionality

**Example**:
```json
{
  "current_stage": 3,
  "completed_stages": [1, 2],
  "project_name": "AI Chatbots Language Learning",
  "last_updated": "2025-10-14T10:30:00Z"
}
```

**Updated**: After each stage completion

---

## Common Abbreviations

| Abbreviation | Full Term | Definition |
|--------------|-----------|------------|
| **PRISMA** | Preferred Reporting Items for Systematic Reviews and Meta-Analyses | Systematic review methodology |
| **RAG** | Retrieval-Augmented Generation | AI system combining retrieval and generation |
| **LLM** | Large Language Model | AI model (e.g., Claude, GPT) |
| **PDF** | Portable Document Format | Standard format for academic papers |
| **DOI** | Digital Object Identifier | Unique identifier for papers |
| **API** | Application Programming Interface | Interface for accessing databases |
| **CSV** | Comma-Separated Values | Spreadsheet file format |
| **JSON** | JavaScript Object Notation | Data storage format |
| **YAML** | YAML Ain't Markup Language | Human-readable config format |

---

## Stage Mapping (5 vs 7)

| User-Facing (5 Stages) | Technical (7 Prompts) | Scripts | Purpose |
|------------------------|----------------------|---------|---------|
| **Stage 1: Planning** | 01_research_domain_setup.md | - | Define research question |
|                       | 02_query_strategy.md | - | Design search query |
| **Stage 2: PRISMA Setup** | 03_prisma_configuration.md | - | Configure screening |
| **Stage 3: RAG Design** | 04_rag_design.md | - | Design vector DB |
| **Stage 4: Execution** | 05_execution_plan.md | 01-05.py | Run automated pipeline |
| **Stage 5: Analysis** | 06_research_conversation.md | 06.py | Query RAG system |
| **(Optional) Documentation** | 07_documentation_writing.md | 07.py | Generate reports |

**Why two numbering systems?**
- **5 stages**: User-friendly presentation (homepage)
- **7 prompts**: Technical accuracy (implementation)
- **Both are correct** - serve different purposes

---

## Related Resources

- [PRISMA 2020 Official Website](http://www.prisma-statement.org/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)

---

**Can't find a term?** [Open an issue on GitHub](https://github.com/HosungYou/researcherRAG/issues) to request an addition.
