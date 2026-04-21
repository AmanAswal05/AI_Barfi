"""
Tests for configuration module.
"""

import os
import pytest
from src.config import Config


def test_config_validation():
    """Test configuration validation."""
    # Should not raise
    Config.validate()
    
    # Test invalid URL
    original_url = Config.OLLAMA_BASE_URL
    Config.OLLAMA_BASE_URL = "invalid"
    with pytest.raises(ValueError):
        Config.validate()
    Config.OLLAMA_BASE_URL = original_url
    
    # Test invalid log level
    original_level = Config.LOG_LEVEL
    Config.LOG_LEVEL = "INVALID"
    with pytest.raises(ValueError):
        Config.validate()
    Config.LOG_LEVEL = original_level


def test_config_defaults():
    """Test default configuration values."""
    assert Config.PRIMARY_MODEL == "codellama"
    assert Config.FALLBACK_MODEL == "llama3.2"
    assert Config.LOG_LEVEL == "INFO"
    assert Config.BACKUP_SUFFIX == ".bak"
