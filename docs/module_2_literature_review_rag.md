# Module 2: Building Literature Review RAG with Claude Code

## Learning Objectives
By the end of this module, you will:
- Build a production-ready Literature Review RAG system
- Use Claude Code to customize and extend functionality
- Deploy a web interface for your research team
- Handle large-scale document processing (200+ papers)

---

## System Architecture

```
Literature Review RAG System
├── Backend (FastAPI)
│   ├── Document ingestion pipeline
│   ├── Vector search (ChromaDB/Qdrant)
│   ├── LLM integration (OpenAI/Claude)
│   └── Metadata management
├── Frontend (Chainlit)
│   ├── Chat interface
│   ├── Document upload
│   ├── Citation tracking
│   └── Export features
└── Data Storage
    ├── PDF storage
    ├── Vector database
    └── Metadata database (SQLite)
```

---

## Step-by-Step Implementation

### Phase 1: Project Setup (5 minutes)

#### 1.1 Create Project Structure

**Claude Code Prompt:**
```
Create a new Literature Review RAG project with the following structure:

/Volumes/External SSD/Projects/Research/ResearcherRAG/01_literature_review_rag/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routes/
│   │   │   ├── documents.py
│   │   │   ├── query.py
│   │   │   └── metadata.py
│   │   └── models/
│   │       ├── document.py
│   │       └── query.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── ingestion.py
│   │   ├── retrieval.py
│   │   └── llm.py
│   └── utils/
│       ├── __init__.py
│       ├── pdf_parser.py
│       └── chunking.py
├── frontend/
│   ├── chainlit_app.py
│   └── config.toml
├── data/
│   ├── raw_pdfs/
│   ├── processed/
│   └── vector_db/
├── tests/
│   ├── test_ingestion.py
│   └── test_retrieval.py
├── requirements.txt
├── .env.example
├── Dockerfile
└── README.md

Create all necessary __init__.py files and basic README.
```

#### 1.2 Install Dependencies

**requirements.txt:**
```txt
# Core RAG
langchain==0.1.0
langchain-community==0.0.20
chromadb==0.4.22
# Alternative: qdrant-client==1.7.0

# LLM Providers
openai==1.12.0
anthropic==0.18.0

# Document Processing
pypdf==4.0.1
pymupdf==1.23.0
python-docx==1.1.0
openpyxl==3.1.2
unstructured==0.12.0

# Web Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
chainlit==1.0.0

# Utilities
python-dotenv==1.0.1
pydantic==2.6.0
pandas==2.2.0
numpy==1.26.3
tqdm==4.66.1

# Database
sqlalchemy==2.0.25
alembic==1.13.0

# Testing
pytest==8.0.0
pytest-asyncio==0.23.0
```

**Installation command:**
```bash
cd "/Volumes/External SSD/Projects/Research/ResearcherRAG/01_literature_review_rag"
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 1.3 Environment Configuration

**.env.example:**
```bash
# LLM API Keys
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Vector Database
CHROMA_DB_PATH=./data/vector_db
# For Qdrant Cloud:
# QDRANT_URL=https://your-cluster.qdrant.io
# QDRANT_API_KEY=your_qdrant_key

# Model Configuration
EMBEDDING_MODEL=text-embedding-3-large
LLM_MODEL=gpt-4-turbo-preview
# Alternative: claude-3-opus-20240229

# Processing Settings
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

---

### Phase 2: Core Implementation (30-45 minutes)

#### 2.1 Configuration Management

**File: backend/core/config.py**

**Claude Code Prompt:**
```
Create a Pydantic-based configuration management system in backend/core/config.py that:
1. Loads settings from .env file
2. Validates all required API keys
3. Provides type-safe access to configuration
4. Includes sensible defaults
5. Supports different environments (dev, prod)

Use Pydantic BaseSettings for environment variable management.
```

