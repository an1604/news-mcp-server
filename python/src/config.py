"""
Config module for loading environment variables.

This module provides a Config class that loads environment variables from a .env file.
It also includes a singleton instance of the Config class that can be accessed globally.
"""
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    def __init__(self):
        """Initialize config by loading values from environment variables."""
        self.NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

config = Config()
