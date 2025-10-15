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
import json
import shutil
import subprocess
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


# ============================================================================
# Stage Management Commands (v1.0.6+)
# ============================================================================

@cli.command('stage-status')
def stage_status():
    """
    Show current stage and progress in the workflow.

    This command reads .claude/context.json to determine which stage
    the researcher is currently in and displays completion status.

    Example:
        researcherrag stage-status
    """
    context_file = '.claude/context.json'
    stages_file = '.claude/stages.yaml'

    # Check if .claude/ exists
    if not os.path.exists('.claude'):
        click.echo("\n❌ No .claude/ folder found.")
        click.echo("   This command requires ResearcherRAG v1.0.6+")
        click.echo("   Run: researcherrag upgrade\n")
        sys.exit(1)

    # Load context
    if not os.path.exists(context_file):
        click.echo("\n📍 No active project detected.")
        click.echo("   Start a new project with: researcherrag init\n")
        sys.exit(0)

    with open(context_file, 'r') as f:
        context = json.load(f)

    # Load stages config
    if not os.path.exists(stages_file):
        click.echo("\n❌ Missing .claude/stages.yaml")
        click.echo("   Run: researcherrag upgrade\n")
        sys.exit(1)

    with open(stages_file, 'r') as f:
        stages_config = yaml.safe_load(f)

    # Display current status
    click.echo("\n" + "="*60)
    click.echo("📍 RESEARCHERRAG STAGE STATUS")
    click.echo("="*60 + "\n")

    project = context.get('project', {})
    click.echo(f"📁 Project: {project.get('name', 'Unknown')}")
    click.echo(f"📅 Created: {project.get('created', 'Unknown')}")
    click.echo()

    current_stage_info = context.get('current_stage', {})
    current_stage = current_stage_info.get('stage', 1)
    current_status = current_stage_info.get('status', 'not_started')

    click.echo(f"📍 Current Stage: {current_stage} - {stages_config['stages'][current_stage]['name']}")
    click.echo(f"   Status: {current_status}")
    click.echo(f"   Duration: {stages_config['stages'][current_stage]['duration']}")
    click.echo()

    # Show completed stages
    completed = context.get('completed_stages', [])
    click.echo("✅ Completed Stages:")
    if completed:
        for stage_info in completed:
            stage_num = stage_info['stage']
            stage_name = stages_config['stages'][stage_num]['name']
            completed_at = stage_info.get('completed_at', 'Unknown')
            click.echo(f"   ✓ Stage {stage_num}: {stage_name} (completed: {completed_at})")
    else:
        click.echo("   (none yet)")
    click.echo()

    # Show next stage
    if current_stage < 7:
        next_stage = current_stage + 1
        next_stage_name = stages_config['stages'][next_stage]['name']
        click.echo(f"➡️  Next Stage: {next_stage} - {next_stage_name}")
        click.echo(f"   Prompt: {stages_config['stages'][next_stage]['prompt_file']}")
    else:
        click.echo("🎉 All stages complete!")

    click.echo("\n" + "="*60 + "\n")


