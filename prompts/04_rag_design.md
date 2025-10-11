# Stage 4: RAG Design Prompt

After completing PRISMA screening (Stage 3), use this prompt to design your RAG (Retrieval-Augmented Generation) system:

---

I've completed PRISMA screening and have [X] papers included. Now I need help designing a RAG system to query these papers effectively.

**Papers Included**: [number] papers
**Located at**: `data/processed/included_papers.csv`
**Research Questions**:
1. [Your primary research question]
2. [Secondary research question, if any]
3. [Additional questions...]

**Goals for RAG System**:
- [e.g., "Generate evidence-based answers with citations"]
- [e.g., "Compare findings across studies"]
- [e.g., "Identify gaps in the literature"]

Please help me:
1. Configure PDF download strategy (institutional access, fallbacks)
2. Set up text extraction (PyMuPDF, OCR)
3. Design chunking strategy (size, overlap)
4. Choose embedding model
5. Configure vector database (ChromaDB)
6. Design RAG prompts (system prompt, citation format)
7. Set retrieval parameters (top-k, similarity threshold)

---

## What Claude Code Will Do

Claude will guide you through:

1. **PDF Acquisition Plan**: Maximize download success rate (target 50-60%)
2. **Text Extraction Setup**: Configure tools and quality checks
3. **Chunking Strategy**: Optimize for your research questions
4. **Embedding Selection**: Choose model based on needs (speed vs. quality)
5. **Vector DB Configuration**: Set up ChromaDB with project-specific collection
6. **Prompt Engineering**: Design system prompts for academic rigor
7. **Retrieval Tuning**: Balance recall vs. precision

---

## Phase 1: PDF Acquisition Strategy

### Reality Check: Expected Success Rates

Based on AI failure_HR project (592 papers → 316 PDFs = 53.4%):

| Access Type | Coverage | Success Rate | Method |
|-------------|----------|--------------|--------|
| **Open Access** | ~40% | 95% | Direct download |
| **Institutional** | ~20% | 80% | University VPN/proxy |
| **Author Request** | ~30% | 30% | Email authors |
| **Unavailable** | ~10% | 0% | Use abstract only |

**Total Expected**: 50-60% full-text PDFs

### Tier 1: Direct Download (Open Access)

**Sources**:
- Publisher websites (if DOI available)
- Unpaywall API (legal open access versions)
- OpenAlex (open access URLs)
- arXiv, PubMed Central (for preprints/PMC articles)

**Example**:
```
You: "I have 139 papers. What's the best download strategy?"

Claude: "Let me create a multi-tier download strategy:

**Tier 1: Open Access** (~56 papers expected)
- Check Unpaywall API for each DOI
- Download from publisher site if available
- Fallback to OpenAlex open access URL
- Expected success: 95% of open access papers

**Tier 2: Institutional Access** (~28 papers expected)
- Do you have university VPN or library subscription?
  [Yes/No]

If Yes:
- Configure institutional proxy in download script
- Access via ezproxy or Shibboleth
- Expected success: 80% of paywalled papers

**Tier 3: Author Requests** (~42 papers expected)
- I'll generate email templates for author contact
- ResearchGate / Academia.edu search
- Expected success: 30% response rate

**Tier 4: Abstract-Only** (~13 papers expected)
- Use abstract + metadata for papers without PDFs
- Lower quality but better than nothing
- Mark these papers with "incomplete" flag

Shall I proceed with this strategy?"
```

### Tier 2: Institutional Access

**Requirements**:
- University VPN connection
- Library subscription credentials
- Proxy configuration (ezproxy, Shibboleth)

**Claude will ask**:
```
"Do you have institutional access?

[A] Yes, I'm connected via university VPN
[B] Yes, but I need help configuring proxy
[C] No, I'm an independent researcher
[D] Not sure / need to check

If [A]: I'll configure direct downloads
If [B]: I'll help set up proxy authentication
If [C]: We'll skip to Tier 3 (author requests)
```

### Tier 3: Author Requests

**Claude generates email templates**:

