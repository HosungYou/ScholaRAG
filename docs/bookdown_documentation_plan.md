# Bookdown-Style Online Documentation Plan

**Inspired By**: https://bookdown.org/MathiasHarrer/Doing_Meta_Analysis_in_R/
**Target Audience**: Researchers (academic, non-programmer friendly)
**Purpose**: Comprehensive online guide for building RAG systems with Claude Code

---

## 📚 Why Bookdown?

### Advantages for Academic Users
1. **Familiar Format**: Researchers already use Bookdown for methodology guides (meta-analysis, statistics, R programming)
2. **Progressive Navigation**: Left sidebar with chapters, right sidebar with sections
3. **Search Functionality**: Full-text search across all chapters
4. **Code Highlighting**: Syntax highlighting for Python, YAML, bash
5. **Interactive Elements**: Collapsible sections, tabbed code examples
6. **PDF Export**: Downloadable as single PDF for offline reading
7. **Mobile Friendly**: Responsive design works on tablets
8. **Version Control**: Git-based, easy to update

### Comparison with Current Approach

| Aspect | Current (Markdown files) | Bookdown Site |
|--------|-------------------------|---------------|
| **Discovery** | Must navigate GitHub folders | Single entry point, hierarchical navigation |
| **Search** | GitHub search (limited) | Full-text search with previews |
| **Reading Flow** | Jump between files | Continuous reading with "Previous/Next" |
| **Code Examples** | Static markdown | Copy buttons, syntax highlighting |
| **Accessibility** | Requires Git knowledge | Web browser, no Git needed |
| **Updates** | Git pull required | Auto-refresh on new commits |
| **Citation** | Hard to reference sections | Permanent URLs per section |
| **Offline** | Clone repo | Download as PDF/ePub |

---

## 🏗️ Proposed Site Structure

### Homepage (index.Rmd)
**URL**: `https://[your-domain].github.io/ResearcherRAG/`

**Content**:
- Project overview (1 paragraph)
- "What is RAG?" explainer (non-technical)
- "Who is this for?" (Graduate students, researchers, librarians)
- Quick navigation boxes:
  - 🚀 **Get Started** → Chapter 1
  - 📖 **Full Guide** → Table of Contents
  - 💻 **Workshop** → Workshop materials
  - 🔧 **Templates** → Code templates
  - 💬 **Community** → Forum/Discord

---

### Part I: Introduction (Chapters 1-3)

#### Chapter 1: Getting Started
**File**: `01-getting-started.Rmd`

**Sections**:
1.1 What You'll Build
- Visual: Screenshot of final RAG system in action
- "In 3 hours, you'll build a custom RAG system for your research"

1.2 Prerequisites
- VS Code + Claude Code installation
- Python 3.9+ setup
- API keys (optional: Semantic Scholar, OpenAlex)
- Time commitment: 3 hours workshop + 2 hours homework

1.3 Learning Path
- Flowchart: Beginner → Intermediate → Advanced
- "Choose your path" quiz (research domain, technical skill)

1.4 Installation Guide
- Step-by-step with screenshots
- Troubleshooting common issues (permissions, Python not found)
- Video embed (if available)

---

#### Chapter 2: RAG Fundamentals for Researchers
**File**: `02-rag-fundamentals.Rmd`

**Sections**:
2.1 What is RAG? (Non-technical)
- Analogy: "RAG = Smart research assistant with perfect memory"
- Diagram: Traditional search vs. RAG
- Real example: "Show me papers on chatbot effectiveness" → RAG answer with citations

2.2 Why RAG for Research?
- Problem: Information overload (20,555 papers → how to read all?)
- Solution: RAG reads papers, you ask questions
- Benefits:
  - **Speed**: 2 hours vs. 2 weeks for screening
  - **Accuracy**: Consistent criteria, no fatigue
  - **Recall**: Query 100s of papers instantly
  - **Synthesis**: Cross-paper insights

2.3 How RAG Works (Simplified)
- 3-step process:
  1. **Embed**: Convert papers to numbers (vectors)
  2. **Retrieve**: Find relevant chunks (semantic search)
  3. **Generate**: AI writes answer with citations
