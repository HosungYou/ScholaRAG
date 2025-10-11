"""
PRISMA Integration for Literature Review RAG
============================================

Integrates PRISMA screening pipeline with document ingestion and retrieval.
"""

import logging
from pathlib import Path
from typing import List, Tuple
import shutil

from langchain.schema import Document

from .config import settings
from .ingestion import ingest_documents
from .prisma_pipeline import LiteratureReviewPRISMA, PRISMAResult
from .research_profile import ResearchProfile, get_profile
from .retrieval import get_retriever

logger = logging.getLogger(__name__)


def upload_and_process_with_prisma(
    files: List,
    research_profile_name: str = "default"
) -> Tuple[str, PRISMAResult]:
    """
    Upload and process PDF files with PRISMA screening.

    Args:
        files: List of uploaded file objects
        research_profile_name: Name of research profile to use

    Returns:
        Tuple of (HTML status message, PRISMA result object)
    """
    if not files:
        return (
            "<div class='warning-box'>⚠️ No files uploaded. Please select PDF files to upload.</div>",
            None
        )

    try:
        # Create temp directory
        temp_dir = Path(settings.raw_pdfs_path) / "temp_upload"
        temp_dir.mkdir(parents=True, exist_ok=True)

        # Save uploaded files
        uploaded_count = 0
        for file in files:
            if file is not None:
                file_path = temp_dir / Path(file.name).name
                shutil.copy(file.name, file_path)
                uploaded_count += 1

        logger.info(f"Uploaded {uploaded_count} files")

        # Ingest documents
        logger.info("Processing documents...")
        raw_documents = ingest_documents(str(temp_dir))

        if not raw_documents:
            return (
                f"<div class='warning-box'>⚠️ No documents could be processed from {uploaded_count} uploaded files.</div>",
                None
            )

        # Load research profile
        profile = get_profile(research_profile_name)
        if profile is None:
            # Try loading from file
            profile_path = f"config/research_profiles/{research_profile_name}.yaml"
            try:
                profile = ResearchProfile.from_yaml(profile_path)
            except FileNotFoundError:
                logger.warning(f"Profile '{research_profile_name}' not found, using default")
                profile = ResearchProfile.create_default()

        # Run PRISMA screening
        logger.info(f"Running PRISMA screening with profile: {profile.name}")
        prisma = LiteratureReviewPRISMA(profile)
        result = prisma.run_full_pipeline(raw_documents)

        # Add only included documents to vector store
        retriever = get_retriever()
        if result.stage4.documents:
            logger.info(f"Adding {len(result.stage4.documents)} included documents to vector store")
            retriever.add_documents(result.stage4.documents)

        # Get updated stats
        stats = retriever.get_collection_stats()

        # Clean up temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)

        # Generate status HTML
        status_html = _generate_prisma_status_html(
            uploaded_count=uploaded_count,
            result=result,
            db_count=stats.get('count', 0)
        )

        return status_html, result

    except Exception as e:
        logger.error(f"Upload failed: {e}", exc_info=True)
        return f"<div class='warning-box'>❌ Error: {str(e)}</div>", None