```
Subject: Request for full text: [Paper Title]

Dear Dr. [Author],

I am conducting a systematic review on [your research topic] and came
across your paper "[Paper Title]" published in [Journal, Year].

I would greatly appreciate access to the full text of this article, as
it is highly relevant to my research on [brief description].

If possible, could you please share a copy via email or provide a link
to an open access version?

Thank you for your time and consideration.

Best regards,
[Your Name]
[Your Affiliation]
[Your Email]
```

### Tier 4: Abstract-Only Fallback

**When to use**:
- PDF download failed in all tiers
- Paper is critical to research (cited heavily, seminal work)
- Better to include partial information than exclude entirely

**Limitations**:
- Abstracts are shorter (200-300 words vs. 6,000-8,000 words)
- Missing methods, results details, discussion
- Lower RAG answer quality for these papers

**Claude will mark these**:
```yaml
# In vector database metadata
document:
  title: "Paper Title"
  full_text_available: false
  content_type: "abstract_only"
  quality_flag: "incomplete"
```

---

## Phase 2: Text Extraction

### Tool Selection

**Primary: PyMuPDF** (fitz)
- **Pros**: Fast, good quality, handles most PDFs
- **Cons**: Struggles with scanned PDFs
- **Use case**: 80-90% of papers (born-digital PDFs)

**Backup: pdfplumber**
- **Pros**: Better table extraction, handles complex layouts
- **Cons**: Slower than PyMuPDF
- **Use case**: When PyMuPDF fails or produces garbled text

**Fallback: Tesseract OCR**
- **Pros**: Works on scanned PDFs (images)
- **Cons**: Slow, requires preprocessing, may have errors
- **Use case**: Old papers (pre-2000) or scanned documents

### Extraction Quality Checks

**Claude will implement**:
```python
def extract_text_with_quality_check(pdf_path):
    # Try PyMuPDF first
    text = extract_with_pymupdf(pdf_path)

    # Quality checks
    if len(text) < 1000:  # Too short
        text = extract_with_pdfplumber(pdf_path)

    if has_garbled_text(text):  # Encoding issues
        text = extract_with_pdfplumber(pdf_path)

    if still_bad(text):  # Last resort
        text = extract_with_ocr(pdf_path)

    return text, quality_score

def has_garbled_text(text):
    # Check for high ratio of non-ASCII characters
    non_ascii_ratio = sum(1 for c in text if ord(c) > 127) / len(text)
    return non_ascii_ratio > 0.3  # >30% garbled
```

---

## Phase 3: Chunking Strategy

### Why Chunking Matters

**Problem**: Papers are long (6,000-8,000 words), but embeddings work best on shorter texts (500-1,000 words).

**Solution**: Split papers into chunks with overlap.

### Recommended Settings

```yaml
chunking:
  chunk_size: 1000  # tokens (~750 words)
  chunk_overlap: 200  # tokens (~150 words)

# Why these numbers?
# - 1000 tokens: ~2-3 paragraphs (good semantic unit)
# - 200 overlap: Ensures continuity across chunks
# - Result: ~8-10 chunks per paper (for 8,000-word paper)
```

### Example

**Original text** (2,000 words):
```
[Introduction section: 500 words]
[Methods section: 700 words]
[Results section: 500 words]
[Discussion section: 300 words]
```

**After chunking**:
```
Chunk 1: [Introduction] (500 words)
Chunk 2: [Last 150 words of Intro + First 600 words of Methods] (750 words)
Chunk 3: [Last 150 words of Methods + First 600 words of Results] (750 words)
Chunk 4: [Last 150 words of Results + Discussion] (450 words)
```

**Benefits**:
- Context preserved (overlap ensures no info lost at boundaries)
- Semantic coherence (each chunk is meaningful)
- Good retrieval (relevant chunks retrieved even if answer spans boundaries)

---

## Phase 4: Embedding Model Selection

### Options

| Model | Dimensions | Speed | Quality | Cost | Use Case |
|-------|-----------|-------|---------|------|----------|
| **all-MiniLM-L6-v2** | 384 | Fast | Good | Free | Default (recommended) |
| **text-embedding-3-small** (OpenAI) | 1536 | Medium | Excellent | $0.02/1M tokens | High quality needed |
| **multilingual-e5-base** | 768 | Medium | Good | Free | Non-English papers |

