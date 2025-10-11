"""
ResearcherRAG Chat Interface

This script lets you query your Vector Database through conversational AI.

USAGE:

  Method 1: Interactive Mode (Recommended)
    $ python interfaces/claude_code_interface.py

    Then type questions when prompted:
    You: What are the main adoption barriers?
    You: Show me papers from 2023
    You: exit

  Method 2: Single Question Mode
    $ python interfaces/claude_code_interface.py "What are the key findings?"

  Method 3: From Claude Code
    Tell Claude Code: "Run python interfaces/claude_code_interface.py"
    Then interact with the prompts

PREREQUISITES:
  - Completed Stages 1-5 (Vector DB built in ./chroma_db)
  - Environment variable: ANTHROPIC_API_KEY
  - Dependencies: pip install chromadb anthropic

WHY USE THIS?
  Without this script, Claude uses GENERAL KNOWLEDGE.
  With this script, Claude searches YOUR PAPERS and cites them!

Author: ResearcherRAG Team
License: MIT
"""

import os
import sys
import json
from typing import List, Dict
from pathlib import Path

try:
    import chromadb
    from anthropic import Anthropic
except ImportError:
    print("❌ Missing dependencies. Install with:")
    print("   pip install chromadb anthropic")
    sys.exit(1)


class ResearcherRAGChat:
    """Simple chat interface for querying your Vector DB"""

    def __init__(self, db_path: str = "./chroma_db", collection_name: str = "papers"):
        """Initialize connection to Vector DB and Claude API"""

        # Load Vector DB
        print(f"📂 Loading Vector DB from {db_path}...")
        self.client = chromadb.PersistentClient(path=db_path)

        try:
            self.collection = self.client.get_collection(name=collection_name)
            paper_count = self.collection.count()
            print(f"✅ Loaded {paper_count} papers from collection '{collection_name}'")
        except Exception as e:
            print(f"❌ Error loading collection: {e}")
            print(f"   Available collections: {[c.name for c in self.client.list_collections()]}")
            sys.exit(1)

        # Initialize Claude API
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("❌ ANTHROPIC_API_KEY not found in environment")
            print("   Set it in your .env file or export it:")
            print("   export ANTHROPIC_API_KEY='your-key-here'")
            sys.exit(1)

        self.anthropic = Anthropic(api_key=api_key)
        print("✅ Connected to Claude API\n")

    def query(self, question: str, top_k: int = 5) -> Dict:
        """Query the Vector DB and generate answer"""

        print(f"🔍 Searching papers for: '{question}'\n")

        # Search Vector DB
        # Note: ChromaDB generates embeddings automatically if using default embedding function
        results = self.collection.query(
            query_texts=[question],
            n_results=top_k
        )

        # Extract documents and metadata
        documents = results['documents'][0]
        metadatas = results['metadatas'][0] if 'metadatas' in results else [{}] * len(documents)
        distances = results['distances'][0] if 'distances' in results else [0] * len(documents)

        if not documents:
            return {
                "answer": "No relevant papers found for this question.",
                "citations": [],
                "retrieved_chunks": 0
            }

        # Build context for Claude
        context_parts = []
        for i, (doc, meta) in enumerate(zip(documents, metadatas)):
            paper_id = meta.get('paper_id', f'Paper_{i+1}')
            author = meta.get('author', 'Unknown')
            year = meta.get('year', 'N/A')

            context_parts.append(
                f"[{paper_id}] {author} ({year})\n{doc}\n"
            )

        context = "\n---\n".join(context_parts)

        # Generate answer with Claude
        print("💭 Generating answer with Claude...\n")

        response = self.anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            temperature=0,
            messages=[{
                "role": "user",
                "content": f"""You are a research assistant helping with a systematic literature review.

Based ONLY on these research paper excerpts:

{context}

Question: {question}

Instructions:
1. Answer the question using ONLY information from the provided excerpts
2. Cite papers using [Paper_ID] format for every claim
3. If the excerpts don't contain relevant information, say so
4. Provide a structured, academic-quality answer

Answer:"""
            }]
        )

        answer = response.content[0].text

        # Extract citations from answer
        import re
        citations = list(set(re.findall(r'\[([^\]]+)\]', answer)))

        return {
            "answer": answer,
            "citations": citations,
            "retrieved_chunks": len(documents),
            "similarity_scores": [f"{1-d:.3f}" for d in distances]
        }

    def interactive_mode(self):
        """Interactive chat mode"""
        print("=" * 60)
        print("  ResearcherRAG Interactive Chat")
        print("=" * 60)
        print("\nType your questions (or 'exit' to quit)\n")

        while True:
            try:
                question = input("You: ").strip()

                if not question:
                    continue

                if question.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Goodbye!")
                    break

                result = self.query(question)

                print("\n" + "=" * 60)
                print("Answer:")
                print("=" * 60)
                print(result["answer"])
                print("\n" + "-" * 60)
                print(f"📚 Retrieved {result['retrieved_chunks']} relevant chunks")
                print(f"📖 Citations: {', '.join(result['citations'])}")
                print("=" * 60 + "\n")

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")


def main():
    """Main entry point"""

    # Check if question provided as argument
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])

        # Single query mode
        chat = ResearcherRAGChat()
        result = chat.query(question)

        print("\n" + "=" * 60)
        print("Answer:")
        print("=" * 60)
        print(result["answer"])
        print("\n" + "-" * 60)
        print(f"📚 Retrieved {result['retrieved_chunks']} relevant chunks")
        print(f"📖 Citations: {', '.join(result['citations'])}")
        print("=" * 60)
    else:
        # Interactive mode
        chat = ResearcherRAGChat()
        chat.interactive_mode()


if __name__ == "__main__":
    main()
