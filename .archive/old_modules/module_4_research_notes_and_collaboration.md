# Module 4: Research Notes RAG & Team Collaboration

## Learning Objectives
By the end of this module, you will:
- Build a personal research notes RAG system (second brain for researchers)
- Implement multi-user collaboration features
- Create project-based RAG collections with access control
- Set up automated knowledge synthesis across projects
- Deploy the complete ResearcherRAG platform for team use

---

## Module 4A: Research Notes RAG (Personal Knowledge Management)

### The Problem: Information Overload for Researchers

Researchers accumulate vast amounts of information:
- 📚 **Literature notes**: Summaries from papers
- 💡 **Ideas**: Spontaneous thoughts, research questions
- 📊 **Data observations**: Patterns noticed during analysis
- 🎓 **Conference notes**: Presentations, conversations
- 📝 **Grant drafts**: Proposals, reviewer feedback
- 🗂️ **Project logs**: Meeting notes, decisions

**Challenge**: Retrieving the right information at the right time!

### Solution: Research Notes RAG

A personal knowledge base that:
- Connects related ideas automatically
- Surfaces relevant past insights
- Generates synthesis across projects
- Tracks the evolution of your thinking

---

### Architecture

```
Research Notes RAG System
├── Input Sources
│   ├── Markdown notes (Obsidian, Notion, Roam)
│   ├── Voice memos (transcribed)
│   ├── Email annotations
│   ├── PDF highlights (from Zotero, Mendeley)
│   └── Meeting transcripts
├── Processing
│   ├── Automatic tagging & categorization
│   ├── Entity extraction (authors, concepts, dates)
│   ├── Relationship mapping (notes that should link)
│   └── Temporal indexing (find "what I was thinking in June 2023")
├── Retrieval & Synthesis
│   ├── Semantic search across all notes
│   ├── Chronological browsing
│   ├── Concept network visualization
│   └── Automated literature review from notes
└── Output
    ├── Research briefs (synthesize notes on topic)
    ├── Writing assistant (relevant quotes & ideas)
    └── Grant proposal helper (find supporting evidence)
```

---

### Implementation

**Directory Structure:**
```
03_research_notes_rag/
├── backend/
│   ├── core/
│   │   ├── note_parser.py          # Parse markdown, Obsidian, etc.
│   │   ├── entity_extractor.py     # Extract authors, concepts
│   │   ├── relationship_mapper.py  # Find connections
│   │   └── synthesis_engine.py     # Generate insights
│   └── integrations/
│       ├── obsidian_sync.py        # Bi-directional Obsidian sync
│       ├── zotero_highlights.py    # Import Zotero annotations
│       └── email_clipper.py        # Save emails as notes
├── frontend/
│   ├── chainlit_app.py
│   └── components/
│       ├── graph_visualizer.py     # Knowledge graph display
│       └── timeline_view.py        # Chronological notes
└── data/
    ├── notes/
    ├── highlights/
    └── vector_db/
```

**Key Features to Implement:**

**1. Markdown Note Parser**

**Claude Code Prompt:**
```
Create a markdown note parser in backend/core/note_parser.py that:

1. Parses markdown files with frontmatter (YAML metadata):
   ---
   title: "Literature Notes - Smith 2023"
   date: 2024-01-15
   tags: [technology-adoption, meta-analysis]
   project: teacher-ai-study
   ---

2. Extracts wiki-links [[like this]] (Obsidian/Roam style)

3. Identifies different note types:
   - Literature notes (from papers)
   - Fleeting notes (quick ideas)
   - Permanent notes (synthesized insights)
   - Project notes (specific to a study)

4. Extracts structured elements:
   - Block quotes (> quote)
   - Code blocks
   - Highlighted text (==highlight==)
   - Tasks (- [ ] todo)

5. Preserves relationships:
   - Backlinks (notes linking to this note)
   - Forward links (notes this links to)
   - Shared tags

6. Handles different markdown flavors:
   - Standard markdown
   - Obsidian extended syntax
   - Notion export format

Make it robust to malformed markdown and provide helpful error messages.
```

**2. Automated Synthesis Engine**

