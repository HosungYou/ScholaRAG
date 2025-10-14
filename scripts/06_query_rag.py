#!/usr/bin/env python3
"""
Stage 6: Query RAG System for Literature Review

Interactive and batch query interface for the RAG system.
Generates answers with proper citations and evidence.

Usage:
    # Interactive mode
    python scripts/06_query_rag.py --project <project_path> --interactive

    # Single query mode
    python scripts/06_query_rag.py --project <project_path> --query "What are the main findings?"

    # Batch mode
    python scripts/06_query_rag.py --project <project_path> --queries queries.txt

Example:
    python scripts/06_query_rag.py \
        --project projects/2025-10-13_AI-Chatbots \
        --interactive
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List, Dict
import anthropic
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import json


class RAGQuerier:
    """Query RAG system with Claude for literature review"""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.rag_dir = self.project_path / "data" / "04_rag"
        self.output_dir = self.project_path / "data" / "05_analysis"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load RAG configuration
        self.load_rag_config()

        # Load environment variables
        load_dotenv()
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            print("❌ Error: ANTHROPIC_API_KEY not found in environment")
            sys.exit(1)

        self.client = anthropic.Anthropic(api_key=api_key)

        # Load vector store
        self.vectorstore = self.load_vectorstore()

    def load_rag_config(self):
        """Load RAG system configuration"""
        config_file = self.rag_dir / "rag_config.json"
        if not config_file.exists():
            print(f"❌ Error: RAG config not found: {config_file}")
            print("   Run RAG building first: python scripts/05_build_rag.py")
            sys.exit(1)

        with open(config_file, 'r') as f:
            self.config = json.load(f)

    def load_vectorstore(self) -> Chroma:
        """
        Load existing vector database

        Returns:
            Chroma vector store
        """
        print("\n📂 Loading vector database...")

        persist_directory = self.config['persist_directory']

        if not Path(persist_directory).exists():
            print(f"❌ Error: Vector database not found: {persist_directory}")
            sys.exit(1)

        # Load embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name=self.config['embedding_model'],
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )

        # Load vector store
        vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )

        print(f"   ✓ Loaded {self.config['total_chunks']} chunks from {self.config['total_papers']} papers")

        return vectorstore

    def retrieve_context(self, query: str, k: int = 10) -> List[Dict]:
        """
        Retrieve relevant context for query

        Args:
            query: User query
            k: Number of chunks to retrieve

        Returns:
            List of relevant documents with metadata
        """
        results = self.vectorstore.similarity_search_with_score(query, k=k)

        context_docs = []
        for doc, score in results:
            context_docs.append({
                'content': doc.page_content,
                'title': doc.metadata.get('title', 'Unknown'),
                'authors': doc.metadata.get('authors', 'Unknown'),
                'year': doc.metadata.get('year', 'N/A'),
                'source': doc.metadata.get('source', 'Unknown'),
                'score': score
            })

        return context_docs

    def generate_answer(self, query: str, context_docs: List[Dict]) -> Dict:
        """
        Generate answer using Claude with retrieved context

        Args:
            query: User query
            context_docs: Retrieved context documents

        Returns:
            Dictionary with answer and citations
        """
        # Prepare context for Claude
        context_text = ""
        for i, doc in enumerate(context_docs, 1):
            context_text += f"\n[{i}] {doc['title']} ({doc['year']})\n"
            context_text += f"Authors: {doc['authors']}\n"
            context_text += f"Content: {doc['content']}\n"
            context_text += "-" * 80 + "\n"

        # Create prompt
        prompt = f"""You are a research assistant conducting a systematic literature review.

Research Question: {query}

Context from Academic Papers:
{context_text}

Task: Provide a comprehensive answer to the research question based on the provided papers.

Response Format:
1. **Direct Answer**: Start with a clear, concise answer (2-3 sentences)
2. **Detailed Analysis**: Provide in-depth analysis organized by themes or findings
3. **Evidence**: Quote relevant passages and cite sources using [number] format
4. **Synthesis**: Identify patterns, agreements, or contradictions across papers
5. **Limitations**: Note any gaps or limitations in the literature

Citation Style: Use [1], [2], etc. to reference papers. Include author and year in text when relevant.