**Expected Output:**
```python
# backend/core/config.py

from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import Literal
import os

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # API Keys
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    anthropic_api_key: str | None = Field(None, env="ANTHROPIC_API_KEY")

    # Model Configuration
    embedding_model: str = Field(
        "text-embedding-3-large",
        env="EMBEDDING_MODEL"
    )
    llm_model: str = Field(
        "gpt-4-turbo-preview",
        env="LLM_MODEL"
    )
    llm_provider: Literal["openai", "anthropic"] = Field(
        "openai",
        env="LLM_PROVIDER"
    )

    # Vector Database
    vector_db_type: Literal["chroma", "qdrant"] = Field(
        "chroma",
        env="VECTOR_DB_TYPE"
    )
    chroma_db_path: str = Field(
        "./data/vector_db",
        env="CHROMA_DB_PATH"
    )
    qdrant_url: str | None = Field(None, env="QDRANT_URL")
    qdrant_api_key: str | None = Field(None, env="QDRANT_API_KEY")

    # Processing Configuration
    chunk_size: int = Field(1000, env="CHUNK_SIZE")
    chunk_overlap: int = Field(200, env="CHUNK_OVERLAP")
    top_k_results: int = Field(5, env="TOP_K_RESULTS")

    # API Configuration
    api_host: str = Field("0.0.0.0", env="API_HOST")
    api_port: int = Field(8000, env="API_PORT")

    # Paths
    raw_pdfs_path: str = "./data/raw_pdfs"
    processed_data_path: str = "./data/processed"

    @validator("anthropic_api_key", always=True)
    def validate_llm_key(cls, v, values):
        """Ensure the correct API key is set based on provider."""
        provider = values.get("llm_provider")
        if provider == "anthropic" and not v:
            raise ValueError("ANTHROPIC_API_KEY required when using Anthropic")
        return v

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
```

#### 2.2 Document Ingestion Pipeline

**File: backend/core/ingestion.py**

**Claude Code Prompt:**
```
Create a robust document ingestion system in backend/core/ingestion.py that:

1. Supports multiple file formats: PDF, DOCX, TXT
2. Extracts text with metadata (title, author, year, DOI if available)
3. Handles academic papers specifically (detect sections: abstract, methods, results, etc.)
4. Implements smart chunking that respects paragraph boundaries
5. Extracts citations/references automatically
6. Handles errors gracefully (corrupt PDFs, encoding issues)
7. Shows progress bars for batch processing
8. Saves metadata to SQLite for later queries

Use PyMuPDF for PDFs (faster than PyPDF), include fallback to Unstructured for difficult PDFs.
Include comprehensive logging and error handling.
```