@cli.command('run-stage')
@click.argument('stage', type=int)
@click.option('--force', is_flag=True, help='Skip prerequisite validation')
def run_stage(stage, force):
    """
    Execute a specific stage with prerequisite validation.

    This command checks prerequisites, runs the stage command,
    and updates .claude/context.json upon completion.

    Arguments:
        STAGE: Stage number (1-7)

    Options:
        --force: Skip prerequisite checks (use with caution)

    Example:
        researcherrag run-stage 2
        researcherrag run-stage 3 --force
    """
    stages_file = '.claude/stages.yaml'
    context_file = '.claude/context.json'

    # Validate stage number
    if stage < 1 or stage > 7:
        click.echo(f"\n❌ Invalid stage: {stage}")
        click.echo("   Valid stages: 1-7\n")
        sys.exit(1)

    # Load stages config
    if not os.path.exists(stages_file):
        click.echo("\n❌ Missing .claude/stages.yaml")
        click.echo("   Run: researcherrag upgrade\n")
        sys.exit(1)

    with open(stages_file, 'r') as f:
        stages_config = yaml.safe_load(f)

    stage_info = stages_config['stages'][stage]

    click.echo(f"\n🚀 Running Stage {stage}: {stage_info['name']}")
    click.echo(f"⏱️  Expected duration: {stage_info['duration']}\n")

    # Check prerequisites
    if not force:
        prerequisites = stage_info.get('prerequisites', [])
        if prerequisites:
            click.echo("🔍 Checking prerequisites...")
            for prereq in prerequisites:
                prereq_stage = prereq.get('stage')
                required_files = prereq.get('files', [])

                # Check if prerequisite stage is completed
                if os.path.exists(context_file):
                    with open(context_file, 'r') as f:
                        context = json.load(f)
                    completed_stages = [s['stage'] for s in context.get('completed_stages', [])]

                    if prereq_stage not in completed_stages:
                        click.echo(f"\n❌ Prerequisite not met: Stage {prereq_stage} not completed")
                        click.echo(f"   Complete Stage {prereq_stage} first, or use --force to skip\n")
                        sys.exit(1)

                # Check required files
                for required_file in required_files:
                    if not os.path.exists(required_file):
                        click.echo(f"\n❌ Missing required file: {required_file}")
                        click.echo(f"   Complete Stage {prereq_stage} first\n")
                        sys.exit(1)

            click.echo("✅ All prerequisites met\n")

    # Check if auto-execute or needs approval
    auto_execute = stage_info.get('auto_execute', False)

    if not auto_execute and not force:
        click.echo("⚠️  This stage requires approval to execute.")
        click.echo(f"   Command: {stage_info.get('cli_command', 'N/A')}")

        if 'cli_commands' in stage_info:
            click.echo("   Commands:")
            for cmd in stage_info['cli_commands']:
                click.echo(f"   - {cmd}")

        click.echo()
        if not click.confirm('Proceed with execution?'):
            click.echo("\n❌ Cancelled by user\n")
            sys.exit(0)

    # Execute command
    click.echo("▶️  Executing stage command...\n")

    commands_to_run = []
    if 'cli_command' in stage_info:
        commands_to_run.append(stage_info['cli_command'])
    elif 'cli_commands' in stage_info:
        commands_to_run.extend(stage_info['cli_commands'])

    for command in commands_to_run:
        click.echo(f"   $ {command}")
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=False)
        except subprocess.CalledProcessError as e:
            click.echo(f"\n❌ Command failed with exit code {e.returncode}")
            click.echo(f"   Command: {command}\n")
            sys.exit(e.returncode)

    # Update context
    if os.path.exists(context_file):
        with open(context_file, 'r') as f:
            context = json.load(f)
    else:
        context = {
            'project': {},
            'current_stage': {},
            'completed_stages': [],
            'conversation_history': [],
            'checkpoints': {}
        }

    # Mark stage as completed
    context['completed_stages'].append({
        'stage': stage,
        'name': stage_info['name'],
        'completed_at': datetime.now().isoformat(),
        'outputs': stage_info.get('outputs', [])
    })

    # Update current stage
    if stage < 7:
        context['current_stage'] = {
            'stage': stage + 1,
            'name': stages_config['stages'][stage + 1]['name'],
            'started_at': datetime.now().isoformat(),
            'status': 'not_started'
        }
    else:
        context['current_stage'] = {
            'stage': 7,
            'name': 'All stages complete',
            'status': 'completed'
        }

    # Save context
    with open(context_file, 'w') as f:
        json.dump(context, f, indent=2)

    click.echo(f"\n✅ Stage {stage} completed successfully!")

    if stage < 7:
        next_stage = stage + 1
        click.echo(f"➡️  Next: Stage {next_stage} - {stages_config['stages'][next_stage]['name']}")
        click.echo(f"   Prompt: {stages_config['stages'][next_stage]['prompt_file']}\n")
    else:
        click.echo("🎉 All stages complete! Your systematic review is ready.\n")


