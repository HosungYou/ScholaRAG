# Stage 5: Execution & Build

**Load when**: Stage 5 prompt or user ready to execute pipeline

**Duration**: 2-4 hours (mostly automated, run overnight recommended)

**Goal**: Execute full pipeline from paper fetching to RAG building

---

## Quick Overview

**5 Scripts Execute Automatically**:
1. `01_fetch_papers.py` (30-60 min) - Fetch from 3 APIs
2. `02_deduplicate.py` (5-10 min) - Remove duplicates
3. `03_screen_papers.py` (60-120 min) - AI screening with Claude
4. `04_download_pdfs.py` (120-240 min) - Download PDFs
5. `05_build_rag.py` (30-60 min) - Build vector database

**Total**: ~4-8 hours (run overnight)

---

## Conversation Flow

### Turn 1: Pre-Execution Checklist

```
YOU: "Before we execute the pipeline, let's verify everything is configured:

**Configuration Summary**:
- ✅ Project: AI-Chatbots-Speaking-Proficiency
- ✅ Query: (chatbot OR agent) AND (language learning) AND speaking
- ✅ Databases: Semantic Scholar, OpenAlex, arXiv (3)
- ✅ project_type: systematic_review (90% threshold)
- ✅ PRISMA criteria: Defined
- ✅ RAG config: Saved

**Pre-requisites Check**:
- [ ] ANTHROPIC_API_KEY set in environment
- [ ] Internet connection stable
- [ ] Disk space: ~5GB available (for PDFs)
- [ ] Time availability: 4-8 hours (can run overnight)

Let me verify your API key:

```bash
echo $ANTHROPIC_API_KEY | grep -q "sk-ant-" && echo "✅ API key set" || echo "❌ API key missing"
```

Are you ready to start execution?"
```

### Turn 2: Execute Pipeline

**User confirms**: Ready

**Your action**: Execute all 5 scripts sequentially, show progress

```python
import subprocess
import os

project_path = "projects/2025-10-24_AI-Chatbots"

# Verify API key
if not os.getenv('ANTHROPIC_API_KEY'):
    print("❌ Error: ANTHROPIC_API_KEY not set")
    print("Set it with: export ANTHROPIC_API_KEY='sk-ant-...'")
    exit(1)

print("🚀 Starting pipeline execution...")
print("⏱️  Estimated duration: 4-8 hours")
print("You can close this window - scripts run independently\n")

# Stage 1: Fetch papers
print("📥 Stage 1/5: Fetching papers from 3 databases...")
subprocess.run([
    'python', 'scripts/01_fetch_papers.py',
    '--project', project_path
])

# Stage 2: Deduplicate
print("\n🔍 Stage 2/5: Removing duplicates...")
subprocess.run([
    'python', 'scripts/02_deduplicate.py',
    '--project', project_path
])

# Stage 3: Screen papers (LONG DURATION)
print("\n🤖 Stage 3/5: AI screening with Claude (60-120 min)...")
subprocess.run([
    'python', 'scripts/03_screen_papers.py',
    '--project', project_path
])

# Stage 4: Download PDFs (LONG DURATION)
print("\n📄 Stage 4/5: Downloading PDFs (120-240 min)...")
subprocess.run([
    'python', 'scripts/04_download_pdfs.py',
    '--project', project_path
])

# Stage 5: Build RAG
print("\n🧠 Stage 5/5: Building RAG vector database...")
subprocess.run([
    'python', 'scripts/05_build_rag.py',
    '--project', project_path
])

print("\n✅ Pipeline execution complete!")
print(f"📊 Results saved in: {project_path}/")
print("\n🎯 Next: Stage 6 - Research Conversation")
```

### Turn 3-5: Monitor Progress

**During execution**: Show progress updates after each stage

**Example**:
```
📥 Stage 1/5 Complete: Fetch Papers
├─ Semantic Scholar: 1,247 papers
├─ OpenAlex: 892 papers
├─ arXiv: 134 papers
└─ Total: 2,273 papers

🔍 Stage 2/5 Complete: Deduplication
├─ Before: 2,273 papers
├─ Duplicates removed: 687 (30%)
└─ After: 1,586 unique papers

🤖 Stage 3/5 In Progress: AI Screening
├─ Threshold: 90% (systematic_review mode)
├─ Progress: 487/1,586 papers (31%)
├─ Estimated time remaining: 47 minutes
└─ Current retention rate: 8% (123 papers kept so far)
```

### Turn 6: Validation After Completion

**Your action**: Validate outputs, check paper counts

```bash
# Validate execution results
cd projects/2025-10-24_AI-Chatbots

echo "📊 Pipeline Results Summary:"
echo ""
echo "Stage 1: Fetch Papers"
wc -l data/01_identification/combined.csv
echo ""
echo "Stage 2: Deduplication"
wc -l data/01_identification/deduplicated.csv
echo ""
echo "Stage 3: Screening (90% threshold)"
wc -l data/02_screening/relevant.csv
echo ""
echo "Stage 4: PDF Download"
ls data/pdfs/*.pdf 2>/dev/null | wc -l
echo ""
echo "Stage 5: RAG Database"
du -sh rag/chroma_db

# Test RAG
echo ""
echo "Testing RAG with sample query..."
python ../../scripts/06_query_rag.py \
  --project . \
  --query "What are the main findings?" \
  --limit 3
```

---

## Common Issues

### Issue: API Rate Limit Hit

**Symptom**: Script pauses, shows "Rate limit exceeded, waiting..."

**Response**:
```
"This is normal! Academic APIs have rate limits:

**Semantic Scholar**: 100 requests/5 min
- Script auto-retries with exponential backoff
- No action needed - just wait

**arXiv**: 1 request/3 sec
- Script includes 3-second delay
- Expected for large queries

**Total added time**: Usually 10-20 minutes extra

Let it run - it will complete automatically."
```

### Issue: Low PDF Success Rate (<30%)

**Symptom**: Only 25% of papers have PDFs downloaded

**Response**:
```
"30-60% PDF success is NORMAL for academic papers:

**Why PDFs aren't available**:
- Paywalled journals (Elsevier, Springer, Wiley)
- Publisher embargoes
- Pre-prints not yet published

**Your results**: 25% success rate
- You have 50 papers with PDFs (out of 200 relevant)
- This is enough for systematic review!

**Options**:
1. ✅ Proceed with 50 papers (recommended)
2. Manual download via university VPN (adds 20-30 more)
3. Contact authors for PDFs (time-consuming)

For systematic_review with 50 papers, you can still:
- Conduct narrative synthesis
- Extract themes and methodologies
- Perform limited meta-analysis (if effect sizes available)

Shall we proceed to Stage 6 (RAG analysis) with these 50 papers?"
```

---

## Completion Checklist

- [ ] All 5 scripts executed successfully
- [ ] Paper counts validated at each stage
- [ ] PDF download results acceptable (>20% success)
- [ ] RAG database created and tested
- [ ] Sample query returns relevant results

**If complete**: ✅ Show Stage 6 prompt

---

## Next Stage

[skills/claude_only/stage6_research_conversation.md](stage6_research_conversation.md)

---

**Version**: 2.0 | **Token Budget**: ~300 lines
