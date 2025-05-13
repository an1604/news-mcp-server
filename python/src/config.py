"""
Config module for loading environment variables.

This module provides a Config class that loads environment variables from a .env file.
It also includes a singleton instance of the Config class that can be accessed globally.
"""
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

logger.info(f"Environment variables loaded. OPENAI_API_KEY present: {bool(os.getenv('OPENAI_API_KEY'))}")

class Config:
    def __init__(self):
        """Initialize config by loading values from environment variables."""
        self.NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        
        logger.info(f"Config initialized. OPENAI_API_KEY loaded: {bool(self.OPENAI_API_KEY)}")
        logger.info(f"Config initialized. NEWSAPI_API_KEY loaded: {bool(self.NEWSAPI_API_KEY)}")

config = Config()
