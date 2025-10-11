# Deployment Guide: Hugging Face Spaces + Qdrant Cloud

## Architecture Decision: Final Recommendation

For your 3 RAG systems (Literature Review, Qualitative Coding, Research Notes), we recommend:

```
┌─────────────────────────────────────────────────────────────┐
│           Hugging Face Space (Gradio Interface)             │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Literature  │  │ Qualitative │  │  Research   │         │
│  │   Review    │  │   Coding    │  │   Notes     │         │
│  │ (LangGraph) │  │ (LangGraph) │  │(LangChain)  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                           │
                           ├─→ Qdrant Cloud (Vector Storage)
                           ├─→ Anthropic Claude API (LLM)
                           └─→ HuggingFace Embeddings (Free)
```

---

## Why This Stack?

### LangGraph vs LangChain Comparison

| Feature | LangChain | LangGraph | Use For |
|---------|-----------|-----------|---------|
| **Simple Q&A** | ✅ Perfect | ⚠️ Overkill | Research Notes |
| **Multi-step workflows** | ⚠️ Complex chains | ✅ Built-in | Literature Review |
| **Human-in-loop** | ❌ Manual | ✅ Native | Qualitative Coding |
| **Conditional logic** | ⚠️ RouterChain | ✅ Easy | All |
| **State persistence** | ❌ Limited | ✅ Checkpointing | Qualitative Coding |
| **Debugging** | ⚠️ Hard | ✅ Visual graph | All |
| **Learning curve** | Easy | Medium | - |

**Decision:**
- **Literature Review RAG**: LangGraph (complex multi-step retrieval)
- **Qualitative Coding RAG**: LangGraph (iterative, stateful workflow)
- **Research Notes RAG**: LangChain (simple conversational chain)

---

## Step-by-Step Implementation

### Phase 1: Setup Qdrant Cloud (5 minutes)

1. **Create Qdrant Cloud Account**
   - Go to https://cloud.qdrant.io
   - Sign up (free tier: 1GB storage)

2. **Create Cluster**
   - Click "Create Cluster"
   - Select region closest to you
   - Free tier is sufficient

3. **Get Credentials**
   ```
   Cluster URL: https://xyz-example.aws.cloud.qdrant.io
   API Key: your-api-key-here
   ```

4. **Create Collections (one per project type)**
   ```python
   from qdrant_client import QdrantClient
   from qdrant_client.models import Distance, VectorParams

   client = QdrantClient(url="YOUR_URL", api_key="YOUR_KEY")

   # Collection for Literature Review
   client.create_collection(
       collection_name="literature_review",
       vectors_config=VectorParams(size=768, distance=Distance.COSINE)
   )

   # Collection for Qualitative Coding
   client.create_collection(
       collection_name="qualitative_coding",
       vectors_config=VectorParams(size=768, distance=Distance.COSINE)
   )

   # Collection for Research Notes
   client.create_collection(
       collection_name="research_notes",
       vectors_config=VectorParams(size=768, distance=Distance.COSINE)
   )
   ```

---

### Phase 2: Create Hugging Face Space (10 minutes)

1. **Create New Space**
   - Go to https://huggingface.co/new-space
   - Name: `researcherrag`
   - License: MIT
   - SDK: Gradio
   - Hardware: CPU Basic (free)

2. **Add Secrets (Settings → Repository secrets)**
   ```
   QDRANT_URL=https://your-cluster.qdrant.io
   QDRANT_API_KEY=your-api-key
   ANTHROPIC_API_KEY=your-anthropic-key
   OPENAI_API_KEY=your-openai-key (optional)
   ```

3. **Project Structure**
   ```
   researcherrag/
   ├── app.py                        # Main Gradio app
   ├── requirements.txt
   ├── README.md
   ├── modules/
   │   ├── literature_review_graph.py    # LangGraph for lit review
   │   ├── qualitative_coding_graph.py   # LangGraph for coding
   │   ├── research_notes_chain.py       # LangChain for notes
   │   └── utils.py
   └── assets/
       └── logo.png
   ```

---

### Phase 3: Implement Literature Review RAG with LangGraph

**File: modules/literature_review_graph.py**

