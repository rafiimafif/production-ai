"""
Application configuration loaded from environment variables.

Uses pydantic-settings to validate and type-check all config values at startup.
If a required variable is missing or malformed, the app will fail fast with a
clear error message rather than crashing at runtime.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for the Production AI system."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # -- Ollama ---------------------------------------------------------------
    ollama_host: str = "http://localhost:11434"
    default_model: str = "qwen2.5:7b"

    # -- ChromaDB -------------------------------------------------------------
    chroma_persist_dir: str = "./data/chroma_db"

    # -- Database -------------------------------------------------------------
    database_url: str = "sqlite:///./data/app.db"
    duckdb_path: str = "./data/analytics.duckdb"

    # -- Langfuse (Observability) ---------------------------------------------
    langfuse_secret_key: str = ""
    langfuse_public_key: str = ""
    langfuse_host: str = "http://localhost:3100"

    # -- Application ----------------------------------------------------------
    app_env: str = "development"
    log_level: str = "INFO"
    frontend_url: str = "http://localhost:3000"


# Singleton — import this from anywhere in the codebase.
settings = Settings()
