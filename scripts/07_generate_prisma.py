#!/usr/bin/env python3
"""
Stage 7: Generate PRISMA 2020 Flow Diagram

Creates PRISMA flow diagram showing the systematic review process
from identification to inclusion.

Usage:
    python scripts/07_generate_prisma.py --project <project_path>

Example:
    python scripts/07_generate_prisma.py --project projects/2025-10-13_AI-Chatbots
"""

import argparse
import pandas as pd
import sys
from pathlib import Path
from typing import Dict
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import yaml


class PRISMAGenerator:
    """Generate PRISMA 2020 flow diagram from project data"""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.output_dir = self.project_path / "outputs"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load project config
        self.load_config()

    def load_config(self):
        """Load project configuration"""
        config_file = self.project_path / "config.yaml"
        if config_file.exists():
            with open(config_file, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = {}

    def collect_statistics(self) -> Dict[str, int]:
        """
        Collect statistics from all pipeline stages

        Returns:
            Dictionary with PRISMA statistics
        """
        print("\n📊 Collecting statistics from pipeline...")

        stats = {}

        # Stage 1: Identification
        identification_dir = self.project_path / "data" / "01_identification"

        # Count papers from each database
        ss_file = identification_dir / "semantic_scholar_results.csv"
        oa_file = identification_dir / "openalex_results.csv"
        arxiv_file = identification_dir / "arxiv_results.csv"

        stats['semantic_scholar'] = len(pd.read_csv(ss_file)) if ss_file.exists() else 0
        stats['openalex'] = len(pd.read_csv(oa_file)) if oa_file.exists() else 0
        stats['arxiv'] = len(pd.read_csv(arxiv_file)) if arxiv_file.exists() else 0

        stats['total_identified'] = stats['semantic_scholar'] + stats['openalex'] + stats['arxiv']

        print(f"   Semantic Scholar: {stats['semantic_scholar']}")
        print(f"   OpenAlex: {stats['openalex']}")
        print(f"   arXiv: {stats['arxiv']}")
        print(f"   Total identified: {stats['total_identified']}")

        # Deduplication
        dedup_file = identification_dir / "deduplicated.csv"
        if dedup_file.exists():
            df_dedup = pd.read_csv(dedup_file)
            stats['after_deduplication'] = len(df_dedup)
            stats['duplicates_removed'] = stats['total_identified'] - stats['after_deduplication']
            print(f"   After deduplication: {stats['after_deduplication']}")
            print(f"   Duplicates removed: {stats['duplicates_removed']}")
        else:
            print("   ⚠️  Deduplication data not found")
            stats['after_deduplication'] = stats['total_identified']
            stats['duplicates_removed'] = 0

        # Stage 2: Screening
        screening_dir = self.project_path / "data" / "02_screening"

        relevant_file = screening_dir / "relevant_papers.csv"
        excluded_file = screening_dir / "excluded_papers.csv"

        if relevant_file.exists() and excluded_file.exists():
            df_relevant = pd.read_csv(relevant_file)
            df_excluded = pd.read_csv(excluded_file)

            stats['relevant'] = len(df_relevant)
            stats['excluded_screening'] = len(df_excluded)

            print(f"   Relevant after screening: {stats['relevant']}")
            print(f"   Excluded in screening: {stats['excluded_screening']}")
        else:
            print("   ⚠️  Screening data not found")
            stats['relevant'] = stats['after_deduplication']
            stats['excluded_screening'] = 0

        # Stage 3: PDF Download
        pdf_dir = self.project_path / "data" / "03_pdfs"
        metadata_file = pdf_dir / "papers_metadata.csv"

        if metadata_file.exists():
            df_metadata = pd.read_csv(metadata_file)
            stats['pdfs_downloaded'] = df_metadata['downloaded'].sum()
            stats['pdfs_failed'] = (df_metadata['downloaded'] == False).sum()

            print(f"   PDFs downloaded: {stats['pdfs_downloaded']}")
            print(f"   PDFs failed: {stats['pdfs_failed']}")
        else:
            print("   ⚠️  PDF download data not found")
            stats['pdfs_downloaded'] = 0
            stats['pdfs_failed'] = 0

        # Stage 4: Final inclusion in RAG
        rag_dir = self.project_path / "data" / "04_rag"
        rag_config_file = rag_dir / "rag_config.json"

        if rag_config_file.exists():
            import json
            with open(rag_config_file, 'r') as f:
                rag_config = json.load(f)
            stats['included_in_review'] = rag_config['total_papers']
            print(f"   Included in review: {stats['included_in_review']}")
        else:
            print("   ⚠️  RAG data not found")
            stats['included_in_review'] = stats['pdfs_downloaded']

        return stats

    def create_prisma_diagram(self, stats: Dict[str, int]):
        """
        Create PRISMA 2020 flow diagram

        Args:
            stats: Dictionary with statistics
        """
        print("\n🎨 Creating PRISMA diagram...")

        # Create figure
        fig, ax = plt.subplots(figsize=(12, 14))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 14)
        ax.axis('off')

        # Colors (PRISMA 2020 standard)
        color_identification = '#E8F4F8'
        color_screening = '#FFF4E6'
        color_included = '#E8F5E9'
        color_excluded = '#FFEBEE'

        # Box style
        box_style = "round,pad=0.1"

        # Title (different for knowledge repository vs systematic review)
        project_type = self.config.get('project_type', 'systematic_review')
        if project_type == 'knowledge_repository':
            title = 'Paper Processing Pipeline'
            subtitle = 'Comprehensive Knowledge Repository'
        else:
            title = 'PRISMA 2020 Flow Diagram'
            subtitle = 'Systematic Literature Review'

        ax.text(5, 13.5, title,
                ha='center', va='center', fontsize=16, fontweight='bold')

        # Project name with subtitle
        project_name = self.config.get('project_name', self.project_path.name)
        ax.text(5, 13, f'{project_name}\n({subtitle})',
                ha='center', va='center', fontsize=12, style='italic')

        # ============================================================
        # IDENTIFICATION
        # ============================================================

        y = 11.5

        # Database searches
        box1 = FancyBboxPatch((0.5, y-0.4), 2.5, 0.8,
                              boxstyle=box_style,
                              facecolor=color_identification,
                              edgecolor='black', linewidth=1.5)
        ax.add_patch(box1)
        ax.text(1.75, y, f'Semantic Scholar\nn = {stats["semantic_scholar"]}',
                ha='center', va='center', fontsize=10)

        box2 = FancyBboxPatch((3.5, y-0.4), 2.5, 0.8,
                              boxstyle=box_style,
                              facecolor=color_identification,
                              edgecolor='black', linewidth=1.5)
        ax.add_patch(box2)
        ax.text(4.75, y, f'OpenAlex\nn = {stats["openalex"]}',
                ha='center', va='center', fontsize=10)

        box3 = FancyBboxPatch((6.5, y-0.4), 2.5, 0.8,
                              boxstyle=box_style,
                              facecolor=color_identification,
                              edgecolor='black', linewidth=1.5)
        ax.add_patch(box3)
        ax.text(7.75, y, f'arXiv\nn = {stats["arxiv"]}',
                ha='center', va='center', fontsize=10)

        # Arrow down
        arrow1 = FancyArrowPatch((5, y-0.5), (5, y-1.2),
                                arrowstyle='->', mutation_scale=20, linewidth=2)
        ax.add_patch(arrow1)

        # ============================================================
        # TOTAL IDENTIFIED
        # ============================================================

        y = 9.5

        box4 = FancyBboxPatch((2, y-0.5), 6, 1,
                              boxstyle=box_style,
                              facecolor=color_identification,
                              edgecolor='black', linewidth=2)
        ax.add_patch(box4)
        ax.text(5, y, f'Records identified\nn = {stats["total_identified"]}',
                ha='center', va='center', fontsize=11, fontweight='bold')

        # Arrow down
        arrow2 = FancyArrowPatch((5, y-0.6), (5, y-1.3),
                                arrowstyle='->', mutation_scale=20, linewidth=2)
        ax.add_patch(arrow2)

        # ============================================================
        # DEDUPLICATION
        # ============================================================

        y = 7.8

        # Removed duplicates (right side)
        box_dup = FancyBboxPatch((6.5, y-0.4), 3, 0.8,
                                boxstyle=box_style,
                                facecolor=color_excluded,
                                edgecolor='black', linewidth=1)
        ax.add_patch(box_dup)
        ax.text(8, y, f'Duplicates removed\nn = {stats["duplicates_removed"]}',
                ha='center', va='center', fontsize=10)

        # After deduplication
        box5 = FancyBboxPatch((2, y-0.5), 3.5, 1,
                              boxstyle=box_style,
                              facecolor=color_identification,
                              edgecolor='black', linewidth=2)
        ax.add_patch(box5)
        ax.text(3.75, y, f'Records after\ndeduplication\nn = {stats["after_deduplication"]}',
                ha='center', va='center', fontsize=11, fontweight='bold')

        # Arrow down
        arrow3 = FancyArrowPatch((3.75, y-0.6), (3.75, y-1.3),
                                arrowstyle='->', mutation_scale=20, linewidth=2)
        ax.add_patch(arrow3)

        # ============================================================
        # SCREENING
        # ============================================================

        y = 6.1

        # Excluded in screening (right side)
        box_excl1 = FancyBboxPatch((6.5, y-0.4), 3, 0.8,
                                  boxstyle=box_style,
                                  facecolor=color_excluded,
                                  edgecolor='black', linewidth=1)
        ax.add_patch(box_excl1)
        ax.text(8, y, f'Excluded (irrelevant)\nn = {stats["excluded_screening"]}',
                ha='center', va='center', fontsize=10)

        # Records screened
        box6 = FancyBboxPatch((2, y-0.5), 3.5, 1,
                              boxstyle=box_style,
                              facecolor=color_screening,
                              edgecolor='black', linewidth=2)
        ax.add_patch(box6)
        ax.text(3.75, y, f'Records screened\n(AI-assisted)\nn = {stats["after_deduplication"]}',
                ha='center', va='center', fontsize=11, fontweight='bold')

        # Arrow down
        arrow4 = FancyArrowPatch((3.75, y-0.6), (3.75, y-1.3),
                                arrowstyle='->', mutation_scale=20, linewidth=2)
        ax.add_patch(arrow4)

        # ============================================================
        # ELIGIBILITY (PDF DOWNLOAD)
        # ============================================================

        y = 4.4

        # PDF download failed (right side)
        box_pdf_fail = FancyBboxPatch((6.5, y-0.4), 3, 0.8,
                                     boxstyle=box_style,
                                     facecolor=color_excluded,
                                     edgecolor='black', linewidth=1)
        ax.add_patch(box_pdf_fail)
        ax.text(8, y, f'PDF unavailable\nn = {stats["pdfs_failed"]}',
                ha='center', va='center', fontsize=10)

        # Reports sought for retrieval
        box7 = FancyBboxPatch((2, y-0.5), 3.5, 1,
                              boxstyle=box_style,
                              facecolor=color_screening,
                              edgecolor='black', linewidth=2)
        ax.add_patch(box7)
        ax.text(3.75, y, f'Reports sought\nfor retrieval\nn = {stats["relevant"]}',
                ha='center', va='center', fontsize=11, fontweight='bold')

        # Arrow down
        arrow5 = FancyArrowPatch((3.75, y-0.6), (3.75, y-1.3),
                                arrowstyle='->', mutation_scale=20, linewidth=2)
        ax.add_patch(arrow5)

        # ============================================================
        # INCLUDED
        # ============================================================

        y = 2.7

        box8 = FancyBboxPatch((2, y-0.5), 3.5, 1,
                              boxstyle=box_style,
                              facecolor=color_included,
                              edgecolor='black', linewidth=2)
        ax.add_patch(box8)
        ax.text(3.75, y, f'Studies included\nin review\nn = {stats["included_in_review"]}',
                ha='center', va='center', fontsize=11, fontweight='bold')

        # ============================================================
        # FOOTER
        # ============================================================

        ax.text(5, 0.8, 'Diagram follows PRISMA 2020 guidelines',
                ha='center', va='center', fontsize=9, style='italic', color='gray')

        ax.text(5, 0.4, f'Generated by ScholaRAG',
                ha='center', va='center', fontsize=8, color='gray')

        # Save figure
        output_file = self.output_dir / "prisma_diagram.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"   ✓ Saved to: {output_file}")

        # Also save as PDF for publication
        pdf_file = self.output_dir / "prisma_diagram.pdf"
        plt.savefig(pdf_file, bbox_inches='tight', facecolor='white')
        print(f"   ✓ PDF saved to: {pdf_file}")

        plt.close()

    def generate_statistics_report(self, stats: Dict[str, int]):
        """
        Generate detailed statistics report

        Args:
            stats: Dictionary with statistics
        """
        print("\n📋 Generating statistics report...")

        report = f"""# Systematic Review Statistics Report

**Project**: {self.config.get('project_name', self.project_path.name)}
**Research Question**: {self.config.get('research_question', 'N/A')}
**Date**: {pd.Timestamp.now().strftime('%Y-%m-%d')}

---

## PRISMA Flow Statistics

### Stage 1: Identification

| Database | Records Found |
|----------|---------------|
| Semantic Scholar | {stats['semantic_scholar']} |
| OpenAlex | {stats['openalex']} |
| arXiv | {stats['arxiv']} |
| **Total** | **{stats['total_identified']}** |

### Stage 2: Deduplication

- Records after deduplication: **{stats['after_deduplication']}**
- Duplicates removed: **{stats['duplicates_removed']}** ({stats['duplicates_removed']/stats['total_identified']*100:.1f}%)

### Stage 3: Screening

- Records screened: **{stats['after_deduplication']}**
- Relevant papers: **{stats['relevant']}** ({stats['relevant']/stats['after_deduplication']*100:.1f}%)
- Excluded papers: **{stats['excluded_screening']}** ({stats['excluded_screening']/stats['after_deduplication']*100:.1f}%)

### Stage 4: Eligibility (PDF Retrieval)

- Reports sought: **{stats['relevant']}**
- PDFs downloaded: **{stats['pdfs_downloaded']}** ({stats['pdfs_downloaded']/stats['relevant']*100:.1f}%)
- PDFs unavailable: **{stats['pdfs_failed']}** ({stats['pdfs_failed']/stats['relevant']*100:.1f}%)

### Stage 5: Included

- **Studies included in review: {stats['included_in_review']}**

---

## Overall Statistics

- **Total identified**: {stats['total_identified']} papers
- **Final included**: {stats['included_in_review']} papers
- **Overall inclusion rate**: {stats['included_in_review']/stats['total_identified']*100:.1f}%
- **Screening precision**: {stats['relevant']/stats['after_deduplication']*100:.1f}%
- **PDF retrieval success**: {stats['pdfs_downloaded']/stats['relevant']*100:.1f}%

---

*Generated by ScholaRAG following PRISMA 2020 guidelines*
"""

        # Save report
        report_file = self.output_dir / "statistics_report.md"
        with open(report_file, 'w') as f:
            f.write(report)

        print(f"   ✓ Saved to: {report_file}")

        # Also save as JSON for programmatic access
        json_file = self.output_dir / "statistics.json"
        import json
        with open(json_file, 'w') as f:
            json.dump(stats, f, indent=2)
        print(f"   ✓ JSON saved to: {json_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate PRISMA 2020 flow diagram"
    )
    parser.add_argument(
        '--project',
        required=True,
        help='Path to project directory'
    )

    args = parser.parse_args()

    # Validate project path
    project_path = Path(args.project)
    if not project_path.exists():
        print(f"❌ Error: Project path does not exist: {project_path}")
        sys.exit(1)

    print("\n" + "="*60)
    print("📊 PRISMA DIAGRAM GENERATION")
    print("="*60)

    # Initialize generator
    generator = PRISMAGenerator(args.project)

    # Collect statistics
    stats = generator.collect_statistics()

    # Create PRISMA diagram
    generator.create_prisma_diagram(stats)

    # Generate statistics report
    generator.generate_statistics_report(stats)

    print("\n" + "="*60)
    print("✨ SYSTEMATIC REVIEW COMPLETE!")
    print("="*60)
    print(f"\nOutputs saved to: {generator.output_dir}")
    print(f"  - PRISMA diagram: prisma_diagram.png / .pdf")
    print(f"  - Statistics report: statistics_report.md")
    print(f"  - JSON data: statistics.json")
    print("\n🎉 Your systematic literature review is complete!")
    print("="*60)


if __name__ == '__main__':
    main()
