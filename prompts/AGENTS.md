# Prompts Folder - Codex Agent Instructions

**Framework**: PRISMA 2020 + RAG systematic literature review prompts
**Target**: OpenAI Codex agents executing ScholarRAG pipeline
**Context**: 7-stage conversational workflow for academic research automation

---

## Critical Understanding

### What This Folder Contains

7 prompt files representing conversation templates for guiding researchers through systematic literature reviews:

1. `01_research_domain_setup.md` - Research scope definition
2. `02_query_strategy.md` - Database query design
3. `03_prisma_configuration.md` - PRISMA screening criteria
4. `04_rag_design.md` - RAG system architecture
5. `05_execution_plan.md` - Pipeline execution (automated)
6. `06_research_conversation.md` - RAG query interface
7. `07_documentation_writing.md` - PRISMA flowchart generation

**Each file contains**:
- HTML `<!-- METADATA -->` block (YOU MUST READ)
- User-facing prompt template
- Validation checklist
- Expected conversation flow

---

## Your Role as Codex Agent

### When Working with Prompt Files

**DO**:
- ✅ Read HTML metadata block at top of each file
- ✅ Execute scripts specified in `cli_commands` section
- ✅ Validate outputs against expected ranges
- ✅ Update `.scholarag/context.json` after stage completion
- ✅ Run ALL programmatic validation checks before proceeding

**DON'T**:
- ❌ Skip metadata blocks (they contain execution instructions)
- ❌ Execute stages out of order (1→2→3→4→5→6→7 required)
- ❌ Modify result counts in PRISMA diagrams
- ❌ Proceed without completing validation checklist

---

## Stage-by-Stage Execution

### Stage 1: Research Domain Setup

**Metadata location**: `01_research_domain_setup.md` lines 1-69

**Key metadata fields**:
```yaml
stage: 1
cli_commands:
  - command: "scholarag init"
    auto_execute: true
scripts_triggered:
  - none (initialization only)
```

**Execution**:
```bash
# Create project structure
mkdir -p data/01_identification
mkdir -p data/02_screening
mkdir -p data/03_pdfs
mkdir -p data/04_rag
mkdir -p .scholarag

# Create config.yaml
cat > config.yaml <<EOF
project_name: "User's Research Project"
research_question: "From user conversation"
databases: ["semantic_scholar", "openalex", "arxiv"]
year_range: [2015, 2024]
EOF

# Create context.json
cat > .scholarag/context.json <<EOF
{
  "current_stage": 1,
  "completed_stages": [],
  "project_name": "User's Research Project",
  "last_updated": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
```

**Validation**:
```bash
# Check files created
test -f config.yaml || echo "ERROR: config.yaml missing"
test -f .scholarag/context.json || echo "ERROR: context.json missing"
test -d data/01_identification || echo "ERROR: data directory missing"
```

**Expected result**: Project structure initialized, config.yaml created

---

### Stage 2: Query Strategy

**Metadata location**: `02_query_strategy.md` lines 1-78

**Key metadata fields**:
```yaml
stage: 2
scripts_triggered:
  - none (configuration only)
```

**Execution**:
```bash
# Update config.yaml with query
python -c "
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

config['query'] = '(chatbot OR agent) AND language learning'
config['databases'] = ['semantic_scholar', 'openalex', 'arxiv']

with open('config.yaml', 'w') as f:
    yaml.dump(config, f)
"
```

**Validation**:
```bash
# Check query syntax
python -c "
import yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
assert 'query' in config, 'Query not found in config'
assert len(config['query']) > 10, 'Query too short'
print('✅ Query validated')
"
```

**Expected result**: Query saved to config.yaml, syntax validated

---

### Stage 3: PRISMA Configuration

**Metadata location**: `03_prisma_configuration.md` lines 1-85

**Key metadata fields**:
```yaml
stage: 3
scripts_triggered:
  - none (configuration only)
```

**Execution**:
```bash
# Save PRISMA criteria to config.yaml
python -c "
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

config['prisma_criteria'] = {
    'domain_keywords': ['education', 'learning'],
    'method_requirements': ['experimental', 'quasi-experimental'],
    'topic_keywords': ['chatbot', 'speaking', 'oral'],
    'min_score': 4,
    'dimensions': 6
}

with open('config.yaml', 'w') as f:
    yaml.dump(config, f)
"
```