- Interactive diagram (click each step to learn more)

2.4 RAG vs. Traditional Methods
- Comparison table:
  - Manual review
  - Reference managers (Zotero, Mendeley)
  - Citation databases (Web of Science)
  - RAG systems

---

#### Chapter 3: PRISMA Systematic Reviews
**File**: `03-prisma-intro.Rmd`

**Sections**:
3.1 What is PRISMA?
- PRISMA 2020 guidelines overview
- 4 stages: Identification → Screening → Eligibility → Inclusion
- Flowchart visual

3.2 Why Automate PRISMA?
- Problem: Manual screening takes weeks
- Solution: AI-powered multi-dimensional scoring
- Case study: AI failure_HR (20,555 → 592 papers in 2 hours)

3.3 Multi-dimensional Scoring
- Explain keyword weighting system
- Example: How a paper gets scored (step-by-step)
- Interactive calculator (input title/abstract, see score)

3.4 PRISMA + RAG Integration
- How PRISMA screening feeds into RAG
- "Quality in, quality out" principle
- Visual: PRISMA → Vector DB → RAG queries

---

### Part II: Building Your RAG System (Chapters 4-8)

#### Chapter 4: Define Your Research Scope
**File**: `04-research-scope.Rmd`

**Sections**:
4.1 Why This Matters
- "Garbage in, garbage out"
- Narrow vs. broad: Trade-offs

4.2 Interactive Exercise: Research Domain Setup
- Copy-paste prompt template (from `prompts/01_research_domain_setup.md`)
- Sample conversation with Claude Code
- Common pitfalls and how to avoid them

4.3 Example: Education Research
- Walkthrough: "AI chatbots in language learning"
- Show actual Claude conversation
- Result: Research scope defined

4.4 Example: Medical Research
- Walkthrough: "EHR alert fatigue"
- Different keywords, same process
- Result: Medical-specific profile

4.5 Your Turn
- Checklist: Before moving to next chapter
- Self-assessment: "Is my scope clear?"

---

#### Chapter 5: Design Search Queries
**File**: `05-search-queries.Rmd`

**Sections**:
5.1 Query Strategy Fundamentals
- Boolean operators (AND, OR, NOT)
- Synonyms and wildcards
- Field-specific search (title, abstract, fulltext)

5.2 Data Sources Comparison
- Semantic Scholar (CS, Engineering, General)
- OpenAlex (All fields, metadata)
- arXiv (STEM preprints)
- PubMed (Medicine)
- ERIC (Education)
- Comparison table with pros/cons

5.3 Interactive Exercise: Query Design
- Prompt template (from `prompts/02_query_strategy.md`)
- Query builder tool (future: interactive form)
- Expected results calculator

5.4 Example Queries by Domain
- Education: Language learning chatbots
- Medicine: Clinical decision support systems
- Psychology: Mindfulness interventions
- Economics: Minimum wage employment effects

5.5 Troubleshooting Query Issues
- Too many results (>2000) → Narrow with AND
- Too few results (<100) → Broaden with OR
- Irrelevant results → Add exclusion keywords

---

#### Chapter 6: Configure PRISMA Screening
**File**: `06-prisma-configuration.Rmd`

**Sections**:
6.1 Collecting Papers
- API integration code (Semantic Scholar, OpenAlex)
- Rate limits and best practices
- Saving metadata (CSV format)

6.2 Analyzing Paper Metadata
- Year distribution analysis
- Keyword extraction (BERTopic)
- Methodology estimation (experimental, survey, qualitative)

6.3 Building Research Profiles (YAML)
- Domain keywords with weights
- Method keywords
- Topic keywords
- Exclusion keywords
- Threshold settings

6.4 Interactive Exercise: Profile Generation
- Claude auto-generates profile from metadata
- User reviews and adjusts
- Test with sample papers

6.5 Running PRISMA Screening
- Execute `2_run_prisma.py`
- Interpret results (pass rates per stage)
- PRISMA flow diagram

