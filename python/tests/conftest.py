"""Pytest configuration file."""
import os
import pytest


@pytest.fixture(autouse=True)
def setup_test_env():
    """Set up test environment variables before each test and clean up after.
    
    This fixture automatically runs for each test and ensures the environment
    is clean before and after tests.
    """
    original_env = os.environ.copy()
    
    yield
    
    os.environ.clear()
    os.environ.update(original_env) 