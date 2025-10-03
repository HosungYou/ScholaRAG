"""
LangGraph-based RAG workflow for Literature Review
Multi-step: Query Decomposition → Retrieval → Reranking → Synthesis
"""
from typing import TypedDict, List, Annotated
import json
import logging

from langgraph.graph import StateGraph, END
from langchain.schema import Document
from langchain_anthropic import ChatAnthropic

from .config import settings
from .retrieval import get_retriever

logger = logging.getLogger(__name__)


# Define workflow state
class LiteratureReviewState(TypedDict):
    """State for literature review workflow"""
    original_query: str
    decomposed_queries: List[str]
    retrieved_docs: List[Document]
    reranked_docs: List[Document]
    final_answer: str
    citations: List[dict]
    error: str


# Initialize LLM
def get_llm():
    """Get configured LLM"""
    if settings.llm_provider == "anthropic":
        return ChatAnthropic(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            anthropic_api_key=settings.anthropic_api_key
        )
    else:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            openai_api_key=settings.openai_api_key
        )


# Node functions
def decompose_query(state: LiteratureReviewState) -> LiteratureReviewState:
    """
    Break complex query into simpler sub-queries
    Example: "Compare TAM and UTAUT" → ["TAM theory", "UTAUT theory", "TAM vs UTAUT comparison"]
    """
    query = state["original_query"]
    logger.info(f"Decomposing query: {query}")

    llm = get_llm()

    decomposition_prompt = f"""You are a research librarian helping to search academic literature.

Given this research question: "{query}"

Break it down into 2-4 simpler search queries that cover all aspects. These queries will be used to search a literature database.

Requirements:
- Each query should be focused and specific
- Cover all aspects of the original question
- Use terminology that would appear in academic papers

Return ONLY a JSON array of strings, nothing else.
Example format: ["query 1", "query 2", "query 3"]

JSON array:"""

    try:
        response = llm.invoke(decomposition_prompt)
        content = response.content.strip()

        # Try to extract JSON array
        if content.startswith("```"):
            # Remove code block markers
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()

        queries = json.loads(content)

        if not isinstance(queries, list) or len(queries) == 0:
            logger.warning("Invalid query decomposition, using original query")
            queries = [query]

    except Exception as e:
        logger.warning(f"Query decomposition failed: {e}. Using original query.")
        queries = [query]

    state["decomposed_queries"] = queries
    logger.info(f"Decomposed into {len(queries)} queries: {queries}")

    return state


def retrieve_documents(state: LiteratureReviewState) -> LiteratureReviewState:
    """Retrieve documents for each sub-query"""
    logger.info("Retrieving documents...")

    retriever = get_retriever()
    all_docs = []

    for query in state["decomposed_queries"]:
        logger.info(f"  Searching: {query}")
        docs = retriever.search(query, k=5)
        all_docs.extend(docs)

    # Remove duplicates (by content hash)
    seen_content = set()
    unique_docs = []

    for doc in all_docs:
        content_hash = hash(doc.page_content[:200])
        if content_hash not in seen_content:
            seen_content.add(content_hash)
            unique_docs.append(doc)

    state["retrieved_docs"] = unique_docs
    logger.info(f"Retrieved {len(unique_docs)} unique documents")

    return state


