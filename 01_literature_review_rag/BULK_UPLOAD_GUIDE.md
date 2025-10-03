# Bulk Upload Guide - Works on Any Computer

## 🎯 Quick Start (Any Computer)

### Option 1: Auto-Detection (Easiest)

```bash
# Script automatically finds your papers
python scripts/batch_ingest_flexible.py
```

The script checks these locations automatically:
- ✅ Project folder: `data/raw_pdfs/`
- ✅ Google Drive: `~/Google Drive/Research/Papers`
- ✅ Dropbox: `~/Dropbox/Research/Papers`
- ✅ OneDrive: `~/OneDrive/Research/Papers`
- ✅ Desktop: `~/Desktop/Research_Papers`
- ✅ Documents: `~/Documents/Research/Papers`

### Option 2: Specify Your Folder

```bash
# Use any folder on your computer
python scripts/batch_ingest_flexible.py --dir /path/to/your/papers

# Examples for different systems:

# macOS
python scripts/batch_ingest_flexible.py --dir ~/Documents/Papers

# Windows
python scripts/batch_ingest_flexible.py --dir "C:/Users/YourName/Documents/Papers"

# External drive (macOS)
python scripts/batch_ingest_flexible.py --dir "/Volumes/My Drive/Research/Papers"

# External drive (Windows)
python scripts/batch_ingest_flexible.py --dir "D:/Research/Papers"
```

### Option 3: Google Drive Sync Folder

```bash
# If you use Google Drive desktop app
python scripts/batch_ingest_flexible.py --dir ~/GoogleDrive/Research/Papers

# Or auto-detect
python scripts/batch_ingest_flexible.py
```

---

## 📋 How It Works

### Step 1: Put PDFs in a Folder

**Any of these work:**

**A. Project folder** (included with ResearcherRAG):
```
01_literature_review_rag/
└── data/
    └── raw_pdfs/          ← Put PDFs here
        ├── paper1.pdf
        ├── paper2.pdf
        └── paper3.pdf
```

**B. Your Documents folder**:
```
~/Documents/
└── Research_Papers/       ← Create this folder
    ├── paper1.pdf
    └── paper2.pdf
```

**C. Google Drive sync folder**:
```
~/Google Drive/
└── Research/
    └── Papers/            ← Create this folder in Google Drive
        ├── paper1.pdf
        └── paper2.pdf
```

### Step 2: Run the Script

```bash
# Auto-detect
python scripts/batch_ingest_flexible.py

# Or specify folder
python scripts/batch_ingest_flexible.py --dir ~/Documents/Research_Papers
```

### Step 3: Confirm

```
📁 Found 25 PDF files

Files to process:
   1. smith_2023_technology.pdf
   2. jones_2022_education.pdf
   ...

Process these files? (y/n): y     ← Type 'y' and press Enter
```

### Step 4: Wait for Processing

```
📝 Processing papers...
⏳ This may take a few minutes...

✓ Created 487 text chunks from 25 papers
🔄 Adding to vector database...

✅ Ingestion Complete!
```

### Step 5: Query Your Papers

```bash
python app.py
# Go to http://localhost:7860
# Click "Ask Questions" tab
```

---

## 🌐 Google Drive Integration (Two Methods)

### Method A: Google Drive Sync Folder (Easiest) ⭐

