import os
import sys
import unittest
from unittest.mock import patch
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

class TestLLMService(unittest.TestCase):
    """Tests for the LLMService class in llm.py."""
    def setUp(self):
        from src.config import config
        if not config.OPENAI_API_KEY:
            self.skipTest("Skipping test as OpenAI API key is not available")

        from src.services.llm import LLMService
        self.llm_service = LLMService()

    @pytest.mark.skip_if_no_openai
    def test_extract_article_information_real(self):
        test_title = "Apple launches new iPhone with advanced AI capabilities"
        test_description = "Apple Inc. has unveiled its latest iPhone model featuring advanced AI capabilities. " \
                           "CEO Tim Cook announced the new device at an event in Cupertino, California. " \
                           "The new model includes improved camera technology and enhanced battery life."
        
        result = self.llm_service.extract_article_information(test_title, test_description)
        
        self.assertIn("people", result)
        self.assertIn("organizations", result)
        self.assertIn("locations", result)
        self.assertIn("key_quotes", result)
        
        self.assertTrue(any("Tim Cook" in person for person in result["people"]), 
                        f"Tim Cook not found in people: {result['people']}")
        
        self.assertTrue(any("Apple" in org for org in result["organizations"]),
                        f"Apple not found in organizations: {result['organizations']}")
        
        self.assertTrue(any("Cupertino" in loc for loc in result["locations"]),
                        f"Cupertino not found in locations: {result['locations']}")

    @pytest.mark.skip_if_no_openai
    def test_analyze_sentiment_real(self):
        test_query = "climate change"
        test_articles = [
            {
                "title": "Global temperatures reach record high for third consecutive year",
                "description": "Scientists report alarming rise in global temperatures, with devastating impacts on ecosystems worldwide."
            },
            {
                "title": "New study shows promising results for carbon capture technology",
                "description": "Researchers at MIT have developed a breakthrough technology that can capture carbon emissions at a fraction of the current cost."
            }
        ]
        
        result = self.llm_service.analyze_sentiment(test_query, test_articles)
        
        # Check structure without asserting exact content
        self.assertIn("overall_sentiment", result)
        self.assertIn("sentiment_confidence", result)
        self.assertIn("key_entities", result)
        self.assertIn("key_takeaway_summary", result)
        
        # Verify sentiment is one of the valid values
        self.assertIn(result["overall_sentiment"], ["positive", "negative", "neutral", "mixed"])
        
        # Verify confidence is one of the valid values
        self.assertIn(result["sentiment_confidence"], ["high", "medium", "low"])
        
        # Check key_entities contains expected fields
        self.assertIn("people", result["key_entities"])
        self.assertIn("organizations", result["key_entities"])
        self.assertIn("locations", result["key_entities"])

    # Include mock tests for when API is unavailable
    @patch('src.services.llm.config')
    def test_missing_api_key(self, mock_config):
        mock_config.OPENAI_API_KEY = None
        
        with self.assertRaises(ValueError) as context:
            from src.services.llm import LLMService
            LLMService()
        
        self.assertIn("No OpenAI API key provided", str(context.exception))

    @pytest.mark.skip_if_no_openai
    def test_schema_definitions(self):
        from src.services.llm import EXTRACT_INFO_SCHEMAS, SENTIMENT_ANALYSIS_SCHEMAS
        
        self.assertEqual(len(EXTRACT_INFO_SCHEMAS), 4)
        schema_names = [schema.name for schema in EXTRACT_INFO_SCHEMAS]
        self.assertIn("people", schema_names)
        self.assertIn("organizations", schema_names)
        self.assertIn("locations", schema_names)
        self.assertIn("key_quotes", schema_names)
        
        self.assertEqual(len(SENTIMENT_ANALYSIS_SCHEMAS), 4)
        schema_names = [schema.name for schema in SENTIMENT_ANALYSIS_SCHEMAS]
        self.assertIn("overall_sentiment", schema_names)
        self.assertIn("sentiment_confidence", schema_names)
        self.assertIn("key_entities", schema_names)
        self.assertIn("key_takeaway_summary", schema_names)


if __name__ == '__main__':
    unittest.main() 