import logging
from typing import Dict, Any

from src.tools.search_news import search_news
from src.services.llm import llm_service

logger = logging.getLogger(__name__)

def extract_key_info_and_sentiment(query: str, language: str = "en", max_articles_to_analyze: int = 5) -> Dict[str, Any]:
    """Analyze news articles to extract key entities and determine sentiment.
    
    Args:
        query: Search news query
        language: News language (e.g., "en")
        max_articles_to_analyze: Maximum articles to analyze
        
    Returns:
        A dictionary with sentiment analysis and key information
    """
    if not query:
        logger.error("Query parameter is required")
        return {"error": "Query parameter is required"}
    
    if max_articles_to_analyze < 1 or max_articles_to_analyze > 10:
        logger.error(f"Invalid max_articles_to_analyze: {max_articles_to_analyze}")
        return {"error": "Invalid parameter", "message": "max_articles_to_analyze must be between 1 and 10"}
    
    try:
        search_result = search_news(query, language, max_articles_to_analyze)
        
        if "error" in search_result:
            logger.error(f"Error searching for articles: {search_result['error']}")
            return search_result
        
        articles = search_result["articles"]
        if not articles:
            logger.warning(f"No articles found for query: {query}")
            return {"error": "No articles found", "message": f"No articles found for query: {query}"}
        
        try:
            sentiment_analysis = llm_service.analyze_sentiment(query, articles)
            
            return {
                "status": "success",
                "result": {
                    "query": query,
                    "analyzed_article_count": len(articles),
                    "overall_sentiment": sentiment_analysis["overall_sentiment"],
                    "sentiment_confidence": sentiment_analysis["sentiment_confidence"],
                    "key_entities": sentiment_analysis["key_entities"],
                    "key_takeaway_summary": sentiment_analysis["key_takeaway_summary"]
                }
            }
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return {"error": "LLM processing error", "message": str(e)}
        
    except Exception as e:
        logger.error(f"Error in extract_key_info_and_sentiment: {str(e)}")
        return {"error": "Processing error", "message": str(e)}
