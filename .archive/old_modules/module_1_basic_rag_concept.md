# Module 1: Understanding RAG for Social Science Research

## What is RAG?

RAG (Retrieval-Augmented Generation) is a technique that enhances Large Language Models (LLMs) by providing them with relevant context from your own documents before generating responses.

### Traditional LLM vs RAG

**Traditional LLM:**
```
User Question → LLM → Answer (based on training data only)
```
- Limited to knowledge cutoff date
- Cannot access your specific research documents
- May hallucinate facts

**RAG System:**
```
User Question → Search Your Documents → Retrieve Relevant Passages → LLM + Context → Accurate Answer
```
- Uses YOUR research corpus
- Provides citations and sources
- Grounded in actual documents

---

## Why RAG for Social Science Research?

### Use Case 1: Literature Review Automation
**Traditional Method:**
- Manually read 200 papers
- Create Excel spreadsheet with key findings
- Takes weeks/months

**RAG Method:**
```python
# Query your RAG system
query = "What are the main theories of technology adoption in education?"

# Get instant answer with citations
answer = rag_system.query(query)
# Returns: "Based on your 200 papers, the main theories are:
# 1. TAM (Davis, 1989) - cited in 45 papers
# 2. UTAUT (Venkatesh et al., 2003) - cited in 38 papers
# ..."
```

### Use Case 2: Qualitative Data Coding
**Traditional Method:**
- Manually code 50 interview transcripts
- Use NVivo or Atlas.ti
- Takes days per interview

**RAG Method:**
```python
# Extract themes from all interviews
query = "What are the main barriers to AI adoption mentioned by teachers?"

# RAG finds relevant quotes from all 50 interviews
themes = qualitative_rag.extract_themes(query)
# Automatically groups similar responses and provides evidence
```

### Use Case 3: Meta-Analysis Support
**Traditional Method:**
- Manually extract effect sizes from each paper
- Record sample sizes, methods, variables

**RAG Method:**
```python
# Extract statistical information
query = "Extract all correlation coefficients between self-efficacy and performance"

# RAG finds and structures data
results = meta_analysis_rag.extract_statistics(query)
# Returns structured DataFrame ready for meta-analysis
```

---

## Key Concepts

### 1. Vector Embeddings
**What are embeddings?**
Text is converted to numerical vectors that capture semantic meaning.

```python
# Example: Similar sentences have similar vectors
sentence_1 = "Teachers resist new technology"
sentence_2 = "Educators show resistance to innovative tools"
sentence_3 = "Students love pizza"

# After embedding:
# sentence_1 and sentence_2 are close in vector space
# sentence_3 is far from both
```

**Why it matters for research:**
- Find conceptually similar content, not just keyword matches
- "technology adoption" matches "innovation diffusion"
- Works across different terminology/jargon

### 2. Vector Databases
Where embeddings are stored and searched efficiently.

**Popular Options:**
- **ChromaDB**: Easy to use, local, free
- **Pinecone**: Cloud-based, scalable
- **Qdrant**: Open-source, feature-rich
- **FAISS**: Fast, Facebook-developed

**For this workshop, we use ChromaDB** (easiest for beginners)

### 3. Chunking Strategy
How documents are split before embedding.

**Example: Chunking a research paper**
```
Original Paper (30 pages)
    ↓
Split into chunks:
- Chunk 1: Abstract (300 tokens)
- Chunk 2: Introduction (500 tokens)
- Chunk 3: Literature Review - Section 1 (500 tokens)
- Chunk 4: Literature Review - Section 2 (500 tokens)
...
```

**Why chunking matters:**
- LLMs have token limits (context window)
- Smaller chunks = more precise retrieval
- Larger chunks = more context preserved

**Research-specific chunking:**
- **Papers**: By section (abstract, intro, methods, results, discussion)
- **Interviews**: By question or by paragraph
- **Reports**: By chapter or subsection