**Claude Code Prompt:**
```
Create a synthesis engine in backend/core/synthesis_engine.py that can:

1. Generate research briefs:
   Input: "Summarize everything I've learned about teacher resistance to AI"
   Output: Comprehensive summary with:
   - Main themes
   - Supporting evidence from your notes
   - Contradictions/tensions found
   - Gaps in knowledge
   - Suggested next steps

2. Writing assistant mode:
   Input: "I'm writing the literature review section on TAM theory"
   Output:
   - Relevant quotes from your literature notes
   - Your own insights/commentary
   - Suggested structure
   - Citations (if paper metadata available)

3. Idea connector:
   Input: "Show me notes related to 'intrinsic motivation' that I haven't connected yet"
   Output:
   - Notes with similar concepts but no explicit links
   - Suggested connections with reasoning
   - Visualization of concept network

4. Temporal analysis:
   Input: "How has my thinking about mixed methods evolved?"
   Output:
   - Chronological summary
   - Key turning points (when thinking shifted)
   - Evolution of terminology used

Use advanced prompting with chain-of-thought reasoning.
```

**3. Obsidian Integration (Popular Research Tool)**

**Claude Code Prompt:**
```
Create bi-directional Obsidian sync in backend/integrations/obsidian_sync.py:

1. Watch Obsidian vault for changes (using file system watcher)
2. Auto-ingest new/modified notes into RAG system
3. Allow RAG to create new notes in Obsidian (AI-generated insights)
4. Preserve Obsidian graph structure
5. Handle conflicts (if note edited in both places)

This allows researchers to:
- Keep using Obsidian as note-taking tool
- Get RAG superpowers on top of existing notes
- Have AI suggestions appear as new Obsidian notes
```

---

## Module 4B: Team Collaboration Features

### Multi-User Collaboration Architecture

```
Team Collaboration System
├── User Management
│   ├── Authentication (OAuth, institutional SSO)
│   ├── Roles (Admin, Researcher, Read-only)
│   └── Teams & Projects
├── Project Collections
│   ├── Shared vector stores (team-wide)
│   ├── Private collections (individual)
│   ├── Access control (who can read/write)
│   └── Version control (track changes)
├── Collaboration Features
│   ├── Shared annotations
│   ├── Comments & discussions
│   ├── Export/import between projects
│   └── Activity feeds (who added what)
└── Knowledge Synthesis
    ├── Cross-project insights
    ├── Team-wide patterns
    └── Collaboration analytics
```

---

### Implementation

**File: backend/core/project_manager.py**

**Claude Code Prompt:**
```
Create a project management system in backend/core/project_manager.py that:

1. Project structure:
   - Each project has its own vector store collection
   - Projects can be: private, team-shared, or public
   - Projects have metadata: name, description, members, created_date

2. Access control:
   - Owner: Full control
   - Editor: Can add documents, query, annotate
   - Viewer: Can only query, no additions
   - Use role-based permissions

3. Features:
   - Create/delete projects
   - Add/remove team members
   - Clone project (duplicate for new study)
   - Merge projects (combine two RAG collections)
   - Archive projects (preserve but make read-only)

4. Cross-project search:
   - Search across all projects user has access to
   - Filter by project, date range, document type
   - See which project each result comes from

5. Collaboration tracking:
   - Log all actions (who added what, when)
   - Show activity feed per project
   - Generate usage analytics

Implement using SQLite for metadata and ChromaDB collections for RAG data.
```

**File: backend/api/collaboration.py**

**Claude Code Prompt:**
```
Create collaboration API endpoints in backend/api/collaboration.py:

1. POST /projects/create
   Body: {name, description, visibility: "private"|"team"|"public"}

2. POST /projects/{project_id}/members/add
   Body: {user_email, role: "owner"|"editor"|"viewer"}

3. POST /projects/{project_id}/annotations
   Body: {document_id, quote, comment, tags}
   - Allow team members to annotate documents
   - Others can see annotations

4. GET /projects/{project_id}/activity
   - Return activity feed (recent additions, queries, annotations)

5. POST /projects/{project_id}/export
   - Export entire project (documents + annotations + metadata)
   - Format: ZIP file with JSON manifest

6. POST /projects/import
   - Import project from export file
   - Useful for sharing between teams

Include comprehensive error handling and validation.
```

---

### Deployment Architecture

```
Production Deployment
├── Frontend (Chainlit App)
│   └── Served via: Nginx
├── Backend (FastAPI)
│   └── Served via: Uvicorn + Gunicorn
├── Vector Database
│   ├── Option 1: ChromaDB (local, simple)
│   └── Option 2: Qdrant Cloud (scalable, production)
├── Metadata Database
│   └── PostgreSQL (for user data, projects)
├── File Storage
│   ├── Option 1: Local disk
│   └── Option 2: S3/MinIO (scalable)
└── Authentication
    ├── Option 1: Simple username/password
    └── Option 2: OAuth (Google, institutional SSO)

Containerization: Docker Compose
Orchestration: Docker Swarm or Kubernetes (for large deployments)
```