**Expected Output:**
```python
# backend/core/ingestion.py

import os
import re
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

import fitz  # PyMuPDF
from docx import Document as DocxDocument
from tqdm import tqdm
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from .config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PaperMetadata:
    """Structured metadata for academic papers."""
    filename: str
    file_path: str
    title: Optional[str] = None
    authors: Optional[List[str]] = None
    year: Optional[int] = None
    doi: Optional[str] = None
    abstract: Optional[str] = None
    keywords: Optional[List[str]] = None
    num_pages: Optional[int] = None
    file_size: Optional[int] = None
    processed_date: datetime = None

    def __post_init__(self):
        if self.processed_date is None:
            self.processed_date = datetime.now()


class DocumentIngestionPipeline:
    """
    Comprehensive document ingestion pipeline for academic papers.
    """

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
        file_extensions: List[str] = [".pdf", ".docx", ".txt"]
    ) -> List[Document]:
        """
        Process all documents in a directory.

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
            files.extend(directory_path.rglob(f"*{ext}"))

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
        Process a single file based on its extension.

        Args:
            file_path: Path to the file

        Returns:
            List of chunked Document objects
        """
        file_ext = Path(file_path).suffix.lower()

        if file_ext == ".pdf":
            return self._process_pdf(file_path)
        elif file_ext == ".docx":
            return self._process_docx(file_path)
        elif file_ext == ".txt":
            return self._process_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")

    def _process_pdf(self, file_path: str) -> List[Document]:
        """
        Process PDF with metadata extraction and intelligent chunking.
        """
        try:
            doc = fitz.open(file_path)
        except Exception as e:
            logger.error(f"PyMuPDF failed, trying fallback: {e}")
            return self._process_pdf_fallback(file_path)

        # Extract metadata
        metadata = self._extract_pdf_metadata(doc, file_path)

        # Extract full text
        full_text = ""
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            full_text += f"\n--- Page {page_num} ---\n{text}"

        doc.close()

        # Detect sections if possible
        sections = self._detect_paper_sections(full_text)

        # Create chunks
        chunks = self._create_chunks(full_text, metadata.dict())

        return chunks

    def _process_pdf_fallback(self, file_path: str) -> List[Document]:
        """
        Fallback PDF processing using Unstructured.
        """
        from unstructured.partition.pdf import partition_pdf

        elements = partition_pdf(filename=file_path)
        text = "\n\n".join([str(el) for el in elements])

        metadata = {
            "source": file_path,
            "filename": Path(file_path).name
        }

        return self._create_chunks(text, metadata)

    def _process_docx(self, file_path: str) -> List[Document]:
        """Process Word documents."""
        doc = DocxDocument(file_path)

        # Extract text from paragraphs
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        full_text = "\n\n".join(paragraphs)

        metadata = {
            "source": file_path,
            "filename": Path(file_path).name,
            "file_type": "docx"
        }

        return self._create_chunks(full_text, metadata)

    def _process_txt(self, file_path: str) -> List[Document]:
        """Process plain text files."""
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        metadata = {
            "source": file_path,
            "filename": Path(file_path).name,
            "file_type": "txt"
        }

        return self._create_chunks(text, metadata)

    def _extract_pdf_metadata(
        self,
        doc: fitz.Document,
        file_path: str
    ) -> PaperMetadata:
        """
        Extract metadata from PDF.
        """
        pdf_metadata = doc.metadata

        # Try to extract title (first line of first page, often in larger font)
        first_page = doc[0]
        blocks = first_page.get_text("dict")["blocks"]

        title = None
        for block in blocks[:5]:  # Check first 5 blocks
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["size"] > 12:  # Likely title
                            title = span["text"]
                            break
                    if title:
                        break
            if title:
                break

        # Extract year from text
        year = self._extract_year(doc[0].get_text())

        # Extract DOI if present
        doi = self._extract_doi(doc[0].get_text())

        return PaperMetadata(
            filename=Path(file_path).name,
            file_path=file_path,
            title=title or pdf_metadata.get("title"),
            authors=pdf_metadata.get("author", "").split(";") if pdf_metadata.get("author") else None,
            year=year,
            doi=doi,
            num_pages=len(doc),
            file_size=os.path.getsize(file_path)
        )

    def _extract_year(self, text: str) -> Optional[int]:
        """Extract publication year using regex."""
        # Look for 4-digit years between 1900-2100
        matches = re.findall(r'\b(19\d{2}|20\d{2}|21\d{2})\b', text[:2000])
        if matches:
            # Return the most common year found
            return int(max(set(matches), key=matches.count))
        return None

    def _extract_doi(self, text: str) -> Optional[str]:
        """Extract DOI from text."""
        doi_pattern = r'\b(10\.\d{4,}(?:\.\d+)*\/\S+)\b'
        match = re.search(doi_pattern, text[:2000])
        return match.group(1) if match else None

    def _detect_paper_sections(self, text: str) -> Dict[str, str]:
        """
        Detect and extract common paper sections.
        """
        sections = {}
        section_patterns = {
            "abstract": r"(?i)\bABSTRACT\b(.{100,2000}?)(?=\b(?:INTRODUCTION|KEYWORDS|1\.|I\.)\b)",
            "introduction": r"(?i)\b(?:INTRODUCTION|1\. INTRODUCTION)\b(.{100,}?)(?=\b(?:METHOD|LITERATURE|2\.)\b)",
            "methods": r"(?i)\b(?:METHOD|METHODOLOGY|METHODS)\b(.{100,}?)(?=\b(?:RESULTS|FINDINGS|3\.)\b)",
            "results": r"(?i)\b(?:RESULTS|FINDINGS)\b(.{100,}?)(?=\b(?:DISCUSSION|CONCLUSION|4\.)\b)",
            "discussion": r"(?i)\b(?:DISCUSSION)\b(.{100,}?)(?=\b(?:CONCLUSION|REFERENCES|5\.)\b)"
        }

        for section_name, pattern in section_patterns.items():
            match = re.search(pattern, text, re.DOTALL)
            if match:
                sections[section_name] = match.group(1).strip()

        return sections

    def _create_chunks(
        self,
        text: str,
        metadata: Dict
    ) -> List[Document]:
        """
        Create chunks from text with metadata.
        """
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
    Convenience function to ingest all documents from a directory.

    Usage:
        from backend.core.ingestion import ingest_documents

        documents = ingest_documents("./data/raw_pdfs")
    """
    pipeline = DocumentIngestionPipeline(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    return pipeline.process_directory(directory)
```