6.6 Adjusting Thresholds
- Too strict (5% pass) → Lower thresholds
- Too lenient (80% pass) → Raise thresholds
- Iterative refinement process

---

#### Chapter 7: Build Vector Database
**File**: `07-vector-database.Rmd`

**Sections**:
7.1 PDF Acquisition
- **Reality check**: 50-60% success rate expected
- Tier 1: Institutional access (VPN)
- Tier 2: Unpaywall (open access)
- Tier 3: Author requests (email templates)
- Tier 4: Abstracts as fallback

7.2 Text Extraction
- PyMuPDF (primary method)
- pdfplumber (backup)
- Tesseract OCR (fallback for scanned PDFs)
- Quality checks

7.3 Chunking Strategy
- Chunk size (1000 tokens recommended)
- Overlap (200 tokens recommended)
- Why chunking matters (retrieval precision)

7.4 Embedding Models
- sentence-transformers/all-MiniLM-L6-v2 (default)
- OpenAI text-embedding-3-small (paid, higher quality)
- Comparison and when to use each

7.5 ChromaDB Setup
- Local vector database
- Collection organization (one per project)
- Storage requirements (~ 1 MB per 100 papers)

7.6 Interactive Exercise: Build Your Vector DB
- Execute `5_build_vectordb.py`
- Monitor progress (embeddings, indexing)
- Verify success (query test)

---

#### Chapter 8: Design RAG Prompts
**File**: `08-rag-prompts.Rmd`

**Sections**:
8.1 System Prompt Engineering
- Role definition ("research assistant specializing in...")
- Task instructions (cite papers, report methods, etc.)
- Citation format requirements
- Tone and style

8.2 Example System Prompts by Domain
- Education research
- Medical research
- Psychology research
- Social science

8.3 Retrieval Configuration
- Top-k (how many chunks to retrieve)
- Similarity threshold (minimum relevance)
- Re-ranking (cross-encoder for better quality)

8.4 Generation Settings
- Model selection (Claude 3.5 Sonnet recommended)
- Temperature (0.3 for factual, 0.7 for creative)
- Max tokens (1500 for answers)

8.5 Interactive Exercise: Test Your RAG
- Execute `6_query_rag.py`
- Try 5 sample questions
- Evaluate answer quality (accuracy, citations, completeness)

---

### Part III: Advanced Topics (Chapters 9-11)

#### Chapter 9: Troubleshooting Common Issues
**File**: `09-troubleshooting.Rmd`

**Sections**:
9.1 Low PDF Download Success (<30%)
- Check institutional access
- Enable Unpaywall
- Try OpenAlex open access filter
- Use abstracts as fallback

9.2 Wrong PRISMA Results
- Analyze score distribution
- Adjust thresholds
- Review keyword weights
- Check for excluded papers that should pass

9.3 Generic RAG Answers (Not Citing Papers)
- Lower similarity threshold
- Increase top-k retrieved chunks
- Strengthen citation requirement in prompt
- Enable re-ranking

9.4 Slow Query Performance
- Reduce embedding dimensions (384 → 256)
- Limit max retrieved chunks
- Use faster models (GPT-3.5 vs GPT-4)

9.5 Out of Memory Errors
- Reduce batch size for embedding
- Process papers in smaller groups
- Use streaming for large queries

---

#### Chapter 10: Managing Multiple Projects
**File**: `10-multi-project.Rmd`

**Sections**:
10.1 Directory Structure
- One folder per research project
- Shared templates, separate data
- Version control best practices

10.2 Project Switching
- Activate correct environment
- Load correct research profile
- Query correct vector DB collection

10.3 Cross-Project Queries
- Query multiple RAG systems simultaneously
- Synthesize insights across domains
- Use cases: Interdisciplinary research

10.4 Collaboration
- Sharing research profiles (YAML on GitHub)
- Sharing vector DBs (export/import)
- Team workflows (Git branches)

---

#### Chapter 11: Advanced Features (Preview)
**File**: `11-advanced-features.Rmd`

**Sections**:
11.1 Citation Graph Analysis
- Find seminal papers (high citation count)
- Discover "bridge" papers (connect fields)
- Visualize citation networks

