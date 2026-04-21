"""
Configuration module for the AI-powered coding assistant.
Loads environment variables with defaults and validation.
"""

import os
from typing import Optional


class Config:
    """Central configuration class using environment variables."""

    # AI Model Configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    PRIMARY_MODEL: str = os.getenv("PRIMARY_MODEL", "codellama")
    FALLBACK_MODEL: str = os.getenv("FALLBACK_MODEL", "llama3.2")

    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "ai_assistant.log")

    # File Handling
    BACKUP_SUFFIX: str = os.getenv("BACKUP_SUFFIX", ".bak")

    # Git Configuration
    GIT_REMOTE: str = os.getenv("GIT_REMOTE", "origin")
    GIT_BRANCH: str = os.getenv("GIT_BRANCH", "main")

    # Performance
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "false").lower() == "true"
    CACHE_DIR: str = os.getenv("CACHE_DIR", ".ai_cache")

    @classmethod
    def validate(cls) -> None:
        """Validate configuration values."""
        if not cls.OLLAMA_BASE_URL.startswith("http"):
            raise ValueError("OLLAMA_BASE_URL must be a valid HTTP URL")

        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if cls.LOG_LEVEL.upper() not in valid_log_levels:
            raise ValueError(f"LOG_LEVEL must be one of {valid_log_levels}")


# Validate on import
Config.validate()
