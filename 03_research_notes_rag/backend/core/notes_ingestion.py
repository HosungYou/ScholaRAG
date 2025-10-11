"""Markdown note ingestion for Research Notes RAG."""
from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from .config import settings

logger = logging.getLogger(__name__)


_FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(?P<meta>.*?\n)---\s*\n", re.DOTALL)
_WIKILINK_PATTERN = re.compile(r"\[\[(?P<link>[^\]]+)\]\]")
_HIGHLIGHT_PATTERN = re.compile(r"==(?P<text>[^=]+)==")


@dataclass
class NoteMetadata:
    """Structured metadata extracted from a markdown note."""

    title: str
    note_type: str
    tags: List[str]
    project: Optional[str]
    created: Optional[str]
    modified: Optional[str]
    source_path: str
    backlinks: List[str]
    forward_links: List[str]

    def to_dict(self) -> Dict[str, Optional[str]]:
        """Return metadata as a dictionary suitable for LangChain."""
        return {
            "title": self.title,
            "note_type": self.note_type,
            "tags": self.tags,
            "project": self.project,
            "created": self.created,
            "modified": self.modified,
            "source_path": self.source_path,
            "backlinks": json.dumps(self.backlinks),
            "forward_links": json.dumps(self.forward_links),
        }


class MarkdownNoteIngestor:
    """Parse markdown notes into LangChain documents."""

    def __init__(
        self,
        notes_root: str = settings.notes_root,
        chunk_size: int = settings.chunk_size,
        chunk_overlap: int = settings.chunk_overlap,
    ) -> None:
        self.notes_root = Path(notes_root)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " "],
        )

    def ingest_directory(self, path: Optional[str] = None) -> List[Document]:
        """Ingest all markdown notes from a directory."""
        target = Path(path or self.notes_root)
        if not target.exists():
            raise FileNotFoundError(f"Notes directory not found: {target}")

        documents: List[Document] = []
        for filepath in target.rglob("*.md"):
            try:
                docs = self._parse_note(filepath)
                documents.extend(docs)
            except Exception as exc:  # pragma: no cover - logged for visibility
                logger.error("Failed to parse note %s: %s", filepath, exc)

        logger.info("Ingested %d note chunks from %s", len(documents), target)
        return documents

    def ingest_files(self, files: List[Path]) -> List[Document]:
        """Ingest a list of markdown files."""
        documents: List[Document] = []
        for filepath in files:
            docs = self._parse_note(Path(filepath))
            documents.extend(docs)
        return documents

    def _parse_note(self, path: Path) -> List[Document]:
        """Parse a single note into chunks with metadata."""
        content = path.read_text(encoding="utf-8")
        frontmatter, body = self._extract_frontmatter(content)
        metadata = self._build_metadata(path, frontmatter, body)

        chunks = self.text_splitter.split_text(body)
        documents: List[Document] = []
        for index, chunk in enumerate(chunks):
            chunk_meta = metadata.to_dict()
            chunk_meta.update(
                {
                    "chunk_id": index,
                    "chunk_count": len(chunks),
                    "highlights": json.dumps(self._extract_highlights(chunk)),
                }
            )
            documents.append(Document(page_content=chunk, metadata=chunk_meta))
        return documents

    @staticmethod
    def _extract_frontmatter(content: str) -> Tuple[Dict[str, str], str]:
        """Split frontmatter from markdown body."""
        match = _FRONTMATTER_PATTERN.match(content)
        if not match:
            return {}, content

        meta_raw = match.group("meta")
        try:
            metadata = yaml.safe_load(meta_raw) or {}
        except yaml.YAMLError as exc:
            logger.warning("Invalid frontmatter, skipping: %s", exc)
            metadata = {}

        body = content[match.end() :]
        return metadata, body

    def _build_metadata(
        self,
        path: Path,
        frontmatter: Dict[str, str],
        body: str,
    ) -> NoteMetadata:
        """Construct NoteMetadata from frontmatter and body."""
        title = frontmatter.get("title") or path.stem
        tags = frontmatter.get("tags") or []
        if isinstance(tags, str):
            tags = [tag.strip() for tag in tags.split(",") if tag.strip()]

        note_type = frontmatter.get("type") or self._guess_note_type(body)
        project = frontmatter.get("project")
        created = frontmatter.get("date") or frontmatter.get("created")
        modified = frontmatter.get("updated")

        forward_links = sorted({match.group("link") for match in _WIKILINK_PATTERN.finditer(body)})
        backlinks = frontmatter.get("backlinks") or []
        if isinstance(backlinks, str):
            backlinks = [item.strip() for item in backlinks.split(",") if item.strip()]

        return NoteMetadata(
            title=title,
            note_type=note_type,
            tags=tags,
            project=project,
            created=created,
            modified=modified,
            source_path=str(path),
            backlinks=backlinks,
            forward_links=forward_links,
        )

    @staticmethod
    def _guess_note_type(body: str) -> str:
        """Infer a note type based on content heuristics."""
        lowered = body.lower()
        if "# summary" in lowered or "# key takeaways" in lowered:
            return "literature"
        if "todo" in lowered or "- [ ]" in body:
            return "project"
        if len(body.splitlines()) < 20:
            return "fleeting"
        return "permanent"

    @staticmethod
    def _extract_highlights(text: str) -> List[str]:
        """Return highlighted passages using Obsidian-style markers."""
        return [match.group("text").strip() for match in _HIGHLIGHT_PATTERN.finditer(text)]


def ingest_notes(path: Optional[str] = None) -> List[Document]:
    """Convenience wrapper used by downstream scripts."""
    ingestor = MarkdownNoteIngestor()
    return ingestor.ingest_directory(path)
