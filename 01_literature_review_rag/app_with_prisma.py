"""
Gradio Web Interface for Literature Review RAG with PRISMA Screening
=====================================================================

Enhanced version of app.py with integrated PRISMA pipeline.
"""
import gradio as gr
import sys
from pathlib import Path
from typing import Tuple
import logging

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.core.config import settings
from backend.core.prisma_integration import (
    upload_and_process_with_prisma,
    get_prisma_flow_diagram,
    get_review_queue_data
)
from backend.core.retrieval import get_retriever
from backend.core.rag_graph import query_literature_review

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Custom CSS (same as original)
custom_css = """
.gradio-container {
    font-family: 'Inter', sans-serif;
    max-width: 1400px !important;
}

.citation-box {
    background-color: #f8f9fa;
    border-left: 4px solid #4CAF50;
    padding: 12px;
    margin: 10px 0;
    border-radius: 4px;
}

.prisma-flow {
    background-color: #f0f4ff;
    padding: 20px;
    border-radius: 8px;
    margin: 20px 0;
}

.main-header {
    text-align: center;
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px;
    margin-bottom: 20px;
}

.info-box {
    background-color: #e3f2fd;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #2196F3;
    margin: 10px 0;
}

.success-box {
    background-color: #e8f5e9;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #4CAF50;
    margin: 10px 0;
}

.warning-box {
    background-color: #fff3e0;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #FF9800;
    margin: 10px 0;
}
"""

# Global state
retriever = get_retriever()
latest_prisma_result = None


def upload_papers_with_screening(files, profile_name: str) -> Tuple[str, str]:
    """Upload and screen papers with PRISMA."""
    global latest_prisma_result

    status_html, prisma_result = upload_and_process_with_prisma(files, profile_name)
    latest_prisma_result = prisma_result

    # Generate PRISMA flow diagram
    flow_diagram = ""
    if prisma_result:
        flow_diagram = get_prisma_flow_diagram(prisma_result)

    return status_html, flow_diagram


def get_review_queue() -> str:
    """Get manual review queue as HTML table."""
    global latest_prisma_result

    if latest_prisma_result is None:
        return "<p>No review queue available. Please upload papers first.</p>"

    queue_data = get_review_queue_data(latest_prisma_result)

    if not queue_data:
        return "<div class='success-box'>✅ No papers in review queue. All papers were automatically classified!</div>"

    html = """
    <div class='warning-box'>
        <h3>⚠️ Manual Review Queue</h3>
        <p>These papers scored in the borderline range and need your decision:</p>
        <table style='width: 100%; border-collapse: collapse; margin-top: 10px;'>
            <tr style='border-bottom: 2px solid #ddd; background-color: #f5f5f5;'>
                <th style='padding: 10px; text-align: left;'>Score</th>
                <th style='padding: 10px; text-align: left;'>Title</th>
                <th style='padding: 10px; text-align: left;'>Year</th>
                <th style='padding: 10px; text-align: left;'>Reason</th>
            </tr>
    """

    for paper in queue_data:
        html += f"""
        <tr style='border-bottom: 1px solid #eee;'>
            <td style='padding: 10px;'><strong>{paper['score']:.0f}</strong></td>
            <td style='padding: 10px;'>{paper['title'][:80]}...</td>
            <td style='padding: 10px;'>{paper['year']}</td>
            <td style='padding: 10px;'><em>{paper['reason']}</em></td>
        </tr>
        """

    html += """
        </table>
        <br>
        <p><em>💡 Tip: Papers with score 45-55 often need expert judgment. Consider domain expertise and research goals.</em></p>
    </div>
    """

    return html


def format_citations(citations: list) -> str:
    """Format citations as HTML (from original app.py)"""
    if not citations:
        return "<p>No citations available.</p>"

    html = "<div style='margin-top: 20px;'><h3>📚 Sources & Citations</h3>"

    for cite in citations:
        score = cite.get('prisma_score', 'N/A')
        score_badge = f"<span style='background: #4CAF50; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.9em;'>Quality: {score}</span>" if score != 'N/A' else ""

        html += f"""
        <div class="citation-box">
            <strong>[{cite['id']}] {cite.get('title', 'Untitled')}</strong> {score_badge}
            <br>
            <em>Year: {cite.get('year', 'N/A')} | File: {cite.get('filename', 'Unknown')}</em>
            <br><br>
            <details>
                <summary>View excerpt</summary>
                <p style="margin-top: 10px; padding: 10px; background: white; border-radius: 4px;">
                    {cite.get('excerpt', 'No excerpt available')}
                </p>
            </details>
        </div>
        """

    html += "</div>"
    return html