```python
"""
Literature Review RAG using LangGraph
Handles complex multi-step retrieval with query decomposition and reranking
"""

from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, END
from langchain_core.documents import Document
from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import Qdrant
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
import os

# Define workflow state
class LiteratureReviewState(TypedDict):
    """State for literature review workflow"""
    original_query: str
    decomposed_queries: List[str]
    retrieved_docs: List[Document]
    reranked_docs: List[Document]
    final_answer: str
    citations: List[dict]

# Initialize components
def get_vectorstore(collection_name: str = "literature_review"):
    """Get Qdrant vector store"""
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    return Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings
    )

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.3,
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
)

vectorstore = get_vectorstore()

# Node functions
def decompose_query(state: LiteratureReviewState) -> LiteratureReviewState:
    """
    Break complex query into simpler sub-queries
    Example: "Compare TAM and UTAUT" → ["TAM theory", "UTAUT theory", "TAM vs UTAUT comparison"]
    """
    query = state["original_query"]

    decomposition_prompt = f"""You are a research librarian helping to search academic literature.

Given this research question: "{query}"

Break it down into 2-4 simpler search queries that cover all aspects.

Return ONLY a JSON array of strings, nothing else.
Example: ["query 1", "query 2", "query 3"]
"""

    response = llm.invoke(decomposition_prompt)

    # Parse response (expecting JSON array)
    import json
    try:
        queries = json.loads(response.content)
    except:
        # Fallback: use original query
        queries = [query]

    state["decomposed_queries"] = queries
    return state

def retrieve_documents(state: LiteratureReviewState) -> LiteratureReviewState:
    """
    Retrieve documents for each sub-query
    """
    all_docs = []

    for query in state["decomposed_queries"]:
        docs = vectorstore.similarity_search(
            query,
            k=5,  # 5 per sub-query
            filter=None  # Can add metadata filters here
        )
        all_docs.extend(docs)

    # Remove duplicates (by document ID)
    seen_ids = set()
    unique_docs = []
    for doc in all_docs:
        doc_id = doc.metadata.get("source", "") + str(hash(doc.page_content[:100]))
        if doc_id not in seen_ids:
            seen_ids.add(doc_id)
            unique_docs.append(doc)

    state["retrieved_docs"] = unique_docs
    return state

def rerank_documents(state: LiteratureReviewState) -> LiteratureReviewState:
    """
    Rerank documents using LLM to assess relevance
    """
    original_query = state["original_query"]
    docs = state["retrieved_docs"]

    # Score each document
    scored_docs = []
    for doc in docs[:15]:  # Limit to top 15 for cost efficiency
        relevance_prompt = f"""You are assessing document relevance for academic research.

Research Question: "{original_query}"

Document Excerpt:
{doc.page_content[:500]}

Rate relevance from 0.0 (not relevant) to 1.0 (highly relevant).
Consider:
- Direct relevance to research question
- Quality of evidence
- Recency (prefer recent studies)

Return ONLY a number between 0.0 and 1.0, nothing else."""

        try:
            score_response = llm.invoke(relevance_prompt)
            score = float(score_response.content.strip())
        except:
            score = 0.5  # Default moderate relevance

        scored_docs.append((doc, score))

    # Sort by score and take top 5
    scored_docs.sort(key=lambda x: x[1], reverse=True)
    top_docs = [doc for doc, score in scored_docs[:5]]

    state["reranked_docs"] = top_docs
    return state

def synthesize_answer(state: LiteratureReviewState) -> LiteratureReviewState:
    """
    Generate final answer with citations
    """
    query = state["original_query"]
    docs = state["reranked_docs"]

    # Prepare context from documents
    context = "\n\n".join([
        f"[Document {i+1}] {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}"
        for i, doc in enumerate(docs)
    ])

    synthesis_prompt = f"""You are a research assistant helping to review academic literature.

Research Question: "{query}"

Relevant Documents:
{context}

Provide a comprehensive answer that:
1. Synthesizes information across all documents
2. Highlights key themes and findings
3. Notes areas of agreement or disagreement
4. Uses inline citations [1], [2], etc. referring to Document numbers
5. Is written for an academic audience

If documents don't fully answer the question, note gaps in the literature.

Answer:"""

    response = llm.invoke(synthesis_prompt)

    # Extract citations
    citations = [
        {
            "id": i+1,
            "source": doc.metadata.get("source", "Unknown"),
            "title": doc.metadata.get("title", "Untitled"),
            "excerpt": doc.page_content[:200] + "..."
        }
        for i, doc in enumerate(docs)
    ]

    state["final_answer"] = response.content
    state["citations"] = citations
    return state

# Build LangGraph
def create_literature_review_graph():
    """
    Create the complete workflow graph
    """
    workflow = StateGraph(LiteratureReviewState)

    # Add nodes
    workflow.add_node("decompose", decompose_query)
    workflow.add_node("retrieve", retrieve_documents)
    workflow.add_node("rerank", rerank_documents)
    workflow.add_node("synthesize", synthesize_answer)

    # Define edges (linear workflow)
    workflow.add_edge("decompose", "retrieve")
    workflow.add_edge("retrieve", "rerank")
    workflow.add_edge("rerank", "synthesize")
    workflow.add_edge("synthesize", END)

    # Set entry point
    workflow.set_entry_point("decompose")

    # Compile
    return workflow.compile()

# Convenience function
def query_literature_review(question: str) -> tuple[str, list]:
    """
    Query the literature review RAG system

    Args:
        question: Research question

    Returns:
        (answer, citations)
    """
    graph = create_literature_review_graph()

    result = graph.invoke({
        "original_query": question,
        "decomposed_queries": [],
        "retrieved_docs": [],
        "reranked_docs": [],
        "final_answer": "",
        "citations": []
    })

    return result["final_answer"], result["citations"]
```

