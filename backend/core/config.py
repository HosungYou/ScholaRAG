"""
Configuration management for Literature Review RAG
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Literal
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # API Keys
    anthropic_api_key: str = Field(default="", env="ANTHROPIC_API_KEY")
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")

    # Model Configuration
    embedding_model: str = Field(
        default="sentence-transformers/all-mpnet-base-v2",
        env="EMBEDDING_MODEL"
    )

    llm_model: str = Field(
        default="claude-3-5-sonnet-20241022",
        env="LLM_MODEL"
    )

    llm_provider: Literal["anthropic", "openai"] = Field(
        default="anthropic",
        env="LLM_PROVIDER"
    )

    llm_temperature: float = Field(default=0.3, env="LLM_TEMPERATURE")

    # Vector Database
    vector_db_type: Literal["chroma", "qdrant"] = Field(
        default="chroma",
        env="VECTOR_DB_TYPE"
    )

    chroma_db_path: str = Field(
        default="./data/vector_db",
        env="CHROMA_DB_PATH"
    )

    qdrant_url: str = Field(default="", env="QDRANT_URL")
    qdrant_api_key: str = Field(default="", env="QDRANT_API_KEY")

    # Processing Configuration
    chunk_size: int = Field(default=1000, env="CHUNK_SIZE")
    chunk_overlap: int = Field(default=200, env="CHUNK_OVERLAP")
    top_k_results: int = Field(default=5, env="TOP_K_RESULTS")

    # Paths
    raw_pdfs_path: str = Field(default="./data/raw_pdfs", env="RAW_PDFS_PATH")
    processed_data_path: str = Field(default="./data/processed", env="PROCESSED_DATA_PATH")

    # API Server
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")

    # Gradio Settings
    gradio_server_name: str = Field(default="0.0.0.0", env="GRADIO_SERVER_NAME")
    gradio_server_port: int = Field(default=7860, env="GRADIO_SERVER_PORT")
    gradio_share: bool = Field(default=False, env="GRADIO_SHARE")

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"

    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        dirs = [
            self.chroma_db_path,
            self.raw_pdfs_path,
            self.processed_data_path
        ]
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)

    def validate_api_keys(self):
        """Validate that required API keys are present"""
        if self.llm_provider == "anthropic" and not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is required when using Anthropic as LLM provider")
        if self.llm_provider == "openai" and not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when using OpenAI as LLM provider")


# Global settings instance
settings = Settings()

# Ensure directories exist on import
settings.ensure_directories()