**Validation**:
```bash
# Check PRISMA criteria
python -c "
import yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
criteria = config.get('prisma_criteria', {})
assert criteria.get('min_score', 0) >= 3, 'min_score should be ≥3'
assert criteria.get('dimensions', 0) == 6, 'PRISMA should have 6 dimensions'
print('✅ PRISMA criteria validated')
"
```

**Expected result**: PRISMA criteria configured with 6 dimensions

---

### Stage 4: RAG Design

**Metadata location**: `04_rag_design.md` lines 1-76

**Key metadata fields**:
```yaml
stage: 4
scripts_triggered:
  - none (configuration only, RAG builds in Stage 5)
```

**CRITICAL**: Explain PRISMA-RAG connection

**Execution**:
```bash
# Save RAG configuration
python -c "
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

config['rag_config'] = {
    'chunk_size': 1000,
    'chunk_overlap': 200,
    'embedding_model': 'sentence-transformers/all-MiniLM-L6-v2',
    'top_k': 5,
    'similarity_threshold': 0.7
}

with open('config.yaml', 'w') as f:
    yaml.dump(config, f)
"
```

**Validation**:
```bash
# Check RAG config ranges
python -c "
import yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
rag = config.get('rag_config', {})

chunk_size = rag.get('chunk_size', 0)
assert 500 <= chunk_size <= 2000, f'chunk_size {chunk_size} out of range 500-2000'

overlap = rag.get('chunk_overlap', 0)
assert 50 <= overlap <= 500, f'chunk_overlap {overlap} out of range 50-500'

print('✅ RAG config validated')
"
```

**Expected result**: RAG configuration saved with validated parameters

---

### Stage 5: Execution & Build

**Metadata location**: `05_execution_plan.md` lines 1-85

**Key metadata fields**:
```yaml
stage: 5
cli_commands:
  - command: "python scripts/01_fetch_papers.py"
    auto_execute: true
  - command: "python scripts/02_deduplicate.py"
    auto_execute: true
  - command: "python scripts/03_screen_papers.py"
    auto_execute: true
  - command: "python scripts/04_download_pdfs.py"
    auto_execute: true
  - command: "python scripts/05_build_rag.py"
    auto_execute: true
```

**Execution** (sequential, must run in order):

#### Script 1: Fetch Papers
```bash
cd /path/to/ScholarRAG
python scripts/01_fetch_papers.py --project <project_path>
```

**Expected output**:
- `data/01_identification/semantic_scholar_results.csv`
- `data/01_identification/openalex_results.csv`
- `data/01_identification/arxiv_results.csv`

**Validation**:
```bash
python -c "
import pandas as pd
from pathlib import Path

project = Path('<project_path>')
ss = len(pd.read_csv(project / 'data/01_identification/semantic_scholar_results.csv'))
oa = len(pd.read_csv(project / 'data/01_identification/openalex_results.csv'))
ar = len(pd.read_csv(project / 'data/01_identification/arxiv_results.csv'))

total = ss + oa + ar
assert 100 <= total <= 10000, f'Total {total} papers out of expected range 100-10000'
print(f'✅ Fetched {total} papers (SS:{ss}, OA:{oa}, arXiv:{ar})')
"
```

#### Script 2: Deduplicate
```bash
python scripts/02_deduplicate.py --project <project_path>
```

**Expected output**:
- `data/01_identification/deduplicated.csv`

**Validation**:
```bash
python -c "
import pandas as pd
from pathlib import Path

project = Path('<project_path>')
dedup = len(pd.read_csv(project / 'data/01_identification/deduplicated.csv'))

# Check for duplicates
df = pd.read_csv(project / 'data/01_identification/deduplicated.csv')
dups = df.duplicated(subset=['doi']).sum()
assert dups == 0, f'Found {dups} duplicates after deduplication'

print(f'✅ Deduplicated to {dedup} unique papers')
"
```

#### Script 3: PRISMA Screening
```bash
python scripts/03_screen_papers.py --project <project_path>
```

**Expected output**:
- `data/02_screening/relevant_papers.csv`
- `data/02_screening/excluded_papers.csv`