#### 2.3 Vector Store and Retrieval

**File: backend/core/retrieval.py**

**Claude Code Prompt:**
```
Create an advanced retrieval system in backend/core/retrieval.py that:

1. Supports both ChromaDB and Qdrant vector stores
2. Implements hybrid search (dense + sparse/keyword)
3. Supports metadata filtering (e.g., "papers from 2020-2023", "authors containing 'Smith'")
4. Implements re-ranking of results
5. Provides relevance scores
6. Handles multi-query retrieval (generate multiple query variations)
7. Includes methods to persist and load vector stores

Use LangChain abstractions where possible but add custom enhancements.
```

**Expected Output:**
```python
# backend/core/retrieval.py

import logging
from typing import List, Dict, Any, Optional, Literal
from pathlib import Path

from langchain.schema import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.chat_models import ChatOpenAI

from .config import settings

logger = logging.getLogger(__name__)


class AdvancedRetriever:
    """
    Advanced retrieval system with hybrid search, re-ranking, and filtering.
    """

    def __init__(
        self,
        vector_db_type: Literal["chroma", "qdrant"] = settings.vector_db_type,
        embedding_model: str = settings.embedding_model,
        persist_directory: str = settings.chroma_db_path,
        collection_name: str = "literature_review"
    ):
        self.vector_db_type = vector_db_type
        self.collection_name = collection_name
        self.persist_directory = persist_directory

        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model=embedding_model,
            openai_api_key=settings.openai_api_key
        )

        # Initialize vector store
        self.vectorstore = None
        self._initialize_vectorstore()

    def _initialize_vectorstore(self):
        """Initialize or load existing vector store."""

        if self.vector_db_type == "chroma":
            persist_path = Path(self.persist_directory)

            if persist_path.exists() and any(persist_path.iterdir()):
                logger.info(f"Loading existing ChromaDB from {self.persist_directory}")
                self.vectorstore = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings,
                    collection_name=self.collection_name
                )
            else:
                logger.info("No existing ChromaDB found. Will create on first ingestion.")
                self.vectorstore = None

        elif self.vector_db_type == "qdrant":
            # Implement Qdrant initialization
            raise NotImplementedError("Qdrant support coming in future version")

    def add_documents(
        self,
        documents: List[Document],
        batch_size: int = 100
    ) -> None:
        """
        Add documents to vector store in batches.

        Args:
            documents: List of LangChain Document objects
            batch_size: Number of documents to process at once
        """

        if not documents:
            logger.warning("No documents to add")
            return

        logger.info(f"Adding {len(documents)} documents to vector store...")

        if self.vectorstore is None:
            # Create new vector store
            logger.info("Creating new vector store...")
            self.vectorstore = Chroma.from_documents(
                documents=documents[:batch_size],
                embedding=self.embeddings,
                persist_directory=self.persist_directory,
                collection_name=self.collection_name
            )

            # Add remaining documents
            for i in range(batch_size, len(documents), batch_size):
                batch = documents[i:i+batch_size]
                self.vectorstore.add_documents(batch)
                logger.info(f"Processed {min(i+batch_size, len(documents))}/{len(documents)}")

        else:
            # Add to existing vector store
            for i in range(0, len(documents), batch_size):
                batch = documents[i:i+batch_size]
                self.vectorstore.add_documents(batch)
                logger.info(f"Processed {min(i+batch_size, len(documents))}/{len(documents)}")

        # Persist
        if hasattr(self.vectorstore, 'persist'):
            self.vectorstore.persist()
            logger.info("Vector store persisted successfully")

    def search(
        self,
        query: str,
        k: int = settings.top_k_results,
        filter_dict: Optional[Dict[str, Any]] = None,
        search_type: Literal["similarity", "mmr"] = "similarity"
    ) -> List[Document]:
        """
        Search for relevant documents.

        Args:
            query: Search query
            k: Number of results to return
            filter_dict: Metadata filters (e.g., {"year": {"$gte": 2020}})
            search_type: "similarity" or "mmr" (maximal marginal relevance)

        Returns:
            List of relevant documents with scores
        """

        if self.vectorstore is None:
            logger.error("Vector store not initialized. Please add documents first.")
            return []

        logger.info(f"Searching for: '{query}' (top {k} results)")

        if search_type == "similarity":
            if filter_dict:
                results = self.vectorstore.similarity_search(
                    query,
                    k=k,
                    filter=filter_dict
                )
            else:
                results = self.vectorstore.similarity_search(query, k=k)

        elif search_type == "mmr":
            # MMR for diversity
            results = self.vectorstore.max_marginal_relevance_search(
                query,
                k=k,
                fetch_k=k*2,  # Fetch more, then re-rank
                lambda_mult=0.5  # Balance relevance vs diversity
            )

        else:
            raise ValueError(f"Invalid search_type: {search_type}")

        logger.info(f"Found {len(results)} results")
        return results

    def search_with_scores(
        self,
        query: str,
        k: int = settings.top_k_results,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[tuple[Document, float]]:
        """
        Search with relevance scores.

        Returns:
            List of (document, score) tuples
        """

        if self.vectorstore is None:
            logger.error("Vector store not initialized")
            return []

        if filter_dict:
            results = self.vectorstore.similarity_search_with_score(
                query,
                k=k,
                filter=filter_dict
            )
        else:
            results = self.vectorstore.similarity_search_with_score(query, k=k)

        return results

    def create_contextual_compression_retriever(
        self,
        llm_model: str = settings.llm_model,
        top_k: int = 10
    ):
        """
        Create a retriever with contextual compression (re-ranking).

        This retriever:
        1. Retrieves top_k documents
        2. Uses LLM to extract only relevant parts
        3. Returns compressed, highly relevant results
        """

        if self.vectorstore is None:
            raise ValueError("Vector store not initialized")

        llm = ChatOpenAI(
            model=llm_model,
            temperature=0,
            openai_api_key=settings.openai_api_key
        )

        compressor = LLMChainExtractor.from_llm(llm)

        base_retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": top_k}
        )

        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=base_retriever
        )

        return compression_retriever

    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""

        if self.vectorstore is None:
            return {"status": "empty", "count": 0}

        try:
            collection = self.vectorstore._collection
            count = collection.count()

            return {
                "status": "active",
                "count": count,
                "collection_name": self.collection_name
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"status": "error", "message": str(e)}

    def delete_collection(self):
        """Delete the entire collection (use with caution!)"""

        if self.vectorstore is not None:
            logger.warning(f"Deleting collection: {self.collection_name}")
            self.vectorstore.delete_collection()
            self.vectorstore = None


# Example usage functions
def example_metadata_filtering():
    """
    Example of advanced metadata filtering.
    """

    retriever = AdvancedRetriever()

    # Filter by year range
    results = retriever.search(
        query="technology adoption in education",
        k=10,
        filter_dict={"year": {"$gte": 2020, "$lte": 2023}}
    )

    # Filter by author
    results = retriever.search(
        query="self-efficacy and technology use",
        k=5,
        filter_dict={"authors": {"$in": ["Smith", "Johnson"]}}
    )

    # Combine multiple filters
    results = retriever.search(
        query="artificial intelligence in K-12",
        k=10,
        filter_dict={
            "$and": [
                {"year": {"$gte": 2020}},
                {"file_type": "pdf"}
            ]
        }
    )


if __name__ == "__main__":
    # Test retrieval system
    retriever = AdvancedRetriever()
    stats = retriever.get_collection_stats()
    print(f"Collection stats: {stats}")
```