def ask_question(question: str, progress=gr.Progress()) -> Tuple[str, str]:
    """Process question (from original app.py with minor enhancements)"""
    if not question or len(question.strip()) < 3:
        return "Please enter a valid question (at least 3 characters).", ""

    stats = retriever.get_collection_stats()
    if stats.get('count', 0) == 0:
        return """
        <div class='warning-box'>
        ⚠️ <strong>No documents in database</strong>
        <br><br>
        Please upload some PDF papers first using the "Upload & Screen Papers" tab above.
        </div>
        """, ""

    try:
        progress(0.2, desc="Decomposing query...")
        logger.info(f"Processing question: {question}")

        progress(0.5, desc="Searching documents...")
        answer, citations = query_literature_review(question)

        progress(0.9, desc="Formatting response...")

        answer_html = f"""
        <div style="padding: 15px; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h3>💡 Answer</h3>
            <div style="line-height: 1.6;">
                {answer}
            </div>
        </div>
        """

        citations_html = format_citations(citations)
        progress(1.0, desc="Done!")

        return answer_html, citations_html

    except Exception as e:
        logger.error(f"Question processing failed: {e}")
        return f"""
        <div class='warning-box'>
            ❌ <strong>Error processing question</strong>
            <br><br>
            {str(e)}
        </div>
        """, ""


def get_collection_info() -> str:
    """Get database statistics."""
    stats = retriever.get_collection_stats()

    if stats.get('count', 0) == 0:
        return """
        <div class='info-box'>
            <strong>📊 Database Status: Empty</strong>
            <br><br>
            No papers have been uploaded yet.
        </div>
        """

    return f"""
    <div class='info-box'>
        <strong>📊 Database Statistics</strong>
        <br><br>
        🗄️ Total document chunks: <strong>{stats.get('count', 'Unknown')}</strong>
        <br>
        📁 Collection: <strong>{stats.get('collection_name', 'Unknown')}</strong>
        <br>
        💾 Status: <strong>{stats.get('status', 'Unknown').title()}</strong>
        <br><br>
        <em>✅ All documents have been screened with PRISMA protocol</em>
    </div>
    """