---

### Phase 4: Implement Qualitative Coding RAG with LangGraph

**File: modules/qualitative_coding_graph.py**

```python
"""
Qualitative Coding RAG using LangGraph
Implements iterative coding with human-in-the-loop refinement
"""

from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_anthropic import ChatAnthropic
import os

# State definition
class CodingState(TypedDict):
    """State for qualitative coding workflow"""
    interview_texts: List[str]
    research_question: str
    current_codes: List[dict]  # [{"code": "name", "definition": "...", "count": 0}]
    coded_segments: List[dict]  # [{"text": "...", "codes": [...], "interview_id": "..."}]
    themes: List[dict]
    iteration: int
    max_iterations: int
    user_feedback: Optional[str]

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    temperature=0.3,
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
)

# Node functions
def generate_initial_codes(state: CodingState) -> CodingState:
    """
    Generate initial codes from interview data (inductive coding)
    """
    sample_texts = "\n\n".join(state["interview_texts"][:10])  # Sample first 10
    research_q = state["research_question"]

    prompt = f"""You are a qualitative researcher conducting thematic analysis.

Research Question: "{research_q}"

Interview Excerpts:
{sample_texts}

Generate 10-15 initial codes using a grounded theory approach.
Codes should:
- Be descriptive yet concise (2-4 words)
- Capture meaningful patterns, not just topics
- Be data-driven (emerge from the data)

For each code, provide:
- code_name: Short name
- definition: When to apply this code
- examples: 2-3 phrases from data

Return as JSON array:
[
  {{"code_name": "...", "definition": "...", "examples": ["...", "..."]}},
  ...
]

JSON array only, no explanation:"""

    response = llm.invoke(prompt)

    import json
    try:
        codes = json.loads(response.content)
        state["current_codes"] = codes
    except:
        state["current_codes"] = []

    state["iteration"] = 1
    return state

def apply_codes_to_data(state: CodingState) -> CodingState:
    """
    Apply current codes to all interview data
    """
    codes_json = json.dumps(state["current_codes"], indent=2)
    coded_segments = []

    for idx, text in enumerate(state["interview_texts"]):
        coding_prompt = f"""Apply these codes to the interview excerpt below.

Codes:
{codes_json}

Interview Excerpt:
{text}

For each meaningful segment (1-3 sentences), assign relevant codes.

Return JSON array:
[
  {{"segment": "text excerpt", "codes": ["code1", "code2"], "rationale": "why"}},
  ...
]

JSON only:"""

        response = llm.invoke(coding_prompt)

        try:
            segments = json.loads(response.content)
            for seg in segments:
                seg["interview_id"] = idx
            coded_segments.extend(segments)
        except:
            pass

    state["coded_segments"] = coded_segments
    return state

def identify_themes(state: CodingState) -> CodingState:
    """
    Organize codes into hierarchical themes
    """
    codes = state["current_codes"]
    codes_json = json.dumps(codes, indent=2)

    theme_prompt = f"""You are organizing qualitative codes into themes.

Codes:
{codes_json}

Identify 3-5 overarching themes that group related codes.

Return JSON:
{{
  "themes": [
    {{
      "theme_name": "...",
      "description": "...",
      "codes": ["code1", "code2", ...]
    }},
    ...
  ]
}}

JSON only:"""

    response = llm.invoke(theme_prompt)

    import json
    try:
        result = json.loads(response.content)
        state["themes"] = result["themes"]
    except:
        state["themes"] = []

    return state

def should_continue(state: CodingState) -> str:
    """
    Decide whether to continue refinement or finish
    """
    if state["iteration"] >= state["max_iterations"]:
        return "finish"
    elif state.get("user_feedback"):
        return "refine"
    else:
        return "finish"

# Build graph
def create_qualitative_coding_graph():
    """
    Create coding workflow with checkpointing
    """
    workflow = StateGraph(CodingState)

    # Add nodes
    workflow.add_node("initial_coding", generate_initial_codes)
    workflow.add_node("apply_codes", apply_codes_to_data)
    workflow.add_node("identify_themes", identify_themes)

    # Edges
    workflow.add_edge("initial_coding", "apply_codes")
    workflow.add_edge("apply_codes", "identify_themes")

    # Conditional edge (can loop back for refinement)
    workflow.add_conditional_edges(
        "identify_themes",
        should_continue,
        {
            "refine": "apply_codes",  # Loop back
            "finish": END
        }
    )

    workflow.set_entry_point("initial_coding")

    # Compile with memory (save progress)
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)

# Convenience function
def analyze_interviews(
    interview_texts: List[str],
    research_question: str,
    max_iterations: int = 2
) -> dict:
    """
    Analyze interviews with qualitative coding

    Args:
        interview_texts: List of interview transcripts
        research_question: Focus of analysis
        max_iterations: Number of refinement cycles

    Returns:
        Dictionary with codes, themes, coded segments
    """
    graph = create_qualitative_coding_graph()

    result = graph.invoke({
        "interview_texts": interview_texts,
        "research_question": research_question,
        "current_codes": [],
        "coded_segments": [],
        "themes": [],
        "iteration": 0,
        "max_iterations": max_iterations,
        "user_feedback": None
    })

    return {
        "codes": result["current_codes"],
        "themes": result["themes"],
        "coded_segments": result["coded_segments"]
    }
```