@cli.command('next')
def next_stage():
    """
    Show the next stage to work on.

    Displays the next prompt file and expected actions.

    Example:
        researcherrag next
    """
    context_file = '.claude/context.json'
    stages_file = '.claude/stages.yaml'

    if not os.path.exists(context_file):
        click.echo("\n📍 No active project. Next step: Initialize project")
        click.echo("   Run: researcherrag init\n")
        sys.exit(0)

    with open(context_file, 'r') as f:
        context = json.load(f)

    with open(stages_file, 'r') as f:
        stages_config = yaml.safe_load(f)

    current_stage_info = context.get('current_stage', {})
    current_stage = current_stage_info.get('stage', 1)

    if current_stage > 7:
        click.echo("\n🎉 All stages complete!")
        click.echo("   Your systematic review is finished.\n")
        sys.exit(0)

    stage_info = stages_config['stages'][current_stage]

    click.echo("\n" + "="*60)
    click.echo(f"➡️  NEXT STAGE: {current_stage} - {stage_info['name']}")
    click.echo("="*60 + "\n")

    click.echo(f"⏱️  Expected duration: {stage_info['duration']}")
    click.echo(f"📄 Prompt file: {stage_info['prompt_file']}")
    click.echo()

    click.echo("📋 To complete this stage:")
    click.echo(f"   1. Read the prompt: {stage_info['prompt_file']}")
    click.echo("   2. Paste prompt content to Claude Code")
    click.echo("   3. Follow the conversation")
    click.echo(f"   4. Claude will auto-execute: {stage_info.get('cli_command', 'N/A')}")
    click.echo()

    if stage_info.get('outputs'):
        click.echo("📤 Expected outputs:")
        for output in stage_info['outputs']:
            click.echo(f"   - {output}")
        click.echo()

    # Stage 6 특화: 예시 프롬프트 추천
    if current_stage == 6:
        click.echo("🎯 Stage 6 특화 기능:")
        click.echo("   ResearcherRAG v1.0.8에서 7가지 연구 시나리오를 제공합니다.")
        click.echo()
        click.echo("   예시 프롬프트 보기:")
        click.echo("   $ researcherrag stage6-examples")
        click.echo()
        click.echo("   특정 시나리오 프롬프트 복사:")
        click.echo("   $ researcherrag stage6-prompt hypothesis")
        click.echo("   $ researcherrag stage6-prompt statistics")
        click.echo()

    click.echo("💡 Tip: Open prompt file with:")
    click.echo(f"   cat {stage_info['prompt_file']}")
    click.echo("\n" + "="*60 + "\n")


