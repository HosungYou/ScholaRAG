# Error Recovery Workflows

**Purpose**: Step-by-step recovery procedures for critical failures

**For**: Both Claude Code and Codex agents

**When to load**: Pipeline interrupted, data corrupted, or catastrophic errors

---

## Recovery Scenarios

### Scenario 1: Pipeline Interrupted Mid-Execution

**Symptom**:
```
Computer crashed during Stage 3 screening
OR
User accidentally closed terminal during PDF download
```

**Recovery Procedure**:

#### Step 1: Identify Last Successful Stage

```bash
cd projects/YYYY-MM-DD_ProjectName

# Check which data files exist
ls -lah data/01_identification/
ls -lah data/02_screening/
ls -lah data/pdfs/

# Determine last complete stage:
# - combined.csv exists → Stage 1 complete
# - deduplicated.csv exists → Stage 2 complete
# - relevant.csv exists → Stage 3 complete
# - pdfs/*.pdf exist → Stage 4 in progress or complete
```

#### Step 2: Validate Last Stage Data

```bash
# For Stage 1: Check combined.csv not truncated
wc -l data/01_identification/combined.csv
# Should show realistic count (500-5,000 for systematic_review)

# For Stage 2: Check deduplicated.csv not corrupted
head -5 data/01_identification/deduplicated.csv
tail -5 data/01_identification/deduplicated.csv
# Should show proper CSV format with headers

# For Stage 3: Check relevant.csv not partial
wc -l data/02_screening/relevant.csv
# Compare to deduplicated.csv count - should be smaller (2-10% for systematic_review)
```

#### Step 3: Resume from Next Stage

```bash
# If Stage 1 complete, resume from Stage 2
python ../../scripts/02_deduplicate.py --project .

# If Stage 2 complete, resume from Stage 3
python ../../scripts/03_screen_papers.py --project .

# If Stage 3 complete, resume from Stage 4
python ../../scripts/04_download_pdfs.py --project .

# Scripts are idempotent - safe to re-run if previous execution was partial
```

---

### Scenario 2: Corrupted Data File

**Symptom**:
```
Error reading CSV: ParserError at line 547
OR
CSV file shows 0 bytes (empty file)
```

**Recovery Procedure**:

#### Step 1: Identify Corrupted File

```bash
# Check file sizes
du -h data/01_identification/*.csv

# If any file shows 0 bytes or suspiciously small:
ls -lah data/01_identification/combined.csv
# -rw-r--r--  1 user  staff    0B Oct 24 02:34 combined.csv
# ^ 0 bytes = CORRUPTED
```

#### Step 2: Delete Corrupted File

```bash
# Delete only the corrupted file
rm data/01_identification/combined.csv

# Do NOT delete entire folder (may have partial good data)
```

#### Step 3: Re-run Stage from Scratch

```bash
# For Stage 1:
python ../../scripts/01_fetch_papers.py --project .

# For Stage 2:
python ../../scripts/02_deduplicate.py --project .

# For Stage 3:
python ../../scripts/03_screen_papers.py --project .
```

#### Step 4: Validate Re-run Results

```bash
# Check new file size is reasonable
du -h data/01_identification/combined.csv
# Should show MBs, not 0 bytes

# Check row count
wc -l data/01_identification/combined.csv
# Should show hundreds to thousands of papers
```

---

### Scenario 3: API Key Revoked/Expired Mid-Pipeline

**Symptom**:
```
Error: ANTHROPIC_API_KEY invalid or expired
Authentication failed (401 Unauthorized)
Pipeline stopped at Stage 3 (paper 247/1,586)
```

**Recovery Procedure**:

#### Step 1: Update API Key

```bash
# Get new API key from provider dashboard
# For Anthropic: console.anthropic.com

# Set new key in environment
export ANTHROPIC_API_KEY='sk-ant-NEW-KEY-HERE'

# Verify key works
curl https://api.anthropic.com/v1/complete \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "content-type: application/json" \
  -d '{"prompt": "Hello", "model": "claude-3-sonnet-20240229", "max_tokens": 10}' \
  | grep -q "completion" && echo "✅ API key valid" || echo "❌ API key invalid"
```

#### Step 2: Resume Screening from Last Paper

**If script supports checkpointing** (ScholaRAG v2.0+):
```bash
# Script auto-detects last screened paper and resumes
python ../../scripts/03_screen_papers.py --project . --resume

# Output:
# Resuming from paper 248/1,586 (15% complete)
# Estimated remaining: 45 minutes
```

**If script doesn't support checkpointing**:
```bash
# Manually split remaining papers and re-screen

# 1. Check how many papers already screened
wc -l data/02_screening/relevant.csv

# 2. Re-run screening (will skip already-screened papers if script is idempotent)
python ../../scripts/03_screen_papers.py --project .
```

