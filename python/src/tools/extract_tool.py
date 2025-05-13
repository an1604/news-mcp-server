import logging
from typing import Dict, Any

import sys
import os  
# Add the python directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.tools.search_news import search_news
from src.services.llm import llm_service

logger = logging.getLogger(__name__)

def extract_information_from_article(query: str, language: str = "en") -> Dict[str, Any]:
    """Extract structured information from a news article.
    
    Args:
        query: Search news query to find article
        language: News language (e.g., "en")
        
    Returns:
        A dictionary with structured information from the article
    """
    if not query:
        logger.error("Query parameter is required")
        return {"error": "Query parameter is required"}
    
    try:
        search_result = search_news(query, language, 1)
        
        if "error" in search_result:
            logger.error(f"Error searching for articles: {search_result['error']}")
            return search_result
        
        articles = search_result.get("articles", [])
        if not articles:
            logger.warning(f"No articles found for query: {query}")
            return {"error": "No articles found", "message": f"No articles found for query: {query}"}
        
        article = articles[0]
        title = article["title"]
        description = article["description"]
        
        try:
            extracted_info = llm_service.extract_article_information(title, description)
            return {
                "result": {
                    "fetched_article_title": title,
                    "people": extracted_info.get("people", []),
                    "organizations": extracted_info.get("organizations", []),
                    "locations": extracted_info.get("locations", []),
                    "key_quotes": extracted_info.get("key_quotes", [])
                }
            }
        except Exception as e:
            logger.error(f"Error extracting information from article: {str(e)}")
            return {"error": "LLM processing error", "message": str(e)}
        
    except Exception as e:
        logger.error(f"Error in extract_information_from_article: {str(e)}")
        return {"error": "Processing error", "message": str(e)}