@cli.command('stage6-examples')
def stage6_examples():
    """
    Show available Stage 6 research scenarios (v1.0.8+).

    Lists all 7 research conversation scenarios with descriptions.

    Example:
        researcherrag stage6-examples
    """
    click.echo("\n" + "="*70)
    click.echo("🎯 Stage 6: Research Conversation Scenarios (v1.0.8)")
    click.echo("="*70 + "\n")

    scenarios = {
        "overview": {
            "name": "Context Scanning",
            "description": "Get high-level overview of literature themes, methods, findings",
            "use_case": "Initial exploration, understanding corpus structure"
        },
        "hypothesis": {
            "name": "Hypothesis Validation",
            "description": "Test hypothesis with supporting/refuting evidence + effect sizes",
            "use_case": "Validate research assumptions, build argument"
        },
        "statistics": {
            "name": "Statistical Extraction",
            "description": "Extract RCT data (tools, effect sizes, samples) in table format",
            "use_case": "Meta-analysis preparation, quantitative synthesis"
        },
        "methods": {
            "name": "Methodology Comparison",
            "description": "Compare RCT vs quasi-experimental vs mixed methods",
            "use_case": "Choose methodology, understand trade-offs"
        },
        "contradictions": {
            "name": "Contradiction Detection",
            "description": "Find conflicting results, analyze reasons, propose follow-up",
            "use_case": "Resolve inconsistencies, identify moderators"
        },
        "policy": {
            "name": "Policy Translation",
            "description": "Create policy memo with recommendations and checklists",
            "use_case": "Stakeholder communication, implementation"
        },
        "grant": {
            "name": "Future Research Design",
            "description": "Design follow-up study with hypotheses, methods, budget",
            "use_case": "Grant proposals, identifying research gaps"
        }
    }

    for key, info in scenarios.items():
        click.echo(f"📌 {info['name']}")
        click.echo(f"   설명: {info['description']}")
        click.echo(f"   활용: {info['use_case']}")
        click.echo(f"   프롬프트 복사: researcherrag stage6-prompt {key}")
        click.echo()

    click.echo("💡 팁:")
    click.echo("   - 각 시나리오는 프롬프트 예시입니다 (자동 실행 아님)")
    click.echo("   - 프롬프트를 복사해서 연구 상황에 맞게 수정하세요")
    click.echo("   - 전체 가이드: prompts/06_research_conversation.md")
    click.echo("\n" + "="*70 + "\n")


@cli.command('stage6-prompt')
@click.argument('scenario', type=click.Choice([
    'overview', 'hypothesis', 'statistics', 'methods',
    'contradictions', 'policy', 'grant'
]))
def stage6_prompt(scenario):
    """
    Copy example prompt for a specific Stage 6 scenario.

    Scenarios:
        overview        Context Scanning (literature overview)
        hypothesis      Hypothesis Validation (evidence for/against)
        statistics      Statistical Extraction (RCT data table)
        methods         Methodology Comparison (RCT vs quasi vs mixed)
        contradictions  Contradiction Detection (conflicting results)
        policy          Policy Translation (actionable recommendations)
        grant           Future Research Design (grant proposal)

    Example:
        researcherrag stage6-prompt hypothesis
    """
    prompts = {
        "overview": """Analyze the papers in my database and provide a structured overview of:
1. Core themes and topics
2. Methodological approaches
3. Key findings and outcomes

Organize the response hierarchically with citations and page ranges for each category.""",

        "hypothesis": """My hypothesis: "[여기에 가설을 입력하세요]"

Please:
1. List evidence SUPPORTING this hypothesis
2. List evidence REFUTING or contradicting this hypothesis
3. Provide reasoning for each piece of evidence
4. Include effect sizes, statistical values, and page numbers""",

        "statistics": """Extract from all RCT studies:
1. Measurement tools used for [outcome] assessment
2. Effect sizes (Cohen's d or similar)
3. Sample sizes (intervention and control groups)
4. Organize in a table format

For missing values, indicate "Not reported".""",

        "methods": """Compare the three main methodologies used in my papers:
1. Experimental (RCT)
2. Quasi-experimental
3. Mixed methods

For each, provide:
- Strengths
- Limitations
- Recommended use scenarios
- Cite specific papers as examples""",

        "contradictions": """Identify cases where studies report conflicting results (e.g., positive vs. negative outcomes).

For each contradiction:
1. Describe the conflicting findings
2. Analyze potential reasons (sample, duration, tools, context)
3. Provide direct quotes from the papers
4. Suggest follow-up research to resolve the contradiction""",

        "policy": """Based on my RAG database, create a policy memo for education administrators.

Include:
1. Executive summary (3 key takeaways)
2. Policy recommendations (3-5 actionable items)
3. Implementation checklist for practitioners
4. Evidence citations supporting each recommendation""",

        "grant": """Based on the research gaps identified in my database, propose a follow-up study design.

Include:
1. Research question and hypotheses
2. Study design (methodology, sample, measures)
3. Analysis plan
4. Expected contributions to the field
5. Budget estimate and timeline"""
    }

    scenario_names = {
        "overview": "Context Scanning",
        "hypothesis": "Hypothesis Validation",
        "statistics": "Statistical Extraction",
        "methods": "Methodology Comparison",
        "contradictions": "Contradiction Detection",
        "policy": "Policy Translation",
        "grant": "Future Research Design"
    }

    click.echo("\n" + "="*70)
    click.echo(f"📋 Stage 6 Prompt: {scenario_names[scenario]}")
    click.echo("="*70 + "\n")

    click.echo("아래 프롬프트를 복사해서 RAG 인터페이스에 붙여넣으세요:")
    click.echo("(필요시 대괄호 [] 부분을 수정하세요)\n")
    click.echo("-" * 70)
    click.echo(prompts[scenario])
    click.echo("-" * 70)
    click.echo()

    click.echo("💡 사용 방법:")
    click.echo("   1. 위 프롬프트를 복사 (Ctrl+C / Cmd+C)")
    click.echo("   2. RAG 인터페이스 시작: python scripts/06_query_rag.py")
    click.echo("   3. 프롬프트 붙여넣기 (Ctrl+V / Cmd+V)")
    click.echo("   4. 연구 상황에 맞게 수정 후 실행")
    click.echo()

    click.echo("📖 전체 예시 및 최적 응답 구조:")
    click.echo("   prompts/06_research_conversation.md")
    click.echo("\n" + "="*70 + "\n")


