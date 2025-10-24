# config.yaml Schema Reference

**Purpose**: Complete specification of all config.yaml fields

**For**: Both Claude Code and Codex agents

**When to load**: User asks "What fields can I configure?" or encountering config validation errors

---

## Complete Schema

```yaml
# Project Metadata
project_name: string (required)
  # Descriptive project name, used for folder naming
  # Constraints: No spaces (use hyphens), 5-100 chars
  # Example: "AI-Chatbots-Speaking-Proficiency"

research_question: string (required)
  # Clear, answerable research question
  # Constraints: 20-500 chars, specific and focused
  # Example: "How do AI chatbots improve speaking proficiency in university language learners?"

research_field: string (required)
  # Academic domain/discipline
  # Allowed values: Education, Medicine, Psychology, Computer Science, Engineering, Business, etc.
  # Example: "Education"

project_type: string (required)
  # System mode: comprehensive vs focused
  # Allowed values: "knowledge_repository" | "systematic_review"
  # Default: None (must be explicitly chosen)
  # Impact:
  #   - knowledge_repository: 50% screening threshold, 10K-20K final papers
  #   - systematic_review: 90% screening threshold, 50-300 final papers

# Search Configuration
year_start: integer (optional)
  # Start of publication year range
  # Default: No constraint (all years)
  # Example: 2015

year_end: integer (optional)
  # End of publication year range
  # Default: Current year
  # Validation: Must be >= year_start, <= current year
  # Example: 2024

databases: list[string] (required)
  # Academic databases to search
  # Allowed values: ["semantic_scholar", "openalex", "arxiv"]
  # Minimum: 1 database
  # Recommended: All 3 for comprehensive coverage
  # Example: ["semantic_scholar", "openalex", "arxiv"]

search_query: string (required, set in Stage 2)
  # Boolean search query
  # Syntax: Supports AND, OR, NOT, parentheses, "exact phrases"
  # Example: '(chatbot OR "conversational agent") AND ("language learning" OR L2) AND (speaking OR oral)'

# PRISMA Configuration (set in Stage 3)
prisma:
  screening_threshold: integer (auto-set from project_type)
    # AI confidence threshold for screening
    # knowledge_repository: 50
    # systematic_review: 90
    # Range: 0-100
    # Do NOT manually override (tied to project_type)

  inclusion_criteria: list[string] (required)
    # Papers we WANT
    # Minimum: 3 criteria
    # Each criterion should be specific and checkable
    # Example:
    #   - "University/college students (higher education)"
    #   - "AI-powered chatbot or conversational agent"
    #   - "Speaking proficiency outcome measured"

  exclusion_criteria: list[string] (required)
    # Papers we DON'T want
    # Minimum: 3 criteria
    # Should complement inclusion criteria
    # Example:
    #   - "K-12 students or corporate training"
    #   - "Rule-based chatbots (non-AI)"
    #   - "No speaking outcome measured"

  ai_reviewer_prompt: string (required)
    # Instructions for AI screening
    # Should reference inclusion/exclusion criteria
    # Example: "Score 0-100% based on inclusion criteria match. Must have ALL: university population, AI chatbot, speaking outcome, empirical data."

# RAG Configuration (set in Stage 4)
rag:
  chunking:
    method: string (required)
      # Chunking strategy
      # Allowed values: "semantic" | "fixed" | "hybrid"
      # Default: "semantic"
      # Recommendations:
      #   - semantic: Most papers (paragraph-based)
      #   - hybrid: Papers with tables/figures
      #   - fixed: Technical papers with code

    chunk_size: integer (required)
      # Tokens per chunk
      # Range: 200-1000
      # Default: 500
      # Recommendations:
      #   - 300-400: Short papers, dense information
      #   - 500-600: Standard papers
      #   - 700-1000: Papers with tables, need full context

    overlap: integer (required)
      # Overlapping tokens between chunks
      # Range: 0-200
      # Default: 50
      # Percentage: ~10% of chunk_size
      # Purpose: Preserve context across chunk boundaries

    preserve_tables: boolean (optional)
      # Keep tables intact (don't split across chunks)
      # Default: false
      # Set to true if extracting statistical tables

  embedding:
    model: string (required)
      # Embedding model
      # Allowed values:
      #   - "text-embedding-3-small" (OpenAI, recommended)
      #   - "text-embedding-3-large" (OpenAI, higher quality)
      #   - "all-MiniLM-L6-v2" (local, free)
      # Default: "text-embedding-3-small"
      # Costs:
      #   - text-embedding-3-small: $0.02 / 1M tokens (~$2 for 50 papers)
      #   - text-embedding-3-large: $0.13 / 1M tokens (~$13 for 50 papers)
      #   - all-MiniLM-L6-v2: Free (runs locally)

    provider: string (required)
      # Embedding provider
      # Allowed values: "openai" | "local"
      # Default: "openai"
      # Requires: OPENAI_API_KEY env var if provider=openai

  vector_db:
    type: string (required)
      # Vector database type
      # Allowed values: "chromadb"
      # Default: "chromadb"
      # (Future: "qdrant", "pinecone", "weaviate")

    collection_name: string (required)
      # ChromaDB collection identifier
      # Default: {project_name}_papers (auto-generated)
      # Example: "ai_chatbots_speaking_proficiency_papers"

  retrieval:
    top_k: integer (required)
      # Number of chunks to retrieve per query
      # Range: 1-20
      # Default: 5
      # Recommendations:
      #   - 3-5: Focused questions (specific data extraction)
      #   - 5-10: Broad questions (thematic analysis)
      #   - 10-20: Comprehensive synthesis (literature overview)

    similarity_threshold: float (required)
      # Minimum cosine similarity to include chunk
      # Range: 0.0-1.0
      # Default: 0.7
      # Recommendations:
      #   - 0.8-0.9: High precision (only very relevant chunks)
      #   - 0.7-0.8: Balanced (recommended)
      #   - 0.5-0.7: High recall (more chunks, lower relevance)

# Target Outcomes (informational, not used by scripts)
target_paper_count: integer (optional)
  # Expected final paper count
  # knowledge_repository: 10,000-20,000
  # systematic_review: 50-300
  # Used for feasibility validation only

estimated_duration: string (optional)
  # Expected pipeline runtime
  # Format: "X-Y hours"
  # Example: "4-8 hours"
  # Used for user planning only
```

