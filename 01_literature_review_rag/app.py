"""
Gradio Web Interface for Literature Review RAG
Demo-ready interface for researchers
"""
import gradio as gr
import os
import sys
from pathlib import Path
from typing import List, Tuple
import logging

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.core.config import settings
from backend.core.ingestion import ingest_documents
from backend.core.retrieval import get_retriever
from backend.core.rag_graph import query_literature_review

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Custom CSS
custom_css = """
.gradio-container {
    font-family: 'Inter', sans-serif;
    max-width: 1200px !important;
}

.citation-box {
    background-color: #f8f9fa;
    border-left: 4px solid #4CAF50;
    padding: 12px;
    margin: 10px 0;
    border-radius: 4px;
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


def format_citations(citations: List[dict]) -> str:
    """Format citations as HTML"""
    if not citations:
        return "<p>No citations available.</p>"

    html = "<div style='margin-top: 20px;'><h3>📚 Sources & Citations</h3>"

    for cite in citations:
        html += f"""
        <div class="citation-box">
            <strong>[{cite['id']}] {cite.get('title', 'Untitled')}</strong>
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


def upload_and_process(files) -> str:
    """Upload and process PDF files"""
    if not files:
        return "<div class='warning-box'>⚠️ No files uploaded. Please select PDF files to upload.</div>"

    try:
        # Create temp directory
        temp_dir = Path(settings.raw_pdfs_path) / "temp_upload"
        temp_dir.mkdir(parents=True, exist_ok=True)

        # Save uploaded files
        uploaded_count = 0
        for file in files:
            if file is not None:
                file_path = temp_dir / Path(file.name).name
                # Copy file
                import shutil
                shutil.copy(file.name, file_path)
                uploaded_count += 1

        logger.info(f"Uploaded {uploaded_count} files")

        # Process documents
        logger.info("Processing documents...")
        documents = ingest_documents(str(temp_dir))

        if not documents:
            return f"<div class='warning-box'>⚠️ No documents could be processed from {uploaded_count} uploaded files.</div>"

        # Add to vector store
        logger.info(f"Adding {len(documents)} chunks to vector store...")
        retriever.add_documents(documents)

        # Get stats
        stats = retriever.get_collection_stats()

        return f"""
        <div class='success-box'>
            ✅ <strong>Upload Successful!</strong>
            <br><br>
            📄 Files processed: <strong>{uploaded_count}</strong>
            <br>
            📦 Text chunks created: <strong>{len(documents)}</strong>
            <br>
            🗄️ Total documents in database: <strong>{stats.get('count', 'Unknown')}</strong>
            <br><br>
            <em>You can now ask questions about your papers below!</em>
        </div>
        """

    except Exception as e:
        logger.error(f"Upload failed: {e}")
        return f"<div class='warning-box'>❌ Error: {str(e)}</div>"


def ask_question(question: str, progress=gr.Progress()) -> Tuple[str, str]:
    """Process question and return answer with citations"""
    if not question or len(question.strip()) < 3:
        return "Please enter a valid question (at least 3 characters).", ""

    # Check if database has documents
    stats = retriever.get_collection_stats()
    if stats.get('count', 0) == 0:
        return """
        <div class='warning-box'>
        ⚠️ <strong>No documents in database</strong>
        <br><br>
        Please upload some PDF papers first using the "Upload Papers" tab above.
        </div>
        """, ""

    try:
        # Update progress
        progress(0.2, desc="Decomposing query...")

        # Query the system
        logger.info(f"Processing question: {question}")

        progress(0.5, desc="Searching documents...")

        answer, citations = query_literature_review(question)

        progress(0.9, desc="Formatting response...")

        # Format output
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
        error_html = f"""
        <div class='warning-box'>
            ❌ <strong>Error processing question</strong>
            <br><br>
            {str(e)}
            <br><br>
            <em>Please check your API keys in the .env file and try again.</em>
        </div>
        """
        return error_html, ""


def get_collection_info() -> str:
    """Get information about current collection"""
    stats = retriever.get_collection_stats()

    if stats.get('count', 0) == 0:
        return """
        <div class='info-box'>
            <strong>📊 Database Status: Empty</strong>
            <br><br>
            No papers have been uploaded yet.
            <br>
            Upload PDF papers using the "Upload Papers" tab to get started!
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
        <em>Chunk = a segment of text from a paper (~1000 characters)</em>
    </div>
    """


