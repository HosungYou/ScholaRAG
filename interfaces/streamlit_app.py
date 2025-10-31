"""
ScholaRAG Streamlit Interface

A visual web interface for chatting with your research papers.

Usage:
    streamlit run streamlit_app.py

Features:
- Chat history
- Export conversations
- Citation tracking
- Paper statistics

Author: ScholaRAG Team
License: MIT
"""

import os
import streamlit as st
import chromadb
from anthropic import Anthropic
from datetime import datetime
import json


# Page config
st.set_page_config(
    page_title="ScholaRAG Chat",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_resource
def init_vector_db(db_path: str = "./chroma_db", collection_name: str = "papers"):
    """Initialize Vector DB connection (cached)"""
    client = chromadb.PersistentClient(path=db_path)
    try:
        collection = client.get_collection(name=collection_name)
        return collection
    except Exception as e:
        st.error(f"❌ Error loading collection: {e}")
        st.stop()


@st.cache_resource
def init_claude():
    """Initialize Claude API (cached)"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("❌ ANTHROPIC_API_KEY not found. Set it in your .env file.")
        st.stop()
    return Anthropic(api_key=api_key)


def query_rag(question: str, collection, anthropic_client, top_k: int = 5):
    """Query Vector DB and generate answer"""

    # Search papers
    results = collection.query(
        query_texts=[question],
        n_results=top_k
    )

    documents = results['documents'][0]
    metadatas = results['metadatas'][0] if 'metadatas' in results else [{}] * len(documents)

    if not documents:
        return {
            "answer": "No relevant papers found for this question.",
            "citations": [],
            "papers": []
        }

    # Build context
    context_parts = []
    papers_info = []

    for i, (doc, meta) in enumerate(zip(documents, metadatas)):
        paper_id = meta.get('paper_id', f'Paper_{i+1}')
        author = meta.get('author', 'Unknown')
        year = meta.get('year', 'N/A')
        title = meta.get('title', 'Untitled')

        context_parts.append(f"[{paper_id}] {author} ({year})\n{doc}\n")
        papers_info.append({
            "id": paper_id,
            "author": author,
            "year": year,
            "title": title
        })

    context = "\n---\n".join(context_parts)

    # Generate answer
    response = anthropic_client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=2048,
        temperature=0,
        messages=[{
            "role": "user",
            "content": f"""You are a research assistant. Answer based ONLY on these excerpts:

{context}

Question: {question}

Provide a clear answer with [Paper_ID] citations for every claim."""
        }]
    )

    answer = response.content[0].text

    # Extract citations
    import re
    citations = list(set(re.findall(r'\[([^\]]+)\]', answer)))

    return {
        "answer": answer,
        "citations": citations,
        "papers": papers_info
    }


def main():
    """Main app"""

    # Header
    st.title("🔍 ScholaRAG Chat Interface")
    st.markdown("Ask questions about your research papers")

    # Initialize
    collection = init_vector_db()
    anthropic_client = init_claude()

    # Sidebar
    with st.sidebar:
        st.header("📚 Knowledge Base")

        paper_count = collection.count()
        st.metric("Total Papers", paper_count)

        st.markdown("---")

        st.header("⚙️ Settings")
        top_k = st.slider("Papers to retrieve", 3, 10, 5)

        st.markdown("---")

        # Export chat history
        if st.button("💾 Export Chat History"):
            if "messages" in st.session_state and st.session_state.messages:
                export_data = json.dumps(st.session_state.messages, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=export_data,
                    file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            else:
                st.info("No chat history to export")

        # Clear history
        if st.button("🗑️ Clear History"):
            st.session_state.messages = []
            st.rerun()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # Show citations for assistant messages
            if message["role"] == "assistant" and "citations" in message:
                with st.expander("📖 Citations"):
                    for citation in message["citations"]:
                        st.markdown(f"- `{citation}`")

    # Chat input
    if prompt := st.chat_input("Ask about your research papers..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching papers and generating answer..."):
                result = query_rag(prompt, collection, anthropic_client, top_k)

                st.markdown(result["answer"])

                # Citations
                if result["citations"]:
                    with st.expander("📖 Citations"):
                        for citation in result["citations"]:
                            st.markdown(f"- `{citation}`")

                # Retrieved papers
                if result["papers"]:
                    with st.expander(f"📚 Retrieved {len(result['papers'])} papers"):
                        for paper in result["papers"]:
                            st.markdown(f"**{paper['id']}**: {paper['title']} ({paper['author']}, {paper['year']})")

        # Add assistant response to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "citations": result["citations"],
            "timestamp": datetime.now().isoformat()
        })


if __name__ == "__main__":
    main()
