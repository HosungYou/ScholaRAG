# How to Upload Papers - Complete Guide

## 📚 Three Methods to Upload Papers

---

## Method 1: Web Interface (Easiest) ⭐ **RECOMMENDED**

### Step 1: Start the Application

```bash
cd "/Volumes/External SSD/Projects/Research/ResearcherRAG/01_literature_review_rag"
python app.py
```

### Step 2: Open Browser

Go to: **http://localhost:7860**

### Step 3: Upload Papers

1. Click **"📤 Upload Papers"** tab
2. Click **"Select PDF Files"** button
3. Select your PDF papers (can select multiple at once)
4. Click **"📤 Process & Upload"**
5. Wait for processing (~20 seconds per paper)

### Step 4: See Success Message

You'll see:
```
✅ Upload Successful!

📄 Files processed: 5
📦 Text chunks created: 87
🗄️ Total documents in database: 87
```

### Step 5: Ask Questions!

1. Go to **"❓ Ask Questions"** tab
2. Type your question
3. Click **"🔍 Search & Synthesize"**

**Example Questions:**
- "What are the main theories discussed?"
- "What research methods were used?"
- "Summarize the key findings"

---

## Method 2: Drag and Drop into Folder (Bulk Upload)

### For Many Papers at Once

**Step 1: Copy PDFs to Folder**

```bash
# Copy your papers to this folder:
cp /path/to/your/papers/*.pdf "/Volumes/External SSD/Projects/Research/ResearcherRAG/01_literature_review_rag/data/raw_pdfs/"
```

Or use Finder:
1. Open Finder
2. Navigate to: `External SSD/Projects/Research/ResearcherRAG/01_literature_review_rag/data/raw_pdfs/`
3. Drag and drop your PDF files

**Step 2: Run Batch Ingestion**

```bash
cd "/Volumes/External SSD/Projects/Research/ResearcherRAG/01_literature_review_rag"
python scripts/batch_ingest.py
```

The script will:
- Find all PDFs in `data/raw_pdfs/`
- Show you the list
- Ask for confirmation
- Process all papers
- Add to database

**Output:**
```
Found 25 PDF files

Files to process:
  1. smith_2023_technology_adoption.pdf
  2. johnson_2022_ai_education.pdf
  ...

Process these files? (y/n): y

Processing papers...
✓ Created 453 text chunks

✅ Ingestion Complete!

Papers processed: 25
Text chunks: 453
Total in database: 453
```

---

## Method 3: Programmatic Upload (Advanced)

### Using Python Script

Create a custom script:

```python
from backend.core.ingestion import ingest_documents
from backend.core.retrieval import get_retriever

# Ingest from specific directory
documents = ingest_documents("/path/to/your/papers")

# Add to database
retriever = get_retriever()
retriever.add_documents(documents)

print(f"Added {len(documents)} chunks")
```

---

## 📍 File Locations Explained

### Where Files Are Stored

```
01_literature_review_rag/
└── data/
    ├── raw_pdfs/              ← Original PDF files
    │   ├── paper1.pdf         (Your uploaded papers)
    │   ├── paper2.pdf
    │   └── temp_upload/       (Web interface uploads here first)
    │
    ├── processed/             ← Extracted text (optional backup)
    │
    └── vector_db/             ← Database (searchable chunks)
        └── chroma.sqlite3     (ChromaDB database file)
```

**Important:**
- `raw_pdfs/` = Your original papers (safe to delete after processing)
- `vector_db/` = Searchable database (DO NOT delete!)

---

## 🔍 Checking What's Uploaded

### Method 1: Web Interface

1. Open app: `python app.py`
2. Go to **"📊 Database Info"** tab
3. Click **"🔄 Refresh Stats"**

You'll see:
```
📊 Database Statistics

🗄️ Total document chunks: 453
📁 Collection: literature_review
💾 Status: Active
```

### Method 2: Command Line

```bash
cd "/Volumes/External SSD/Projects/Research/ResearcherRAG/01_literature_review_rag"
python test_system.py
```

Output includes:
```
Vector store initialized
  Current document count: 453
```

### Method 3: Python

```python
from backend.core.retrieval import get_retriever

retriever = get_retriever()
stats = retriever.get_collection_stats()
print(f"Documents in database: {stats['count']}")
```

