#!/usr/bin/env python3
"""
Stage 5: Build RAG System from Downloaded PDFs

Processes PDFs, generates embeddings, and creates vector database
for semantic search and question answering.

Usage:
    python scripts/05_build_rag.py --project <project_path>

Example:
    python scripts/05_build_rag.py --project projects/2025-10-13_AI-Chatbots
"""

import argparse
import pandas as pd
import sys
import os
from pathlib import Path
from typing import List, Dict
import chromadb
from chromadb.config import Settings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
import hashlib
from dotenv import load_dotenv


class RAGBuilder:
    """Build RAG system from PDF documents"""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.input_dir = self.project_path / "data" / "03_pdfs"
        self.output_dir = self.project_path / "data" / "04_rag"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # RAG settings
        self.chunk_size = 1000
        self.chunk_overlap = 200
        self.embedding_model = "sentence-transformers/all-MiniLM-L6-v2"

        # Load environment variables
        load_dotenv()

    def load_metadata(self) -> pd.DataFrame:
        """
        Load paper metadata

        Returns:
            DataFrame with paper metadata
        """
        print("\n📂 Loading paper metadata...")

        metadata_file = self.input_dir / "papers_metadata.csv"
        if not metadata_file.exists():
            print(f"❌ Error: Metadata file not found: {metadata_file}")
            print("   Run PDF download first: python scripts/04_download_pdfs.py")
            sys.exit(1)

        df = pd.read_csv(metadata_file)

        # Filter only successfully downloaded papers
        df_downloaded = df[df['downloaded'] == True].copy()
        print(f"   ✓ Loaded {len(df_downloaded)} papers with PDFs")

        return df_downloaded

    def load_pdf(self, pdf_path: str, metadata: Dict) -> List[Document]:
        """
        Load and chunk a single PDF

        Args:
            pdf_path: Path to PDF file
            metadata: Paper metadata to attach

        Returns:
            List of Document objects with chunks
        """
        try:
            # Load PDF
            loader = PyMuPDFLoader(pdf_path)
            pages = loader.load()

            # Add metadata to each page
            for page in pages:
                page.metadata.update(metadata)

            # Split into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                length_function=len,
                separators=["\n\n", "\n", ". ", " ", ""]
            )

            chunks = text_splitter.split_documents(pages)

            return chunks

        except Exception as e:
            print(f"   ⚠️  Error loading {pdf_path}: {e}")
            return []

    def load_all_pdfs(self, df: pd.DataFrame) -> List[Document]:
        """
        Load and chunk all PDFs

        Args:
            df: DataFrame with paper metadata

        Returns:
            List of all document chunks
        """
        print("\n" + "="*60)
        print("📄 PDF PROCESSING")
        print("="*60)
        print(f"\nTotal PDFs to process: {len(df)}")

        all_chunks = []

        for idx, row in df.iterrows():
            paper_idx = idx + 1
            pdf_path = row['local_path']

            print(f"\n[{paper_idx}/{len(df)}] Processing: {row['title'][:50]}...")

            # Prepare metadata
            metadata = {
                'title': row['title'],
                'authors': row.get('authors', 'Unknown'),
                'year': int(row.get('year', 0)) if pd.notna(row.get('year')) else None,
                'source': row.get('source', 'Unknown'),
                'doi': row.get('doi', None),
                'pdf_path': pdf_path
            }

            # Load and chunk PDF
            chunks = self.load_pdf(pdf_path, metadata)

            if chunks:
                all_chunks.extend(chunks)
                print(f"   ✓ Extracted {len(chunks)} chunks")
            else:
                print(f"   ✗ Failed to process")

        print(f"\n✓ Total chunks extracted: {len(all_chunks)}")

        return all_chunks

    def create_vector_database(self, chunks: List[Document]) -> Chroma:
        """
        Create vector database from document chunks

        Args:
            chunks: List of document chunks

        Returns:
            Chroma vector store
        """
        print("\n" + "="*60)
        print("🧠 EMBEDDING GENERATION")
        print("="*60)
        print(f"\nTotal chunks to embed: {len(chunks)}")
        print(f"Embedding model: {self.embedding_model}")

        # Initialize embeddings
        print("\n⏳ Loading embedding model...")
        embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        print("   ✓ Model loaded")

        # Create collection name from project
        project_name = self.project_path.name.replace('_', '-').lower()
        collection_name = f"papers-{project_name}"

        # Create ChromaDB vector store
        print(f"\n⏳ Creating vector database: {collection_name}")

        persist_directory = str(self.output_dir / "chroma_db")

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name=collection_name,
            persist_directory=persist_directory
        )

        print(f"   ✓ Vector database created")
        print(f"   💾 Saved to: {persist_directory}")

        return vectorstore

    def test_retrieval(self, vectorstore: Chroma, df: pd.DataFrame):
        """
        Test retrieval with sample queries

        Args:
            vectorstore: Chroma vector store
            df: DataFrame with paper metadata
        """
        print("\n" + "="*60)
        print("🔍 TESTING RETRIEVAL")
        print("="*60)

        # Load research question from config
        config_file = self.project_path / "config.yaml"
        if config_file.exists():
            import yaml
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
                research_question = config.get('research_question', 'Test query')
        else:
            research_question = "What are the main findings?"

        print(f"\nQuery: {research_question}")

        # Retrieve relevant chunks
        results = vectorstore.similarity_search(
            research_question,
            k=5
        )

        print(f"\n✓ Found {len(results)} relevant chunks:\n")

        for i, doc in enumerate(results, 1):
            print(f"{i}. {doc.metadata.get('title', 'Unknown')} ({doc.metadata.get('year', 'N/A')})")
            print(f"   Preview: {doc.page_content[:150]}...")
            print()

    def generate_summary(self, df: pd.DataFrame, chunks: List[Document]):
        """
        Generate RAG system summary

        Args:
            df: DataFrame with paper metadata
            chunks: List of document chunks
        """
        print("\n" + "="*60)
        print("📊 RAG SYSTEM SUMMARY")
        print("="*60)

        print(f"\nDocuments:")
        print(f"  Total papers: {len(df)}")
        print(f"  Total chunks: {len(chunks)}")
        print(f"  Avg chunks per paper: {len(chunks) / len(df):.1f}")

        print(f"\nChunking:")
        print(f"  Chunk size: {self.chunk_size} characters")
        print(f"  Chunk overlap: {self.chunk_overlap} characters")

        print(f"\nEmbeddings:")
        print(f"  Model: {self.embedding_model}")
        print(f"  Dimension: 384")

        print(f"\nVector Database:")
        print(f"  Type: ChromaDB")
        print(f"  Location: {self.output_dir / 'chroma_db'}")

        # Calculate statistics
        chunk_lengths = [len(chunk.page_content) for chunk in chunks]
        avg_length = sum(chunk_lengths) / len(chunk_lengths)
        min_length = min(chunk_lengths)
        max_length = max(chunk_lengths)

        print(f"\nChunk Statistics:")
        print(f"  Average length: {avg_length:.0f} characters")
        print(f"  Min length: {min_length} characters")
        print(f"  Max length: {max_length} characters")

        print("="*60)

        # Save configuration
        config = {
            'total_papers': len(df),
            'total_chunks': len(chunks),
            'chunk_size': self.chunk_size,
            'chunk_overlap': self.chunk_overlap,
            'embedding_model': self.embedding_model,
            'vector_db': 'ChromaDB',
            'persist_directory': str(self.output_dir / 'chroma_db')
        }

        import json
        config_file = self.output_dir / "rag_config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)

        print(f"\n💾 RAG configuration saved to: {config_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Build RAG system from downloaded PDFs"
    )
    parser.add_argument(
        '--project',
        required=True,
        help='Path to project directory'
    )
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=1000,
        help='Chunk size in characters (default: 1000)'
    )
    parser.add_argument(
        '--chunk-overlap',
        type=int,
        default=200,
        help='Chunk overlap in characters (default: 200)'
    )
    parser.add_argument(
        '--embedding-model',
        type=str,
        default='sentence-transformers/all-MiniLM-L6-v2',
        help='Embedding model name (default: all-MiniLM-L6-v2)'
    )

    args = parser.parse_args()

    # Validate project path
    project_path = Path(args.project)
    if not project_path.exists():
        print(f"❌ Error: Project path does not exist: {project_path}")
        sys.exit(1)

    # Initialize RAG builder
    builder = RAGBuilder(args.project)
    builder.chunk_size = args.chunk_size
    builder.chunk_overlap = args.chunk_overlap
    builder.embedding_model = args.embedding_model

    # Load metadata
    df = builder.load_metadata()

    # Process PDFs
    chunks = builder.load_all_pdfs(df)

    if not chunks:
        print("\n❌ Error: No chunks extracted from PDFs")
        sys.exit(1)

    # Create vector database
    vectorstore = builder.create_vector_database(chunks)

    # Test retrieval
    builder.test_retrieval(vectorstore, df)

    # Generate summary
    builder.generate_summary(df, chunks)

    print("\n✨ Next step: Query the RAG system")
    print(f"   python scripts/06_query_rag.py --project {args.project}")


if __name__ == '__main__':
    main()
