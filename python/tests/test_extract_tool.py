import unittest
import os
import pytest
from unittest.mock import patch, MagicMock

class TestExtractInformationFromArticle(unittest.TestCase):
    
    def setUp(self):
        """Check if API keys are available and skip tests if they aren't."""
        if not os.environ.get('OPENAI_API_KEY'):
            self.skipTest("Skipping test as missing API keys")
    
    @patch('src.tools.extract_tool.search_news')
    @patch('src.tools.extract_tool.llm_service')
    def test_successful_extraction(self, mock_llm_service, mock_search_news):
        mock_search_news.return_value = {
            "articles": [
                {
                    "title": "Global Tech Summit Announces Partnership",
                    "description": "TechCorp Inc. and Innovate Solutions have announced a partnership at the Global Tech Summit in Metropolis. Jane Doe, CEO of TechCorp, said 'This collaboration marks a new era'.",
                    "url": "https://example.com/article",
                    "source_name": "Tech News",
                    "published_at": "2023-01-01T12:00:00Z"
                }
            ]
        }
        
        # Mock the LLM service to return structured information
        mock_llm_service.extract_article_information.return_value = {
            "people": ["Jane Doe", "John Smith"],
            "organizations": ["TechCorp Inc.", "Innovate Solutions", "Global Tech Summit"],
            "locations": ["Metropolis"],
            "key_quotes": ["This collaboration marks a new era"]
        }
        
        # Call the function with a test query
        from src.tools.extract_tool import extract_information_from_article
        result = extract_information_from_article("tech summit", "en")
        
        # Verify that search_news was called with the correct parameters
        mock_search_news.assert_called_with("tech summit", "en", 1)
        
        # Verify that the LLM service was called with the article title and description
        mock_llm_service.extract_article_information.assert_called_with(
            "Global Tech Summit Announces Partnership",
            "TechCorp Inc. and Innovate Solutions have announced a partnership at the Global Tech Summit in Metropolis. Jane Doe, CEO of TechCorp, said 'This collaboration marks a new era'."
        )
        
        # Verify the function returned the expected result
        self.assertIn("result", result)
        self.assertEqual(result["result"]["fetched_article_title"], "Global Tech Summit Announces Partnership")
        self.assertEqual(result["result"]["people"], ["Jane Doe", "John Smith"])
        self.assertEqual(result["result"]["organizations"], ["TechCorp Inc.", "Innovate Solutions", "Global Tech Summit"])
        self.assertEqual(result["result"]["locations"], ["Metropolis"])
        self.assertEqual(result["result"]["key_quotes"], ["This collaboration marks a new era"])
    
    def test_empty_query(self):
        # Test with an empty query
        from src.tools.extract_tool import extract_information_from_article
        result = extract_information_from_article("", "en")
        
        # Verify the error response
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Query parameter is required")
    
    @patch('src.tools.extract_tool.search_news')
    def test_no_articles_found(self, mock_search_news):
        # Mock search_news to return no articles
        mock_search_news.return_value = {"articles": []}
        
        # Call the function with a test query
        from src.tools.extract_tool import extract_information_from_article
        result = extract_information_from_article("nonexistent topic", "en")
        
        # Verify the error response
        self.assertIn("error", result)
        self.assertEqual(result["error"], "No articles found")
        self.assertIn("No articles found for query", result["message"])
    
    @patch('src.tools.extract_tool.search_news')
    def test_search_error(self, mock_search_news):
        # Mock search_news to return an error
        mock_search_news.return_value = {"error": "API error", "message": "Rate limit exceeded"}
        
        # Call the function with a test query
        from src.tools.extract_tool import extract_information_from_article
        result = extract_information_from_article("test query", "en")
        
        # Verify that the search error is propagated
        self.assertIn("error", result)
        self.assertEqual(result["error"], "API error")
        self.assertEqual(result["message"], "Rate limit exceeded")
    
    @patch('src.tools.extract_tool.search_news')
    @patch('src.tools.extract_tool.llm_service')
    def test_llm_processing_error(self, mock_llm_service, mock_search_news):
        mock_search_news.return_value = {
            "articles": [
                {
                    "title": "Test Article",
                    "description": "Test Description",
                    "url": "https://example.com/article",
                    "source_name": "Test Source",
                    "published_at": "2023-01-01T12:00:00Z"
                }
            ]
        }
        
        mock_llm_service.extract_article_information.side_effect = Exception("LLM API Error")
        
        from src.tools.extract_tool import extract_information_from_article
        result = extract_information_from_article("test query", "en")
        
        self.assertIn("error", result)
        self.assertEqual(result["error"], "LLM processing error")
        self.assertEqual(result["message"], "LLM API Error")

if __name__ == '__main__':
    unittest.main() 