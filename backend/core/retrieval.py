"""
Advanced retrieval system with hybrid search and metadata filtering
"""
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from .config import settings

logger = logging.getLogger(__name__)


class AdvancedRetriever:
    """Advanced retrieval system with semantic search and filtering"""

    def __init__(
        self,
        collection_name: str = "literature_review",
        persist_directory: str = None
    ):
        self.collection_name = collection_name
        self.persist_directory = persist_directory or settings.chroma_db_path

        # Initialize embeddings (using free HuggingFace model)
        logger.info(f"Loading embedding model: {settings.embedding_model}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )

        # Initialize vector store
        self.vectorstore = None
        self._initialize_vectorstore()

    def _initialize_vectorstore(self):
        """Initialize or load existing vector store"""
        persist_path = Path(self.persist_directory)

        if persist_path.exists() and any(persist_path.iterdir()):
            logger.info(f"Loading existing ChromaDB from {self.persist_directory}")
            try:
                self.vectorstore = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings,
                    collection_name=self.collection_name
                )
                logger.info("ChromaDB loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load existing ChromaDB: {e}")
                logger.info("Will create new collection on first ingestion")
                self.vectorstore = None
        else:
            logger.info("No existing ChromaDB found. Will create on first ingestion.")
            self.vectorstore = None

    def add_documents(
        self,
        documents: List[Document],
        batch_size: int = 100
    ) -> None:
        """
        Add documents to vector store in batches

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
        k: int = None,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Search for relevant documents

        Args:
            query: Search query
            k: Number of results to return (defaults to settings.top_k_results)
            filter_dict: Metadata filters (e.g., {"year": 2020})

        Returns:
            List of relevant documents
        """
        if self.vectorstore is None:
            logger.error("Vector store not initialized. Please add documents first.")
            return []

        k = k or settings.top_k_results

        logger.info(f"Searching for: '{query}' (top {k} results)")

        try:
            if filter_dict:
                results = self.vectorstore.similarity_search(
                    query,
                    k=k,
                    filter=filter_dict
                )
            else:
                results = self.vectorstore.similarity_search(query, k=k)

            logger.info(f"Found {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def search_with_scores(
        self,
        query: str,
        k: int = None,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[tuple]:
        """
        Search with relevance scores

        Returns:
            List of (document, score) tuples
        """
        if self.vectorstore is None:
            logger.error("Vector store not initialized")
            return []

        k = k or settings.top_k_results

        try:
            if filter_dict:
                results = self.vectorstore.similarity_search_with_score(
                    query,
                    k=k,
                    filter=filter_dict
                )
            else:
                results = self.vectorstore.similarity_search_with_score(query, k=k)

            return results

        except Exception as e:
            logger.error(f"Search with scores failed: {e}")
            return []

    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection"""
        if self.vectorstore is None:
            return {"status": "empty", "count": 0}

        try:
            collection = self.vectorstore._collection
            count = collection.count()

            return {
                "status": "active",
                "count": count,
                "collection_name": self.collection_name,
                "persist_directory": self.persist_directory
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"status": "error", "message": str(e)}

    def delete_collection(self):
        """Delete the entire collection (use with caution!)"""
        if self.vectorstore is not None:
            logger.warning(f"Deleting collection: {self.collection_name}")
            try:
                self.vectorstore.delete_collection()
                self.vectorstore = None
                logger.info("Collection deleted successfully")
            except Exception as e:
                logger.error(f"Failed to delete collection: {e}")


# Singleton instance
_retriever_instance = None


def get_retriever() -> AdvancedRetriever:
    """Get or create the global retriever instance"""
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = AdvancedRetriever()
    return _retriever_instance