---

### Docker Deployment

**File: docker-compose.yml**

**Claude Code Prompt:**
```
Create a production-ready docker-compose.yml that:

1. Services:
   - fastapi_backend (FastAPI app)
   - chainlit_frontend (Chainlit app)
   - postgres (user metadata, projects)
   - nginx (reverse proxy, SSL termination)
   - qdrant (optional: vector database)

2. Volumes:
   - Persist vector databases
   - Persist uploaded documents
   - Persist PostgreSQL data

3. Networking:
   - Internal network for services
   - Only expose Nginx to internet

4. Environment management:
   - Load from .env file
   - Support different configs (dev, staging, prod)

5. Health checks:
   - Ensure services are running
   - Auto-restart on failure

6. Logging:
   - Centralized logging
   - Rotation to prevent disk fill

Include clear comments for beginners to understand each service.
```

**Expected Output:**
```yaml
version: '3.8'

services:
  # PostgreSQL Database (User accounts, projects, metadata)
  postgres:
    image: postgres:15-alpine
    container_name: researcherrag_postgres
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-researcherrag}
      POSTGRES_USER: ${POSTGRES_USER:-researcher}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-changeme}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U researcher"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Qdrant Vector Database (Optional: for production scale)
  qdrant:
    image: qdrant/qdrant:latest
    container_name: researcherrag_qdrant
    volumes:
      - qdrant_data:/qdrant/storage
    ports:
      - "6333:6333"  # REST API
      - "6334:6334"  # gRPC
    networks:
      - internal
    environment:
      QDRANT__SERVICE__GRPC_PORT: 6334

  # FastAPI Backend
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: researcherrag_backend
    environment:
      # Database
      DATABASE_URL: postgresql://${POSTGRES_USER:-researcher}:${POSTGRES_PASSWORD:-changeme}@postgres:5432/${POSTGRES_DB:-researcherrag}

      # Vector DB
      VECTOR_DB_TYPE: ${VECTOR_DB_TYPE:-chroma}
      QDRANT_URL: http://qdrant:6333

      # API Keys
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}

      # Application
      API_HOST: 0.0.0.0
      API_PORT: 8000
    volumes:
      - uploaded_docs:/app/data/raw_pdfs
      - processed_data:/app/data/processed
      - chroma_db:/app/data/vector_db
    depends_on:
      - postgres
      - qdrant
    networks:
      - internal
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Chainlit Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: researcherrag_frontend
    environment:
      BACKEND_URL: http://backend:8000
      CHAINLIT_HOST: 0.0.0.0
      CHAINLIT_PORT: 8001
    volumes:
      - frontend_sessions:/app/.chainlit
    depends_on:
      - backend
    networks:
      - internal
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: researcherrag_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro  # SSL certificates
      - nginx_logs:/var/log/nginx
    depends_on:
      - frontend
      - backend
    networks:
      - internal
      - external
    restart: unless-stopped

volumes:
  postgres_data:
    driver: local
  qdrant_data:
    driver: local
  chroma_db:
    driver: local
  uploaded_docs:
    driver: local
  processed_data:
    driver: local
  frontend_sessions:
    driver: local
  nginx_logs:
    driver: local

networks:
  internal:
    driver: bridge
  external:
    driver: bridge
```

---

## Deployment Guide for Teams

### Step 1: Server Setup (15 minutes)

**For University/Institutional Server:**
```bash
# SSH into your server
ssh user@your-server.university.edu

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker & Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose-plugin -y

# Clone the repository
git clone https://github.com/your-username/ResearcherRAG.git
cd ResearcherRAG
```

### Step 2: Configuration

**Create .env file:**
```bash
cp .env.example .env
nano .env
```

**Set these variables:**
```bash
# API Keys (REQUIRED)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Database (change password!)
POSTGRES_PASSWORD=your_secure_password_here

# Vector Database
VECTOR_DB_TYPE=qdrant  # or "chroma" for simpler setup

# Domain (for production)
DOMAIN=researcherrag.your-university.edu
```

### Step 3: Launch

```bash
# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f frontend
```

### Step 4: Access

Open browser: `http://your-server-ip`

**First-time setup:**
1. Create admin account
2. Create first project
3. Upload test documents
4. Try a query!

---

## Advanced Features for Teams

### Feature 1: Automated Literature Monitoring

