# Quick Start Guide: ResearcherRAG

**Get up and running in 15 minutes**

---

## For Complete Beginners (No Coding Experience)

### Step 1: Access the Demo (2 minutes)

1. Go to: `https://huggingface.co/spaces/your-username/researcherrag`
2. Click on one of the three tabs:
   - 📚 **Literature Review**: For analyzing research papers
   - 🎤 **Qualitative Coding**: For interview transcripts
   - 📝 **Research Notes**: For your personal notes

### Step 2: Upload Your Data (5 minutes)

**For Literature Review:**
```
1. Click "Literature Review" tab
2. Drag and drop 5-10 PDF research papers
3. Wait for processing (1-2 minutes)
4. Ask a question like:
   "What are the main findings about teacher technology adoption?"
```

**For Qualitative Coding:**
```
1. Click "Qualitative Coding" tab
2. Upload interview transcripts (.txt or .docx files)
3. Enter your research question: "Teachers' barriers to AI adoption"
4. Click "Analyze Interviews"
5. Review generated codes and themes
```

**For Research Notes:**
```
1. Click "Research Notes" tab
2. Upload your markdown notes or text files
3. Chat with your notes:
   "What did I learn about mixed methods last month?"
```

### Step 3: Explore Results (8 minutes)

**Understanding Outputs:**

**Literature Review Output:**
```
Answer: Based on 8 relevant papers, the main theories are:

1. Technology Acceptance Model (TAM) [1,2,3] - Focuses on perceived
   usefulness and ease of use...

2. UTAUT Framework [4,5] - Extends TAM by adding social influence...

Citations:
[1] Smith et al. (2023) - "Teacher Technology Adoption in K-12..."
[2] Johnson & Lee (2022) - "Understanding AI Resistance..."
```

**Qualitative Coding Output:**
```json
{
  "codes": [
    {
      "code_name": "Time constraints",
      "definition": "Lack of time to learn new technology",
      "count": 12,
      "examples": ["no time", "too busy", "overloaded"]
    },
    ...
  ],
  "themes": [
    {
      "theme_name": "Resource Barriers",
      "codes": ["Time constraints", "Lack of training", "Budget limits"],
      "description": "Structural barriers preventing adoption"
    },
    ...
  ]
}
```

---

## For Researchers with Basic Python Knowledge

### Option 1: Use Pre-Built Hugging Face Space

Same as above, but you can also:
- **Customize prompts** via the interface settings
- **Export results** as CSV or JSON
- **Filter by metadata** (year, author, etc.)

### Option 2: Run Locally (Recommended)

**Setup (10 minutes):**

```bash
# 1. Clone repository
git clone https://github.com/your-username/ResearcherRAG.git
cd ResearcherRAG

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up API keys
cp .env.example .env
nano .env  # Add your keys (instructions below)
```

**Get API Keys (5 minutes):**

1. **Anthropic Claude** (recommended):
   - Go to: https://console.anthropic.com
   - Sign up → Get API key
   - Free tier: $5 credit (sufficient for testing)

2. **Qdrant Cloud** (vector database):
   - Go to: https://cloud.qdrant.io
   - Sign up → Create cluster (free 1GB)
   - Get cluster URL and API key

3. **Add to .env file:**
   ```bash
   ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
   QDRANT_URL=https://xxx.aws.cloud.qdrant.io
   QDRANT_API_KEY=xxxxx
   ```

**Run Literature Review RAG:**

```bash
cd 01_literature_review_rag
chainlit run frontend/chainlit_app.py
```

Open browser: `http://localhost:8000`

---

## For Advanced Users (Customization)

### Customize with Claude Code

**Use Case: Modify chunking strategy**

**Claude Code Prompt:**
```
I want to change the chunking strategy for academic papers to preserve:
1. Section boundaries (Abstract, Methods, Results, Discussion)
2. Table content (don't split tables)
3. Reference lists (extract separately)

Modify the chunking logic in backend/core/ingestion.py to implement this.
```