---

### Phase 5: Research Notes RAG (Simple LangChain)

**File: modules/research_notes_chain.py**

```python
"""
Research Notes RAG using simple LangChain ConversationalRetrievalChain
"""

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import Qdrant
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
import os

def create_research_notes_chain():
    """
    Create simple conversational RAG chain for research notes
    """
    # Setup vector store
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    vectorstore = Qdrant(
        client=client,
        collection_name="research_notes",
        embeddings=embeddings
    )

    # Setup LLM
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0.7,  # Higher for more creative connections
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    # Memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

    # Create chain
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(
            search_kwargs={"k": 5}
        ),
        memory=memory,
        return_source_documents=True,
        verbose=False
    )

    return chain

# Global chain instance
_notes_chain = None

def query_research_notes(question: str) -> tuple[str, list]:
    """
    Query research notes

    Args:
        question: User question

    Returns:
        (answer, source_documents)
    """
    global _notes_chain

    if _notes_chain is None:
        _notes_chain = create_research_notes_chain()

    result = _notes_chain({"question": question})

    return result["answer"], result["source_documents"]
```

---

### Phase 6: Main Gradio App

**File: app.py**

```python
"""
ResearcherRAG: AI-Powered Research Assistant
Main Gradio interface for Hugging Face Spaces
"""

import gradio as gr
import os
from modules.literature_review_graph import query_literature_review
from modules.qualitative_coding_graph import analyze_interviews
from modules.research_notes_chain import query_research_notes

# Custom CSS
custom_css = """
.gradio-container {
    font-family: 'Inter', sans-serif;
}
.citation-box {
    background-color: #f0f0f0;
    border-left: 4px solid #4CAF50;
    padding: 10px;
    margin: 10px 0;
}
"""

# Tab 1: Literature Review
def literature_review_tab():
    with gr.Tab("📚 Literature Review"):
        gr.Markdown("""
        ### Literature Review RAG
        Ask questions about your research corpus. The system will:
        1. Decompose complex questions
        2. Search across all papers
        3. Rerank results
        4. Synthesize answer with citations
        """)

        with gr.Row():
            with gr.Column():
                lit_question = gr.Textbox(
                    label="Research Question",
                    placeholder="e.g., What are the main barriers to AI adoption in K-12 education?",
                    lines=3
                )
                lit_submit = gr.Button("Search Literature", variant="primary")

            with gr.Column():
                lit_answer = gr.Textbox(
                    label="Synthesized Answer",
                    lines=15
                )
                lit_citations = gr.JSON(label="Citations & Sources")

        lit_submit.click(
            fn=query_literature_review,
            inputs=[lit_question],
            outputs=[lit_answer, lit_citations]
        )

# Tab 2: Qualitative Coding
def qualitative_coding_tab():
    with gr.Tab("🎤 Qualitative Coding"):
        gr.Markdown("""
        ### Qualitative Interview Analysis
        Upload interview transcripts for AI-assisted thematic coding.
        """)

        with gr.Row():
            with gr.Column():
                interview_files = gr.File(
                    label="Upload Interview Transcripts (.txt, .docx)",
                    file_count="multiple"
                )
                research_focus = gr.Textbox(
                    label="Research Question / Focus",
                    placeholder="e.g., Teachers' experiences with AI tools",
                    lines=2
                )
                code_btn = gr.Button("Analyze Interviews", variant="primary")

            with gr.Column():
                codes_output = gr.JSON(label="Generated Codes")
                themes_output = gr.JSON(label="Identified Themes")

        def process_interviews(files, focus):
            # Extract text from uploaded files
            texts = []
            for file in files:
                with open(file.name, 'r') as f:
                    texts.append(f.read())

            result = analyze_interviews(texts, focus)
            return result["codes"], result["themes"]

        code_btn.click(
            fn=process_interviews,
            inputs=[interview_files, research_focus],
            outputs=[codes_output, themes_output]
        )

# Tab 3: Research Notes
def research_notes_tab():
    with gr.Tab("📝 Research Notes"):
        gr.Markdown("""
        ### Personal Research Knowledge Base
        Chat with your research notes, ideas, and observations.
        """)

        chatbot = gr.Chatbot(height=400)
        msg = gr.Textbox(
            label="Ask a question",
            placeholder="e.g., What did I learn about mixed methods last month?"
        )
        clear = gr.Button("Clear Chat")

        def respond(message, chat_history):
            answer, sources = query_research_notes(message)
            chat_history.append((message, answer))
            return "", chat_history

        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        clear.click(lambda: None, None, chatbot, queue=False)

# Main app
with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🔬 ResearcherRAG: AI-Powered Research Assistant

    **Three specialized RAG systems for social science research:**
    - 📚 Literature Review: Synthesize findings across papers
    - 🎤 Qualitative Coding: Automated thematic analysis
    - 📝 Research Notes: Your personal knowledge base
    """)

    literature_review_tab()
    qualitative_coding_tab()
    research_notes_tab()

    gr.Markdown("""
    ---
    **Built with:** LangGraph, LangChain, Qdrant, Claude, HuggingFace

    [Documentation](https://github.com/your-username/ResearcherRAG) | [Report Issue](https://github.com/your-username/ResearcherRAG/issues)
    """)

# Launch
if __name__ == "__main__":
    demo.launch()
```