**Validation**:
```bash
python -c "
import pandas as pd
from pathlib import Path

project = Path('<project_path>')
identified = len(pd.read_csv(project / 'data/01_identification/deduplicated.csv'))
screened = len(pd.read_csv(project / 'data/02_screening/relevant_papers.csv'))

relevance = screened / identified
assert 0.10 <= relevance <= 0.70, f'Relevance {relevance:.1%} out of range 10-70%'
print(f'✅ Screened {screened}/{identified} papers ({relevance:.1%} relevance rate)')
"
```

#### Script 4: Download PDFs
```bash
python scripts/04_download_pdfs.py --project <project_path>
```

**Expected output**:
- `data/03_pdfs/*.pdf`
- `data/03_pdfs/papers_metadata.csv`

**Validation**:
```bash
python -c "
import pandas as pd
from pathlib import Path

project = Path('<project_path>')
metadata = pd.read_csv(project / 'data/03_pdfs/papers_metadata.csv')
downloaded = metadata['downloaded'].sum()
total = len(metadata)

success_rate = downloaded / total
assert 0.20 <= success_rate <= 0.90, f'PDF success rate {success_rate:.1%} out of range 20-90%'
print(f'✅ Downloaded {downloaded}/{total} PDFs ({success_rate:.1%} success rate)')
"
```

#### Script 5: Build RAG
```bash
python scripts/05_build_rag.py --project <project_path>
```

**Expected output**:
- `data/04_rag/chroma_db/` (vector database)
- `data/04_rag/rag_config.json`

**Validation**:
```bash
python -c "
import json
from pathlib import Path

project = Path('<project_path>')
config_path = project / 'data/04_rag/rag_config.json'

with open(config_path, 'r') as f:
    rag_config = json.load(f)

total_chunks = rag_config.get('total_chunks', 0)
total_papers = rag_config.get('total_papers', 0)

assert total_chunks > 0, 'No chunks created'
assert total_papers > 0, 'No papers processed'

chunks_per_paper = total_chunks / total_papers
assert 5 <= chunks_per_paper <= 100, f'{chunks_per_paper:.1f} chunks/paper out of range 5-100'

print(f'✅ RAG built: {total_chunks} chunks from {total_papers} papers ({chunks_per_paper:.1f} chunks/paper)')
"
```

**Test RAG**:
```bash
python scripts/06_query_rag.py --project <project_path> \
  --query "What are the main findings?" \
  | grep -q "【" || echo "WARNING: No citations in response"
```

**Expected result**: All 5 scripts execute successfully, RAG validated

---

### Stage 6: Research Conversation

**Metadata location**: `06_research_conversation.md` lines 1-54

**Key metadata fields**:
```yaml
stage: 6
cli_commands:
  - command: "python scripts/06_query_rag.py --query 'your research question'"
    auto_execute: false
scripts_triggered:
  - scripts/06_query_rag.py (interactive mode)
```

**Execution**:
```bash
# Interactive mode
python scripts/06_query_rag.py --project <project_path> --interactive

# Single query mode
python scripts/06_query_rag.py --project <project_path> \
  --query "What methodologies are used in my papers?"

# Batch mode
python scripts/06_query_rag.py --project <project_path> \
  --queries queries.txt
```

**Validation**:
```bash
# Check that responses include citations
python scripts/06_query_rag.py --project <project_path> \
  --query "Summarize main findings" > response.txt

python -c "
with open('response.txt', 'r') as f:
    response = f.read()

assert '【' in response or '[' in response, 'No citations found in response'
print('✅ RAG responses include citations')
"
```

**Expected result**: User can query RAG, receives citation-backed answers

---

### Stage 7: Documentation & Writing

**Metadata location**: `07_documentation_writing.md` lines 1-45

**Key metadata fields**:
```yaml
stage: 7
cli_commands:
  - command: "python scripts/07_generate_prisma.py"
    auto_execute: true
```

**Execution**:
```bash
python scripts/07_generate_prisma.py --project <project_path>
```

**Expected output**:
- `outputs/prisma_flowchart.png`
- `outputs/prisma_stats.json`

