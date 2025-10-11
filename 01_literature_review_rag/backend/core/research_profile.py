"""
Research Profile Configuration System
======================================

Defines research domain, methodology, and topic keywords for PRISMA screening.
Profiles are stored as YAML files for easy customization.

Example Profile Structure:
    name: "HRM AI Bias Research"
    description: "AI bias and fairness in HR practices"

    domain_keywords:
      - "human resource management"
      - "employee selection"

    method_keywords:
      - "artificial intelligence"
      - "machine learning"

    topic_keywords:
      - "bias"
      - "fairness"

    exclusion_keywords:
      - "medical"
      - "clinical"

    context_validators:
      - "employee"
      - "workplace"

    thresholds:
      screening: 30
      eligibility: 50
      review: 40
      min_inclusion: 60
"""

from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field
import yaml
from pydantic import BaseModel, Field


class ResearchProfileConfig(BaseModel):
    """Pydantic model for research profile configuration."""

    name: str = Field(..., description="Profile name")
    description: str = Field(default="", description="Profile description")

    domain_keywords: List[str] = Field(
        default_factory=list,
        description="Domain/discipline keywords (e.g., HRM, education)"
    )

    method_keywords: List[str] = Field(
        default_factory=list,
        description="Methodology keywords (e.g., AI, machine learning)"
    )

    topic_keywords: List[str] = Field(
        default_factory=list,
        description="Research topic keywords (e.g., bias, ethics)"
    )

    exclusion_keywords: List[str] = Field(
        default_factory=list,
        description="Keywords that indicate irrelevant papers"
    )

    context_validators: List[str] = Field(
        default_factory=list,
        description="Keywords that validate domain context"
    )

    # Scoring thresholds
    screening_threshold: int = Field(
        default=30,
        ge=0,
        le=100,
        description="Minimum score to pass screening (Stage 2)"
    )

    eligibility_threshold: int = Field(
        default=50,
        ge=0,
        le=100,
        description="Minimum score for automatic inclusion (Stage 3)"
    )

    review_threshold: int = Field(
        default=40,
        ge=0,
        le=100,
        description="Minimum score to enter manual review queue"
    )

    min_inclusion_score: int = Field(
        default=60,
        ge=0,
        le=100,
        description="Minimum score for final inclusion (Stage 4)"
    )


@dataclass
class ResearchProfile:
    """
    Research profile for PRISMA screening.

    Provides keyword lists and thresholds for literature filtering.
    """

    name: str
    description: str = ""

    domain_keywords: List[str] = field(default_factory=list)
    method_keywords: List[str] = field(default_factory=list)
    topic_keywords: List[str] = field(default_factory=list)
    exclusion_keywords: List[str] = field(default_factory=list)
    context_validators: List[str] = field(default_factory=list)

    screening_threshold: int = 30
    eligibility_threshold: int = 50
    review_threshold: int = 40
    min_inclusion_score: int = 60

    @classmethod
    def from_yaml(cls, filepath: str) -> 'ResearchProfile':
        """
        Load research profile from YAML file.

        Args:
            filepath: Path to YAML configuration file

        Returns:
            ResearchProfile instance

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If YAML is invalid
        """
        path = Path(filepath)

        if not path.exists():
            raise FileNotFoundError(f"Profile not found: {filepath}")

        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        # Validate with Pydantic
        config = ResearchProfileConfig(**data)

        # Convert to dataclass
        return cls(
            name=config.name,
            description=config.description,
            domain_keywords=config.domain_keywords,
            method_keywords=config.method_keywords,
            topic_keywords=config.topic_keywords,
            exclusion_keywords=config.exclusion_keywords,
            context_validators=config.context_validators,
            screening_threshold=config.screening_threshold,
            eligibility_threshold=config.eligibility_threshold,
            review_threshold=config.review_threshold,
            min_inclusion_score=config.min_inclusion_score
        )

    def to_yaml(self, filepath: str) -> None:
        """
        Save research profile to YAML file.

        Args:
            filepath: Path to save YAML file
        """
        data = {
            'name': self.name,
            'description': self.description,
            'domain_keywords': self.domain_keywords,
            'method_keywords': self.method_keywords,
            'topic_keywords': self.topic_keywords,
            'exclusion_keywords': self.exclusion_keywords,
            'context_validators': self.context_validators,
            'thresholds': {
                'screening': self.screening_threshold,
                'eligibility': self.eligibility_threshold,
                'review': self.review_threshold,
                'min_inclusion': self.min_inclusion_score
            }
        }

        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    @classmethod
    def create_default(cls) -> 'ResearchProfile':
        """
        Create a default research profile for general literature review.

        Returns:
            ResearchProfile with generic keywords
        """
        return cls(
            name="General Research",
            description="Default profile for general academic research",
            domain_keywords=[
                "research", "study", "investigation", "analysis",
                "experiment", "survey", "case study"
            ],
            method_keywords=[
                "quantitative", "qualitative", "mixed methods",
                "statistical analysis", "regression", "correlation",
                "content analysis", "thematic analysis"
            ],
            topic_keywords=[
                "finding", "result", "outcome", "effect",
                "relationship", "association", "impact"
            ],
            exclusion_keywords=[
                "review article", "editorial", "commentary",
                "book review", "conference abstract"
            ],
            context_validators=[
                "participant", "sample", "data", "measure",
                "instrument", "variable", "hypothesis"
            ],
            screening_threshold=25,
            eligibility_threshold=45,
            review_threshold=35,
            min_inclusion_score=50
        )