**requirements.txt:**
```txt
gradio==4.44.0
langchain==0.2.16
langchain-anthropic==0.1.23
langchain-community==0.2.16
langchain-huggingface==0.0.3
langgraph==0.2.28
qdrant-client==1.11.2
sentence-transformers==3.1.1
python-docx==1.1.2
pydantic==2.9.2
```

---

## Deployment

1. **Push to HuggingFace:**
   ```bash
   git clone https://huggingface.co/spaces/your-username/researcherrag
   cd researcherrag
   # Copy all files
   git add .
   git commit -m "Initial deployment"
   git push
   ```

2. **Set Secrets** in HF Space settings

3. **Access:** `https://huggingface.co/spaces/your-username/researcherrag`

---

## Summary

✅ **Literature Review**: LangGraph (multi-step retrieval)
✅ **Qualitative Coding**: LangGraph (iterative, stateful)
✅ **Research Notes**: LangChain (simple conversational)
✅ **Vector Store**: Qdrant Cloud (1GB free)
✅ **Deployment**: Hugging Face Spaces (easy sharing)

**Total Cost:** $0 for prototype (using free tiers)

**Production Cost (100 users):**
- Qdrant Cloud: $0 (1GB tier)
- Claude API: ~$50-100/month
- HF Spaces: $0 (or upgrade to $9/month for persistent storage)
