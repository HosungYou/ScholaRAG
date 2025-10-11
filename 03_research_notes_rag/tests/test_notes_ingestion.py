import json
from pathlib import Path

from backend.core.notes_ingestion import MarkdownNoteIngestor


def test_markdown_ingestion(tmp_path: Path):
    note = tmp_path / "sample.md"
    note.write_text(
        "---\n"
        "title: Sample Literature Note\n"
        "tags: [education, ai]\n"
        "project: teacher-ai\n"
        "---\n"
        "# Summary\n"
        "==Key insight== about adoption.\n"
        "[[Another Note]] provides context.\n",
        encoding="utf-8",
    )

    ingestor = MarkdownNoteIngestor(notes_root=str(tmp_path))
    documents = ingestor.ingest_directory(str(tmp_path))

    assert len(documents) == 1
    metadata = documents[0].metadata
    assert metadata["title"] == "Sample Literature Note"
    assert "education" in metadata["tags"]
    highlights = json.loads(metadata["highlights"])
    assert "Key insight" in highlights[0]