**Use Case: Add new metadata filter**

**Claude Code Prompt:**
```
Add a metadata filter for "study design" (experimental, survey, qualitative, mixed).
Users should be able to filter searches like:
"Find papers using experimental design published after 2020"

Add this to:
1. Document ingestion (auto-detect study design from text)
2. Search interface (dropdown filter)
3. API endpoint (filter parameter)
```

**Use Case: Custom export format**

**Claude Code Prompt:**
```
Add export functionality to convert qualitative codes to NVivo XML format.
The export should include:
- Hierarchical code structure
- All coded segments with source info
- Code definitions and descriptions

Create a new function in backend/core/export_manager.py
```

---

## Common Tasks

### Task 1: Analyze Your Own Papers

```bash
# 1. Create folder with your PDFs
mkdir data/my_papers
# Copy your PDFs to this folder

# 2. Run ingestion script
python scripts/ingest_papers.py data/my_papers

# 3. Query via interface or API
```

### Task 2: Share with Collaborators

**Method 1: Deploy to Hugging Face (Public/Private)**
```bash
# 1. Create HF account
# 2. Create new Space
# 3. Push code:
git clone https://huggingface.co/spaces/your-username/researcherrag
cp -r /path/to/ResearcherRAG/* researcherrag/
cd researcherrag
git add .
git commit -m "Deploy ResearcherRAG"
git push
```

**Method 2: Deploy to University Server**
```bash
# On your server:
git clone https://github.com/your-username/ResearcherRAG.git
cd ResearcherRAG
docker-compose up -d

# Access at: http://your-server.edu
```

### Task 3: Batch Process Multiple Studies

```python
# scripts/batch_analyze_interviews.py

from modules.qualitative_coding_graph import analyze_interviews
import os
import json

# Process all studies in a folder
studies_dir = "data/interview_studies"

for study_folder in os.listdir(studies_dir):
    print(f"Processing {study_folder}...")

    # Load interview transcripts
    transcripts = []
    for file in os.listdir(f"{studies_dir}/{study_folder}"):
        with open(f"{studies_dir}/{study_folder}/{file}", 'r') as f:
            transcripts.append(f.read())

    # Analyze
    result = analyze_interviews(
        transcripts,
        research_question=f"Analysis of {study_folder}"
    )

    # Save results
    output_path = f"outputs/{study_folder}_codes.json"
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"✓ Saved to {output_path}")
```

---

## Troubleshooting

### Issue: "API key not found"

**Solution:**
```bash
# Check if .env file exists
ls -la .env

# If not, create it:
cp .env.example .env
nano .env  # Add your keys

# Verify keys are loaded:
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('ANTHROPIC_API_KEY'))"
```

### Issue: "Vector store empty" error

**Solution:**
```bash
# Check if documents were ingested
python -c "from backend.core.retrieval import AdvancedRetriever; r = AdvancedRetriever(); print(r.get_collection_stats())"

# If count is 0, re-ingest:
python scripts/ingest_papers.py data/raw_pdfs
```

### Issue: "Out of memory" during processing

**Solution:**
```python
# Reduce batch size in ingestion.py
# Change from:
batch_size = 100

# To:
batch_size = 20
```

### Issue: API rate limits

**Solution:**
```python
# Add delay between API calls
import time
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    result = chain.invoke(query)
    time.sleep(1)  # 1 second delay
    print(f"Tokens used: {cb.total_tokens}")
```

---

## Next Steps

### Beginner Path
1. ✅ Complete Module 1: [RAG Basics](docs/module_1_basic_rag_concept.md)
2. ✅ Try Module 2: [Literature Review RAG](docs/module_2_literature_review_rag.md)
3. 📧 Join community Discord (link in README)

### Intermediate Path
1. ✅ Deploy your own instance to HF Spaces
2. ✅ Customize for your research domain
3. ✅ Integrate with Zotero/Mendeley
4. 🤝 Contribute improvements back

