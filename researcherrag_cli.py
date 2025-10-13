#!/usr/bin/env python3
"""
ResearcherRAG CLI - Project Management Tool

This CLI tool creates and manages standardized ResearcherRAG projects,
ensuring consistent folder structures that work with Claude Code and the web dashboard.

Usage:
    python researcherrag_cli.py init       # Create new project
    python researcherrag_cli.py status     # Check project status
    python researcherrag_cli.py list       # List all projects
"""

import click
import os
import sys
from datetime import datetime
import yaml
import shutil
from pathlib import Path


@click.group()
def cli():
    """ResearcherRAG CLI - Project Management Tool"""
    pass


@cli.command()
@click.option('--name', prompt='Project name (e.g., AI-Healthcare-Adoption)',
              help='Project name')
@click.option('--question', prompt='Research question',
              help='Main research question')
@click.option('--domain',
              type=click.Choice(['education', 'medicine', 'psychology', 'social-science', 'custom']),
              default='custom',
              prompt='Research domain',
              help='Research domain (loads template)')
def init(name, question, domain):
    """
    Initialize a new ResearcherRAG project with standardized folder structure.

    This command creates:
    - Standardized folder structure (PRISMA 2020 compliant)
    - config.yaml with project settings
    - README.md with project documentation
    - .researcherrag metadata file for dashboard tracking

    Example:
        python researcherrag_cli.py init
        # Follow prompts interactively

        # Or provide all arguments:
        python researcherrag_cli.py init \\
            --name "AI-Healthcare-Adoption" \\
            --question "What factors influence AI adoption in hospitals?" \\
            --domain medicine
    """
    # 1. Sanitize project name
    sanitized_name = name.replace(' ', '-').replace('_', '-')
    today = datetime.now().strftime("%Y-%m-%d")
    project_folder = f"projects/{today}_{sanitized_name}"

    # 2. Check if project already exists
    if os.path.exists(project_folder):
        click.echo(f"\n❌ Error: Project folder already exists: {project_folder}")
        click.echo(f"   Either delete it or choose a different name.\n")
        sys.exit(1)

    # 3. Create folder structure
    click.echo(f"\n📁 Creating project structure...\n")

    folders = [
        f"{project_folder}/data/01_identification",
        f"{project_folder}/data/02_screening",
        f"{project_folder}/data/03_full_text",
        f"{project_folder}/data/pdfs",
        f"{project_folder}/rag/chroma_db",
        f"{project_folder}/outputs",
        f"{project_folder}/conversations",
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        click.echo(f"   ✓ Created: {folder}")

    # 4. Create config.yaml from template
    click.echo(f"\n📝 Creating configuration files...\n")

    if domain != 'custom' and os.path.exists(f"templates/research_profiles/{domain}_template.yaml"):
        # Use domain template
        shutil.copy(
            f"templates/research_profiles/{domain}_template.yaml",
            f"{project_folder}/config.yaml"
        )
        # Update project metadata in config
        with open(f"{project_folder}/config.yaml", 'r') as f:
            config = yaml.safe_load(f)
        config['project']['name'] = name
        config['project']['created'] = today
        config['project']['research_question'] = question
        with open(f"{project_folder}/config.yaml", 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        click.echo(f"   ✓ config.yaml (from {domain} template)")
    else:
        # Create default config
        _create_default_config(project_folder, name, question, domain, today)
        click.echo(f"   ✓ config.yaml (default)")

    # 5. Create README.md
    _create_project_readme(project_folder, name, question, today, sanitized_name)
    click.echo(f"   ✓ README.md")

    # 6. Create .researcherrag metadata (for dashboard tracking)
    metadata = {
        'version': '1.2.0',
        'created': today,
        'project_name': name,
        'research_question': question,
        'domain': domain,
        'current_stage': 1,
        'folder_structure_verified': True,
        'last_updated': today
    }

    with open(f"{project_folder}/.researcherrag", 'w') as f:
        yaml.dump(metadata, f, default_flow_style=False)
    click.echo(f"   ✓ .researcherrag (metadata)")

    # 7. Create .gitkeep files for empty directories
    for folder in folders:
        gitkeep_path = os.path.join(folder, '.gitkeep')
        Path(gitkeep_path).touch()

    # 8. Success message with next steps
    click.echo(f"\n{'='*70}")
    click.echo(f"✅ Project created successfully!")
    click.echo(f"{'='*70}\n")

    click.echo(f"📂 Project Location: {project_folder}\n")

    click.echo("📋 Next Steps:\n")
    click.echo("1️⃣  Open the project in VS Code:")
    click.echo(f"   cd {project_folder}")
    click.echo(f"   code .\n")

    click.echo("2️⃣  Start Claude Code chat:")
    click.echo("   • Press: Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows/Linux)")
    click.echo("   • Type: 'Claude: Open Chat'")
    click.echo("   • Press Enter\n")

    click.echo("3️⃣  Copy-paste this prompt to Claude Code:")
    click.echo("   " + "-" * 66)
    click.echo(f"   I'm starting a new ResearcherRAG project: {name}")
    click.echo(f"   Research question: {question}")
    click.echo(f"   Domain: {domain}")
    click.echo(f"   ")
    click.echo(f"   Please read my config.yaml and guide me through Stage 1")
    click.echo(f"   (Research Domain Setup) using the 5-stage workflow.")
    click.echo(f"   ")
    click.echo(f"   Make sure to save all outputs to the correct folders:")
    click.echo(f"   - Stage 1 → data/01_identification/")
    click.echo(f"   - Stage 2 → data/02_screening/")
    click.echo(f"   - Stage 3 → data/03_full_text/")
    click.echo("   " + "-" * 66 + "\n")

    click.echo("📖 Documentation:")
    click.echo("   https://researcher-rag-helper.vercel.app/guide/02-getting-started\n")

    click.echo("📊 Dashboard (check progress anytime):")
    click.echo(f"   https://researcher-rag-helper.vercel.app/dashboard?project={today}_{sanitized_name}\n")

    click.echo("💡 Check project status anytime:")
    click.echo(f"   python researcherrag_cli.py status {project_folder}\n")


@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
def status(project_path):
    """
    Show current project status and validate folder structure.

    This command:
    - Validates folder structure
    - Shows progress through 6 stages
    - Counts papers at each stage
    - Reports file statistics

    Example:
        python researcherrag_cli.py status projects/2025-01-12_AI-Healthcare
    """
    # 1. Load and validate metadata
    metadata_path = os.path.join(project_path, '.researcherrag')
    if not os.path.exists(metadata_path):
        click.echo(f"\n❌ Error: Not a valid ResearcherRAG project")
        click.echo(f"   Missing .researcherrag metadata file in: {project_path}")
        click.echo(f"\n   Did you create this project with 'researcherrag_cli.py init'?\n")
        sys.exit(1)

    with open(metadata_path, 'r') as f:
        metadata = yaml.safe_load(f)

    # 2. Display project header
    click.echo(f"\n{'='*70}")
    click.echo(f"📊 Project Status: {metadata['project_name']}")
    click.echo(f"{'='*70}\n")

    click.echo(f"📅 Created: {metadata['created']}")
    click.echo(f"📝 Question: {metadata['research_question']}")
    click.echo(f"🏷️  Domain: {metadata['domain']}")
    click.echo(f"📍 Stage: {metadata.get('current_stage', 1)}/6")
    if 'last_updated' in metadata:
        click.echo(f"🔄 Last Updated: {metadata['last_updated']}")
    click.echo()

    # 3. Validate folder structure
    expected_folders = [
        'data/01_identification',
        'data/02_screening',
        'data/03_full_text',
        'data/pdfs',
        'rag',
        'outputs',
        'conversations'
    ]

    missing_folders = []
    for folder in expected_folders:
        if not os.path.exists(os.path.join(project_path, folder)):
            missing_folders.append(folder)

    if missing_folders:
        click.echo("⚠️  Warning: Missing folders:")
        for folder in missing_folders:
            click.echo(f"   ❌ {folder}")
        click.echo()

    # 4. Check each stage's files
    click.echo("📁 File Status:\n")

    stage_files = {
        '1. Identification': [
            ('data/01_identification/pubmed_results.csv', 'PubMed results'),
            ('data/01_identification/scopus_results.csv', 'Scopus results'),
            ('data/01_identification/openalex_results.csv', 'OpenAlex results'),
            ('data/01_identification/deduplicated.csv', 'Deduplicated dataset')
        ],
        '2. Screening': [
            ('data/02_screening/title_abstract.csv', 'Passed title/abstract screening'),
            ('data/02_screening/excluded.csv', 'Excluded papers'),
            ('data/02_screening/decisions.json', 'Screening decisions')
        ],
        '3. Full-text Review': [
            ('data/03_full_text/assessment.csv', 'Full-text assessment'),
            ('data/03_full_text/final_dataset.csv', 'Final included papers ⭐'),
            ('data/03_full_text/exclusion_reasons.csv', 'Exclusion reasons')
        ],
        '4. RAG Setup': [
            ('rag/chroma_db', 'Vector database'),
            ('rag/rag_config.yaml', 'RAG configuration'),
            ('rag/ingestion_log.txt', 'Ingestion log')
        ],
        '5. Research Conversations': [
            ('conversations/', 'Conversation logs')
        ],
        '6. Documentation': [
            ('outputs/prisma_flowchart.png', 'PRISMA flowchart'),
            ('outputs/prisma_flowchart.mmd', 'PRISMA flowchart (Mermaid)'),
            ('outputs/search_strategy.md', 'Search strategy document')
        ]
    }

    for stage, files in stage_files.items():
        click.echo(f"  {stage}")
        for filepath, description in files:
            full_path = os.path.join(project_path, filepath)
            if os.path.exists(full_path):
                if os.path.isdir(full_path):
                    file_count = len([f for f in os.listdir(full_path) if not f.startswith('.')])
                    if file_count > 0:
                        click.echo(f"    ✅ {description}: {file_count} files")
                    else:
                        click.echo(f"    ⏳ {description}: Empty directory")
                else:
                    # Check if it's a CSV file
                    if filepath.endswith('.csv'):
                        rows = _count_csv_rows(full_path)
                        if rows is not None and rows > 0:
                            click.echo(f"    ✅ {description}: {rows} rows")
                        else:
                            click.echo(f"    ⏳ {description}: Empty or invalid CSV")
                    else:
                        file_size = os.path.getsize(full_path)
                        click.echo(f"    ✅ {description}: {file_size/1024:.1f} KB")
            else:
                click.echo(f"    ⏳ {description}: Not yet created")
        click.echo()

    # 5. Show quick statistics
    click.echo("📈 Quick Statistics:\n")
    stats = _calculate_project_stats(project_path)

    if stats:
        for key, value in stats.items():
            click.echo(f"  • {key}: {value}")
    else:
        click.echo("  No data files found yet. Start with Stage 1!")

    click.echo()

    # 6. Show dashboard link
    project_name = os.path.basename(project_path)
    click.echo("📊 View in Dashboard:")
    click.echo(f"   https://researcher-rag-helper.vercel.app/dashboard?project={project_name}\n")

    # 7. Show next action recommendation
    current_stage = metadata.get('current_stage', 1)
    if current_stage <= 6:
        click.echo("💡 Next Action:")
        next_actions = {
            1: "Run Stage 1: Paper collection from databases (PubMed, Scopus, etc.)",
            2: "Run Stage 2: Title/abstract screening with PRISMA criteria",
            3: "Run Stage 3: Full-text review and PDF download",
            4: "Run Stage 4: Build RAG system (vector database + embeddings)",
            5: "Run Stage 5: Start research conversations with your RAG",
            6: "Run Stage 6: Generate documentation (PRISMA flowchart, search strategy)"
        }
        click.echo(f"   {next_actions[current_stage]}\n")


@cli.command()
def list():
    """
    List all ResearcherRAG projects in the projects/ directory.

    Shows:
    - Project name and creation date
    - Research question
    - Current stage progress
    - Domain

    Example:
        python researcherrag_cli.py list
    """
    projects_dir = 'projects'

    if not os.path.exists(projects_dir):
        click.echo(f"\n❌ No projects directory found.")
        click.echo(f"   Create your first project with: python researcherrag_cli.py init\n")
        return

    projects = [d for d in os.listdir(projects_dir)
                if os.path.isdir(os.path.join(projects_dir, d)) and not d.startswith('.')]

    if not projects:
        click.echo(f"\n📂 Projects directory is empty.")
        click.echo(f"   Create your first project with: python researcherrag_cli.py init\n")
        return

    click.echo(f"\n{'='*70}")
    click.echo(f"📚 ResearcherRAG Projects ({len(projects)} total)")
    click.echo(f"{'='*70}\n")

    # Sort by date (newest first)
    projects_sorted = sorted(projects, reverse=True)

    for project in projects_sorted:
        metadata_path = os.path.join(projects_dir, project, '.researcherrag')

        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = yaml.safe_load(f)

            # Determine status emoji
            stage = metadata.get('current_stage', 1)
            if stage == 6:
                status_emoji = "✅"
                status_text = "Complete"
            elif stage > 1:
                status_emoji = "⚙️"
                status_text = f"Stage {stage}/6"
            else:
                status_emoji = "🆕"
                status_text = "New"

            click.echo(f"{status_emoji} {project}")
            click.echo(f"   📝 {metadata['research_question'][:65]}{'...' if len(metadata['research_question']) > 65 else ''}")
            click.echo(f"   📊 {status_text} • Domain: {metadata['domain']} • Created: {metadata['created']}")

            # Show quick stats
            stats = _calculate_project_stats(os.path.join(projects_dir, project))
            if stats:
                stats_text = " • ".join([f"{k}: {v}" for k, v in list(stats.items())[:3]])
                click.echo(f"   📈 {stats_text}")

            click.echo()
        else:
            # Project without metadata
            click.echo(f"⚠️  {project}")
            click.echo(f"   Missing .researcherrag metadata (not created with CLI)")
            click.echo()

    click.echo("💡 Check project status: python researcherrag_cli.py status projects/PROJECT_NAME\n")


# ============================================================================
# Helper Functions
# ============================================================================

def _create_default_config(project_folder, name, question, domain, today):
    """Create default config.yaml"""
    config = {
        'project': {
            'name': name,
            'created': today,
            'research_question': question,
            'domain': domain
        },
        'databases': ['pubmed', 'scopus', 'openalex', 'eric'],
        'inclusion_criteria': {
            'year_start': 2010,
            'year_end': 2025,
            'study_types': ['empirical', 'systematic_review', 'meta_analysis'],
            'languages': ['english']
        },
        'exclusion_criteria': [
            'Opinion pieces',
            'Editorials',
            'Conference abstracts without full text'
        ],
        'rag': {
            'vector_db': 'chromadb',
            'embeddings': 'text-embedding-3-small',
            'llm': 'claude-3-5-sonnet-20241022',
            'chunk_size': 1000,
            'chunk_overlap': 200
        }
    }

    with open(f"{project_folder}/config.yaml", 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)


def _create_project_readme(project_folder, name, question, today, sanitized_name):
    """Create project README.md"""
    readme = f"""# {name}

**Created**: {today}
**Research Question**: {question}

## Project Overview

This project uses ResearcherRAG to conduct a systematic literature review following PRISMA 2020 guidelines.

### Current Status

- [ ] Stage 1: Identification (Paper search from databases)
- [ ] Stage 2: Screening (Title/abstract review)
- [ ] Stage 3: Full-text assessment
- [ ] Stage 4: RAG system setup (Vector database)
- [ ] Stage 5: Research conversation (Query RAG)
- [ ] Stage 6: Documentation (PRISMA flowchart, reports)

### Key Numbers

- Papers identified: TBD
- Papers screened: TBD
- Papers included: TBD
- PDFs downloaded: TBD
- RAG system: Not built

## File Structure

```
{os.path.basename(project_folder)}/
├── .researcherrag          # Metadata for dashboard tracking
├── config.yaml             # Project configuration
├── README.md               # This file
├── data/
│   ├── 01_identification/  # Stage 1: Database search results
│   ├── 02_screening/       # Stage 2: Screening decisions
│   ├── 03_full_text/       # Stage 3: Final included papers
│   └── pdfs/               # Downloaded PDF files
├── rag/
│   ├── chroma_db/          # Vector database
│   └── rag_config.yaml     # RAG configuration
├── outputs/
│   ├── prisma_flowchart.*  # PRISMA flow diagram
│   └── search_strategy.md  # Search strategy documentation
└── conversations/          # RAG session logs
```

## Next Steps

1. **Open in VS Code**:
   ```bash
   cd {os.path.basename(project_folder)}
   code .
   ```

2. **Start Claude Code**:
   - Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
   - Type: "Claude: Open Chat"
   - Copy-paste the initialization prompt from CLI output

3. **Follow the 5-stage workflow**:
   - Stage 1: Define scope, search databases
   - Stage 2: Screen abstracts with PRISMA
   - Stage 3: Review full texts
   - Stage 4: Build vector database
   - Stage 5: Query your research RAG
   - Stage 6: Generate documentation

## Resources

- **Documentation**: https://researcher-rag-helper.vercel.app/guide
- **Dashboard**: https://researcher-rag-helper.vercel.app/dashboard?project={sanitized_name}
- **Check Status**: `python ../../researcherrag_cli.py status .`

## Notes

_Add your notes and observations here as you progress through the project._
"""

    with open(f"{project_folder}/README.md", 'w') as f:
        f.write(readme)


def _count_csv_rows(filepath):
    """Count rows in CSV file (excluding header)"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Skip header and empty lines
            return len([line for line in lines[1:] if line.strip()])
    except Exception as e:
        return None


def _calculate_project_stats(project_path):
    """Calculate project statistics"""
    stats = {}

    # Count papers at each stage
    identification_csv = os.path.join(project_path, 'data/01_identification/deduplicated.csv')
    if os.path.exists(identification_csv):
        count = _count_csv_rows(identification_csv)
        if count:
            stats['Papers identified'] = count

    screening_csv = os.path.join(project_path, 'data/02_screening/title_abstract.csv')
    if os.path.exists(screening_csv):
        count = _count_csv_rows(screening_csv)
        if count:
            stats['Papers screened'] = count

    final_csv = os.path.join(project_path, 'data/03_full_text/final_dataset.csv')
    if os.path.exists(final_csv):
        count = _count_csv_rows(final_csv)
        if count:
            stats['Papers included'] = count

    # Count PDFs
    pdfs_dir = os.path.join(project_path, 'data/pdfs')
    if os.path.exists(pdfs_dir):
        pdf_count = len([f for f in os.listdir(pdfs_dir) if f.endswith('.pdf')])
        if pdf_count > 0:
            stats['PDFs downloaded'] = pdf_count

    # Check RAG status
    chroma_db = os.path.join(project_path, 'rag/chroma_db')
    if os.path.exists(chroma_db):
        files_in_db = [f for f in os.listdir(chroma_db) if not f.startswith('.')]
        if files_in_db:
            stats['RAG system'] = '✅ Built'
        else:
            stats['RAG system'] = '⏳ Not built'
    else:
        stats['RAG system'] = '⏳ Not built'

    return stats


if __name__ == '__main__':
    cli()
