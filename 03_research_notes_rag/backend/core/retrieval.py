"""Vector retrieval for Research Notes RAG."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from .config import settings

logger = logging.getLogger(__name__)


class NotesRetriever:
    """Wrapper around Chroma for semantic note search."""

    def __init__(
        self,
        collection_name: str = "research_notes",
        vector_db_path: Optional[str] = None,
    ) -> None:
        self.collection_name = collection_name
        self.vector_db_path = vector_db_path or settings.vector_db_path
        self._vectorstore: Optional[Chroma] = None

        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        self._load_vectorstore()

    def _load_vectorstore(self) -> None:
        persist_path = Path(self.vector_db_path)
        if persist_path.exists() and any(persist_path.iterdir()):
            logger.info("Loading existing note collection from %s", persist_path)
            self._vectorstore = Chroma(
                persist_directory=str(persist_path),
                embedding_function=self.embeddings,
                collection_name=self.collection_name,
            )
        else:
            logger.info("Vector store not initialised yet; will create on first ingestion.")

    @property
    def vectorstore(self) -> Chroma:
        if self._vectorstore is None:
            raise RuntimeError("Vector store not initialised. Add documents first.")
        return self._vectorstore

    def add_documents(self, documents: List[Document], batch_size: int = 64) -> None:
        if not documents:
            logger.warning("No documents provided to add_documents.")
            return

        persist_path = Path(self.vector_db_path)
        if self._vectorstore is None:
            logger.info("Creating new Chroma collection at %s", persist_path)
            self._vectorstore = Chroma.from_documents(
                documents=documents[:batch_size],
                embedding=self.embeddings,
                persist_directory=str(persist_path),
                collection_name=self.collection_name,
            )
            start_index = batch_size
        else:
            start_index = 0

        for index in range(start_index, len(documents), batch_size):
            chunk = documents[index : index + batch_size]
            self.vectorstore.add_documents(chunk)

        if hasattr(self.vectorstore, "persist"):
            self.vectorstore.persist()
            logger.info("Persisted vector store with %d new chunks.", len(documents))

    def search(self, query: str, k: Optional[int] = None, filters: Optional[Dict[str, Any]] = None) -> List[Document]:
        if self._vectorstore is None:
            logger.error("Search requested before any notes were ingested.")
            return []

        k = k or settings.top_k
        return self.vectorstore.similarity_search(query, k=k, filter=filters)

    def stats(self) -> Dict[str, Any]:
        if self._vectorstore is None:
            return {"status": "empty", "count": 0}

        collection = self.vectorstore._collection
        return {
            "status": "ready",
            "count": collection.count(),
            "persist_directory": self.vector_db_path,
        }


def get_retriever() -> NotesRetriever:
    """Return a singleton retriever for the module."""
    global _RETRIEVER
    try:
        retriever = _RETRIEVER
    except NameError:  # pragma: no cover - first import path
        retriever = None

    if retriever is None:
        retriever = NotesRetriever()
        globals()["_RETRIEVER"] = retriever
    return retriever
