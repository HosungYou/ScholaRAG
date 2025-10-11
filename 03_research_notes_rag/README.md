# Research Notes RAG (Module 3)

Minimal working implementation of the personal knowledge management module described in `docs/module_4_research_notes_and_collaboration.md`.

## Features
- Markdown ingestion with YAML frontmatter, wiki-links, and highlight capture.
- Chroma-based semantic search across note chunks.
- LangChain chat workflow with note-grounded synthesis prompts.
- Gradio interface for uploading notes and asking contextual questions.

## Quick Start
```bash
cd 03_research_notes_rag
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open the URL provided by Gradio, upload a few markdown notes, and start querying your knowledge base.

## Directory Layout
```
03_research_notes_rag/
├── app.py                    # Gradio UI
├── backend/
│   └── core/
│       ├── chains.py         # LangChain orchestration
│       ├── config.py         # Settings
│       ├── notes_ingestion.py# Markdown parsing and chunking
│       ├── prompts.py        # Prompt templates
│       └── retrieval.py      # Chroma wrapper
├── data/
│   ├── notes/                # Stored markdown files
│   └── vector_db/            # Persisted vector store
├── tests/
│   └── test_notes_ingestion.py
└── requirements.txt
```

## Next Steps
- Extend ingestion to Obsidian/Notion exports.
- Persist chat history per project.
- Integrate PRISMA-style quality filters before ingestion.
- Surface backlinks and suggested connections in the UI.
```
