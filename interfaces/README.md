# ResearcherRAG Chat Interfaces

After building your knowledge base using Stages 1-5, you need a way to interact with your papers. This directory provides **three interface options** to chat with your RAG system.

## 📋 Quick Comparison

| Interface | Best For | Setup | Features |
|-----------|----------|-------|----------|
| **Claude Code** | Quick start, iterative research | None (use Claude Code) | CLI, conversational, code execution |
| **Streamlit** | Visual UI, presentations | `pip install streamlit` | Web UI, chat history, export |
| **FastAPI** | Custom frontend, production | `pip install fastapi uvicorn` | REST API, full control |

---

## 🤖 Option 1: Claude Code Interface (Recommended)

**Best for:** Most researchers, especially those already using Claude Code

### What is it?
A Python script you run directly in Claude Code to query your Vector DB conversationally.

### Setup
```bash
# No installation needed! Just download the script
cd your-researcherrag-project/
# File: claude_code_interface.py already in your project
```

### Usage
```python
# In Claude Code:
User: "Run claude_code_interface.py and ask: What are the key adoption barriers in healthcare?"

Claude Code executes:
→ Loads your chroma_db/
→ Searches 137 papers
→ Generates answer with citations
→ Returns: "Based on 5 relevant papers, the key barriers are..."
```

### Example Session
```
User: What methodologies are most common in my papers?