@cli.command('upgrade')
def upgrade():
    """
    Upgrade existing project to v1.0.6+ with .claude/ folder.

    This command adds:
    - .claude/stages.yaml (stage configuration)
    - .claude/context.json (state tracking)
    - .gitignore entry for context.json

    Example:
        researcherrag upgrade
    """
    click.echo("\n🔧 Upgrading to ResearcherRAG v1.0.6+\n")

    # Check if already upgraded
    if os.path.exists('.claude/stages.yaml'):
        click.echo("✅ Already upgraded to v1.0.6+")
        click.echo("   .claude/ folder exists\n")
        sys.exit(0)

    # Create .claude/ folder
    os.makedirs('.claude', exist_ok=True)
    click.echo("✓ Created .claude/ folder")

    # Copy stages.yaml if exists in repo root
    if os.path.exists('.claude/stages.yaml') is False:
        click.echo("❌ Missing .claude/stages.yaml template in repository")
        click.echo("   This should be included in ResearcherRAG v1.0.6+")
        click.echo("   Please update your ResearcherRAG installation\n")
        sys.exit(1)

    click.echo("✓ stages.yaml configuration ready")

    # Create initial context.json
    initial_context = {
        "version": "1.0",
        "project": {
            "name": "Unknown",
            "created": datetime.now().isoformat(),
            "last_active": datetime.now().isoformat()
        },
        "current_stage": {
            "stage": 1,
            "name": "Research Domain Setup",
            "status": "not_started"
        },
        "completed_stages": [],
        "conversation_history": [],
        "checkpoints": {}
    }

    with open('.claude/context.json', 'w') as f:
        json.dump(initial_context, f, indent=2)

    click.echo("✓ Created context.json")

    # Update .gitignore
    gitignore_entry = "\n# ResearcherRAG v1.0.6+ context\n.claude/context.json\n"

    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()

        if '.claude/context.json' not in gitignore_content:
            with open('.gitignore', 'a') as f:
                f.write(gitignore_entry)
            click.echo("✓ Updated .gitignore")
        else:
            click.echo("✓ .gitignore already configured")
    else:
        with open('.gitignore', 'w') as f:
            f.write(gitignore_entry)
        click.echo("✓ Created .gitignore")

    click.echo("\n✅ Upgrade complete!")
    click.echo("\n💡 Try these new commands:")
    click.echo("   researcherrag stage-status  # Show current progress")
    click.echo("   researcherrag next          # Show next stage")
    click.echo("   researcherrag run-stage 1   # Execute specific stage\n")


if __name__ == '__main__':
    cli()