# Create Gradio interface
with gr.Blocks(css=custom_css, theme=gr.themes.Soft(), title="ResearcherRAG - PRISMA Enhanced") as demo:

    # Header
    gr.HTML("""
        <div class="main-header">
            <h1>📚 ResearcherRAG: Literature Review with PRISMA Screening</h1>
            <p style="font-size: 1.1em; margin-top: 10px;">
                Systematic literature review powered by AI + PRISMA 2020 guidelines
            </p>
        </div>
    """)

    gr.Markdown("""
    ### 🎯 What's New in This Version:
    - ✅ **PRISMA Screening**: Automatic 4-stage quality filtering
    - ✅ **Research Profiles**: Customize keywords for your research domain
    - ✅ **Quality Scores**: Every paper gets a relevance score (0-100)
    - ✅ **Manual Review Queue**: Borderline papers flagged for expert review
    - ✅ **PRISMA Flow Diagram**: Auto-generated for your papers

    ---
    """)

    with gr.Tabs():
        # Tab 1: Upload & Screen
        with gr.Tab("📤 Upload & Screen Papers"):
            gr.Markdown("""
            ### Upload Research Papers
            Papers will be screened using PRISMA protocol with your chosen research profile.
            """)

            with gr.Row():
                with gr.Column(scale=2):
                    profile_dropdown = gr.Dropdown(
                        choices=["default", "hrm_ai_bias", "education_tech"],
                        value="default",
                        label="Research Profile",
                        info="Select profile matching your research domain"
                    )

                    file_input = gr.File(
                        label="Select PDF Files",
                        file_count="multiple",
                        file_types=[".pdf"],
                        type="filepath"
                    )

                    upload_btn = gr.Button("📤 Upload & Screen with PRISMA", variant="primary", size="lg")

                with gr.Column(scale=3):
                    upload_output = gr.HTML(label="Screening Results")

            # PRISMA Flow Diagram
            with gr.Row():
                prisma_flow_output = gr.Code(
                    label="📊 PRISMA Flow Diagram (Mermaid)",
                    language="markdown",
                    lines=15
                )

            upload_btn.click(
                fn=upload_papers_with_screening,
                inputs=[file_input, profile_dropdown],
                outputs=[upload_output, prisma_flow_output]
            )

        # Tab 2: Ask Questions (same as original)
        with gr.Tab("❓ Ask Questions"):
            gr.Markdown("""
            ### Query Your Literature
            Ask questions about the papers you've uploaded.
            **Note**: Only high-quality papers (passed PRISMA screening) are used for answers.
            """)

            with gr.Row():
                with gr.Column():
                    question_input = gr.Textbox(
                        label="Research Question",
                        placeholder="e.g., What are the main barriers to AI adoption in K-12 education?",
                        lines=3
                    )
                    ask_btn = gr.Button("🔍 Search & Synthesize", variant="primary", size="lg")

            with gr.Row():
                with gr.Column():
                    answer_output = gr.HTML(label="Answer")

            with gr.Row():
                with gr.Column():
                    citations_output = gr.HTML(label="Sources")

            ask_btn.click(
                fn=ask_question,
                inputs=[question_input],
                outputs=[answer_output, citations_output]
            )

        # Tab 3: Manual Review Queue
        with gr.Tab("🔍 Manual Review Queue"):
            gr.Markdown("""
            ### Papers Needing Manual Review
            Papers with borderline scores (typically 40-55) are flagged for expert review.
            """)

            review_display = gr.HTML()
            refresh_review_btn = gr.Button("🔄 Refresh Review Queue", variant="secondary")

            refresh_review_btn.click(
                fn=get_review_queue,
                outputs=[review_display]
            )

        # Tab 4: Database Info
        with gr.Tab("📊 Database Info"):
            gr.Markdown("""
            ### Current Database Status
            View statistics about your screened papers.
            """)

            info_display = gr.HTML()
            refresh_btn = gr.Button("🔄 Refresh Stats", variant="secondary")

            refresh_btn.click(
                fn=get_collection_info,
                outputs=[info_display]
            )

            demo.load(fn=get_collection_info, outputs=[info_display])

            gr.Markdown("""
            ---
            ### About PRISMA Screening

            This system follows the **PRISMA 2020** (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) guidelines:

            1. **Identification**: Deduplication (DOI + title matching)
            2. **Screening**: Keyword-based relevance scoring (title/abstract)
            3. **Eligibility**: Context validation (full-text assessment)
            4. **Inclusion**: Final quality threshold

            **Quality Scoring (0-100)**:
            - Domain keywords: 0-30 points
            - Methodology keywords: 0-20 points
            - Topic keywords: 0-20 points
            - Context validation: 0-20 points
            - Quality indicators: 0-10 points
            - Title bonus: +10 points
            - Exclusion penalty: -30 points

            **Learn more**: [PRISMA Statement](http://www.prisma-statement.org/)
            """)

    # Footer
    gr.HTML("""
        <div style="text-align: center; margin-top: 30px; padding: 20px; border-top: 1px solid #ddd;">
            <p>
                Built with ❤️ for researchers |
                <a href="https://github.com/HosungYou/researcherRAG" target="_blank">GitHub</a> |
                <strong>Now with PRISMA 2020 compliance!</strong>
            </p>
            <p style="font-size: 0.9em; color: #666;">
                Powered by Claude Code, LangGraph, ChromaDB + PRISMA Protocol
            </p>
        </div>
    """)


if __name__ == "__main__":
    # Check for API key
    if not settings.anthropic_api_key and not settings.openai_api_key:
        print("\n" + "="*60)
        print("⚠️  WARNING: No API keys found!")
        print("="*60)
        print("\nPlease set your API key:")
        print("1. Copy .env.example to .env")
        print("2. Add your ANTHROPIC_API_KEY or OPENAI_API_KEY")
        print("3. Restart the application\n")
        print("="*60 + "\n")

    # Launch
    demo.launch(
        server_name=settings.gradio_server_name,
        server_port=settings.gradio_server_port,
        share=settings.gradio_share
    )
