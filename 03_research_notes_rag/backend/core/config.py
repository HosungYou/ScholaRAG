"""Configuration management for Research Notes RAG."""
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    anthropic_api_key: str = Field(default="", env="ANTHROPIC_API_KEY")
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")

    embedding_model: str = Field(
        default="sentence-transformers/all-mpnet-base-v2",
        env="NOTES_EMBEDDING_MODEL"
    )

    llm_model: str = Field(
        default="claude-3-5-sonnet-20241022",
        env="NOTES_LLM_MODEL"
    )

    llm_provider: Literal["anthropic", "openai"] = Field(
        default="anthropic",
        env="NOTES_LLM_PROVIDER"
    )

    llm_temperature: float = Field(default=0.2, env="NOTES_LLM_TEMPERATURE")

    vector_db_path: str = Field(
        default="./data/vector_db",
        env="NOTES_VECTOR_DB_PATH"
    )

    notes_root: str = Field(
        default="./data/notes",
        env="NOTES_ROOT_PATH"
    )

    chunk_size: int = Field(default=800, env="NOTES_CHUNK_SIZE")
    chunk_overlap: int = Field(default=150, env="NOTES_CHUNK_OVERLAP")

    top_k: int = Field(default=4, env="NOTES_TOP_K")

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"

    def ensure_directories(self) -> None:
        """Create directories that must exist for the module."""
        for path in (self.vector_db_path, self.notes_root):
            Path(path).mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_directories()