Important:
- Only use information from the provided papers
- If papers don't address the question, explicitly state this
- Maintain academic rigor and objectivity"""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            answer = response.content[0].text

            return {
                'query': query,
                'answer': answer,
                'num_sources': len(context_docs),
                'sources': [
                    {
                        'title': doc['title'],
                        'authors': doc['authors'],
                        'year': doc['year'],
                        'source': doc['source']
                    }
                    for doc in context_docs
                ]
            }

        except Exception as e:
            print(f"❌ Error generating answer: {e}")
            return {
                'query': query,
                'answer': f"Error: {str(e)}",
                'num_sources': 0,
                'sources': []
            }

    def query(self, question: str, k: int = 10) -> Dict:
        """
        Full query pipeline: retrieve + generate

        Args:
            question: User question
            k: Number of chunks to retrieve

        Returns:
            Query result with answer and citations
        """
        print(f"\n{'='*60}")
        print(f"Query: {question}")
        print('='*60)

        # Retrieve context
        print("\n🔍 Retrieving relevant papers...")
        context_docs = self.retrieve_context(question, k=k)
        print(f"   ✓ Found {len(context_docs)} relevant chunks")

        # Generate answer
        print("\n🤖 Generating answer with Claude...")
        result = self.generate_answer(question, context_docs)

        print("\n📝 Answer:")
        print(result['answer'])

        print(f"\n📚 Sources ({result['num_sources']}):")
        for i, source in enumerate(result['sources'], 1):
            print(f"   [{i}] {source['authors']} ({source['year']}). {source['title']}")

        return result

    def interactive_mode(self):
        """Run interactive query mode"""
        print("\n" + "="*60)
        print("🔍 INTERACTIVE RAG QUERY MODE")
        print("="*60)
        print(f"\nProject: {self.project_path.name}")
        print(f"Papers: {self.config['total_papers']}")
        print(f"Chunks: {self.config['total_chunks']}")
        print("\nCommands:")
        print("  - Type your question and press Enter")
        print("  - Type 'save' to save current session")
        print("  - Type 'quit' or 'exit' to exit")
        print("="*60)

        session_results = []

        while True:
            try:
                question = input("\n💭 Your question: ").strip()

                if not question:
                    continue

                if question.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Exiting...")
                    break

                if question.lower() == 'save':
                    self.save_session(session_results)
                    continue

                # Process query
                result = self.query(question)
                session_results.append(result)

            except KeyboardInterrupt:
                print("\n\n👋 Exiting...")
                break

        # Offer to save session
        if session_results:
            save = input("\n💾 Save this session? (y/n): ").strip().lower()
            if save == 'y':
                self.save_session(session_results)

    def batch_query(self, queries: List[str]):
        """
        Process multiple queries in batch

        Args:
            queries: List of query strings
        """
        print("\n" + "="*60)
        print("📋 BATCH QUERY MODE")
        print("="*60)
        print(f"\nTotal queries: {len(queries)}")

        results = []

        for i, query in enumerate(queries, 1):
            print(f"\n[{i}/{len(queries)}]")
            result = self.query(query)
            results.append(result)

        # Save all results
        self.save_session(results, filename="batch_results.json")

    def save_session(self, results: List[Dict], filename: str = None):
        """
        Save query results to file

        Args:
            results: List of query results
            filename: Output filename (auto-generated if None)
        """
        if not results:
            print("   No results to save")
            return

        if filename is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"query_session_{timestamp}.json"

        output_file = self.output_dir / filename

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Session saved to: {output_file}")

        # Also save as Markdown for readability
        md_file = output_file.with_suffix('.md')
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(f"# Literature Review Query Session\n\n")
            f.write(f"Project: {self.project_path.name}\n\n")
            f.write(f"Papers: {self.config['total_papers']} | ")
            f.write(f"Chunks: {self.config['total_chunks']}\n\n")
            f.write("---\n\n")

            for i, result in enumerate(results, 1):
                f.write(f"## Query {i}\n\n")
                f.write(f"**Question**: {result['query']}\n\n")
                f.write(f"**Answer**:\n\n{result['answer']}\n\n")
                f.write(f"**Sources** ({result['num_sources']}):\n\n")
                for j, source in enumerate(result['sources'], 1):
                    f.write(f"{j}. {source['authors']} ({source['year']}). {source['title']}\n")
                f.write("\n---\n\n")

        print(f"💾 Markdown saved to: {md_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Query RAG system for literature review"
    )
    parser.add_argument(
        '--project',
        required=True,
        help='Path to project directory'
    )

    # Query modes (mutually exclusive)
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        '--interactive',
        action='store_true',
        help='Start interactive query mode'
    )
    mode_group.add_argument(
        '--query',
        type=str,
        help='Single query to process'
    )
    mode_group.add_argument(
        '--queries',
        type=str,
        help='File with queries (one per line)'
    )

    parser.add_argument(
        '--k',
        type=int,
        default=10,
        help='Number of chunks to retrieve (default: 10)'
    )

    args = parser.parse_args()

    # Validate project path
    project_path = Path(args.project)
    if not project_path.exists():
        print(f"❌ Error: Project path does not exist: {project_path}")
        sys.exit(1)

    # Initialize querier
    querier = RAGQuerier(args.project)

    # Run appropriate mode
    if args.interactive:
        querier.interactive_mode()

    elif args.query:
        result = querier.query(args.query, k=args.k)
        querier.save_session([result])

    elif args.queries:
        queries_file = Path(args.queries)
        if not queries_file.exists():
            print(f"❌ Error: Queries file not found: {queries_file}")
            sys.exit(1)

        with open(queries_file, 'r') as f:
            queries = [line.strip() for line in f if line.strip()]

        querier.batch_query(queries)

    print("\n✨ Next step: Generate PRISMA diagram")
    print(f"   python scripts/07_generate_prisma.py --project {args.project}")


if __name__ == '__main__':
    main()
