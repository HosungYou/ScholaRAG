# Stage 4: RAG Design

**Load when**: Stage 4 prompt or after Stage 3 complete

**Duration**: 20-30 minutes

**Goal**: Design RAG system architecture

---

## Quick Overview

**Configure**:
1. Chunking strategy (token size, overlap)
2. Embedding model (OpenAI vs local)
3. Vector database (ChromaDB settings)
4. Retrieval parameters (top-k, similarity threshold)

**Default configuration** (works for most cases):
```yaml
rag:
  chunking:
    method: "semantic"
    chunk_size: 500
    overlap: 50
  embedding:
    model: "text-embedding-3-small"
    provider: "openai"
  vector_db:
    type: "chromadb"
    collection_name: "papers"
  retrieval:
    top_k: 5
    similarity_threshold: 0.7
```

---

## Conversation Flow

### Turn 1: Explain RAG Purpose

```
YOU: "RAG (Retrieval-Augmented Generation) will let you query your papers like:

**Example queries**:
- 'What methodologies were used to measure speaking proficiency?'
- 'Extract all correlation coefficients between chatbot use and speaking scores'
- 'Summarize main findings about pronunciation improvement'

**How it works**:
1. **Chunking**: Split PDFs into ~500-token semantic chunks
2. **Embedding**: Convert chunks to vectors (OpenAI embeddings)
3. **Vector DB**: Store in ChromaDB for semantic search
4. **Retrieval**: Find most relevant chunks for your queries
5. **Generation**: Claude synthesizes answers with citations

**Default settings work for most systematic reviews**. We'll customize only if you have specific needs.

Do you have any special requirements (e.g., very long papers, need multilingual support)?"
```

### Turn 2-3: Customize If Needed

**Most users**: Use defaults

**Power users**: Customize chunking/embedding

**Example customization**:
```
USER: "My papers have lots of tables with correlation data. Will chunking preserve those?"

YOU: "Great question! Tables need special handling:

**Default chunking** (semantic):
- Splits by paragraphs (~500 tokens)
- Risk: Table rows might be split across chunks

**Recommended for your case** (table-aware):
```yaml
rag:
  chunking:
    method: "hybrid"  # Semantic + table-aware
    chunk_size: 800  # Larger to fit full tables
    overlap: 100  # More overlap to preserve context
    preserve_tables: true  # Keep tables intact
```

**Impact**:
- ✅ Full tables stay in single chunks
- ✅ Query 'Extract correlation coefficients' returns complete tables
- ⚠️ Slightly larger chunks (800 tokens vs 500)

Shall we use table-aware chunking?"
```

### Turn 4: Save Configuration

```python
import yaml

config_path = 'projects/2025-10-24_AI-Chatbots/config.yaml'

with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

config['rag'] = {
    'chunking': {
        'method': 'semantic',
        'chunk_size': 500,
        'overlap': 50
    },
    'embedding': {
        'model': 'text-embedding-3-small',
        'provider': 'openai'
    },
    'vector_db': {
        'type': 'chromadb',
        'collection_name': f"{config['project_name'].lower().replace(' ', '_')}_papers"
    },
    'retrieval': {
        'top_k': 5,
        'similarity_threshold': 0.7
    }
}

with open(config_path, 'w') as f:
    yaml.dump(config, f, sort_keys=False)

print("✅ RAG configuration saved")
```

---

## Completion Checklist

- [ ] RAG config saved to config.yaml
- [ ] User understands RAG will be built in Stage 5
- [ ] Special requirements addressed (if any)

**If complete**: ✅ Show Stage 5 prompt

---

## Next Stage

[skills/claude_only/stage5_execution.md](stage5_execution.md)

---

**Version**: 2.0 | **Token Budget**: ~200 lines