---

## Field Dependencies

### project_type → screening_threshold

```yaml
# If project_type = knowledge_repository
prisma:
  screening_threshold: 50  # Auto-set, lenient

# If project_type = systematic_review
prisma:
  screening_threshold: 90  # Auto-set, strict
```

**Do NOT manually override `screening_threshold`** - it's tied to `project_type` for methodological consistency.

### embedding.provider → API key requirement

```yaml
# If embedding.provider = openai
# Requires: export OPENAI_API_KEY='sk-...'

# If embedding.provider = local
# No API key needed
```

---

## Validation Rules

### At Stage 1 (Initialization)

**Required fields**:
- ✅ `project_name` (5-100 chars, no spaces)
- ✅ `research_question` (20-500 chars)
- ✅ `research_field` (valid domain)
- ✅ `project_type` (knowledge_repository | systematic_review)
- ✅ `databases` (at least 1)

**Optional but recommended**:
- `year_start`, `year_end` (realistic range for domain)

### At Stage 2 (Query Strategy)

**Required additions**:
- ✅ `search_query` (Boolean syntax valid)

**Validation**:
```python
# Check Boolean operators present
assert any(op in config['search_query'] for op in ['AND', 'OR', 'NOT'])

# Check query not too short (likely missing concepts)
assert len(config['search_query']) >= 20

# Check query not too long (likely overly complex)
assert len(config['search_query']) <= 500
```

### At Stage 3 (PRISMA Config)

**Required additions**:
- ✅ `prisma.inclusion_criteria` (at least 3)
- ✅ `prisma.exclusion_criteria` (at least 3)
- ✅ `prisma.ai_reviewer_prompt` (non-empty)

**Auto-set**:
- `prisma.screening_threshold` (from `project_type`)

### At Stage 4 (RAG Design)

**Required additions**:
- ✅ `rag.chunking.*` (method, chunk_size, overlap)
- ✅ `rag.embedding.*` (model, provider)
- ✅ `rag.vector_db.*` (type, collection_name)
- ✅ `rag.retrieval.*` (top_k, similarity_threshold)

**Validation**:
```python
# Overlap should be ~10% of chunk_size
assert config['rag']['chunking']['overlap'] < config['rag']['chunking']['chunk_size'] * 0.2

# top_k should be reasonable
assert 1 <= config['rag']['retrieval']['top_k'] <= 20

# Similarity threshold valid range
assert 0.0 <= config['rag']['retrieval']['similarity_threshold'] <= 1.0
```

