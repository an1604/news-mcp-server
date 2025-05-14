import unittest
import os
import pytest
from unittest.mock import patch, MagicMock

class TestExtractKeyInfoAndSentiment(unittest.TestCase):
    
    def setUp(self):
        """Check if API keys are available and skip tests if they aren't."""
        if not os.environ.get('OPENAI_API_KEY'):
            self.skipTest("Skipping test as missing API keys")
    
    @patch('src.tools.sentiment_tool.search_news')
    @patch('src.tools.sentiment_tool.llm_service')
    def test_successful_sentiment_analysis(self, mock_llm_service, mock_search_news):
        # Mock search_news to return sample articles
        mock_search_news.return_value = {
            "articles": [
                {
                    "title": "Renewable Energy Investment Surges in Europe",
                    "description": "European countries announce major funding for solar and wind projects. Investment Fund B commits $2 billion.",
                    "url": "https://example.com/article1",
                    "source_name": "Energy News",
                    "published_at": "2023-01-01T12:00:00Z"
                },
                {
                    "title": "Region C Leads in Green Energy Transition",
                    "description": "Region C has achieved 50% renewable energy usage. Person X, energy minister, states 'This is just the beginning'.",
                    "url": "https://example.com/article2",
                    "source_name": "Climate Report",
                    "published_at": "2023-01-02T12:00:00Z"
                }
            ]
        }
        
        # Mock the LLM service to return sentiment analysis
        mock_llm_service.analyze_sentiment.return_value = {
            "overall_sentiment": "Positive",
            "sentiment_confidence": "Medium",
            "key_entities": {
                "people": ["Person X", "Person Y"],
                "organizations": ["Company A", "Investment Fund B"],
                "locations": ["Region C", "Europe"]
            },
            "key_takeaway_summary": "Significant growth in renewable energy investments across Europe with Region C leading the transition."
        }
        
        # Call the function with a test query
        from src.tools.sentiment_tool import extract_key_info_and_sentiment
        result = extract_key_info_and_sentiment("renewable energy investment", "en", 2)
        
        # Verify that search_news was called with the correct parameters
        mock_search_news.assert_called_with("renewable energy investment", "en", 2)
        
        # Verify that the LLM service was called with the correct parameters
        mock_llm_service.analyze_sentiment.assert_called_with("renewable energy investment", mock_search_news.return_value["articles"])
        
        # Verify the function returned the expected result
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["result"]["query"], "renewable energy investment")
        self.assertEqual(result["result"]["analyzed_article_count"], 2)
        self.assertEqual(result["result"]["overall_sentiment"], "Positive")
        self.assertEqual(result["result"]["sentiment_confidence"], "Medium")
        self.assertEqual(result["result"]["key_entities"]["people"], ["Person X", "Person Y"])
        self.assertEqual(result["result"]["key_entities"]["organizations"], ["Company A", "Investment Fund B"])
        self.assertEqual(result["result"]["key_entities"]["locations"], ["Region C", "Europe"])
        self.assertEqual(result["result"]["key_takeaway_summary"], 
                         "Significant growth in renewable energy investments across Europe with Region C leading the transition.")
    
    def test_empty_query(self):
        # Test with an empty query
        from src.tools.sentiment_tool import extract_key_info_and_sentiment
        result = extract_key_info_and_sentiment("", "en")
        
        # Verify the error response
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Query parameter is required")
    
    def test_invalid_max_articles(self):
        # Test with invalid max_articles_to_analyze
        from src.tools.sentiment_tool import extract_key_info_and_sentiment
        result = extract_key_info_and_sentiment("test query", "en", 15)
        
        # Verify the error response
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Invalid parameter")
        self.assertEqual(result["message"], "max_articles_to_analyze must be between 1 and 10")
    
    @patch('src.tools.sentiment_tool.search_news')
    def test_no_articles_found(self, mock_search_news):
        # Mock search_news to return no articles
        mock_search_news.return_value = {"articles": []}
        
        # Call the function with a test query
        from src.tools.sentiment_tool import extract_key_info_and_sentiment
        result = extract_key_info_and_sentiment("nonexistent topic", "en")
        
        # Verify the error response
        self.assertIn("error", result)
        self.assertEqual(result["error"], "No articles found")
        self.assertIn("No articles found for query", result["message"])
    
    @patch('src.tools.sentiment_tool.search_news')
    def test_search_error(self, mock_search_news):
        # Mock search_news to return an error
        mock_search_news.return_value = {"error": "API error", "message": "Rate limit exceeded"}
        
        # Call the function with a test query
        from src.tools.sentiment_tool import extract_key_info_and_sentiment
        result = extract_key_info_and_sentiment("test query", "en")
        
        # Verify that the search error is propagated
        self.assertIn("error", result)
        self.assertEqual(result["error"], "API error")
        self.assertEqual(result["message"], "Rate limit exceeded")
    
    @patch('src.tools.sentiment_tool.search_news')
    @patch('src.tools.sentiment_tool.llm_service')
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
        
        mock_llm_service.analyze_sentiment.side_effect = Exception("LLM API Error")
        
        from src.tools.sentiment_tool import extract_key_info_and_sentiment
        result = extract_key_info_and_sentiment("test query", "en")
        
        self.assertIn("error", result)
        self.assertEqual(result["error"], "LLM processing error")
        self.assertEqual(result["message"], "LLM API Error")

if __name__ == '__main__':
    unittest.main() 