def _generate_prisma_status_html(
    uploaded_count: int,
    result: PRISMAResult,
    db_count: int
) -> str:
    """Generate HTML status message with PRISMA results."""

    exclusion_reasons_html = ""
    if result.stage2.exclusion_reasons:
        exclusion_reasons_html = "<br><strong>Exclusion Reasons:</strong><ul>"
        for reason, count in result.stage2.exclusion_reasons.items():
            exclusion_reasons_html += f"<li>{reason}: {count} papers</li>"
        exclusion_reasons_html += "</ul>"

    review_queue_html = ""
    if result.stage4.review_queue_count > 0:
        review_queue_html = f"""
        <br>
        <div class='warning-box' style='margin-top: 10px;'>
            ⚠️ <strong>{result.stage4.review_queue_count} papers need manual review</strong>
            <br>
            These papers scored between {result.stage3.documents[0].metadata.get('prisma_score', 'N/A') if result.stage3.review_queue else 'N/A'}
            and require your decision.
        </div>
        """

    html = f"""
    <div class='success-box'>
        ✅ <strong>PRISMA Screening Complete!</strong>
        <br><br>
        <h3>📊 PRISMA Flow Summary</h3>
        <table style='width: 100%; border-collapse: collapse; margin-top: 10px;'>
            <tr style='border-bottom: 1px solid #ddd;'>
                <td style='padding: 8px;'><strong>Stage</strong></td>
                <td style='padding: 8px;'><strong>Count</strong></td>
                <td style='padding: 8px;'><strong>Details</strong></td>
            </tr>
            <tr>
                <td style='padding: 8px;'>1️⃣ Identification</td>
                <td style='padding: 8px;'>{uploaded_count} uploaded</td>
                <td style='padding: 8px;'>{result.stage1.duplicates_removed} duplicates removed</td>
            </tr>
            <tr>
                <td style='padding: 8px;'>2️⃣ Screening</td>
                <td style='padding: 8px;'>{result.stage2.passed_count} passed</td>
                <td style='padding: 8px;'>{result.stage2.excluded_count} excluded (low relevance)</td>
            </tr>
            <tr>
                <td style='padding: 8px;'>3️⃣ Eligibility</td>
                <td style='padding: 8px;'>{result.stage3.passed_count} eligible</td>
                <td style='padding: 8px;'>{result.stage3.excluded_count} excluded (weak context)</td>
            </tr>
            <tr style='background-color: #e8f5e9;'>
                <td style='padding: 8px;'><strong>4️⃣ Included</strong></td>
                <td style='padding: 8px;'><strong>{result.stage4.included_count} papers</strong></td>
                <td style='padding: 8px;'>Added to vector database</td>
            </tr>
        </table>

        {exclusion_reasons_html}

        <br><br>
        📦 <strong>Text chunks created:</strong> {sum(doc.metadata.get('total_chunks', 1) for doc in result.stage4.documents)}
        <br>
        🗄️ <strong>Total documents in database:</strong> {db_count}

        {review_queue_html}

        <br><br>
        <em>✅ High-quality papers have been added to the database. You can now ask questions!</em>
    </div>
    """

    return html


def get_prisma_flow_diagram(result: PRISMAResult) -> str:
    """
    Generate Mermaid diagram for PRISMA flow.

    Args:
        result: PRISMA pipeline result

    Returns:
        Mermaid markdown string
    """
    if result is None:
        return "No PRISMA flow available. Please upload papers first."

    prisma = LiteratureReviewPRISMA(ResearchProfile.create_default())
    return prisma.generate_prisma_flow_mermaid(result)


def get_review_queue_data(result: PRISMAResult) -> List[dict]:
    """
    Get manual review queue as list of dicts for display.

    Args:
        result: PRISMA pipeline result

    Returns:
        List of paper data for review
    """
    if result is None or not result.stage4.review_queue:
        return []

    queue_data = []
    for doc in result.stage4.review_queue:
        queue_data.append({
            'title': doc.metadata.get('title', 'Untitled'),
            'score': doc.metadata.get('prisma_score', 0),
            'year': doc.metadata.get('year', 'N/A'),
            'doi': doc.metadata.get('doi', 'N/A'),
            'reason': _get_review_reason(doc)
        })

    return queue_data


def _get_review_reason(doc: Document) -> str:
    """Determine why document is in review queue."""
    score_breakdown = doc.metadata.get('score_breakdown', {})

    if score_breakdown.get('domain_score', 0) < 15:
        return "Weak domain relevance"
    elif score_breakdown.get('context_score', 0) < 10:
        return "Limited context validation"
    elif score_breakdown.get('method_score', 0) < 10:
        return "Unclear methodology"
    else:
        return "Borderline score"
