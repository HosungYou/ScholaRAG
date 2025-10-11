"""Gradio interface for the Research Notes RAG module."""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import List, Tuple

import gradio as gr

from backend.core.chains import ask_research_notes
from backend.core.notes_ingestion import MarkdownNoteIngestor
from backend.core.retrieval import get_retriever

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


ingestor = MarkdownNoteIngestor()
retriever = get_retriever()

chat_history: List[Tuple[str, str]] = []


def _save_uploaded_files(files: List[gr.File]) -> List[Path]:
    saved_paths: List[Path] = []
    target_dir = Path(ingestor.notes_root)
    target_dir.mkdir(parents=True, exist_ok=True)

    for file in files:
        path = target_dir / Path(file.name).name
        path.write_bytes(Path(file.name).read_bytes())
        saved_paths.append(path)
    return saved_paths


def upload_notes(files: List[gr.File]) -> str:
    if not files:
        return "⚠️ 업로드된 Markdown 파일이 없습니다."

    saved = _save_uploaded_files(files)
    documents = ingestor.ingest_files(saved)
    retriever.add_documents(documents)
    stats = retriever.stats()
    return (
        "✅ 노트 업로드 완료.\n"
        f"- 새 청크 수: {len(documents)}\n"
        f"- 전체 청크 수: {stats.get('count', 0)}"
    )


def answer_question(question: str) -> Tuple[str, str]:
    if not question.strip():
        return "질문을 입력해주세요.", json.dumps([])

    documents = retriever.search(question)
    if not documents:
        return "아직 검색 가능한 노트가 없습니다. Markdown 노트를 먼저 업로드하세요.", json.dumps([])

    answer = ask_research_notes(question, documents, chat_history)
    chat_history.append((question, answer))

    metadata = [
        {
            "title": doc.metadata.get("title"),
            "note_type": doc.metadata.get("note_type"),
            "tags": doc.metadata.get("tags"),
            "source_path": doc.metadata.get("source_path"),
        }
        for doc in documents
    ]

    return answer, json.dumps(metadata, indent=2)


def reset_history() -> str:
    chat_history.clear()
    return "대화 기록이 초기화되었습니다."


css = """
.gradio-container {
    font-family: 'Inter', sans-serif;
    max-width: 1000px !important;
}

#note-metadata {
    white-space: pre-wrap;
    background-color: #f9f9f9;
    border-radius: 6px;
    padding: 12px;
    border: 1px solid #e0e0e0;
}
"""


with gr.Blocks(css=css, theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 📝 Research Notes RAG
        Markdown 기반 연구 노트를 업로드하고 대화형으로 탐색하세요.
        """
    )

    with gr.Row():
        file_input = gr.File(label="노트 업로드 (Markdown)", file_types=[".md"], multiple=True)
        upload_button = gr.Button("노트 처리")

    upload_status = gr.Markdown()

    with gr.Tab("대화형 검색"):
        question_input = gr.Textbox(label="질문 입력", placeholder="올해 혼합연구에 대해 내가 정리한 메모를 요약해줘")
        ask_button = gr.Button("답변 생성")
        answer_output = gr.Markdown(label="답변")
        metadata_output = gr.Textbox(label="참조 노트 메타데이터", elem_id="note-metadata")

    reset_button = gr.Button("대화 초기화")

    upload_button.click(upload_notes, inputs=file_input, outputs=upload_status)
    ask_button.click(answer_question, inputs=question_input, outputs=[answer_output, metadata_output])
    reset_button.click(reset_history, outputs=upload_status)


if __name__ == "__main__":
    demo.launch()