### Recommendation: all-MiniLM-L6-v2

**Reasons**:
- Free, runs locally (no API costs)
- Fast (50ms per chunk on CPU)
- Good quality for academic text
- Small storage (384 dimensions vs 1536)

**Estimated Storage**:
```
139 papers × 10 chunks/paper = 1,390 chunks
1,390 chunks × 384 dimensions × 4 bytes = 2.1 MB (vectors)
+ text storage (~20 MB)
= ~25 MB total
```

**When to upgrade to OpenAI**:
- Need highest quality retrieval
- Working with complex/technical language
- Budget allows ($0.02 per 1M tokens ≈ $2 for 100 papers)

---

## Phase 5: Vector Database Configuration

### ChromaDB Setup

```python
import chromadb
from chromadb.config import Settings

# Initialize ChromaDB
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="data/vector_db/your_project"
))

# Create collection
collection = client.create_collection(
    name="your_project_papers",
    metadata={
        "description": "Your research project name",
        "total_papers": 139,
        "date_created": "2025-10-11"
    }
)

# Add documents
collection.add(
    documents=[chunk.text for chunk in chunks],
    metadatas=[{
        "paper_id": chunk.paper_id,
        "title": chunk.title,
        "authors": chunk.authors,
        "year": chunk.year,
        "chunk_index": chunk.index
    } for chunk in chunks],
    ids=[f"paper_{chunk.paper_id}_chunk_{chunk.index}" for chunk in chunks]
)
```

### Collection Organization

**Single Project** (Simple):
```
data/vector_db/
└── ai_education_chatbot/
    ├── chroma.sqlite3
    └── ...
```

**Multiple Projects** (Advanced):
```
data/vector_db/
├── project1_ai_education/
│   ├── chroma.sqlite3
│   └── ...
├── project2_medical_ehr/
│   ├── chroma.sqlite3
│   └── ...
└── project3_psych_mindfulness/
    ├── chroma.sqlite3
    └── ...
```

---

## Phase 6: RAG Prompt Engineering

### System Prompt Design

**Claude will generate based on your research questions**:

```
You: "My research questions are:
     1. Do chatbots improve speaking proficiency?
     2. What design features are most effective?
     3. How do learners perceive chatbot interactions?"

Claude: "I'll design a system prompt optimized for these questions:

```
You are a research assistant specializing in AI-powered language learning.
You have access to 139 peer-reviewed papers on chatbot interventions in
higher education language learning contexts.

**Your Task**: Provide evidence-based answers to research questions about
chatbot effectiveness, design features, and learner perceptions.

**Answer Guidelines**:

