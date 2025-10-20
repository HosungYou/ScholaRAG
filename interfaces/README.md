# ScholarRAG Chat Interfaces

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
cd your-scholarag-project/
# File: claude_code_interface.py already in your project
```

### Usage

**Method 1: Interactive Mode (Recommended)**
```bash
# Run the script in your terminal
python interfaces/claude_code_interface.py

# You'll see:
📂 Loading Vector DB from ./chroma_db...
✅ Loaded 137 papers from collection 'papers'
✅ Connected to Claude API

============================================================
  ScholarRAG Interactive Chat
============================================================

Type your questions (or 'exit' to quit)

You: What are the main adoption barriers?
```

**Method 2: Single Question Mode**
```bash
# Ask one question and exit
python interfaces/claude_code_interface.py "What methodologies are most common?"
```

**Method 3: Through Claude Code**
```
You (to Claude Code): "Run python interfaces/claude_code_interface.py in interactive mode"

# Then type your questions when prompted
```

### Example Session
```bash
$ python interfaces/claude_code_interface.py

You: What methodologies are most common in my papers?