---

## 📋 Supported File Formats

### Currently Supported
- ✅ **PDF** (.pdf) - Fully supported
  - Text-based PDFs (best quality)
  - Scanned PDFs with text layer (OCR'd)

### Not Yet Supported
- ❌ **Scanned images** (pure image PDFs without text)
  - Solution: Use OCR tool first (Adobe Acrobat, etc.)
- ❌ **Word documents** (.docx)
  - Solution: Save as PDF first
- ❌ **PowerPoint** (.pptx)
  - Solution: Save as PDF first

---

## ⚠️ Common Issues & Solutions

### Issue 1: "No files uploaded"

**Problem:** Clicked upload but nothing happened

**Solution:**
- Make sure you selected PDF files
- Check file size (very large files >100MB may timeout)
- Try uploading fewer files at once (5-10 at a time)

### Issue 2: "Failed to process"

**Problem:** Some papers failed during processing

**Causes:**
- Scanned PDF without text layer
- Corrupted PDF file
- Password-protected PDF

**Solution:**
1. Check the PDF opens in Adobe Reader
2. Try re-downloading the PDF
3. Remove password protection
4. Use OCR if it's a scanned image

### Issue 3: "Where did my files go?"

**Problem:** Uploaded but can't find original PDFs

**Answer:**
- Web uploads go to: `data/raw_pdfs/temp_upload/`
- Check there for your originals
- The searchable data is in: `data/vector_db/`

### Issue 4: Want to re-upload

**Problem:** Made a mistake, want to start over

**Solution:**
```bash
# Delete database (WARNING: removes all papers!)
rm -rf data/vector_db/*

# Re-upload papers using any method above
```

---

## 💡 Tips & Best Practices

### 1. File Naming

**Good naming:**
```
smith_2023_technology_adoption.pdf
jones_2022_teacher_ai_barriers.pdf
```

**Why:** Easier to identify in citations

### 2. Organize by Project

```
raw_pdfs/
├── project1_teacher_ai/
│   ├── paper1.pdf
│   └── paper2.pdf
└── project2_student_tech/
    ├── paper3.pdf
    └── paper4.pdf
```

Then process each project separately:
```bash
python scripts/batch_ingest.py
# Point to specific folder when asked
```

### 3. Start Small

- Upload 5-10 papers first
- Test with queries
- Add more papers gradually

### 4. Keep Originals

- Don't delete PDFs from `raw_pdfs/`
- You might want to re-process with different settings later

---

## 📊 How Much Can You Upload?

### Limits

| Scenario | Papers | Chunks | Disk Space | RAM Needed |
|----------|--------|---------|------------|------------|
| Small | 10-20 | ~200 | ~50MB | 2GB |
| Medium | 50-100 | ~1000 | ~200MB | 4GB |
| Large | 200-500 | ~5000 | ~1GB | 8GB |
| Very Large | 1000+ | ~20000+ | ~5GB | 16GB+ |

**Recommendation:**
- Start with 20-50 papers
- Test performance
- Scale up if needed

---

## 🧪 Test Upload

### Quick Test with Sample Papers

Don't have papers yet? Download some from:
- [Google Scholar](https://scholar.google.com)
- [arXiv](https://arxiv.org) (open access)
- [ERIC](https://eric.ed.gov) (education papers)
- [PubMed](https://pubmed.ncbi.nlm.nih.gov) (health/psychology)

1. Download 3-5 PDFs
2. Upload via web interface
3. Try sample questions

---

## 🎯 Quick Start Checklist

- [ ] App is running (`python app.py`)
- [ ] Browser open at http://localhost:7860
- [ ] Have PDF papers ready
- [ ] Click "Upload Papers" tab
- [ ] Select PDFs
- [ ] Click "Process & Upload"
- [ ] Wait for success message
- [ ] Go to "Ask Questions" tab
- [ ] Type question and submit
- [ ] View answer and citations!

---

## 📞 Need Help?

**If upload fails:**
1. Check `test_system.py` passes
2. Check `.env` has API key
3. Check PDFs are valid (open in reader)
4. Check logs in terminal for errors

**Still stuck?**
- GitHub Issues: https://github.com/HosungYou/researcherRAG/issues
- Check: QUICK_START.md for setup help

---

**Happy researching!** 📚✨