**Setup** (one-time):
1. Install [Google Drive desktop app](https://www.google.com/drive/download/)
2. Create folder in Google Drive: `Research/Papers`
3. Upload PDFs to that folder
4. Wait for sync to complete

**Usage**:
```bash
# Auto-detect Google Drive folder
python scripts/batch_ingest_flexible.py

# Or specify explicitly
python scripts/batch_ingest_flexible.py --dir ~/GoogleDrive/Research/Papers
```

**Advantages**:
- ✅ No API setup needed
- ✅ Works offline (after first sync)
- ✅ Automatic sync
- ✅ Simple to use

---

### Method B: Direct Google Drive API (Advanced)

**Setup** (one-time, 10 minutes):

**Step 1: Enable Google Drive API**
1. Go to: https://console.cloud.google.com/
2. Create new project: "ResearcherRAG"
3. Enable "Google Drive API"
4. Create credentials:
   - Type: OAuth client ID
   - Application type: Desktop app
   - Name: ResearcherRAG
5. Download `credentials.json`
6. Save to: `01_literature_review_rag/scripts/credentials.json`

**Step 2: Install Google API Libraries**
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

**Step 3: Authenticate**
```bash
python scripts/sync_google_drive.py --setup
```
- Browser opens automatically
- Sign in with Google account
- Grant permissions
- Done! (token saved for future use)

**Usage**:
```bash
# Download from specific folder
python scripts/sync_google_drive.py --folder "Research Papers"

# Download and auto-ingest
python scripts/sync_google_drive.py --folder "Research Papers" --ingest
```

**Advantages**:
- ✅ Access papers without local sync
- ✅ Works from any computer
- ✅ Automatic download + ingestion
- ✅ Always up-to-date

**Example Output**:
```
🔍 Searching for folder: 'Research Papers'...
✓ Found folder: Research Papers

📄 Listing PDF files...
✓ Found 25 PDF files

📥 Downloading files...
  [ 1/25] ⬇️  smith_2023.pdf... ✓
  [ 2/25] ⬇️  jones_2022.pdf... ✓
  ...

✓ Downloaded: 25 files
📝 Ingesting papers into RAG system...
✅ Ingestion complete!
```

---

## 🔧 Advanced Options

### Recursive Scanning (Scan Subdirectories)

```bash
# If your papers are organized in subdirectories:
# Papers/
#   ├── Project1/
#   │   ├── paper1.pdf
#   │   └── paper2.pdf
#   └── Project2/
#       └── paper3.pdf

python scripts/batch_ingest_flexible.py --dir ~/Documents/Papers --recursive
```

### Skip Confirmation

```bash
# Auto-accept (useful for scripts)
python scripts/batch_ingest_flexible.py --yes
```

### Combine Options

```bash
# Recursive + auto-accept
python scripts/batch_ingest_flexible.py --recursive --yes

# Custom dir + recursive
python scripts/batch_ingest_flexible.py --dir ~/Dropbox/Research --recursive
```

---

## 💡 Best Practices

### 1. Organize by Project

**Good folder structure**:
```
Research_Papers/
├── Project_Teacher_AI/
│   ├── paper1.pdf
│   ├── paper2.pdf
│   └── paper3.pdf
├── Project_Student_Tech/
│   ├── paper4.pdf
│   └── paper5.pdf
└── General_Reading/
    └── paper6.pdf
```

**Process each project separately**:
```bash
# Project 1
python scripts/batch_ingest_flexible.py --dir ~/Documents/Research_Papers/Project_Teacher_AI

# Project 2
python scripts/batch_ingest_flexible.py --dir ~/Documents/Research_Papers/Project_Student_Tech
```

### 2. Use Cloud Sync for Collaboration

**Team workflow**:
1. Create shared Google Drive folder: "Team Research Papers"
2. Each team member syncs to their computer
3. Everyone can run batch ingest locally
4. Papers stay in sync automatically

### 3. Naming Convention

**Good naming**:
```
smith_2023_technology_adoption.pdf
jones_2022_teacher_barriers_AI.pdf
doe_2021_meta_analysis_EdTech.pdf
```

**Why**: Easier to identify in search results and citations

### 4. Regular Updates

**Add new papers anytime**:
```bash
# Add new PDFs to your folder
# Then re-run:
python scripts/batch_ingest_flexible.py

# Script only processes new files (skips duplicates)
```

---

## 🆚 Comparison: Which Method to Use?

| Method | Best For | Setup Time | Internet Required |
|--------|----------|------------|-------------------|
| **Auto-detect** | Quick start | 0 min | No |
| **Custom folder** | Personal organization | 1 min | No |
| **Google Drive Sync** | Team sharing | 5 min | Initial sync only |
| **Google Drive API** | Remote access | 10 min | Yes (for download) |

**Recommendation**:
- **Individual researcher**: Auto-detect or custom folder
- **Team/collaboration**: Google Drive Sync
- **Multiple computers**: Google Drive API

---

## 🐛 Troubleshooting

### "No PDF files found"

**Check**:
1. PDFs are in the right folder
2. Files have `.pdf` extension (not `.PDF` or other)
3. Try `--recursive` if papers are in subdirectories

### "Permission denied"

**macOS/Linux**:
```bash
# Make script executable
chmod +x scripts/batch_ingest_flexible.py
```

### "Directory not found"

**Verify path**:
```bash
# Check if directory exists
ls ~/Documents/Research_Papers

# Use full path if unsure
python scripts/batch_ingest_flexible.py --dir "/Users/yourname/Documents/Research_Papers"
```

### Google Drive sync not working

**Check**:
1. Google Drive desktop app is running
2. Folder is fully synced (check for cloud icons)
3. Path is correct:
   ```bash
   # macOS
   ~/Google Drive/
   # Windows
   C:/Users/YourName/Google Drive/
   ```

---

## 📊 System Requirements

### Disk Space

| Papers | Raw PDFs | Vector DB | Total |
|--------|----------|-----------|-------|
| 10 | ~20 MB | ~10 MB | ~30 MB |
| 50 | ~100 MB | ~50 MB | ~150 MB |
| 100 | ~200 MB | ~100 MB | ~300 MB |
| 500 | ~1 GB | ~500 MB | ~1.5 GB |

### Processing Time

- **Average**: 20 seconds per paper
- **50 papers**: ~15-20 minutes
- **100 papers**: ~30-40 minutes

**Tip**: Process in batches of 20-30 for faster feedback

---

## 🎓 Example Workflows

### Workflow 1: New Research Project

```bash
# 1. Create folder
mkdir ~/Documents/Dissertation_Papers

# 2. Add PDFs to folder (download from Google Scholar, etc.)

# 3. Process
python scripts/batch_ingest_flexible.py --dir ~/Documents/Dissertation_Papers

# 4. Query
python app.py
```

### Workflow 2: Team Collaboration

```bash
# Team lead:
# 1. Create Google Drive folder: "Team Project Papers"
# 2. Share with team
# 3. Upload papers

# Each team member:
# 1. Install Google Drive desktop app
# 2. Sync folder to computer
# 3. Run:
python scripts/batch_ingest_flexible.py --dir ~/GoogleDrive/Team\ Project\ Papers

# Everyone has same papers locally!
```

### Workflow 3: Multiple Projects

```bash
# Project structure:
# ~/Research/
#   ├── Project_A/
#   ├── Project_B/
#   └── Project_C/

# Process all at once (recursive):
python scripts/batch_ingest_flexible.py --dir ~/Research --recursive

# Or process separately:
python scripts/batch_ingest_flexible.py --dir ~/Research/Project_A
python scripts/batch_ingest_flexible.py --dir ~/Research/Project_B
```

---

## 🔄 Updating Papers

### Add New Papers

```bash
# 1. Add new PDFs to your folder
# 2. Re-run script
python scripts/batch_ingest_flexible.py

# Script automatically:
# - Detects new files
# - Skips already-processed files
# - Only processes new ones
```

### Remove Papers

```bash
# Current limitation: No automatic removal yet
# Workaround: Delete database and re-ingest

# Delete database:
rm -rf data/vector_db/*

# Re-ingest all papers:
python scripts/batch_ingest_flexible.py
```

---

## 📚 Summary

**Three simple ways to bulk upload**:

1. **Auto-detect** (easiest):
   ```bash
   python scripts/batch_ingest_flexible.py
   ```

2. **Custom folder** (flexible):
   ```bash
   python scripts/batch_ingest_flexible.py --dir /path/to/papers
   ```

3. **Google Drive** (team):
   ```bash
   python scripts/sync_google_drive.py --folder "Research Papers" --ingest
   ```

**All methods work on any computer!** No hard-coded paths! 🎉

---

**Questions?** Open an issue: https://github.com/HosungYou/researcherRAG/issues