11.2 Temporal Trend Analysis
- Track research trend evolution (2010 → 2024)
- Identify emerging topics
- Predict future directions

11.3 Multi-lingual RAG
- Include non-English papers
- Cross-lingual embeddings
- Query in English, retrieve multilingual

11.4 Automated Meta-Analysis
- Extract effect sizes from papers
- Generate forest plots
- Calculate summary statistics

11.5 Roadmap to v2.0
- Collaborative RAG (multi-user)
- RAG-as-a-Service (cloud hosting)
- Writing assistance (related work section)

---

### Part IV: Workshop & Resources (Chapters 12-14)

#### Chapter 12: 3-Hour Workshop Guide
**File**: `12-workshop-guide.Rmd`

**Content**: Embed `workshop/hands_on_guide.md`
- Part 1: Introduction (30 min)
- Part 2: Hands-on exercises (90 min)
- Part 3: Advanced topics (30 min)
- Part 4: Wrap-up (30 min)

**Interactive Elements**:
- Downloadable slides (PDF)
- Sample dataset (50 papers)
- Exercise checklists
- Instructor notes (collapsible sections)

---

#### Chapter 13: Code Templates
**File**: `13-code-templates.Rmd`

**Sections**:
13.1 Research Profile Templates
- Education template (YAML)
- Medicine template (YAML)
- Social science template (YAML)
- How to customize

13.2 Python Script Templates
- 1_collect_papers_template.py (with explanations)
- 2_run_prisma_template.py
- 3_download_pdfs_template.py
- 4_extract_text_template.py
- 5_build_vectordb_template.py
- 6_query_rag_template.py

13.3 Prompt Templates
- Stage 1: Research domain setup
- Stage 2: Query strategy
- Stage 3: PRISMA configuration
- Stage 4: RAG design
- Stage 5: Execution plan

---

#### Chapter 14: Community & Support
**File**: `14-community.Rmd`

**Sections**:
14.1 Getting Help
- GitHub Issues (bug reports)
- GitHub Discussions (questions)
- Office hours (schedule)
- Forum/Discord (community)

14.2 Contributing
- Report bugs
- Suggest features
- Share templates
- Write documentation

14.3 Success Stories
- Published papers using this tool
- Research groups adopting RAG
- Workshop testimonials

14.4 Citation & Acknowledgment
- How to cite this project
- Academic paper (if published)
- Funding acknowledgments

---

## 🛠️ Technical Implementation

### Technology Stack

**Option A: Bookdown (R-based)** ⭐ Recommended
- **Pros**:
  - True Bookdown format (familiar to researchers)
  - Excellent PDF/ePub export
  - Mature, stable, well-documented
  - Great R code integration (if needed for examples)
- **Cons**:
  - Requires R installation for building
  - Less flexible than modern JS frameworks
  - Heavier dependency (R, rmarkdown, etc.)

**Implementation**:
```bash
# Install R and Bookdown
install.packages("bookdown")

# Project structure
ResearcherRAG/
└── docs_site/
    ├── index.Rmd
    ├── 01-getting-started.Rmd
    ├── 02-rag-fundamentals.Rmd
    ├── ...
    ├── _bookdown.yml (config)
    ├── _output.yml (HTML/PDF settings)
    └── style.css (custom CSS)

# Build site
Rscript -e "bookdown::render_book('index.Rmd', 'bookdown::gitbook')"

# Output
└── _book/ (deployable HTML)
```

---

**Option B: MkDocs Material** (Python-based alternative)
- **Pros**:
  - Python ecosystem (matches project stack)
  - Beautiful Material Design UI
  - Fast build times
  - Easy to customize with plugins
- **Cons**:
  - Not "real" Bookdown (different aesthetic)
  - Less familiar to academic audience
  - PDF export requires plugin

**Implementation**:
```bash
pip install mkdocs-material

# Project structure
ResearcherRAG/
└── docs_site/
    ├── docs/
    │   ├── index.md
    │   ├── getting-started.md
    │   └── ...
    └── mkdocs.yml (config)

# Build site
mkdocs build

# Output
└── site/ (deployable HTML)
```

