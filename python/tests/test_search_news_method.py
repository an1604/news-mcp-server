import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from src.tools.search_news import search_news

class TestSearchNews(unittest.TestCase):
    
    @patch('src.tools.search_news.NewsApiClient')
    @patch('src.tools.search_news.config')
    def test_successful_search(self, mock_config, mock_newsapi):
        # Mock the config to return a valid API key
        mock_config.NEWSAPI_API_KEY = "test_api_key"
        
        # Mock the NewsAPI client instance
        mock_client_instance = MagicMock()
        mock_newsapi.return_value = mock_client_instance
        
        # Create sample response data
        mock_response = {
            "status": "ok",
            "totalResults": 2,
            "articles": [
                {
                    "source": {"id": "test-source-1", "name": "Test Source 1"},
                    "author": "Test Author 1",
                    "title": "Test Title 1",
                    "description": "Test Description 1",
                    "url": "https://example.com/1",
                    "urlToImage": "https://example.com/image1.jpg",
                    "publishedAt": "2023-01-01T12:00:00Z",
                    "content": "Test content 1"
                },
                {
                    "source": {"id": "test-source-2", "name": "Test Source 2"},
                    "author": "Test Author 2",
                    "title": "Test Title 2",
                    "description": "Test Description 2",
                    "url": "https://example.com/2",
                    "urlToImage": "https://example.com/image2.jpg",
                    "publishedAt": "2023-01-02T12:00:00Z",
                    "content": "Test content 2"
                }
            ]
        }
        
        # Set up the mock to return test data
        mock_client_instance.get_everything.return_value = mock_response
        
        # Call the function with test parameters
        result = search_news("test query", "en", 2)
        
        # Verify the client was initialized and called with correct parameters
        mock_newsapi.assert_called_once()
        mock_client_instance.get_everything.assert_called_with(
            q="test query",
            language="en",
            page_size=2,
            sort_by='publishedAt'
        )
        
        # Verify the function returned the expected result
        self.assertEqual(len(result["articles"]), 2)
        self.assertEqual(result["articles"][0]["title"], "Test Title 1")
        self.assertEqual(result["articles"][0]["description"], "Test Description 1")
        self.assertEqual(result["articles"][0]["url"], "https://example.com/1")
        self.assertEqual(result["articles"][0]["source_name"], "Test Source 1")
        self.assertEqual(result["articles"][0]["published_at"], "2023-01-01T12:00:00Z")
        
    @patch('src.tools.search_news.config')
    def test_missing_api_key(self, mock_config):
        mock_config.NEWSAPI_API_KEY = None
        
        result = search_news("test query", "en", 5)
        
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Configuration error")
        self.assertIn("NEWSAPI_API_KEY is required", result["message"])
    
    def test_empty_query(self):
        result = search_news("", "en", 5)
        
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Query parameter is required")
    
    @patch('src.tools.search_news.NewsApiClient')
    @patch('src.tools.search_news.config')
    def test_api_exception(self, mock_config, mock_newsapi):
        # Mock the config to return a valid API key so we get past the API key check
        mock_config.NEWSAPI_API_KEY = "test_api_key"
        
        # Mock the NewsAPI client to raise an exception
        mock_client_instance = MagicMock()
        mock_newsapi.return_value = mock_client_instance
        mock_client_instance.get_everything.side_effect = Exception("API Error")
        
        # Call the function
        result = search_news("test query", "en", 5)
        
        # Verify error response
        self.assertIn("error", result)
        self.assertEqual(result["error"], "API error")
        self.assertEqual(result["message"], "API Error")
    
    def test_invalid_page_size(self):
        # Test with invalid page sizes
        result_low = search_news("test", "en", 0)
        result_high = search_news("test", "en", 101)
        
        # Verify the error responses
        self.assertIn("error", result_low)
        self.assertEqual(result_low["error"], "Invalid page size")
        self.assertEqual(result_low["message"], "Page size must be between 1 and 100")
        
        self.assertIn("error", result_high)
        self.assertEqual(result_high["error"], "Invalid page size")
        self.assertEqual(result_high["message"], "Page size must be between 1 and 100")

if __name__ == '__main__':
    unittest.main() 