**Claude Code Prompt:**
```
Create an automated literature monitoring system that:

1. Watches Google Scholar, PubMed, arXiv for new papers matching keywords
2. Automatically downloads and ingests new papers weekly
3. Sends email digest to team: "5 new papers on 'teacher AI adoption' this week"
4. Highlights papers highly relevant to current projects
5. Suggests which team member might be interested based on past queries

Implement as background task using Celery or APScheduler.
```

### Feature 2: Collaborative Annotation & Discussion

**Claude Code Prompt:**
```
Add collaborative annotation features:

1. Team members can highlight passages in documents
2. Add comments/questions to highlights
3. Tag team members for discussion (@username)
4. Thread discussions (reply to comments)
5. Resolve discussions (mark as addressed)
6. Export all annotations as supplementary material for publication

Create React component for rich annotation interface.
```

### Feature 3: Project Templates

**Claude Code Prompt:**
```
Create project templates for common research designs:

1. "Systematic Literature Review" template:
   - Pre-configured prompt templates for PRISMA
   - Automatic inclusion/exclusion criteria checking
   - PRISMA flow diagram generator

2. "Qualitative Interview Study" template:
   - Interview parsing setup
   - Predefined coding framework prompts
   - Saturation detection tools

3. "Mixed Methods Study" template:
   - Separate collections for qual & quant data
   - Integration analysis tools

Users can start from template and customize.
```

---

## Module 4 Summary

You now have:
- ✅ Personal research notes RAG system
- ✅ Multi-user collaboration platform
- ✅ Project-based access control
- ✅ Production-ready deployment setup
- ✅ Integration with popular tools (Obsidian, Zotero)

---

## Complete Workshop Summary

### What We Built

**Module 1**: RAG fundamentals + simple demo
**Module 2**: Literature Review RAG (production system)
**Module 3**: Qualitative Coding RAG (interview analysis)
**Module 4**: Research Notes RAG + Collaboration

### Technology Stack

```
Frontend: Chainlit + Streamlit
Backend: FastAPI
LLMs: OpenAI GPT-4, Anthropic Claude
Vector DB: ChromaDB (dev), Qdrant (prod)
Database: PostgreSQL
Deployment: Docker Compose
Language: Python 3.11+
```

### System Capabilities

✅ **Literature Review**
- Ingest 200+ papers
- Semantic search across corpus
- Citation tracking
- Meta-analysis support

✅ **Qualitative Analysis**
- Parse interview transcripts
- AI-assisted coding
- Theme generation
- Export to NVivo/Atlas.ti

✅ **Research Notes**
- Personal knowledge base
- Obsidian integration
- Automated synthesis
- Writing assistance

✅ **Team Collaboration**
- Multi-user projects
- Shared collections
- Access control
- Activity tracking

---

## Next Steps for Learners

### Beginners
1. Complete Module 1 hands-on demo
2. Install and test Module 2 with 5-10 papers
3. Join community Discord for help
4. Share your use case and get feedback

### Advanced Users
1. Customize prompts for your research domain
2. Add new features with Claude Code
3. Integrate additional data sources
4. Contribute to open-source repository

### Instructors/Workshop Facilitators
1. Use these modules as workshop curriculum
2. Adapt to your institution's tech stack
3. Create discipline-specific examples
4. Share improvements back to community

---

## Resources

### Documentation
- [Full API Reference](./api_reference.md)
- [Deployment Guide](./deployment_guide.md)
- [Troubleshooting FAQ](./faq.md)

### Community
- GitHub Repository: `github.com/your-username/ResearcherRAG`
- Discord Server: [Join link]
- Monthly Office Hours: [Calendar link]

### Research Ethics
- [Guidelines for AI-Assisted Research](./ethics_guidelines.md)
- [Transparency in AI Use](./transparency_guide.md)
- [Citing AI Tools in Publications](./citation_guide.md)

---

## Citation

If you use ResearcherRAG in your research, please cite:

```bibtex
@software{researcherrag2024,
  title = {ResearcherRAG: AI-Powered Research Assistant Platform},
  author = {Your Name},
  year = {2024},
  url = {https://github.com/your-username/ResearcherRAG}
}
```

---

## Acknowledgments

Built with:
- [LangChain](https://langchain.com) - RAG framework
- [Chainlit](https://chainlit.io) - Chat interface
- [ChromaDB](https://trychroma.com) - Vector database
- [Anthropic Claude](https://anthropic.com) - Advanced reasoning
- [OpenAI](https://openai.com) - Embeddings & LLMs

---

**🎉 Workshop Complete! Start building your research RAG system today!**

Questions? Issues? Contributions? → GitHub Issues or Discord