---

**Option C: Quarto** (Next-gen Bookdown)
- **Pros**:
  - Modern replacement for Bookdown
  - Supports Python, R, Julia code
  - Better performance than Bookdown
  - Active development
- **Cons**:
  - Newer, less community knowledge
  - Still maturing

**Implementation**:
```bash
# Install Quarto
# https://quarto.org/docs/get-started/

# Project structure
ResearcherRAG/
└── docs_site/
    ├── _quarto.yml
    ├── index.qmd
    ├── getting-started.qmd
    └── ...

# Build site
quarto render

# Output
└── _site/ (deployable HTML)
```

---

### Recommended Choice: **Bookdown (Option A)**

**Reasons**:
1. Your reference (https://bookdown.org/MathiasHarrer/Doing_Meta_Analysis_in_R/) uses Bookdown
2. Researchers already trust Bookdown format (many methodology guides use it)
3. Excellent for long-form documentation (10+ chapters)
4. Best PDF export quality (for offline reading)
5. Left sidebar navigation matches researcher expectations

**Decision**: Use Bookdown unless you have strong preference for Python stack (then MkDocs Material)

---

### Deployment

**GitHub Pages** (Free, Recommended)
```bash
# Enable GitHub Pages in repo settings
# Point to /docs_site/_book/ folder
# Or use gh-pages branch

# Auto-deploy with GitHub Actions
# .github/workflows/deploy-bookdown.yml
name: Build and Deploy Bookdown Site
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: r-lib/actions/setup-r@v2
      - name: Install Bookdown
        run: Rscript -e 'install.packages("bookdown")'
      - name: Build site
        run: Rscript -e 'bookdown::render_book("docs_site/index.Rmd")'
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs_site/_book
```

**Result**: `https://[your-username].github.io/ResearcherRAG/`

---

### Content Migration Plan

**Phase 1: Core Chapters** (1 week)
- [x] Convert existing markdown to .Rmd
- [ ] Chapter 1: Getting Started
- [ ] Chapter 2: RAG Fundamentals
- [ ] Chapter 3: PRISMA Intro
- [ ] Chapter 4: Research Scope (from prompts/01)
- [ ] Chapter 5: Search Queries (from prompts/02)

**Phase 2: Technical Chapters** (1 week)
- [ ] Chapter 6: PRISMA Configuration (from prompts/03)
- [ ] Chapter 7: Vector Database (from prompts/04)
- [ ] Chapter 8: RAG Prompts (from prompts/05)

**Phase 3: Advanced & Resources** (3 days)
- [ ] Chapter 9: Troubleshooting (from workshop guide Part 3)
- [ ] Chapter 10: Multi-project (from CLAUDE.md)
- [ ] Chapter 11: Advanced Features (from ROADMAP.md)

**Phase 4: Workshop & Community** (2 days)
- [ ] Chapter 12: Workshop Guide (embed workshop/hands_on_guide.md)
- [ ] Chapter 13: Code Templates (embed templates/)
- [ ] Chapter 14: Community (new content)

**Phase 5: Polish** (2 days)
- [ ] Add diagrams (Mermaid, draw.io)
- [ ] Add screenshots
- [ ] Test all code examples
- [ ] Proofread and edit
- [ ] Set up GitHub Pages deployment

**Total Estimate**: 2.5 weeks (20-25 hours)

---

## 📐 Design Specifications

### Visual Style (Matching Reference)
- **Color Scheme**:
  - Primary: Blue (#2780e3) for links and headers
  - Secondary: Gray (#333) for text
  - Accent: Green (#28a745) for success, Red (#dc3545) for warnings
- **Typography**:
  - Headers: Lato or Source Sans Pro (sans-serif)
  - Body: Georgia or Source Serif Pro (serif, easier to read)
  - Code: Fira Code or Source Code Pro (monospace)
- **Layout**:
  - Left sidebar: 250px, chapters + sections
  - Main content: Max 800px wide (optimal line length)
  - Right sidebar: 200px, table of contents for current chapter

### Interactive Elements
1. **Copy Code Buttons**: One-click copy for all code blocks
2. **Collapsible Sections**: Hide/show advanced content
3. **Tabbed Code Examples**: Switch between domains (Education/Medicine)
4. **Search Bar**: Full-text search with live preview
5. **Progress Indicator**: "You've completed 4/14 chapters"
6. **Download Buttons**: PDF, ePub, sample data

### Accessibility
- WCAG 2.1 AA compliance
- Alt text for all images
- Keyboard navigation support
- Screen reader friendly
- High contrast mode option

---

## 📊 Success Metrics

### Traffic (Google Analytics)
- Page views per month: Target 1,000+ by month 3
- Unique visitors: Target 300+ by month 3
- Average time on site: Target 15+ minutes
- Bounce rate: Target <40%

### Engagement
- Chapter completion rate: Target 50%+ finish Chapter 5
- Search usage: Target 30%+ of visitors use search
- Download rate: Target 20%+ download PDF

### Conversion
- GitHub stars: Target +50 from site launch
- Workshop signups: Target 20+ inquiries within 3 months
- Community forum posts: Target 10+ posts per week

### Feedback
- "Was this helpful?" widget on each page
- Target 80%+ positive responses
- Collect feature requests via inline forms

---

## 🚀 Deployment Timeline

### Milestone 1: MVP Site (v1.1.0 launch)
**Target**: 2025-10-25
**Content**:
- Homepage + Chapters 1-5 (Core workflow)
- Basic Bookdown theme
- GitHub Pages deployment
- No advanced features yet

**Goal**: Functional documentation for workshop participants

---

### Milestone 2: Complete Site (v1.2.0)
**Target**: 2025-11-15
**Content**:
- All 14 chapters complete
- Custom CSS styling (match reference)
- Interactive elements (copy buttons, search)
- PDF download available

**Goal**: Comprehensive reference for all users

---

### Milestone 3: Enhanced Site (v1.3.0)
**Target**: 2026-01-15
**Content**:
- Video embeds (tutorial series)
- Interactive demos (query builder, threshold calculator)
- Community showcase (success stories)
- Multi-language support (Korean, Chinese)

**Goal**: Premium documentation experience

---

## 📋 Next Steps

### Immediate (This Week)
1. ✅ Create this planning document
2. ⏳ Add to project_management/TODO.md
3. ⏳ Update release-notes/v1.1.0.md with Bookdown plan
4. ⏳ Create docs_site/ folder structure
5. ⏳ Set up Bookdown project (index.Rmd, _bookdown.yml)

### Short-term (Next 2 Weeks)
1. Convert prompts/01-02 to Chapters 4-5
2. Write Chapters 1-3 (Introduction)
3. Set up GitHub Pages deployment
4. Launch MVP site

### Medium-term (v1.2.0)
1. Complete all 14 chapters
2. Add diagrams and screenshots
3. Custom CSS styling
4. PDF export

---

## 💡 Key Decisions

### Q1: Bookdown vs. MkDocs vs. Quarto?
**Decision**: Bookdown (R-based)
**Reason**: Matches reference site, familiar to researchers, best PDF export

### Q2: Deploy where?
**Decision**: GitHub Pages (free)
**Reason**: No cost, easy Git integration, sufficient traffic for academic project

### Q3: How many chapters?
**Decision**: 14 chapters (Part I-IV)
**Reason**: Comprehensive but not overwhelming, matches 3-hour workshop + advanced topics

### Q4: Interactive elements in MVP?
**Decision**: Copy buttons only, defer calculators/demos to v1.2.0
**Reason**: Focus on content first, interactivity second

### Q5: Who writes the content?
**Decision**: Convert existing markdown (prompts, workshop guide, CLAUDE.md)
**Reason**: 80% content already exists, just needs reformatting + editing

---

**Document Status**: Planning Complete
**Priority**: Medium (launch with v1.2.0, not blocking v1.1.0)
**Owner**: Project Lead
**Contributors**: Claude Code (content conversion), Community (future edits)
**Next Review**: After v1.1.0 release (2025-10-25)
