import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from python.services.search_news import search_news

class TestSearchNews(unittest.TestCase):
    
    @patch('python.services.search_news.NewsApiClient')
    def test_successful_search(self, mock_newsapi):
        mock_client_instance = MagicMock()
        mock_newsapi.return_value = mock_client_instance
        
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
        
        mock_client_instance.get_everything.return_value = mock_response
        
        result = search_news("test query", "en", 2)
        
        mock_newsapi.assert_called_once()
        mock_client_instance.get_everything.assert_called_with(
            q="test query",
            language="en",
            page_size=2,
            sort_by='publishedAt'
        )
        
        self.assertEqual(len(result["articles"]), 2)
        self.assertEqual(result["articles"][0]["title"], "Test Title 1")
        self.assertEqual(result["articles"][0]["description"], "Test Description 1")
        self.assertEqual(result["articles"][0]["url"], "https://example.com/1")
        self.assertEqual(result["articles"][0]["source_name"], "Test Source 1")
        self.assertEqual(result["articles"][0]["published_at"], "2023-01-01T12:00:00Z")
        
    @patch('python.services.search_news.config')
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
    
    @patch('python.services.search_news.NewsApiClient')
    def test_api_exception(self, mock_newsapi):
        mock_client_instance = MagicMock()
        mock_newsapi.return_value = mock_client_instance
        mock_client_instance.get_everything.side_effect = Exception("API Error")
        
        result = search_news("test query", "en", 5)
        
        self.assertIn("error", result)
        self.assertEqual(result["error"], "API error")
        self.assertEqual(result["message"], "API Error")
    
    @patch('python.services.search_news.NewsApiClient')
    def test_invalid_page_size(self, mock_newsapi):
        mock_client_instance = MagicMock()
        mock_newsapi.return_value = mock_client_instance
        mock_client_instance.get_everything.return_value = {"articles": []}
        
        search_news("test", "en", 0)
        search_news("test", "en", 101)
        
        calls = mock_client_instance.get_everything.call_args_list
        self.assertEqual(calls[0][1]["page_size"], 5)
        self.assertEqual(calls[1][1]["page_size"], 5)

if __name__ == '__main__':
    unittest.main() 