### Advanced Path
1. ✅ Implement new RAG techniques (GraphRAG, Corrective RAG)
2. ✅ Add support for non-English languages
3. ✅ Build custom evaluation metrics
4. 📝 Publish about your use case

---

## Example Research Workflows

### Workflow 1: Systematic Literature Review

```
Day 1: Setup
- Deploy ResearcherRAG
- Upload 200 papers from Google Scholar
- Wait for ingestion (1-2 hours)

Day 2-3: Exploration
- Query: "What methodologies are used?"
- Query: "What are the main findings?"
- Query: "What gaps exist in the literature?"
- Export results as structured JSON

Day 4-5: Analysis
- Use JSON to create Excel summary tables
- Generate PRISMA flow diagram
- Create evidence synthesis tables

Day 6: Writing
- Use chat interface as writing assistant
- Ask: "Write introduction paragraph about TAM theory"
- Get relevant quotes and citations
- Human edit and finalize
```

### Workflow 2: Qualitative Interview Study

```
Week 1: Data Collection
- Conduct 30 interviews
- Transcribe using Otter.ai or Rev.com
- Upload transcripts to ResearcherRAG

Week 2: Initial Coding
- Run AI-assisted coding
- Review generated codes (2-3 hours)
- Merge similar codes
- Export codebook

Week 3: Validation
- Second coder reviews AI codes
- Calculate inter-rater reliability
- Resolve disagreements
- Finalize codebook

Week 4: Theme Development
- Generate hierarchical themes
- Select exemplar quotes
- Write findings section
```

### Workflow 3: Grant Proposal Writing

```
Step 1: Literature Foundation
- Query: "What are current trends in [field]?"
- Query: "What methodologies have been successful?"
- Query: "What are the research gaps?"
- Use synthesis for "Significance" section

Step 2: Innovation Claim
- Query: "Has anyone studied [your idea]?"
- Identify similar studies
- Articulate your unique contribution
- Use for "Innovation" section

Step 3: Preliminary Work
- Query your research notes: "What have I done on this topic?"
- Synthesize past findings
- Use for "Preliminary Studies" section
```

---

## Cost Estimation

### Prototype (Testing with 20 papers)
- Qdrant: $0 (free tier)
- Embedding: $0 (local HuggingFace models)
- LLM (Claude): ~$2-5 (50-100 queries)
- **Total: $2-5**

### Small Project (100 papers, 20 interviews)
- Qdrant: $0 (free tier)
- Embedding: $0
- LLM (Claude): ~$20-40 (500 queries)
- **Total: $20-40**

### Large project (500 papers, 100 interviews)
- Qdrant: $0 (still within 1GB)
- Embedding: $0
- LLM (Claude): ~$100-200 (2000 queries)
- **Total: $100-200**

### Research Lab (10 researchers, ongoing)
- Qdrant: $0-25/month (may need paid tier)
- Embedding: $0
- LLM (Claude): ~$300-500/month
- HF Spaces (upgraded): $9/month
- **Total: ~$350-550/month**

---

## Getting Help

**Before Asking:**
1. Check [Documentation](docs/)
2. Search [GitHub Issues](https://github.com/your-username/ResearcherRAG/issues)
3. Try [Troubleshooting](#troubleshooting) section

**How to Ask:**
1. Describe what you're trying to do
2. Show what you tried (code/commands)
3. Include error messages (full traceback)
4. Mention your environment (OS, Python version)

**Good Example:**
```
I'm trying to ingest 50 PDF papers but getting this error:

Error: chromadb.errors.InvalidCollectionException: Collection not found

Steps I tried:
1. Created .env with API keys
2. Ran: python scripts/ingest_papers.py data/papers
3. Got the error above

Environment:
- MacOS 13.0
- Python 3.11
- ResearcherRAG v1.0
```

---

**Ready to start? Choose your path above and dive in!** 🚀

Questions? → [Open an issue](https://github.com/your-username/ResearcherRAG/issues/new)