---

## Example Complete Config

```yaml
# Project Metadata
project_name: "AI-Chatbots-Speaking-Proficiency"
research_question: "How do AI chatbots improve speaking proficiency in university-level language learners?"
research_field: "Education"
project_type: "systematic_review"

# Search Configuration
year_start: 2015
year_end: 2024
databases:
  - semantic_scholar
  - openalex
  - arxiv

search_query: '(chatbot OR "conversational agent") AND ("language learning" OR "L2 acquisition") AND (speaking OR oral OR fluency)'

# PRISMA Configuration
prisma:
  screening_threshold: 90  # Auto-set from project_type
  inclusion_criteria:
    - "University/college students (higher education)"
    - "AI-powered chatbot or conversational agent"
    - "Speaking proficiency outcome (oral skills, fluency, pronunciation)"
    - "Empirical study with data (RCT, quasi-experimental, correlational)"
    - "Peer-reviewed publication (journal or conference)"
    - "English language"
  exclusion_criteria:
    - "K-12 students or corporate training"
    - "Rule-based chatbots (non-AI)"
    - "No speaking outcome measured"
    - "Opinion pieces or non-empirical reviews"
    - "Non-English publications"
  ai_reviewer_prompt: "Score 0-100% based on inclusion criteria match. Must have ALL: university population, AI chatbot, speaking outcome, empirical data. Exclude if any exclusion criterion applies."

# RAG Configuration
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
    collection_name: "ai_chatbots_speaking_proficiency_papers"
  retrieval:
    top_k: 5
    similarity_threshold: 0.7

# Target Outcomes (informational)
target_paper_count: "50-200"
estimated_duration: "4-8 hours"
```

---

## Common Mistakes

### Mistake 1: Overriding screening_threshold

**Wrong**:
```yaml
project_type: "systematic_review"
prisma:
  screening_threshold: 70  # Manual override
```

**Why wrong**: Breaks methodological consistency. `systematic_review` requires 90% for publication-ready rigor.

**Correct**:
```yaml
project_type: "systematic_review"
prisma:
  screening_threshold: 90  # Auto-set, don't override
```

**If you want 70%**: Change `project_type` to `knowledge_repository` (which uses 50%), or manually review 70-90% papers.

### Mistake 2: Chunk overlap > chunk_size

**Wrong**:
```yaml
rag:
  chunking:
    chunk_size: 500
    overlap: 600  # Overlap > chunk_size!
```

**Why wrong**: Chunks would overlap more than their content, creating duplicates.

**Correct**:
```yaml
rag:
  chunking:
    chunk_size: 500
    overlap: 50  # ~10% of chunk_size
```

### Mistake 3: Empty search query

**Wrong**:
```yaml
search_query: "chatbot"  # Too broad, single term
```

**Why wrong**: Will fetch 50,000+ papers, overwhelming the pipeline.

**Correct**:
```yaml
search_query: '(chatbot OR agent) AND (language learning) AND speaking'
```

---

## Updating Config Mid-Pipeline

**General rule**: ✅ Safe to update BEFORE running corresponding stage

**Examples**:

**✅ SAFE - Before Stage 2**:
```bash
# Change search query before fetching papers
vim config.yaml  # Edit search_query
python scripts/01_fetch_papers.py  # Runs with new query
```

**✅ SAFE - Before Stage 3**:
```bash
# Adjust inclusion criteria before screening
vim config.yaml  # Edit prisma.inclusion_criteria
python scripts/03_screen_papers.py  # Screens with new criteria
```

**❌ UNSAFE - After Stage 3**:
```bash
# Already screened 1,000 papers, now changing criteria
vim config.yaml  # Edit prisma.inclusion_criteria
python scripts/04_download_pdfs.py  # Downloads for OLD screening results!
```

**Fix**: Re-run screening with new criteria:
```bash
rm -rf data/02_screening/*  # Delete old screening results
python scripts/03_screen_papers.py --project .  # Re-screen with new criteria
```

---

## Version History

- **v1.0** (2024-10-18): Initial schema
- **v2.0** (2024-10-24): Added RAG configuration, project_type branching

---

**Last Updated**: 2025-10-24
**Version**: 2.0
**For**: ScholaRAG v2.0+