1. **Prioritize Experimental Evidence**
   - Cite RCTs and quasi-experimental studies first
   - Report effect sizes (Cohen's d, η², correlation coefficients)
   - Note sample sizes and statistical significance (p-values)

2. **Focus on Speaking Proficiency** (Primary RQ)
   - Oral fluency (words per minute, speech rate)
   - Accuracy (grammatical errors, pronunciation)
   - Complexity (vocabulary diversity, sentence structure)
   - Self-reported confidence and willingness to communicate (WTC)

3. **Identify Design Features** (Secondary RQ)
   - Chatbot architecture (rule-based, retrieval, neural)
   - Interaction patterns (turn-taking, scaffolding)
   - Feedback types (corrective, confirmatory, reformulation)
   - Integration context (standalone, classroom supplement)

4. **Synthesize Learner Perceptions** (Tertiary RQ)
   - Perceived usefulness and ease of use (TAM model)
   - Engagement and motivation metrics
   - Comparison with human tutors (where available)
   - Concerns and limitations reported by learners

5. **Acknowledge Limitations**
   - Study design weaknesses (lack of control, small N, short duration)
   - Measurement issues (self-report bias, assessment validity)
   - Generalizability constraints (specific contexts, languages)
   - Conflicting findings across studies

**Citation Format**:
For each claim, cite: [Author(s), Year, Design, N=sample, Finding/Effect size]

Example:
"Chatbot interventions showed moderate improvements in speaking fluency
[Kim et al., 2023, RCT, N=120, d=0.65, p<.01], particularly for lower-
proficiency learners [Lee & Park, 2022, Quasi-exp, N=89, η²=0.34].
However, gains were not sustained at 6-month follow-up [Chen, 2024,
Longitudinal, N=67, p=.18, ns]."

**Tone**: Academic but accessible. Critical but constructive. Balanced
presentation of positive and null findings.

**When uncertain**: Acknowledge gaps in the literature. Suggest what
future research should investigate.
```

Does this system prompt align with your research goals?"
```

### Citation Requirements

**Strict format enforcement**:
```python
# In RAG generation settings
generation_config = {
    "model": "claude-3.5-sonnet",
    "temperature": 0.3,  # Lower = more factual
    "max_tokens": 1500,

    # Citation enforcement
    "system_prompt_suffix": """

CRITICAL: You MUST cite at least 3 specific papers for each major claim.
Use format: [Author, Year, Design, N=X, Finding/Effect].

If you cannot find evidence for a claim, state: "No direct evidence found
in the reviewed literature. Further research needed."

Do NOT make claims without citations.
    """
}
```

---

## Phase 7: Retrieval Configuration

### Top-K (How many chunks to retrieve)

```yaml
retrieval:
  top_k: 10  # Retrieve 10 most similar chunks

# Why 10?
# - Too few (k=3): Might miss relevant info
# - Too many (k=50): Noise, slower generation
# - 10 is sweet spot: ~1-2 papers worth of context
```

### Similarity Threshold

```yaml
retrieval:
  similarity_threshold: 0.65  # Minimum 65% similarity

# Interpretation:
# - 1.0 = identical text (rare)
# - 0.8-1.0 = very high similarity
# - 0.65-0.8 = good similarity (recommended)
# - 0.5-0.65 = moderate similarity
# - <0.5 = low similarity (likely irrelevant)
```

### Re-ranking (Optional, but recommended)

**Problem**: Embedding similarity ≠ actual relevance

**Solution**: Two-stage retrieval
1. **Stage 1**: Retrieve 20 chunks with embedding model (fast)
2. **Stage 2**: Re-rank top 20 with cross-encoder (slower, more accurate)
3. **Return**: Top 10 after re-ranking

```python
from sentence_transformers import CrossEncoder

# Stage 1: Fast retrieval
initial_results = collection.query(
    query_texts=[user_question],
    n_results=20  # Over-retrieve
)

# Stage 2: Re-rank with cross-encoder
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
scores = reranker.predict([
    [user_question, doc] for doc in initial_results['documents']
])

# Sort by cross-encoder score and take top 10
final_results = sorted(zip(initial_results, scores),
                       key=lambda x: x[1], reverse=True)[:10]
```

**Trade-off**:
- **Without re-ranking**: Fast (50ms), good quality
- **With re-ranking**: Slower (200ms), excellent quality
- **Recommendation**: Enable re-ranking for complex questions

---

## Interactive Exercise: Configure Your RAG

```
Claude: "Let's configure your RAG system step by step.

**Step 1: PDF Download Strategy**

I estimate you can get ~75 PDFs (54% success rate) from your 139 papers.

Do you have:
[A] University VPN / institutional access
[B] Budget for author requests ($50-100 estimated)
[C] Neither (will use open access only)

You: [A]

Claude: "Great! I'll configure:
- Tier 1: Open Access (~56 papers)
- Tier 2: Institutional proxy (~28 papers)
- Tier 3: Author requests (~42 papers, best effort)

Expected: 75-85 PDFs (54-61%)

**Step 2: Text Extraction**

I'll set up:
- Primary: PyMuPDF (fast, good quality)
- Backup: pdfplumber (if PyMuPDF fails)
- Fallback: Tesseract OCR (for scanned PDFs)

Quality threshold: Minimum 1,000 words per paper (exclude if less)

**Step 3: Chunking**

For your speaking proficiency research:
- Chunk size: 1,000 tokens (~750 words)
- Overlap: 200 tokens (~150 words)
- Why: Balances context preservation and retrieval precision

Expected: ~8-10 chunks per paper, ~750 total chunks

**Step 4: Embedding Model**

Recommended: sentence-transformers/all-MiniLM-L6-v2
- Free, local, fast
- Good quality for academic text
- 384 dimensions (small storage: ~3 MB)

Alternative: OpenAI text-embedding-3-small ($2 total cost)
- Higher quality, especially for complex queries
- 1536 dimensions (larger storage: ~12 MB)

Your choice: [all-MiniLM-L6-v2 / OpenAI]

You: all-MiniLM-L6-v2

Claude: "Good choice! Free and sufficient quality.

**Step 5: Vector Database**

ChromaDB collection name: 'ai_education_chatbot_2025'
Location: data/vector_db/ai_education_chatbot/

**Step 6: RAG Prompts**

I've generated a system prompt for your 3 research questions:
1. Speaking proficiency effects
2. Design features
3. Learner perceptions

[Shows generated prompt]

Any adjustments needed?

You: Looks good!

Claude: **Summary - Ready to Build**

✅ PDF Strategy: Institutional + Open Access (75-85 PDFs expected)
✅ Text Extraction: PyMuPDF → pdfplumber → OCR (3-tier)
✅ Chunking: 1,000 tokens, 200 overlap
✅ Embedding: all-MiniLM-L6-v2 (local, free)
✅ Vector DB: ChromaDB, ~750 chunks, ~25 MB
✅ RAG Prompts: Custom system prompt for your RQs
✅ Retrieval: top_k=10, threshold=0.65, re-ranking enabled

Estimated time:
- PDF download: 2-3 hours
- Text extraction: 30 minutes
- Vector DB build: 15 minutes
- Total: ~3-4 hours

Proceed with Stage 5 (Execution)?

[Yes, create scripts] [Adjust settings] [See detailed config]
```

---

## Output Configuration Files

### 1. rag_config.yaml

```yaml
project:
  name: "AI Education Chatbot - Language Learning"
  description: "Systematic review of chatbot effectiveness"
  date_created: "2025-10-11"

pdf_download:
  strategy:
    - open_access: true
    - institutional_proxy: true
    - author_requests: true
  expected_success_rate: 0.55
  timeout_per_paper: 30  # seconds

text_extraction:
  primary_tool: "pymupdf"
  backup_tool: "pdfplumber"
  ocr_fallback: true
  min_words: 1000  # Minimum viable extraction

chunking:
  chunk_size: 1000  # tokens
  chunk_overlap: 200  # tokens
  separator: "\n\n"  # Split on paragraphs

embedding:
  model: "sentence-transformers/all-MiniLM-L6-v2"
  dimension: 384
  device: "cpu"  # or "cuda" if GPU available

vector_db:
  type: "chromadb"
  persist_directory: "data/vector_db/ai_education_chatbot"
  collection_name: "papers_2025"

retrieval:
  top_k: 10
  similarity_threshold: 0.65
  rerank: true
  rerank_model: "cross-encoder/ms-marco-MiniLM-L-6-v2"

generation:
  model: "claude-3.5-sonnet"
  temperature: 0.3
  max_tokens: 1500
  system_prompt_file: "config/system_prompts/your_project.txt"
```

### 2. system_prompt.txt

```
[Generated custom system prompt based on your research questions]
```

---

## Next Steps

Once RAG design is complete:

1. **Move to Stage 5**: [prompts/05_execution_plan.md](./05_execution_plan.md)
2. **Run Scripts**: Execute PDF download, text extraction, vector DB build
3. **Test RAG**: Try sample queries
4. **Iterate**: Adjust prompts and retrieval settings based on answer quality

---

**Estimated Time**: 15-20 minutes (configuration)
**Prerequisites**: Completed Stage 3 (PRISMA screening)
**Next Stage**: [Stage 5: Execution Plan](./05_execution_plan.md)