---

### Scenario 4: Disk Full During PDF Download

**Symptom**:
```
Error writing to pdfs/0087_Garcia_2023.pdf
OSError: [Errno 28] No space left on device
Downloaded: 86/142 PDFs (61%)
```

**Recovery Procedure**:

#### Step 1: Free Up Disk Space

```bash
# Check current disk usage
df -h

# Find large files to delete
du -h -d 1 . | sort -hr | head -20

# Common space-saving options:
# Option 1: Delete other project PDFs (if multiple projects)
# Option 2: Move PDFs to external drive
# Option 3: Delete cached data

# Free at least 2GB for remaining PDFs
```

#### Step 2: Resume PDF Download

```bash
# Script auto-skips already-downloaded PDFs
python ../../scripts/04_download_pdfs.py --project .

# Output:
# Checking existing PDFs... found 86
# Downloading remaining 56 PDFs...
```

#### Step 3: Validate All PDFs Downloaded

```bash
# Count PDFs
ls data/pdfs/*.pdf | wc -l

# Check for 0-byte corrupted PDFs
find data/pdfs -name "*.pdf" -size 0

# If corrupted PDFs found, delete and re-download
find data/pdfs -name "*.pdf" -size 0 -delete
python ../../scripts/04_download_pdfs.py --project . --retry-failed
```

---

### Scenario 5: RAG Database Corrupted

**Symptom**:
```
Error querying ChromaDB
sqlite3.DatabaseError: database disk image is malformed
OR
Collection 'papers' not found
```

**Recovery Procedure**:

#### Step 1: Backup Current RAG Database (if partially working)

```bash
# Backup existing database before deleting
cp -r rag/chroma_db rag/chroma_db.backup_$(date +%Y%m%d_%H%M%S)
```

#### Step 2: Delete Corrupted Database

```bash
# Remove corrupted ChromaDB
rm -rf rag/chroma_db

# Verify deletion
ls rag/
# Should NOT show chroma_db folder
```

#### Step 3: Rebuild RAG from PDFs

```bash
# Check PDFs still exist
ls data/pdfs/*.pdf | wc -l

# If PDFs exist, rebuild RAG
python ../../scripts/05_build_rag.py --project .

# Expected duration: 30-60 minutes for 50 PDFs
```

#### Step 4: Validate Rebuilt RAG

```bash
# Test query
python ../../scripts/06_query_rag.py \
  --project . \
  --query "What are the main themes?" \
  --limit 3

# Should return 3 relevant chunks with citations
# Format: 【F:pdfs/0023_Chen_2022.pdf†L145】
```

---

### Scenario 6: Wrong project_type Chosen (After Pipeline Complete)

**Symptom**:
```
Chose knowledge_repository (50% threshold) → Got 12,000 papers
Should have chosen systematic_review (90% threshold) → Want ~100 papers
```

**Recovery Procedure**:

#### Step 1: Assess Impact

```bash
# Check what stages are affected:
# ✅ Stage 1 (Fetch): Not affected (same papers fetched)
# ✅ Stage 2 (Dedup): Not affected (same deduplication logic)
# ❌ Stage 3 (Screen): AFFECTED (threshold changes)
# ❌ Stage 4 (PDF): AFFECTED (different papers selected)
# ❌ Stage 5 (RAG): AFFECTED (built from different PDFs)
```

#### Step 2: Change project_type in Config

```bash
vim config.yaml

# Change:
# project_type: knowledge_repository
# to:
# project_type: systematic_review

# Threshold auto-updates:
# prisma.screening_threshold: 50 → 90
```

#### Step 3: Re-run Affected Stages (3-5)

```bash
# Delete old screening results
rm -rf data/02_screening/*

# Delete old PDFs
rm -rf data/pdfs/*

# Delete old RAG database
rm -rf rag/chroma_db

# Re-run screening with new threshold (90%)
python ../../scripts/03_screen_papers.py --project .

# Continue pipeline
python ../../scripts/04_download_pdfs.py --project .
python ../../scripts/05_build_rag.py --project .
```

#### Step 4: Validate New Results

```bash
# Check retention rate changed
wc -l data/02_screening/relevant.csv

# Before (50% threshold): ~800 papers (80% retention)
# After (90% threshold): ~100 papers (10% retention)

# Verify this matches systematic_review expectations
```

---

### Scenario 7: Query Returns Wrong Papers (After Pipeline Complete)

**Symptom**:
```
Query fetched papers about "chatbot programming" instead of "chatbot learning"
Only 5% of papers are actually relevant
```

**Recovery Procedure**:

#### Step 1: Update Search Query

```bash
vim config.yaml

# Improve query specificity:
# Before: "chatbot" AND "programming"
# After: "(chatbot OR agent) AND (language learning OR L2) AND speaking"
```