---

## RAG Architecture for Researchers

```
┌─────────────────────────────────────────────────────────────┐
│                    RESEARCHER'S RAG SYSTEM                  │
└─────────────────────────────────────────────────────────────┘

1. INGESTION PHASE (One-time setup)
   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
   │ Your Papers  │──→   │  Text        │──→   │  Embedding   │
   │ (.pdf, .docx)│      │  Extraction  │      │  Model       │
   └──────────────┘      └──────────────┘      └──────────────┘
                                                       │
                                                       ↓
                                              ┌──────────────┐
                                              │   Vector DB  │
                                              │  (ChromaDB)  │
                                              └──────────────┘

2. QUERY PHASE (Every time you ask a question)
   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
   │   Question   │──→   │  Search      │──→   │  Retrieve    │
   │              │      │  Vector DB   │      │  Top 5 docs  │
   └──────────────┘      └──────────────┘      └──────────────┘
                                                       │
                                                       ↓
                                              ┌──────────────┐
                                              │  LLM with    │
                                              │  Context     │
                                              └──────────────┘
                                                       │
                                                       ↓
                                              ┌──────────────┐
                                              │    Answer    │
                                              │ + Citations  │
                                              └──────────────┘
```

---

## Hands-On Exercise: Build Your First Mini RAG

### Prerequisites
```bash
# Check Python version (need 3.9+)
python --version

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install basic packages
pip install langchain chromadb openai python-dotenv
```

### Step 1: Prepare Sample Documents

Create a folder with 3-5 research papers (PDFs) on a topic you're interested in.

```bash
mkdir sample_papers
# Add your PDFs to this folder
```

### Step 2: Simple RAG Script

```python
# File: simple_rag_demo.py

import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# Load API key
load_dotenv()

# Step 1: Load PDFs
print("Loading papers...")
loader = DirectoryLoader(
    'sample_papers/',
    glob="**/*.pdf",
    loader_cls=PyPDFLoader
)
documents = loader.load()
print(f"Loaded {len(documents)} pages from PDFs")

# Step 2: Split into chunks
print("Splitting into chunks...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""]
)
chunks = text_splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")

# Step 3: Create embeddings and vector store
print("Creating vector database...")
embeddings = OpenAIEmbeddings()
vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
print("Vector database created!")

# Step 4: Create RAG chain
llm = ChatOpenAI(model_name="gpt-4", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectordb.as_retriever(search_kwargs={"k": 5}),
    return_source_documents=True
)

# Step 5: Ask questions!
def ask_question(question):
    result = qa_chain({"query": question})

    print("\n" + "="*80)
    print("QUESTION:", question)
    print("="*80)
    print("\nANSWER:")
    print(result['result'])

    print("\n" + "-"*80)
    print("SOURCES:")
    for i, doc in enumerate(result['source_documents'], 1):
        print(f"\n{i}. {doc.metadata.get('source', 'Unknown')}")
        print(f"   {doc.page_content[:200]}...")
    print("="*80 + "\n")

# Example queries for social science research
if __name__ == "__main__":
    # Example 1: Conceptual question
    ask_question("What are the main theoretical frameworks discussed in these papers?")

    # Example 2: Methodological question
    ask_question("What research methods were used and what were the sample sizes?")

    # Example 3: Findings synthesis
    ask_question("What are the key findings across all studies?")
```

### Step 3: Run the Demo

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-key-here"

# Run the script
python simple_rag_demo.py
```

---

## Understanding the Output

When you run the above script, you'll see:

```
QUESTION: What are the main theoretical frameworks discussed in these papers?
================================================================================

ANSWER:
The papers primarily employ three theoretical frameworks:

1. **Technology Acceptance Model (TAM)** - Used to explain teachers' intentions
   to adopt educational technology based on perceived usefulness and ease of use.

2. **Self-Determination Theory (SDT)** - Applied to understand intrinsic vs
   extrinsic motivation in technology integration.

