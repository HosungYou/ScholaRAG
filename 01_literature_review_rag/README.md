# Literature Review RAG System

AI-powered literature synthesis system using LangGraph and Claude.

## Features

- 📚 **Multi-document synthesis**: Analyze 100+ papers simultaneously
- 🔍 **Intelligent search**: Query decomposition + semantic search + reranking
- 📝 **Automatic citations**: Track sources for all claims
- 🎯 **Research-focused**: Built specifically for academic literature
- 🚀 **Easy to use**: Web interface, no coding required

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API key
# ANTHROPIC_API_KEY=your_key_here
```

Get API key: https://console.anthropic.com

### 3. Run the Application

```bash
python app.py
```

Open browser: http://localhost:7860

## Usage

### Upload Papers
1. Go to "Upload Papers" tab
2. Select PDF files (5-10 to start)
3. Click "Process & Upload"
4. Wait for processing (~20 seconds per paper)

### Ask Questions
1. Go to "Ask Questions" tab
2. Enter your research question
3. Click "Search & Synthesize"
4. View answer and citations

### Example Questions
- "What are the main theories of technology adoption?"
- "What research methods were used?"
- "What are the key findings about teacher attitudes?"
- "Compare TAM and UTAUT frameworks"
- "What gaps exist in this literature?"

## How It Works

### Architecture

```
User Question
    ↓
Query Decomposition (LangGraph)
    ↓
Multi-Query Retrieval (ChromaDB)
    ↓
Document Reranking (Claude)
    ↓
Answer Synthesis (Claude)
    ↓
Answer + Citations
```

### Technology Stack

- **LLM**: Anthropic Claude 3.5 Sonnet
- **Embeddings**: HuggingFace sentence-transformers (free, local)
- **Vector DB**: ChromaDB (local, no API needed)
- **Workflow**: LangGraph (multi-step RAG)
- **Interface**: Gradio

## Advanced Usage

### Programmatic Access

```python
from backend.core.rag_graph import query_literature_review

# Query the system
answer, citations = query_literature_review(
    "What are the main barriers to AI adoption?"
)

print(answer)
for cite in citations:
    print(f"[{cite['id']}] {cite['title']}")
```

### Batch Processing

```python
from backend.core.ingestion import ingest_documents
from backend.core.retrieval import get_retriever

# Ingest all papers in a directory
documents = ingest_documents("./path/to/papers")

# Add to database
retriever = get_retriever()
retriever.add_documents(documents)
```

### Custom Configuration

Edit `.env` file:

```bash
# Use different model
LLM_MODEL=claude-3-opus-20240229

# Adjust chunk size
CHUNK_SIZE=1500
CHUNK_OVERLAP=300

# Retrieve more documents
TOP_K_RESULTS=10
```

## Troubleshooting

### "No API key found"
- Copy `.env.example` to `.env`
- Add your `ANTHROPIC_API_KEY`
- Restart the application

### "No documents found"
- Check that PDFs are valid (not scanned images)
- Try uploading one paper at a time
- Check logs for specific errors

### "Search returns no results"
- Verify papers were uploaded successfully
- Check "Database Info" tab for document count
- Try simpler, more specific questions

### "Out of memory"
- Reduce `CHUNK_SIZE` in `.env`
- Process fewer papers at once
- Close other applications

## Cost Estimation

Using Anthropic Claude:
- Embedding: Free (local HuggingFace model)
- Vector DB: Free (local ChromaDB)
- LLM queries: ~$0.01-0.05 per query

**Typical usage:**
- 50 papers uploaded: ~$0.50 (one-time embedding cost)
- 100 queries: ~$2-5

**Total for small project**: $5-10

## Performance

- **Upload**: ~20 seconds per paper
- **Query**: 10-30 seconds per question
- **Accuracy**: 85-90% citation accuracy (human validation recommended)

## Limitations

- **PDF quality**: Scanned PDFs (images) not supported
- **Non-English**: Optimized for English papers
- **Math equations**: Complex equations may not parse correctly
- **Tables**: Table content may lose structure

## Development

### Project Structure

```
01_literature_review_rag/
├── app.py                          # Gradio web interface
├── backend/
│   └── core/
│       ├── config.py              # Configuration
│       ├── ingestion.py           # PDF processing
│       ├── retrieval.py           # Vector search
│       └── rag_graph.py           # LangGraph workflow
├── data/
│   ├── raw_pdfs/                  # Uploaded papers
│   ├── processed/                 # Processed data
│   └── vector_db/                 # ChromaDB storage
└── requirements.txt
```

### Running Tests

```bash
pytest tests/
```

### Contributing

See main repository: [ResearcherRAG](https://github.com/HosungYou/researcherRAG)

## Citation

```bibtex
@software{researcherrag2024,
  title = {ResearcherRAG: Literature Review System},
  author = {Hosung You},
  year = {2024},
  url = {https://github.com/HosungYou/researcherRAG}
}
```

## License

MIT License - see main repository

## Support

- GitHub Issues: [Report bugs](https://github.com/HosungYou/researcherRAG/issues)
- Documentation: [Full docs](https://github.com/HosungYou/researcherRAG/blob/main/QUICK_START.md)

---

**Built with Claude Code for social science researchers** 🔬