---

### Phase 3: LLM Integration & RAG Chain (15 minutes)

#### 3.1 LLM Integration

**File: backend/core/llm.py**

**Claude Code Prompt:**
```
Create a flexible LLM integration module in backend/core/llm.py that:

1. Supports multiple providers (OpenAI, Anthropic)
2. Implements different RAG chain types (stuff, refine, map-reduce)
3. Includes prompt templates optimized for literature review
4. Has citation formatting (APA, MLA style)
5. Tracks token usage
6. Implements streaming for real-time responses
7. Handles errors and retries

Make it research-focused with prompts that encourage critical analysis and proper citations.
```

**Expected code structure with comprehensive prompts and chain types...**

---

### Phase 4: Web Interface with Chainlit (20 minutes)

#### 4.1 Chainlit Application

**File: frontend/chainlit_app.py**

**Claude Code Prompt:**
```
Create a Chainlit-based web interface in frontend/chainlit_app.py that:

1. Has a clean chat interface for asking questions
2. Supports document upload (drag-and-drop)
3. Shows source citations with clickable links
4. Displays relevance scores
5. Allows metadata filtering (year range, author, etc.)
6. Has export functionality (export conversation as markdown)
7. Shows collection statistics (number of papers loaded)
8. Implements streaming responses
9. Includes a sidebar with:
   - Upload documents section
   - Filter options
   - Settings (temperature, top_k, etc.)
10. Custom styling that looks professional for researchers

Make it intuitive for non-technical users but powerful for advanced users.
```