#### Step 2: Delete All Pipeline Data

```bash
# WARNING: This deletes ALL results, requires full re-run

# Backup config.yaml first
cp config.yaml config.yaml.backup

# Delete all data
rm -rf data/*
rm -rf rag/*
```

#### Step 3: Re-run Entire Pipeline

```bash
# Start from Stage 1 with new query
python ../../scripts/01_fetch_papers.py --project .
python ../../scripts/02_deduplicate.py --project .
python ../../scripts/03_screen_papers.py --project .
python ../../scripts/04_download_pdfs.py --project .
python ../../scripts/05_build_rag.py --project .

# Expected duration: 4-8 hours (run overnight)
```

---

## Prevention Strategies

### 1. Regular Checkpoints

**Create manual checkpoints before long stages**:
```bash
# Before Stage 3 (screening, long duration)
cp -r data data_backup_before_stage3

# Before Stage 5 (RAG build)
cp -r data data_backup_before_stage5

# If error occurs, restore:
rm -rf data
cp -r data_backup_before_stage3 data
```

### 2. Validate After Each Stage

```bash
# Stage 1: Check paper count
wc -l data/01_identification/combined.csv
# Expected: 500-5,000 for systematic_review

# Stage 2: Check deduplication rate
# Expected: 20-40% duplicates removed

# Stage 3: Check retention rate
# knowledge_repository: 80-90%
# systematic_review: 2-10%

# Stage 4: Check PDF success rate
# Expected: 30-60%

# Stage 5: Test RAG
python ../../scripts/06_query_rag.py --project . --query "test" --limit 1
```

### 3. Monitor Disk Space

```bash
# Before starting pipeline
df -h
# Ensure at least 5GB free

# During pipeline
watch -n 60 'df -h'
# Monitor every 60 seconds
```

### 4. Use Tmux/Screen for Long Sessions

```bash
# Start tmux session
tmux new -s scholarag

# Run pipeline
python ../../scripts/03_screen_papers.py --project .

# Detach: Ctrl+B, then D
# Pipeline continues running even if you disconnect

# Reattach later
tmux attach -t scholarag
```

---

## Emergency Procedures

### Complete Reset (Start Over)

```bash
# WARNING: Deletes ALL project data

cd projects/YYYY-MM-DD_ProjectName

# Backup config.yaml
cp config.yaml ~/config_backup.yaml

# Delete everything except config
rm -rf data/
rm -rf rag/
rm -rf outputs/
rm -rf .scholarag/

# Recreate folders
mkdir -p data/01_identification data/02_screening data/pdfs
mkdir -p rag outputs .scholarag

# Restore config
cp ~/config_backup.yaml config.yaml

# Start fresh from Stage 1
python ../../scripts/01_fetch_papers.py --project .
```

### Partial Reset (Specific Stage)

```bash
# Reset Stage 3 only (keep Stages 1-2)
rm -rf data/02_screening/*
python ../../scripts/03_screen_papers.py --project .

# Reset Stages 4-5 only (keep Stages 1-3)
rm -rf data/pdfs/* rag/*
python ../../scripts/04_download_pdfs.py --project .
python ../../scripts/05_build_rag.py --project .
```

---

## Data Recovery from Backup

**If you have backups** (e.g., Git, Time Machine, Cloud sync):

```bash
# Restore entire project folder
cp -r /path/to/backup/projects/YYYY-MM-DD_ProjectName /path/to/ScholaRAG/projects/

# Or restore specific files:
cp /path/to/backup/data/02_screening/relevant.csv projects/YYYY-MM-DD_ProjectName/data/02_screening/

# Validate restored data
head -10 projects/YYYY-MM-DD_ProjectName/data/02_screening/relevant.csv
```

---

## Logging for Debugging

**Enable detailed logging**:
```bash
# Run script with verbose logging
python ../../scripts/03_screen_papers.py --project . --verbose --log-level DEBUG

# Check logs
cat logs/03_screen_papers.log

# Logs show:
# - API requests/responses
# - Paper-by-paper screening decisions
# - Error tracebacks
```

---

## Contact Support

**If recovery fails**:

1. **Gather diagnostics**:
   ```bash
   # System info
   python --version
   pip list

   # Error logs
   cat logs/*.log > all_logs.txt

   # Config (remove API keys!)
   cp config.yaml config_sanitized.yaml
   sed -i '' 's/sk-ant-.*/REDACTED/' config_sanitized.yaml
   ```

2. **Create GitHub Issue**:
   - Title: "Error Recovery: [Brief Description]"
   - Attach: all_logs.txt, config_sanitized.yaml
   - Include: Recovery steps attempted

3. **Link**: https://github.com/HosungYou/ScholaRAG/issues/new

---

**Last Updated**: 2025-10-24
**Version**: 2.0
**For**: ScholaRAG v2.0+
