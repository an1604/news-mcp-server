import pytest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestToolsEdgeCases:
    """Tests for edge cases in the MCP tools."""

    def test_extract_tool_invalid_title(self):
        """Test extract_tool with invalid title parameter."""
        from src.tools.extract_tool import extract_information_from_article
        
        result = extract_information_from_article(None, "en")
        assert "error" in result
        assert result["error"] == "Query parameter is required"
        
        result = extract_information_from_article("", "en")
        assert "error" in result
        assert result["error"] == "Query parameter is required"

    @patch('src.tools.search_news.NewsApiClient')
    @patch('src.tools.search_news.config')
    def test_search_news_special_characters(self, mock_config, mock_news_api_client):
        """Test search_news with special characters in query."""
        mock_config.NEWSAPI_API_KEY = "test-key"
        
        mock_client = MagicMock()
        mock_client.get_everything.return_value = {"articles": []}
        mock_news_api_client.return_value = mock_client
        
        from src.tools.search_news import search_news
        
        result = search_news("test<script>alert(1)</script>", "en", 5)
        mock_news_api_client.assert_called_once_with(api_key="test-key")
        mock_client.get_everything.assert_called_once()
        _, kwargs = mock_client.get_everything.call_args
        assert kwargs["q"] == "test<script>alert(1)</script>"
        assert "articles" in result

    @patch('src.tools.sentiment_tool.search_news')
    @patch('src.tools.sentiment_tool.llm_service')
    def test_sentiment_tool_with_max_articles(self, mock_llm_service, mock_search_news):
        """Test sentiment tool with edge cases for max_articles parameter."""
        from src.tools.sentiment_tool import extract_key_info_and_sentiment
        
        mock_search_news.return_value = {"articles": [{"title": "Test", "description": "Test"}] * 10}
        
        mock_llm_service.analyze_sentiment.return_value = {
            "overall_sentiment": "neutral",
            "sentiment_confidence": "high",
            "key_entities": {"people": [], "organizations": [], "locations": []},
            "key_takeaway_summary": "Test"
        }
        
        result = extract_key_info_and_sentiment("test", "en", 10)
        assert result["status"] == "success"
        
        mock_llm_service.analyze_sentiment.assert_called_once()
        args, _ = mock_llm_service.analyze_sentiment.call_args
        assert args[0] == "test"  # query
        assert len(args[1]) == 10  # articles list length
        
    def test_invalid_max_articles_parameter(self):
        """Test sentiment tool with invalid max_articles_to_analyze."""
        from src.tools.sentiment_tool import extract_key_info_and_sentiment
        
        result = extract_key_info_and_sentiment("test", "en", 15)
        assert "error" in result
        assert result["error"] == "Invalid parameter"
        assert result["message"] == "max_articles_to_analyze must be between 1 and 10"
        
        result = extract_key_info_and_sentiment("test", "en", -1)
        assert "error" in result
        assert result["error"] == "Invalid parameter"
        assert result["message"] == "max_articles_to_analyze must be between 1 and 10"