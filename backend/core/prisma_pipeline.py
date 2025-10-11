"""
PRISMA-Compliant Literature Review Screening Pipeline
======================================================

Systematic screening protocol following PRISMA 2020 guidelines.
Adapted from AI failure_HR project for general literature review use.

Stages:
1. Identification: Metadata extraction and deduplication
2. Screening: Keyword-based relevance scoring (title/abstract)
3. Eligibility: Full-text context validation
4. Inclusion: Final decision with quality threshold

Usage:
    from backend.core.prisma_pipeline import LiteratureReviewPRISMA
    from backend.core.research_profile import ResearchProfile

    profile = ResearchProfile.from_yaml("config/research_profiles/default.yaml")
    prisma = LiteratureReviewPRISMA(profile)
    result = prisma.run_full_pipeline(documents)
"""

import logging
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import re

from langchain.schema import Document

from .config import settings

logger = logging.getLogger(__name__)


@dataclass
class IdentificationResult:
    """Stage 1: Identification results"""
    original_count: int
    unique_count: int
    duplicates_removed: int
    duplicate_dois: List[str] = field(default_factory=list)
    duplicate_titles: List[str] = field(default_factory=list)
    documents: List[Document] = field(default_factory=list)


@dataclass
class ScreeningResult:
    """Stage 2: Screening results"""
    input_count: int
    passed_count: int
    excluded_count: int
    exclusion_reasons: Dict[str, int] = field(default_factory=dict)
    documents: List[Document] = field(default_factory=list)
    excluded_documents: List[Document] = field(default_factory=list)


@dataclass
class EligibilityResult:
    """Stage 3: Eligibility results"""
    input_count: int
    passed_count: int
    excluded_count: int
    documents: List[Document] = field(default_factory=list)
    review_queue: List[Document] = field(default_factory=list)


@dataclass
class InclusionResult:
    """Stage 4: Inclusion results"""
    included_count: int
    review_queue_count: int
    total_excluded: int
    documents: List[Document] = field(default_factory=list)
    review_queue: List[Document] = field(default_factory=list)


@dataclass
class PRISMAResult:
    """Complete PRISMA pipeline results"""
    stage1: IdentificationResult
    stage2: ScreeningResult
    stage3: EligibilityResult
    stage4: InclusionResult
    timestamp: datetime = field(default_factory=datetime.now)