3. **TPACK Framework** - Examines the intersection of technological, pedagogical,
   and content knowledge in teaching practice.

--------------------------------------------------------------------------------
SOURCES:

1. sample_papers/smith_2020_teacher_technology.pdf
   "This study applies the Technology Acceptance Model (TAM; Davis, 1989) to
   investigate factors influencing K-12 teachers' adoption of artificial
   intelligence tools..."

2. sample_papers/jones_2021_motivation_tech.pdf
   "Drawing on Self-Determination Theory (Ryan & Deci, 2000), we examined how
   autonomy, competence, and relatedness needs affect technology integration..."

[... more sources ...]
================================================================================
```

**What just happened?**
1. Your question was converted to a vector
2. ChromaDB found the 5 most similar chunks from your papers
3. GPT-4 received those chunks as context
4. GPT-4 synthesized an answer WITH citations

**This is RAG in action!** 🎉

---

## Key Differences from Traditional Search

| Feature | Google Scholar | Ctrl+F | RAG System |
|---------|----------------|--------|------------|
| **Semantic search** | ✅ Yes | ❌ No | ✅ Yes |
| **Synthesis** | ❌ No | ❌ No | ✅ Yes |
| **Your documents only** | ❌ No | ✅ Yes | ✅ Yes |
| **Citations** | ✅ Yes | ⚠️ Manual | ✅ Automatic |
| **Cross-document** | ⚠️ Limited | ❌ No | ✅ Yes |
| **Ask follow-ups** | ❌ No | ❌ No | ✅ Yes |

---

## Common Questions

### Q: How accurate is RAG?
**A:** RAG is only as good as:
1. Quality of your source documents (garbage in = garbage out)
2. Quality of the LLM (GPT-4 > GPT-3.5)
3. Retrieval strategy (better retrieval = better answers)

**Always verify important findings manually!**

### Q: Can RAG replace human researchers?
**A:** No! RAG is a **tool to augment** research, not replace it.
- Use for: Initial exploration, pattern finding, literature mapping
- Human needed for: Critical analysis, theoretical contributions, interpretation

### Q: What about privacy/confidentiality?
**A:** Important considerations:
- **OpenAI/Claude APIs**: Your data is sent to their servers (check their policies)
- **Local models**: Run entirely on your computer (e.g., Ollama + Llama 3)
- **For sensitive data**: Use local models or on-premise solutions

### Q: How much does it cost?
**A:** Costs breakdown:
- **Embedding**: ~$0.0001 per 1000 tokens (cheap!)
  - 100 papers ≈ $1-5
- **LLM queries**: ~$0.01-0.03 per query (GPT-4)
  - 100 questions ≈ $1-3
- **Total for typical project**: $10-50

---

## Next Steps

In **Module 2**, you'll learn to:
1. Build a production-ready Literature Review RAG system
2. Use Claude Code to customize the system
3. Deploy via Chainlit web interface

### Pre-Module 2 Homework
1. Gather 10-20 papers on your research topic
2. Install Docker (for deployment)
3. Set up API keys (OpenAI, Anthropic)

---

## Additional Resources

### Recommended Reading
- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Quickstart](https://docs.trychroma.com/)
- [RAG for Research Guide](https://github.com/anthropics/anthropic-cookbook)

### Video Tutorials
- "RAG Explained in 5 Minutes" (YouTube)
- "Building RAG Systems for Researchers" (YouTube)

### Community
- [LangChain Discord](https://discord.gg/langchain)
- [r/LanguageTechnology](https://reddit.com/r/LanguageTechnology)

---

**Module 1 Complete!** ✅

You now understand:
- ✅ What RAG is and how it works
- ✅ Why it's valuable for social science research
- ✅ How to build a basic RAG system
- ✅ Key concepts: embeddings, vector databases, chunking

**Ready for Module 2!** 🚀