# Create Gradio interface
with gr.Blocks(css=custom_css, theme=gr.themes.Soft(), title="ResearcherRAG - Literature Review") as demo:

    # Header
    gr.HTML("""
        <div class="main-header">
            <h1>📚 ResearcherRAG: Literature Review Assistant</h1>
            <p style="font-size: 1.1em; margin-top: 10px;">
                AI-powered literature synthesis for social science researchers
            </p>
        </div>
    """)

    gr.Markdown("""
    ### How to Use:
    1. **Upload Papers**: Upload PDF research papers (Tab 1)
    2. **Ask Questions**: Query your literature corpus (Tab 2)
    3. **View Database**: Check what's been uploaded (Tab 3)

    **Example questions:**
    - "What are the main theories of technology adoption discussed in these papers?"
    - "What research methods were used across these studies?"
    - "What are the key findings about teacher attitudes toward AI?"
    """)

    with gr.Tabs():
        # Tab 1: Upload Papers
        with gr.Tab("📤 Upload Papers"):
            gr.Markdown("""
            ### Upload Research Papers
            Upload PDF files of academic papers you want to analyze.
            The system will extract text, create searchable chunks, and add them to the database.
            """)

            with gr.Row():
                with gr.Column():
                    file_input = gr.File(
                        label="Select PDF Files",
                        file_count="multiple",
                        file_types=[".pdf"],
                        type="filepath"
                    )
                    upload_btn = gr.Button("📤 Process & Upload", variant="primary", size="lg")

                with gr.Column():
                    upload_output = gr.HTML(label="Upload Status")

            upload_btn.click(
                fn=upload_and_process,
                inputs=[file_input],
                outputs=[upload_output]
            )

            gr.Markdown("""
            ---
            **💡 Tips:**
            - Upload 5-10 papers to start
            - Papers can be from any discipline
            - Processing takes ~10-30 seconds per paper
            - You can upload more papers anytime
            """)

        # Tab 2: Ask Questions
        with gr.Tab("❓ Ask Questions"):
            gr.Markdown("""
            ### Query Your Literature
            Ask questions about the papers you've uploaded. The AI will:
            - Search across all documents
            - Synthesize findings from multiple papers
            - Provide citations for all claims
            """)

            with gr.Row():
                with gr.Column():
                    question_input = gr.Textbox(
                        label="Research Question",
                        placeholder="e.g., What are the main barriers to AI adoption in K-12 education?",
                        lines=3
                    )
                    ask_btn = gr.Button("🔍 Search & Synthesize", variant="primary", size="lg")

                    gr.Markdown("""
                    **Example Questions:**
                    - What theoretical frameworks are used?
                    - What methodologies were employed?
                    - What are the key findings?
                    - What gaps exist in this literature?
                    - Compare [Theory A] and [Theory B]
                    """)

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

        # Tab 3: Database Info
        with gr.Tab("📊 Database Info"):
            gr.Markdown("""
            ### Current Database Status
            View statistics about your uploaded papers and database.
            """)

            info_display = gr.HTML()
            refresh_btn = gr.Button("🔄 Refresh Stats", variant="secondary")

            refresh_btn.click(
                fn=get_collection_info,
                outputs=[info_display]
            )

            # Auto-load on tab open
            demo.load(fn=get_collection_info, outputs=[info_display])

            gr.Markdown("""
            ---
            ### About the System

            **Technology Stack:**
            - 🤖 LLM: Anthropic Claude 3.5 Sonnet
            - 🔢 Embeddings: HuggingFace sentence-transformers
            - 🗄️ Vector DB: ChromaDB
            - 🔄 Workflow: LangGraph

            **Features:**
            - ✅ Query decomposition (breaks complex questions into simpler searches)
            - ✅ Document reranking (prioritizes most relevant sources)
            - ✅ Multi-document synthesis (combines information across papers)
            - ✅ Automatic citation tracking

            **Privacy:**
            - 🔒 Papers processed locally
            - 🔒 Only query text sent to LLM API
            - 🔒 No paper content shared externally

            **GitHub:** [HosungYou/researcherRAG](https://github.com/HosungYou/researcherRAG)
            """)

    # Footer
    gr.HTML("""
        <div style="text-align: center; margin-top: 30px; padding: 20px; border-top: 1px solid #ddd;">
            <p>
                Built with ❤️ for researchers |
                <a href="https://github.com/HosungYou/researcherRAG" target="_blank">GitHub</a> |
                <a href="https://github.com/HosungYou/researcherRAG/blob/main/QUICK_START.md" target="_blank">Documentation</a>
            </p>
            <p style="font-size: 0.9em; color: #666;">
                Powered by Claude Code, LangGraph, and ChromaDB
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
