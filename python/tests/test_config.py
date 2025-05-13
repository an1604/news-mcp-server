import os
import pytest
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

with patch('dotenv.load_dotenv'):
    from src.config import Config


class TestConfig:
    """Tests for the Config class in config.py."""
    
    def test_config_initialization(self):
        """Test that Config can be initialized."""
        config = Config()
        assert hasattr(config, "NEWSAPI_API_KEY")
        assert hasattr(config, "OPENAI_API_KEY")
    
    def test_env_variables_loaded(self):
        """Test that environment variables are correctly loaded."""
        with patch.dict('os.environ', {"NEWSAPI_API_KEY": "test_news_key", "OPENAI_API_KEY": "test_openai_key"}, clear=True):
            config = Config()
            assert config.NEWSAPI_API_KEY == "test_news_key"
            assert config.OPENAI_API_KEY == "test_openai_key"
    
    def test_missing_env_variables(self):
        """Test behavior when environment variables are missing."""
        with patch.dict('os.environ', {}, clear=True):
            config = Config()
            assert config.NEWSAPI_API_KEY is None
            assert config.OPENAI_API_KEY is None
    
    def test_partial_env_variables(self):
        """Test behavior when only some environment variables are set."""
        with patch.dict('os.environ', {"NEWSAPI_API_KEY": "new_news_key"}, clear=True):
            config = Config()
            assert config.NEWSAPI_API_KEY == "new_news_key"
            assert config.OPENAI_API_KEY is None 