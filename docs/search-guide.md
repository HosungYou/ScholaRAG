---
layout: default
title: Search Guide
nav_order: 10
description: "How to search ResearcherRAG documentation effectively"
---

# Search Guide
{: .no_toc }

Learn how to use the search feature to quickly find what you need in ResearcherRAG documentation.
{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 🔍 How to Search

### Search Box Location

The search box is located at the **top of every page** in the navigation bar.

```
[🔍 Search ResearcherRAG docs...]
```

Just start typing, and results will appear instantly!

---

## 🎯 Search Tips

### 1. Search by Keyword

**Examples**:
```
Search: "PRISMA"
→ Finds: PRISMA 2020, PRISMA Flowchart, PRISMA Configuration, etc.

Search: "RAG"
→ Finds: RAG System, Build RAG, Query RAG, RAG Design, etc.

Search: "Stage 4"
→ Finds: Stage 4 Execution, Prompt 05, Scripts 01-05, etc.
```

### 2. Search by Concept

**Examples**:
```
Search: "vector database"
→ Finds: ChromaDB, Embeddings, Semantic Search

Search: "screening"
→ Finds: PRISMA Screening, 6-Dimension Criteria, Relevance Rate

Search: "chunking"
→ Finds: Chunking Strategy, Chunk Size, Chunk Overlap
```

### 3. Search by Action

**Examples**:
```
Search: "how to query"
→ Finds: Stage 5 Analysis, Script 06, Query RAG

Search: "download pdfs"
→ Finds: Stage 4 Execution, Script 04, PDF Success Rate

Search: "configure"
→ Finds: config.yaml, PRISMA Setup, RAG Design
```

### 4. Search by File or Output

**Examples**:
```
Search: "config.yaml"
→ Finds: Configuration files, Planning stage, PRISMA criteria

Search: "context.json"
→ Finds: Progress tracking, Stage completion, Continue research

Search: "prisma flowchart"
→ Finds: Documentation stage, Script 07, Output examples
```

---

## 📚 Common Search Queries

### Getting Started

| Search Query | What You'll Find |
|--------------|------------------|
| `quick start` | Installation, setup, first steps |
| `prerequisites` | Requirements, API keys, dependencies |
| `install` | Installation instructions |

### Methodology

| Search Query | What You'll Find |
|--------------|------------------|
| `PRISMA` | PRISMA 2020, screening, flowchart, methodology |
| `systematic review` | Systematic review process, PRISMA stages |
| `RAG` | RAG system, vector database, semantic search |
| `why PRISMA` | PRISMA value proposition, comparison diagrams |

### Stages

| Search Query | What You'll Find |
|--------------|------------------|
| `Stage 1` or `planning` | Research domain setup, query design |
| `Stage 2` or `PRISMA setup` | PRISMA configuration, screening criteria |
| `Stage 3` or `RAG design` | RAG architecture, embeddings, chunking |
| `Stage 4` or `execution` | Automated pipeline, scripts 01-05 |
| `Stage 5` or `analysis` | RAG queries, research conversation |

### Technical Components

| Search Query | What You'll Find |
|--------------|------------------|
| `ChromaDB` | Vector database, setup, usage |
| `embeddings` | Embedding models, sentence-transformers, OpenAI |
| `chunking` | Chunk size, overlap, strategy |
| `semantic search` | Vector similarity, retrieval, top-k |

### Scripts & Prompts

| Search Query | What You'll Find |
|--------------|------------------|
| `prompt 01` | Research domain setup prompt |
| `script 03` | PRISMA screening script |
| `05_build_rag.py` | RAG building script |
| `06_query_rag.py` | RAG query interface |

### Troubleshooting

| Search Query | What You'll Find |
|--------------|------------------|
| `low relevance` | Relevance rate troubleshooting |
| `PDF download` | PDF success rate, common issues |
| `API key` | API configuration, environment variables |
| `error` | Common errors, troubleshooting guides |

---

## 💡 Advanced Search Techniques

### 1. Use Exact Phrases

**Wrap in quotes for exact matches**:
```
Search: "6-dimension criteria"
→ Only finds exact phrase "6-dimension criteria"

Search: 6 dimension criteria
→ Finds any combination of these words
```

### 2. Search Multiple Terms

**Combine keywords**:
```
Search: "PRISMA RAG"
→ Finds pages mentioning both PRISMA and RAG

Search: "Stage 4 execution scripts"
→ Finds Stage 4, execution, and scripts
```

### 3. Search by File Type

**Find specific file types**:
```
Search: "yaml"
→ Finds: config.yaml references

Search: "csv"
→ Finds: deduplicated.csv, relevant_papers.csv

Search: "json"
→ Finds: context.json, rag_config.json
```

---

## 🎨 Search Result Features

### What You'll See

Each search result shows:

1. **Page Title** - The document where the term was found
2. **Context** - Text surrounding your search term
3. **Breadcrumb** - Location in documentation hierarchy
4. **Highlight** - Your search term highlighted in yellow

**Example**:
```
[Search: "PRISMA screening"]

Results:

📄 Glossary > Screening
   ...Applying 6-Dimension Criteria to determine if papers are
   relevant. Execution: Script 03 (screen_papers.py). Method:
   LLM-powered (Claude) reads abstracts and scores each dimension...

📄 Stage 2: PRISMA Setup
   ...Configure 6-Dimension Criteria. Set scoring threshold
   (typically 4/6). Review example papers to validate criteria...
```

---

## 🔑 Most Useful Searches for New Users

### If you want to...

**Understand what ResearcherRAG is**:
```
Search: "what is researcherrag" or "overview"
```

**Get started quickly**:
```
Search: "quick start" or "getting started"
```

**Understand PRISMA + RAG**:
```
Search: "why PRISMA" or "PRISMA RAG integration"
```

**Find specific terms**:
```
Search: "glossary" then browse all definitions
```

**Know what to expect at each stage**:
```
Search: "stage 1" or "stage 2" etc.
```

**See example projects**:
```
Search: "example" or "ai chatbots"
```

**Troubleshoot issues**:
```
Search: "common issues" or "troubleshooting"
```

---

## 📊 Search by Metric

| Search Query | What You'll Find |
|--------------|------------------|
| `relevance rate` | Expected ranges, troubleshooting |
| `success rate` | PDF download metrics, expectations |
| `chunks per paper` | RAG building metrics |
| `15-40%` | Typical relevance rate range |
| `30-80%` | Typical PDF success rate |

---

## 🗺️ Search by Stage

### Visual Stage Map

```
Search: "Stage 1" → Planning
   ├─ "prompt 01" → Research domain setup
   └─ "prompt 02" → Query strategy

Search: "Stage 2" → PRISMA Setup
   └─ "prompt 03" → PRISMA configuration

Search: "Stage 3" → RAG Design
   └─ "prompt 04" → RAG architecture

Search: "Stage 4" → Execution
   ├─ "prompt 05" → Execution plan
   ├─ "script 01" → Fetch papers
   ├─ "script 02" → Deduplicate
   ├─ "script 03" → Screen papers
   ├─ "script 04" → Download PDFs
   └─ "script 05" → Build RAG

Search: "Stage 5" → Analysis
   ├─ "prompt 06" → Research conversation
   └─ "script 06" → Query RAG

Search: "Stage 6" → Documentation (Optional)
   ├─ "prompt 07" → Documentation writing
   └─ "script 07" → Generate PRISMA flowchart
```

---

## 🚀 Quick Search Reference

### By Category

**Concepts**:
`PRISMA`, `RAG`, `systematic review`, `vector database`, `embeddings`, `semantic search`

**Stages**:
`planning`, `PRISMA setup`, `RAG design`, `execution`, `analysis`, `documentation`

**Components**:
`ChromaDB`, `Claude`, `OpenAI`, `sentence-transformers`, `LLM`

**Files**:
`config.yaml`, `context.json`, `deduplicated.csv`, `relevant_papers.csv`, `prisma_flowchart.png`

**Metrics**:
`relevance rate`, `success rate`, `chunks per paper`, `6-dimension`

**Actions**:
`configure`, `execute`, `query`, `screen`, `download`, `build`

---

## 💬 Can't Find What You're Looking For?

### Try These

1. **Check the [Glossary]({{ site.baseurl }}{% link glossary.md %})** - All terms defined
2. **Browse [5-Stage Workflow]({{ site.baseurl }}{% link stages/index.md %})** - Complete walkthrough
3. **See [Reference]({{ site.baseurl }}{% link reference/index.md %})** - All prompts, scripts, outputs
4. **Search synonyms**:
   - "vector database" = "ChromaDB"
   - "screening" = "PRISMA filtering"
   - "chunking" = "text splitting"
5. **Open a [GitHub Issue](https://github.com/HosungYou/researcherRAG/issues)** - Request documentation improvement

---

## 🎓 Search Tips from Power Users

### Tip 1: Search Before Asking
```
Before opening an issue, search:
"your question" or "error message"

Often the answer is already documented!
```

### Tip 2: Use the Glossary as Index
```
Search: "glossary"
→ Jump to Glossary
→ Browse all terms alphabetically
→ Click links to relevant pages
```

### Tip 3: Search by Expected Output
```
Want to know what Stage 4 produces?
Search: "stage 4 output" or "deduplicated.csv"
```

### Tip 4: Search by Problem
```
Facing an issue?
Search: "low relevance" or "PDF download failed"
→ Finds troubleshooting guides
```

### Tip 5: Search by Code
```
Looking for specific code?
Search: "python scripts/05" or "config.yaml example"
```

---

## 🔧 Technical Details

### How Search Works

ResearcherRAG documentation uses **Jekyll with Just the Docs theme** for search:

1. **Client-side search** - No server needed, instant results
2. **Full-text indexing** - Every word in every page is searchable
3. **Fuzzy matching** - Finds similar terms even with typos
4. **Context preview** - See surrounding text for each result
5. **Relevance ranking** - Most relevant results appear first

### What Gets Indexed

**Indexed**:
- ✅ Page titles
- ✅ Headings (H1-H6)
- ✅ Body text
- ✅ Code blocks
- ✅ Tables
- ✅ Lists

**Not Indexed**:
- ❌ Comments in code
- ❌ Image alt text (currently)
- ❌ Hidden elements

---

## 📱 Mobile Search

Search works on mobile devices too!

**On mobile**:
1. Tap the **hamburger menu** (☰) at top-left
2. Search box appears at top of menu
3. Type your query
4. Results appear below
5. Tap result to navigate

---

## ⚡ Keyboard Shortcuts

**Desktop shortcuts**:
- `/` or `Ctrl+K` - Focus search box
- `Enter` - Go to first result
- `↓` / `↑` - Navigate results
- `Esc` - Close search

---

**Happy searching!** 🔍

Need help with search? [Open an issue](https://github.com/HosungYou/researcherRAG/issues) and we'll improve this guide.
