import sys
import os
import logging
from fastmcp import FastMCP

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.search_news import search_news
from tools.extract_tool import extract_information_from_article
from tools.sentiment_tool import extract_key_info_and_sentiment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("news_assistant_mcp")

mcp.tool()(search_news)
mcp.tool()(extract_information_from_article)
mcp.tool()(extract_key_info_and_sentiment)

if __name__ == "__main__":
    logger.info("Starting MCP server for news assistant")
    mcp.run(transport="sse", host="0.0.0.0", port=3000, path="/")