**Validation**:
```bash
# CRITICAL: PRISMA numbers MUST match actual data
python -c "
import json
import pandas as pd
from pathlib import Path

project = Path('<project_path>')

# Load PRISMA stats
with open(project / 'outputs/prisma_stats.json', 'r') as f:
    prisma = json.load(f)

# Load actual data
identified = len(pd.read_csv(project / 'data/01_identification/deduplicated.csv'))
screened = len(pd.read_csv(project / 'data/02_screening/relevant_papers.csv'))
pdfs = pd.read_csv(project / 'data/03_pdfs/papers_metadata.csv')['downloaded'].sum()

# Validate PRISMA matches reality
assert prisma['identified'] == identified, 'PRISMA identified count mismatch'
assert prisma['screened'] == screened, 'PRISMA screened count mismatch'
assert prisma['pdfs_downloaded'] == pdfs, 'PRISMA PDF count mismatch'

print('✅ PRISMA flowchart validated (matches actual data)')
"
```

**Expected result**: PRISMA flowchart generated with ACTUAL pipeline counts

---

## Programmatic Validation Checks

### YOU MUST RUN ALL BEFORE MARKING COMPLETE

#### Data Integrity
```bash
# No duplicate DOIs
python -c "
import pandas as pd
df = pd.read_csv('data/02_screening/relevant_papers.csv')
assert df.duplicated(subset=['doi']).sum() == 0, 'Duplicate papers found'
print('✅ No duplicates')
"
```

#### Statistical Ranges
```bash
# Relevance rate
python -c "
import pandas as pd
identified = len(pd.read_csv('data/01_identification/deduplicated.csv'))
screened = len(pd.read_csv('data/02_screening/relevant_papers.csv'))
relevance = screened / identified
assert 0.10 <= relevance <= 0.70, f'Relevance {relevance:.1%} out of range'
print(f'✅ Relevance rate: {relevance:.1%}')
"
```

#### Semantic Validation
```bash
# Keywords present in relevant papers
python -c "
import pandas as pd
df = pd.read_csv('data/02_screening/relevant_papers.csv')
abstracts = df['abstract'].str.lower().fillna('')

# Check domain keywords
has_keywords = abstracts.str.contains('education|learning|teaching').sum()
assert has_keywords >= len(df) * 0.5, 'Less than 50% mention domain keywords'
print(f'✅ {has_keywords}/{len(df)} papers mention domain keywords')
"
```

---

## Citations Format

When referencing code or outputs:

**File reference**:
```
【F:scripts/03_screen_papers.py†L45】
```

**Multi-line reference**:
```
【F:data/02_screening/relevant_papers.csv†L1-L50】
```

**Terminal output**:
```
【T:bash†python scripts/01_fetch_papers.py】
```

---

## Common Issues and Solutions

### Issue: "Fewer papers than expected"
```bash
# Check API rate limits
grep -i "rate limit" logs/*.log

# Check query specificity
python -c "
import yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
print(f'Query: {config[\"query\"]}')
print('Consider broadening query if too specific')
"
```

### Issue: "Low relevance rate (8%)"
```bash
# Check PRISMA criteria strictness
python -c "
import yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
min_score = config['prisma_criteria']['min_score']
print(f'Current min_score: {min_score}/6')
print('Consider lowering to 3/6 if too strict')
"
```

### Issue: "RAG returns generic answers"
```bash
# Verify RAG is using project papers
python -c "
import json
with open('data/04_rag/rag_config.json', 'r') as f:
    config = json.load(f)
print(f'RAG database: {config[\"persist_directory\"]}')
print(f'Total papers: {config[\"total_papers\"]}')

assert config['total_papers'] > 0, 'RAG database empty'
"
```

---

## File Structure

```
prompts/
├── AGENTS.md (this file)
├── CLAUDE.md (guidance for Claude Code)
├── 01_research_domain_setup.md
├── 02_query_strategy.md
├── 03_prisma_configuration.md
├── 04_rag_design.md
├── 05_execution_plan.md
├── 06_research_conversation.md
└── 07_documentation_writing.md
```

---

## Critical Reminders

1. **Read metadata blocks** - Contains execution instructions
2. **Sequential execution** - Stages must run in order 1→7
3. **Validate before proceeding** - Check ALL criteria
4. **Never fabricate data** - PRISMA counts must be actual
5. **Citations required** - RAG answers must cite papers

---

**Last Updated**: 2025-10-14
**Maintained by**: ScholarRAG Team
**GitHub**: https://github.com/HosungYou/ScholarRAG
