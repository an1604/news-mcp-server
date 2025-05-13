"""Pytest configuration file."""
import os
import pytest
from pathlib import Path
from dotenv import load_dotenv
import importlib
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "skip_if_no_openai: mark test to skip if OpenAI API key is not available"
    )


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Skip tests marked with skip_if_no_openai if OpenAI API key is not available."""
    if "skip_if_no_openai" in item.keywords:
        from src.config import config
        if not config.OPENAI_API_KEY:
            pytest.skip("Skipping test as OpenAI API key is not available")


@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Set up test environment variables before test session and clean up after.
    
    This fixture automatically runs once for the entire test session and ensures the 
    environment is clean before and after tests, while loading variables from .env.
    """
    original_env = os.environ.copy()
    
    env_path = Path(__file__).parents[1] / '.env'
    
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=True)
        print(f"Loaded environment variables from {env_path}")
        
        news_key = os.environ['NEWSAPI_API_KEY']
        openai_key = os.environ['OPENAI_API_KEY']
        print(f"NEWSAPI_API_KEY loaded: {bool(news_key)} (starts with: {news_key[:4] if news_key else 'None'}...)")
        print(f"OPENAI_API_KEY loaded: {bool(openai_key)} (starts with: {openai_key[:4] if openai_key else 'None'}...)")
    else:
        print(f"Warning: No .env file found at {env_path}")
    
    if "src.config" in sys.modules:
        importlib.reload(sys.modules["src.config"])
        print("Reloaded src.config module")
    
    yield
    
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def fresh_config():
    """Provide a freshly initialized config object with current environment variables."""
    try:
        if "src.config" in sys.modules:
            importlib.reload(sys.modules["src.config"])
        
        from src.config import Config
        return Config()
    except Exception as e:
        print(f"Error creating fresh config: {e}")
        return None 