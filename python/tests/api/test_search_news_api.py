import unittest
import os
import sys
import pytest
from unittest.mock import patch
from src.tools.search_news import search_news

class TestSearchNewsIntegration(unittest.TestCase):
    """Integration tests for search_news that make real API calls.
    
    NOTE: These tests require a valid NEWSAPI_API_KEY in your environment.
    """
    
    def setUp(self):
        """Set up test with a fresh config and skip tests if no API key is available."""
        self.api_key = os.environ.get('NEWSAPI_API_KEY')
        
        if not self.api_key:
            self.skipTest("NEWSAPI_API_KEY not available in environment")
            
        print(f"Using NEWSAPI_API_KEY: {self.api_key[:5]}..." if self.api_key else "No API key found")
    
    @patch('src.tools.search_news.config')
    def test_real_search_api_call(self, mock_config):
        """Test a real API call to NewsAPI."""
        mock_config.NEWSAPI_API_KEY = self.api_key
        
        query = "technology"
        result = search_news(query, "en", 5)
        
        self.assertIn("articles", result)
        self.assertIsInstance(result["articles"], list)
        
        if result["articles"]:
            article = result["articles"][0]
            self.assertIn("title", article)
            self.assertIn("description", article)
            self.assertIn("url", article)
            self.assertIn("source_name", article)
            self.assertIn("published_at", article)
            self.assertTrue(article["title"])
            self.assertTrue(article["url"])
    
    @patch('src.tools.search_news.config')
    def test_real_search_with_specific_query(self, mock_config):
        """Test searching for a more specific query."""
        mock_config.NEWSAPI_API_KEY = self.api_key
        
        query = "artificial intelligence"
        result = search_news(query, "en", 3)
        
        self.assertIn("articles", result)
        
        self.assertTrue(len(result["articles"]) > 0, "No articles returned for the query")
        
        print("\nArticles found for 'artificial intelligence':")
        for article in result["articles"]:
            print(f"- {article['title']}")
    
    @patch('src.tools.search_news.config')
    def test_real_search_with_language_filter(self, mock_config):
        """Test searching with a language filter."""
        # Set API key on the mocked config object
        mock_config.NEWSAPI_API_KEY = self.api_key
        
        query = "science"
        result = search_news(query, "fr", 3)
        
        self.assertIn("articles", result)
        self.assertNotIn("error", result)

if __name__ == '__main__':
    unittest.main() 