def rerank_documents(state: LiteratureReviewState) -> LiteratureReviewState:
    """Rerank documents using LLM to assess relevance"""
    original_query = state["original_query"]
    docs = state["retrieved_docs"]

    logger.info(f"Reranking {len(docs)} documents...")

    if len(docs) == 0:
        state["reranked_docs"] = []
        return state

    llm = get_llm()

    # Score each document (limit to top 10 for cost efficiency)
    scored_docs = []
    for i, doc in enumerate(docs[:10]):
        relevance_prompt = f"""You are assessing document relevance for academic research.

Research Question: "{original_query}"

Document Excerpt (first 400 characters):
{doc.page_content[:400]}

Rate relevance from 0.0 (not relevant) to 1.0 (highly relevant).

Consider:
- Direct relevance to research question
- Quality and specificity of content
- Academic rigor

Return ONLY a number between 0.0 and 1.0, nothing else.

Score:"""

        try:
            score_response = llm.invoke(relevance_prompt)
            score_text = score_response.content.strip()

            # Extract number
            import re
            match = re.search(r'(0\.\d+|1\.0|0|1)', score_text)
            if match:
                score = float(match.group(1))
            else:
                score = 0.5  # Default moderate relevance

        except Exception as e:
            logger.warning(f"Reranking failed for doc {i}: {e}")
            score = 0.5  # Default

        scored_docs.append((doc, score))
        logger.debug(f"  Doc {i+1}: score {score:.2f}")

    # Sort by score and take top 5
    scored_docs.sort(key=lambda x: x[1], reverse=True)
    top_docs = [doc for doc, score in scored_docs[:5]]

    state["reranked_docs"] = top_docs
    logger.info(f"Reranked to top {len(top_docs)} documents")

    return state


def synthesize_answer(state: LiteratureReviewState) -> LiteratureReviewState:
    """Generate final answer with citations"""
    query = state["original_query"]
    docs = state["reranked_docs"]

    logger.info("Synthesizing answer...")

    if len(docs) == 0:
        state["final_answer"] = "No relevant documents found to answer this question. Please try uploading more papers or rephrasing your question."
        state["citations"] = []
        return state

    llm = get_llm()

    # Prepare context from documents
    context = "\n\n---\n\n".join([
        f"[Document {i+1}]\n"
        f"Source: {doc.metadata.get('title', 'Unknown')} ({doc.metadata.get('year', 'N/A')})\n"
        f"Content:\n{doc.page_content[:800]}"
        for i, doc in enumerate(docs)
    ])

    synthesis_prompt = f"""You are a research assistant helping to synthesize academic literature.

Research Question: "{query}"

Relevant Documents:
{context}

Provide a comprehensive answer that:
1. Synthesizes information across all documents
2. Highlights key themes and findings
3. Notes areas of agreement or disagreement between sources
4. Uses inline citations like [1], [2], etc. referring to Document numbers
5. Is written for an academic audience (clear but scholarly)
6. If documents don't fully answer the question, acknowledge gaps

Important: Base your answer ONLY on the provided documents. Do not add information from your training data.

Answer:"""

    try:
        response = llm.invoke(synthesis_prompt)
        answer = response.content

        # Extract citations
        citations = []
        for i, doc in enumerate(docs):
            citation = {
                "id": i + 1,
                "title": doc.metadata.get("title", "Untitled"),
                "year": doc.metadata.get("year", "N/A"),
                "filename": doc.metadata.get("filename", "Unknown"),
                "excerpt": doc.page_content[:300] + "..."
            }
            citations.append(citation)

        state["final_answer"] = answer
        state["citations"] = citations

        logger.info("Answer synthesized successfully")

    except Exception as e:
        logger.error(f"Synthesis failed: {e}")
        state["final_answer"] = f"Error generating answer: {str(e)}"
        state["citations"] = []
        state["error"] = str(e)

    return state


# Build LangGraph workflow
def create_literature_review_graph():
    """Create the complete workflow graph"""
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
def query_literature_review(question: str) -> tuple:
    """
    Query the literature review RAG system

    Args:
        question: Research question

    Returns:
        (answer, citations) tuple
    """
    logger.info(f"Processing query: {question}")

    graph = create_literature_review_graph()

    try:
        result = graph.invoke({
            "original_query": question,
            "decomposed_queries": [],
            "retrieved_docs": [],
            "reranked_docs": [],
            "final_answer": "",
            "citations": [],
            "error": ""
        })

        return result["final_answer"], result["citations"]

    except Exception as e:
        logger.error(f"Query failed: {e}")
        return f"Error processing query: {str(e)}", []