# Pre-defined profiles for common research domains
HRM_AI_BIAS_PROFILE = ResearchProfile(
    name="HRM AI Bias Research",
    description="AI bias and fairness in human resource management",
    domain_keywords=[
        "human resource management", "HRM", "employee selection",
        "recruitment", "hiring", "talent acquisition",
        "performance appraisal", "performance management",
        "people analytics", "HR analytics", "workforce analytics"
    ],
    method_keywords=[
        "artificial intelligence", "AI", "machine learning", "ML",
        "algorithm", "automated decision", "predictive analytics",
        "natural language processing", "NLP", "computer vision"
    ],
    topic_keywords=[
        "bias", "fairness", "discrimination", "disparate impact",
        "ethics", "transparency", "accountability", "explainability",
        "privacy", "data protection", "algorithmic bias"
    ],
    exclusion_keywords=[
        "alzheimer", "dementia", "cancer", "clinical trial",
        "patient care", "medical imaging", "disease diagnosis",
        "federated learning", "edge computing", "IoT sensor"
    ],
    context_validators=[
        "employee", "worker", "candidate", "applicant",
        "workplace", "organization", "company", "employer",
        "job seeker", "personnel", "staff"
    ],
    screening_threshold=30,
    eligibility_threshold=55,
    review_threshold=45,
    min_inclusion_score=60
)


EDUCATION_TECH_PROFILE = ResearchProfile(
    name="Educational Technology Research",
    description="Technology adoption and effectiveness in education",
    domain_keywords=[
        "education", "learning", "teaching", "pedagogy",
        "classroom", "school", "university", "K-12",
        "higher education", "student", "teacher", "instructor"
    ],
    method_keywords=[
        "technology", "digital tool", "learning management system",
        "LMS", "educational technology", "edtech", "e-learning",
        "online learning", "blended learning", "flipped classroom"
    ],
    topic_keywords=[
        "adoption", "acceptance", "effectiveness", "achievement",
        "engagement", "motivation", "self-efficacy", "attitude",
        "perceived usefulness", "ease of use", "TAM", "UTAUT"
    ],
    exclusion_keywords=[
        "medical education", "clinical training", "surgery",
        "radiology training", "anatomical education"
    ],
    context_validators=[
        "student", "teacher", "learner", "instructor",
        "classroom", "course", "curriculum", "lesson"
    ],
    screening_threshold=30,
    eligibility_threshold=50,
    review_threshold=40,
    min_inclusion_score=55
)


def get_profile(profile_name: str) -> Optional[ResearchProfile]:
    """
    Get predefined research profile by name.

    Args:
        profile_name: Name of profile ("hrm_ai_bias", "education_tech", "default")

    Returns:
        ResearchProfile instance or None if not found
    """
    profiles = {
        "hrm_ai_bias": HRM_AI_BIAS_PROFILE,
        "education_tech": EDUCATION_TECH_PROFILE,
        "default": ResearchProfile.create_default()
    }

    return profiles.get(profile_name.lower())