---

### Phase 5: API Backend (15 minutes)

**File: backend/api/main.py**

**Claude Code Prompt:**
```
Create a FastAPI backend in backend/api/main.py that provides REST API endpoints for:

1. POST /documents/upload - Upload and process documents
2. POST /documents/batch-upload - Batch process from directory
3. GET /documents/list - List all documents with metadata
4. DELETE /documents/{doc_id} - Remove document from vector store
5. POST /query - Query the RAG system
6. GET /query/history - Get query history
7. GET /stats - Get collection statistics
8. POST /export - Export results as CSV/JSON

Include comprehensive error handling, input validation with Pydantic,
and API documentation with examples.
```

---

### Phase 6: Testing & Deployment (10 minutes)

#### 6.1 Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose ports
EXPOSE 8000

# Run application
CMD ["chainlit", "run", "frontend/chainlit_app.py", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Usage Examples

### For Beginners (Using Web Interface)

1. **Upload Papers:**
   - Drag-and-drop PDFs into the upload zone
   - Wait for processing (progress bar shows status)

2. **Ask Questions:**
   ```
   "What are the main theories of technology adoption mentioned in these papers?"
   ```

3. **Filter Results:**
   - Set year range: 2020-2023
   - Select specific authors

4. **Export Findings:**
   - Click "Export" button
   - Download as Markdown with citations

### For Advanced Users (Using Claude Code)

**Claude Code Prompt:**
```
I want to add a new feature to extract all effect sizes (Cohen's d, r, OR) from papers
and create a structured dataset for meta-analysis. Where should this go and how should
it integrate with the existing system?
```

**Claude Code Prompt:**
```
Modify the chunking strategy to preserve table content and extract tables separately.
Tables often contain important statistical results.
```

**Claude Code Prompt:**
```
Add a feature to identify papers that haven't cited each other but discuss similar
topics. This could reveal synthesis opportunities.
```

---

## Troubleshooting Guide

### Common Issues

**Issue: "Vector store empty" error**
```bash
# Check if documents were ingested
python -c "from backend.core.retrieval import AdvancedRetriever; r = AdvancedRetriever(); print(r.get_collection_stats())"

# Re-ingest if needed
python scripts/ingest_papers.py ./data/raw_pdfs
```

**Issue: "Out of memory" during ingestion**
- Reduce batch_size in ingestion settings
- Process papers in smaller batches

**Issue: Poor retrieval quality**
- Adjust chunk_size (try 1500 instead of 1000)
- Use MMR search for more diversity
- Increase top_k to retrieve more context

---

## Module 2 Complete! ✅

You now have:
- ✅ Production-ready Literature Review RAG system
- ✅ Web interface for your team
- ✅ API for programmatic access
- ✅ Skills to customize with Claude Code

**Next: Module 3 - Qualitative Data Coding RAG** 🎤

---

## Additional Resources

- [Chainlit Documentation](https://docs.chainlit.io/)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)
- [ChromaDB Guide](https://docs.trychroma.com/)