class LiteratureReviewPRISMA:
    """
    PRISMA screening pipeline for literature review.

    Customizable through ResearchProfile for different research domains.
    """

    def __init__(self, research_profile: 'ResearchProfile'):
        """
        Initialize PRISMA pipeline with research profile.

        Args:
            research_profile: Configuration with keywords and thresholds
        """
        self.profile = research_profile

    def run_full_pipeline(self, documents: List[Document]) -> PRISMAResult:
        """
        Execute complete PRISMA screening pipeline.

        Args:
            documents: List of ingested documents

        Returns:
            PRISMAResult with all stage results
        """
        logger.info(f"Starting PRISMA pipeline with {len(documents)} documents")

        # Stage 1: Identification
        stage1 = self.stage1_identification(documents)
        logger.info(f"Stage 1: {stage1.unique_count} unique documents "
                   f"({stage1.duplicates_removed} duplicates removed)")

        # Stage 2: Screening
        stage2 = self.stage2_screening(stage1.documents)
        logger.info(f"Stage 2: {stage2.passed_count} passed screening "
                   f"({stage2.excluded_count} excluded)")

        # Stage 3: Eligibility
        stage3 = self.stage3_eligibility(stage2.documents)
        logger.info(f"Stage 3: {stage3.passed_count} eligible "
                   f"({stage3.excluded_count} excluded)")

        # Stage 4: Inclusion
        stage4 = self.stage4_inclusion(stage3.documents, stage3.review_queue)
        logger.info(f"Stage 4: {stage4.included_count} included, "
                   f"{stage4.review_queue_count} need manual review")

        return PRISMAResult(
            stage1=stage1,
            stage2=stage2,
            stage3=stage3,
            stage4=stage4
        )

    def stage1_identification(self, documents: List[Document]) -> IdentificationResult:
        """
        Stage 1: Identify and deduplicate documents.

        Deduplication strategy:
        1. DOI-based exact match
        2. Title normalization and exact match
        """
        original_count = len(documents)

        # Track seen DOIs and titles
        seen_dois: Set[str] = set()
        seen_titles: Set[str] = set()
        duplicate_dois: List[str] = []
        duplicate_titles: List[str] = []
        unique_docs: List[Document] = []

        for doc in documents:
            # Check DOI
            doi = doc.metadata.get('doi', '').strip().lower()
            if doi:
                if doi in seen_dois:
                    duplicate_dois.append(doi)
                    continue
                seen_dois.add(doi)

            # Check title
            title = doc.metadata.get('title', '').strip().lower()
            title_normalized = self._normalize_title(title)

            if title_normalized and title_normalized in seen_titles:
                duplicate_titles.append(title)
                continue

            if title_normalized:
                seen_titles.add(title_normalized)

            unique_docs.append(doc)

        duplicates_removed = original_count - len(unique_docs)

        return IdentificationResult(
            original_count=original_count,
            unique_count=len(unique_docs),
            duplicates_removed=duplicates_removed,
            duplicate_dois=duplicate_dois,
            duplicate_titles=duplicate_titles,
            documents=unique_docs
        )

    def stage2_screening(self, documents: List[Document]) -> ScreeningResult:
        """
        Stage 2: Screen based on title/abstract relevance.

        Scoring:
        - Domain keywords: 0-30 points
        - Method keywords: 0-20 points
        - Topic keywords: 0-20 points
        - Exclusion penalty: -30 points
        - Title bonus: +10 points
        """
        input_count = len(documents)
        passed_docs: List[Document] = []
        excluded_docs: List[Document] = []
        exclusion_reasons: Dict[str, int] = {}

        for doc in documents:
            score_breakdown = self.calculate_relevance_score(doc)

            # Add score to metadata
            doc.metadata['prisma_score'] = score_breakdown['total_score']
            doc.metadata['score_breakdown'] = score_breakdown

            # Check if passed screening threshold
            if score_breakdown['total_score'] >= self.profile.screening_threshold:
                passed_docs.append(doc)
            else:
                excluded_docs.append(doc)

                # Track exclusion reason
                if score_breakdown['exclusion_penalty'] < 0:
                    reason = "Exclusion keywords present"
                elif score_breakdown['domain_score'] < 5:
                    reason = "Low domain relevance"
                elif score_breakdown['method_score'] < 5:
                    reason = "Missing methodology keywords"
                else:
                    reason = "Below threshold"

                exclusion_reasons[reason] = exclusion_reasons.get(reason, 0) + 1

        return ScreeningResult(
            input_count=input_count,
            passed_count=len(passed_docs),
            excluded_count=len(excluded_docs),
            exclusion_reasons=exclusion_reasons,
            documents=passed_docs,
            excluded_documents=excluded_docs
        )

    def stage3_eligibility(self, documents: List[Document]) -> EligibilityResult:
        """
        Stage 3: Assess eligibility with context validation.

        Validates that domain keywords appear in meaningful context.
        """
        input_count = len(documents)
        passed_docs: List[Document] = []
        review_queue: List[Document] = []

        for doc in documents:
            context_score = self._calculate_context_score(doc)
            doc.metadata['context_score'] = context_score

            # Update total score with context
            total_score = doc.metadata.get('prisma_score', 0)
            total_score += context_score
            doc.metadata['prisma_score'] = total_score

            # Check eligibility threshold
            if total_score >= self.profile.eligibility_threshold:
                passed_docs.append(doc)
            elif total_score >= self.profile.review_threshold:
                review_queue.append(doc)

        excluded_count = input_count - len(passed_docs) - len(review_queue)

        return EligibilityResult(
            input_count=input_count,
            passed_count=len(passed_docs),
            excluded_count=excluded_count,
            documents=passed_docs,
            review_queue=review_queue
        )

    def stage4_inclusion(
        self,
        documents: List[Document],
        review_queue: List[Document]
    ) -> InclusionResult:
        """
        Stage 4: Final inclusion decision.

        Documents passing eligibility are included.
        Review queue items need manual review.
        """
        return InclusionResult(
            included_count=len(documents),
            review_queue_count=len(review_queue),
            total_excluded=0,  # Calculated from previous stages
            documents=documents,
            review_queue=review_queue
        )

    def calculate_relevance_score(self, doc: Document) -> Dict[str, float]:
        """
        Calculate multi-dimensional relevance score.

        Returns:
            {
                'domain_score': 0-30,
                'method_score': 0-20,
                'topic_score': 0-20,
                'context_score': 0-20,
                'quality_score': 0-10,
                'exclusion_penalty': 0 or -30,
                'title_bonus': 0 or +10,
                'total_score': sum
            }
        """
        title = doc.metadata.get('title', '').lower()
        abstract = doc.metadata.get('abstract', '').lower()
        text = f"{title} {abstract}"

        # Domain score (0-30)
        domain_matches = sum(
            1 for kw in self.profile.domain_keywords
            if kw.lower() in text
        )
        domain_score = min(domain_matches * 3, 30)

        # Method score (0-20)
        method_matches = sum(
            1 for kw in self.profile.method_keywords
            if kw.lower() in text
        )
        method_score = min(method_matches * 4, 20)

        # Topic score (0-20)
        topic_matches = sum(
            1 for kw in self.profile.topic_keywords
            if kw.lower() in text
        )
        topic_score = min(topic_matches * 4, 20)

        # Exclusion penalty
        exclusion_matches = sum(
            1 for kw in self.profile.exclusion_keywords
            if kw.lower() in text
        )
        exclusion_penalty = -30 if exclusion_matches >= 2 else 0

        # Title bonus
        title_has_domain = any(
            kw.lower() in title
            for kw in self.profile.domain_keywords
        )
        title_bonus = 10 if title_has_domain else 0

        total_score = (
            domain_score + method_score + topic_score +
            exclusion_penalty + title_bonus
        )

        return {
            'domain_score': domain_score,
            'method_score': method_score,
            'topic_score': topic_score,
            'context_score': 0,  # Calculated in stage 3
            'quality_score': 0,  # Future: journal impact, citation count
            'exclusion_penalty': exclusion_penalty,
            'title_bonus': title_bonus,
            'total_score': total_score
        }

    def _calculate_context_score(self, doc: Document) -> float:
        """
        Validate that keywords appear in meaningful context.

        Returns score 0-20 based on context validator presence.
        """
        text = f"{doc.metadata.get('title', '')} {doc.metadata.get('abstract', '')}".lower()

        context_matches = sum(
            1 for kw in self.profile.context_validators
            if kw.lower() in text
        )

        return min(context_matches * 2, 20)

    @staticmethod
    def _normalize_title(title: str) -> str:
        """Normalize title for duplicate detection."""
        # Remove punctuation and extra spaces
        normalized = re.sub(r'[^\w\s]', '', title.lower())
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        return normalized

    def generate_prisma_flow_mermaid(self, result: PRISMAResult) -> str:
        """
        Generate Mermaid diagram for PRISMA flow.

        Returns:
            Mermaid markdown string
        """
        mermaid = f"""
```mermaid
graph TD
    A[Identification<br/>{result.stage1.original_count} papers uploaded]
    B[After Deduplication<br/>{result.stage1.unique_count} unique papers]
    C[Screening<br/>{result.stage2.passed_count} passed]
    D[Eligibility<br/>{result.stage3.passed_count} eligible]
    E[Included<br/>{result.stage4.included_count} papers]
    F[Manual Review<br/>{result.stage4.review_queue_count} papers]

    A -->|{result.stage1.duplicates_removed} duplicates removed| B
    B --> C
    C -->|{result.stage2.excluded_count} excluded| X1[Excluded:<br/>Low relevance]
    C --> D
    D -->|{result.stage3.excluded_count} excluded| X2[Excluded:<br/>Low context]
    D --> E
    D --> F

    style E fill:#90EE90
    style F fill:#FFD700
    style X1 fill:#FFB6C6
    style X2 fill:#FFB6C6
```
"""
        return mermaid
