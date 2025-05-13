import unittest
import os
import sys
from python.services.search_news import search_news
from python.src.config import config

class TestSearchNewsIntegration(unittest.TestCase):
    """Integration tests for search_news that make real API calls.
    
    NOTE: These tests require a valid NEWSAPI_API_KEY in your environment.
    """
    
    def setUp(self):
        # Skip tests if no API key is available
        if not config.NEWSAPI_API_KEY:
            self.skipTest("NEWSAPI_API_KEY not available in environment")
    
    def test_real_search_api_call(self):
        """Test a real API call to NewsAPI."""
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
    
    def test_real_search_with_specific_query(self):
        """Test searching for a more specific query."""
        query = "artificial intelligence"
        result = search_news(query, "en", 3)
        
        self.assertIn("articles", result)
        
        self.assertTrue(len(result["articles"]) > 0, "No articles returned for the query")
        
        print("\nArticles found for 'artificial intelligence':")
        for article in result["articles"]:
            print(f"- {article['title']}")
    
    def test_real_search_with_language_filter(self):
        """Test searching with a language filter."""
        query = "science"
        result = search_news(query, "fr", 3)
        
        self.assertIn("articles", result)
        self.assertNotIn("error", result)

if __name__ == '__main__':
    unittest.main() 