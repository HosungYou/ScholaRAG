"""
Document ingestion pipeline for academic papers
"""
import os
import re
import logging
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

import fitz  # PyMuPDF
from tqdm import tqdm
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from .config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PaperMetadata:
    """Structured metadata for academic papers"""
    filename: str
    file_path: str
    title: Optional[str] = None
    authors: Optional[List[str]] = None
    year: Optional[int] = None
    doi: Optional[str] = None
    num_pages: Optional[int] = None
    file_size: Optional[int] = None
    processed_date: str = None

    def __post_init__(self):
        if self.processed_date is None:
            self.processed_date = datetime.now().isoformat()

    def to_dict(self):
        return {
            "filename": self.filename,
            "file_path": self.file_path,
            "title": self.title,
            "authors": self.authors,
            "year": self.year,
            "doi": self.doi,
            "num_pages": self.num_pages,
            "file_size": self.file_size,
            "processed_date": self.processed_date
        }


class DocumentIngestionPipeline:
    """Comprehensive document ingestion pipeline for academic papers"""

    def __init__(
        self,
        chunk_size: int = settings.chunk_size,
        chunk_overlap: int = settings.chunk_overlap
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
            length_function=len
        )

    def process_directory(
        self,
        directory: str,
        file_extensions: List[str] = [".pdf"]
    ) -> List[Document]:
        """
        Process all documents in a directory

        Args:
            directory: Path to directory containing documents
            file_extensions: List of file extensions to process

        Returns:
            List of LangChain Document objects with metadata
        """
        directory_path = Path(directory)
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")

        # Find all matching files
        files = []
        for ext in file_extensions:
            files.extend(directory_path.glob(f"*{ext}"))

        if not files:
            logger.warning(f"No files with extensions {file_extensions} found in {directory}")
            return []

        logger.info(f"Found {len(files)} documents to process")

        all_chunks = []
        failed_files = []

        for file_path in tqdm(files, desc="Processing documents"):
            try:
                chunks = self.process_file(str(file_path))
                all_chunks.extend(chunks)
                logger.info(f"✓ Processed {file_path.name}: {len(chunks)} chunks")

            except Exception as e:
                logger.error(f"✗ Failed to process {file_path.name}: {str(e)}")
                failed_files.append((file_path.name, str(e)))

        if failed_files:
            logger.warning(f"\n{len(failed_files)} files failed to process:")
            for filename, error in failed_files:
                logger.warning(f"  - {filename}: {error}")

        logger.info(f"\nTotal chunks created: {len(all_chunks)}")
        return all_chunks

    def process_file(self, file_path: str) -> List[Document]:
        """
        Process a single file based on its extension

        Args:
            file_path: Path to the file

        Returns:
            List of chunked Document objects
        """
        file_ext = Path(file_path).suffix.lower()

        if file_ext == ".pdf":
            return self._process_pdf(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")

    def _process_pdf(self, file_path: str) -> List[Document]:
        """Process PDF with metadata extraction and intelligent chunking"""
        try:
            doc = fitz.open(file_path)
        except Exception as e:
            logger.error(f"Failed to open PDF {file_path}: {e}")
            raise

        # Extract metadata
        metadata = self._extract_pdf_metadata(doc, file_path)

        # Extract full text
        full_text = ""
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            full_text += f"\n{text}"

        doc.close()

        # Create chunks
        chunks = self._create_chunks(full_text, metadata.to_dict())

        return chunks

    def _extract_pdf_metadata(
        self,
        doc: fitz.Document,
        file_path: str
    ) -> PaperMetadata:
        """Extract metadata from PDF"""
        pdf_metadata = doc.metadata

        # Try to extract title from first page (often in larger font)
        title = None
        if len(doc) > 0:
            first_page = doc[0]
            blocks = first_page.get_text("dict")["blocks"]

            # Look for text in larger font (likely title)
            for block in blocks[:10]:  # Check first 10 blocks
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            if span["size"] > 14:  # Likely title
                                title = span["text"].strip()
                                if len(title) > 10:  # Reasonable title length
                                    break
                        if title:
                            break
                if title:
                    break

        # Fallback to metadata title
        if not title or len(title) < 10:
            title = pdf_metadata.get("title")

        # Extract year from text
        year = self._extract_year(doc[0].get_text() if len(doc) > 0 else "")

        # Extract DOI if present
        doi = self._extract_doi(doc[0].get_text() if len(doc) > 0 else "")

        # Extract authors if available
        authors = None
        if pdf_metadata.get("author"):
            authors = [a.strip() for a in pdf_metadata.get("author", "").split(";")]

        return PaperMetadata(
            filename=Path(file_path).name,
            file_path=file_path,
            title=title,
            authors=authors,
            year=year,
            doi=doi,
            num_pages=len(doc),
            file_size=os.path.getsize(file_path)
        )

    def _extract_year(self, text: str) -> Optional[int]:
        """Extract publication year using regex"""
        # Look for 4-digit years between 1900-2100 in first 2000 chars
        matches = re.findall(r'\b(19\d{2}|20\d{2}|21\d{2})\b', text[:2000])
        if matches:
            # Return the most common year found
            from collections import Counter
            year_counts = Counter(matches)
            most_common_year = year_counts.most_common(1)[0][0]
            return int(most_common_year)
        return None

    def _extract_doi(self, text: str) -> Optional[str]:
        """Extract DOI from text"""
        doi_pattern = r'\b(10\.\d{4,}(?:\.\d+)*\/[^\s]+)\b'
        match = re.search(doi_pattern, text[:2000])
        if match:
            doi = match.group(1)
            # Clean up common trailing characters
            doi = doi.rstrip('.,;)')
            return doi
        return None

    def _create_chunks(
        self,
        text: str,
        metadata: Dict
    ) -> List[Document]:
        """Create chunks from text with metadata"""
        # Split text
        chunks = self.text_splitter.split_text(text)

        # Create Document objects
        documents = []
        for i, chunk in enumerate(chunks):
            doc_metadata = metadata.copy()
            doc_metadata["chunk_id"] = i
            doc_metadata["total_chunks"] = len(chunks)

            documents.append(Document(
                page_content=chunk,
                metadata=doc_metadata
            ))

        return documents


# Convenience function
def ingest_documents(
    directory: str,
    chunk_size: int = settings.chunk_size,
    chunk_overlap: int = settings.chunk_overlap
) -> List[Document]:
    """
    Convenience function to ingest all documents from a directory

    Usage:
        from backend.core.ingestion import ingest_documents

        documents = ingest_documents("./data/raw_pdfs")
    """
    pipeline = DocumentIngestionPipeline(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    return pipeline.process_directory(directory)
