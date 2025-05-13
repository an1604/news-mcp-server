import logging
from typing import Dict, Any
from python.src.config import config
from newsapi.newsapi_client import NewsApiClient

logger = logging.getLogger(__name__)

def search_news(query: str, language: str = "en", page_size: int = 5) -> Dict[str, Any]:
    """Search for recent news articles matching a specific query.
    
    Args:
        query: Search news query
        language: News language (e.g., "en")
        page_size: Amount of articles to return per page
        
    Returns:
        A dictionary with a list of articles
    """
    if not query:
        return {"error": "Query parameter is required"}
    
    if page_size < 1 or page_size > 100:
        page_size = 5
    
    try:
        api_key = config.NEWSAPI_API_KEY
        if not api_key:
            logger.error("NEWSAPI_API_KEY not configured")
            return {"error": "Configuration error", "message": "NEWSAPI_API_KEY is required in environment variables"}
            
        newsapi = NewsApiClient(api_key=api_key)
        
        logger.info(f"Fetching news for query: {query}")
        
        news_data = newsapi.get_everything(
            q=query,
            language=language,
            page_size=page_size,
            sort_by='publishedAt'
        )
        
        formatted_articles = []
        for article in news_data.get("articles", []):
            formatted_article = {
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "url": article.get("url", ""),
                "source_name": article.get("source", {}).get("name", ""),
                "published_at": article.get("publishedAt", "")
            }
            formatted_articles.append(formatted_article)
        
        return {"articles": formatted_articles}
        
    except ValueError as ve:
        logger.error(f"Configuration error: {str(ve)}")
        return {"error": "Configuration error", "message": str(ve)}
    except Exception as e:
        logger.error(f"Error in search_news: {str(e)}")
        return {"error": "API error", "message": str(e)}
