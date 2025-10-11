"""Conversation and synthesis chains for Research Notes RAG."""
from __future__ import annotations

import logging
from typing import List, Tuple

from langchain.schema import Document
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from .config import settings
from .prompts import FOLLOW_UP_PROMPT, SUMMARY_PROMPT, SYSTEM_PROMPT

logger = logging.getLogger(__name__)


def _get_llm():
    if settings.llm_provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            anthropic_api_key=settings.anthropic_api_key,
        )

    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=settings.llm_model,
        temperature=settings.llm_temperature,
        openai_api_key=settings.openai_api_key,
    )


def format_context(documents: List[Document]) -> str:
    """Join retrieved documents into a readable context block."""
    formatted = []
    for index, doc in enumerate(documents, start=1):
        title = doc.metadata.get("title", f"Note {index}")
        highlights = doc.metadata.get("highlights")
        highlight_text = ""
        if highlights:
            highlight_text = f"\nHighlights: {highlights}"

        formatted.append(
            f"[Source {index}: {title}]\n"
            f"Metadata: note_type={doc.metadata.get('note_type')}, tags={doc.metadata.get('tags')}\n"
            f"Content:\n{doc.page_content.strip()}" + highlight_text
        )
    return "\n\n---\n\n".join(formatted)


def ask_research_notes(question: str, documents: List[Document], history: List[Tuple[str, str]]) -> str:
    """Generate an answer grounded in the retrieved documents and chat history."""
    llm = _get_llm()
    context_block = format_context(documents)

    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    if history:
        messages.append(
            AIMessage(
                content=(
                    "Previous discussion summary:\n" +
                    "\n".join(
                        f"Q: {human}\nA: {ai}" for human, ai in history[-3:]
                    )
                )
            )
        )
        messages.append(HumanMessage(content=FOLLOW_UP_PROMPT))

    prompt = (
        f"{SUMMARY_PROMPT}\n\n"
        f"User Question: {question}\n\n"
        f"Available Notes:\n{context_block}"
    )
    messages.append(HumanMessage(content=prompt))

    try:
        response = llm.invoke(messages)
    except Exception as exc:  # pragma: no cover - protects runtime without keys
        logger.error("LLM invocation failed: %s", exc)
        return (
            "LLM invocation failed. Verify that your API keys are set and the "
            "model name is correct."
        )

    return response.content if hasattr(response, "content") else str(response)
