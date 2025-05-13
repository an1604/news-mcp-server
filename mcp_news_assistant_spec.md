# MCP News Assistant Implementation Specification

## Overview

This project will implement a Model Context Protocol (MCP) server that provides tools for fetching and analyzing news information using NewsAPI.org and LLM capabilities. The server will expose three main tools:
1. `search_news` - Fetches news articles matching specific queries
2. `extract_information_from_article` - Extracts structured information from a news article using an LLM
3. `extract_key_info_and_sentiment` - Analyzes multiple news articles to determine sentiment and extract key information

## Technology Stack

- **Language**: Python
- **MCP Framework**: FastMCP (as seen in the reference implementation)
- **LLM Integration**: LangChain with local model support and OpenAI API fallback
- **News API**: NewsAPI.org
- **Container**: Docker

## Core Components

### 1. MCP Server Implementation

- Create a FastMCP server instance with appropriate naming
- Define MCP tools using the `@mcp.tool()` decorator pattern
- Implement the SSE transport protocol for communication
- Configure server to listen on appropriate host/port

### 2. Tool Implementation

#### 2.1 `search_news` Tool

- **Implementation**:
  ```python
  @mcp.tool()
  def search_news(query: str, language: str = "en", pageSize: int = 5) -> dict:
      """Search for recent news articles matching a specific query.
      
      Args:
          query: Search news query
          language: News language (e.g., "en")
          pageSize: Amount per page
          
      Returns:
          A dictionary with a list of articles
      """
      # Implementation details
  ```

- **Inputs**:
  - `query` (string): Search query for news articles
  - `language` (string, default="en"): Language code
  - `pageSize` (integer, default=5): Number of articles to return

- **Processing**:
  - Validate inputs
  - Call NewsAPI.org `/v2/everything` endpoint
  - Format response according to MCP specification
  - Implement caching to handle API rate limits

- **Outputs**:
  - Dictionary with an "articles" array containing:
    - title
    - description
    - url
    - source_name
    - published_at

#### 2.2 `extract_information_from_article` Tool

- **Implementation**:
  ```python
  @mcp.tool()
  def extract_information_from_article(query: str, language: str = "en") -> dict:
      """Extract structured information from a news article.
      
      Args:
          query: Search news query to find article
          language: News language (e.g., "en")
          
      Returns:
          A dictionary with structured information from the article
      """
      # Implementation details
  ```

- **Inputs**:
  - `query` (string): Search query to find a news article
  - `language` (string, default="en"): Language code

- **Processing**:
  - Use `search_news` to get the latest article matching the query
  - Extract article title and description
  - Prepare a LangChain prompt to extract structured information
  - Process with local LLM or OpenAI API (configurable)
  - Parse LLM response into structured format

- **Outputs**:
  - Dictionary with "result" containing:
    - fetched_article_title
    - people
    - organizations
    - locations
    - key_quotes

#### 2.3 `extract_key_info_and_sentiment` Tool

- **Implementation**:
  ```python
  @mcp.tool()
  def extract_key_info_and_sentiment(query: str, language: str = "en", max_articles_to_analyze: int = 5) -> dict:
      """Analyze news articles to extract key entities and determine sentiment.
      
      Args:
          query: Search news query
          language: News language (e.g., "en")
          max_articles_to_analyze: Maximum articles to analyze
          
      Returns:
          A dictionary with sentiment analysis and key information
      """
      # Implementation details
  ```

- **Inputs**:
  - `query` (string): Search query for news articles
  - `language` (string, default="en"): Language code
  - `max_articles_to_analyze` (integer, default=5): Maximum number of articles to analyze

- **Processing**:
  - Get multiple articles using `search_news`
  - Prepare article titles and descriptions for analysis
  - Create a LangChain prompt for sentiment analysis and entity extraction
  - Process with local LLM or OpenAI API (configurable)
  - Parse LLM response into structured format

- **Outputs**:
  - Dictionary with "status" and "result" containing:
    - query
    - analyzed_article_count
    - overall_sentiment
    - sentiment_confidence
    - key_entities (people, organizations, locations)
    - key_takeaway_summary

### 3. Additional Features (Optional)

Following the pattern in `gh_mcp_server.py`, we could also implement:

- **Resource endpoints** using `@mcp.resource()` for providing formatted outputs
- **Prompt templates** using `@mcp.prompt()` for guiding LLM interactions

### 4. LLM Integration with LangChain

- **Implementation Approach**:
  - Create helper functions for LLM processing
  - Configure LLM provider based on environment
  - Define output parsing functions

- **LLM Provider Configuration**:
  - Primary: Local LLM via LangChain (e.g., using llama.cpp or other compatible model)
  - Fallback: OpenAI API integration when LLM_API_KEY is provided

- **Prompt Engineering**:
  - Create structured prompts for information extraction
  - Design prompts for sentiment analysis
  - Implement output parsers to ensure consistent JSON formatting

### 5. NewsAPI Integration

- **Implementation Approach**:
  - Create helper functions for API calls
  - Implement error handling and retries
  - Add caching mechanism

- **API Client Functions**:
  - Search function for `/v2/everything` endpoint
  - Top headlines function for `/v2/top-headlines` endpoint
  - Error handling and response formatting

- **Caching Layer**:
  - In-memory cache for API responses
  - TTL-based cache expiration
  - Cache invalidation strategy

### 6. Environment Configuration

- Required environment variables:
  - `NEWS_API_KEY`: API key for NewsAPI.org
  - `LLM_API_KEY`: API key for OpenAI (optional, for fallback)
  - `LOCAL_LLM_PATH`: Path to local LLM model files (if using local mode)
  - `USE_LOCAL_LLM`: Boolean flag to use local LLM (default: true)

### 7. Error Handling

- Implement comprehensive error handling following the pattern in `gh_mcp_server.py`:
  - Return error dictionaries with appropriate keys
  - Provide informative error messages
  - Handle API errors gracefully

### 8. Logging Configuration

- Setup basic logging configuration
- Log all API calls and responses
- Track LLM usage and performance

## Main Application Structure

```python
from fastmcp import FastMCP
from typing import List, Optional
import requests
import os
import logging
from langchain.llms import OpenAI  # Or appropriate local LLM
from langchain.prompts import PromptTemplate
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP
mcp = FastMCP("news_assistant_mcp")

# API helper functions
def fetch_news(query, language="en", page_size=5):
    # Implementation

# LLM helper functions
def process_with_llm(prompt, text):
    # Implementation

# Tool implementations (as shown above)
@mcp.tool()
def search_news(query: str, language: str = "en", pageSize: int = 5) -> dict:
    # Implementation

@mcp.tool()
def extract_information_from_article(query: str, language: str = "en") -> dict:
    # Implementation

@mcp.tool()
def extract_key_info_and_sentiment(query: str, language: str = "en", max_articles_to_analyze: int = 5) -> dict:
    # Implementation

# Main entry point
if __name__ == "__main__":
    # Run the FastMCP server
    mcp.run(transport="sse", host="0.0.0.0", port=3000, path="/")
```

## File Structure

```
python/
├── src/
│   ├── main.py                  # Application entry point with FastMCP setup
│   ├── config.py                # Environment and configuration management
│   ├── services/
│   │   ├── __init__.py
│   │   ├── news_service.py      # NewsAPI client functions
│   │   └── llm_service.py       # LLM service with LangChain
│   ├── tools/
│   │   ├── __init__.py  
│   │   ├── search_tool.py       # search_news implementation
│   │   ├── extract_tool.py      # extract_information_from_article implementation
│   │   └── sentiment_tool.py    # extract_key_info_and_sentiment implementation
│   └── utils/
│       ├── __init__.py
│       ├── cache.py             # Caching utilities (BONUS - THIS IS NOT A PART OF THE REQUIERMENTS!!)
│       └── logging.py           # Logging configuration
├── tests/
│   ├── __init__.py
│   ├── test_news_service.py     # Tests for NewsAPI integration
│   ├── test_llm_service.py      # Tests for LLM integration
│   ├── test_tools.py            # Tests for MCP tools
│   └── mocks/                   # Mock data for testing
├── Dockerfile                   # Docker configuration (already provided)
├── requirements.txt             # Python dependencies (needs to be populated)
└── .env.example                 # Example environment variables
```

## Testing Strategy

1. **Unit Tests**: For individual components (tools, API clients, LLM integration)
2. **Integration Tests**: End-to-end testing of MCP protocol and tools
3. **Mock Testing**: Use mock responses for NewsAPI and LLM to avoid API costs during testing

## Development Roadmap

1. Set up project structure and environment
2. Implement NewsAPI service with caching
3. Implement LangChain integration
4. Create FastMCP tool implementations
5. Write tests
6. Configure Docker settings
7. Document setup and usage

## Considerations and Challenges

1. **Rate Limiting**: NewsAPI.org limits to 100 requests/day on the free tier
   - Solution: Implement aggressive caching

2. **LLM Cost Management**:
   - Primary solution: Use local LLM via LangChain
   - Fallback: Use OpenAI API with structured prompts to minimize token usage

3. **Error Handling**:
   - Implement graceful fallbacks for API failures
   - Provide clear error messages in MCP responses

4. **Prompt Engineering**:
   - Design prompts that efficiently extract required information
   - Ensure consistent output formatting

5. **MCP Compliance**:
   - Strictly follow the MCP specification for all message types
   - Validate against the official MCP documentation

## Docker Configuration

- Base image: Python 3.11-slim (as specified in the template Dockerfile)
- Expose port 3000 (as specified in the template Dockerfile)
- Environment variable configuration for API keys
- Proper shutdown handling for graceful termination

## Testing with Claude Desktop

The application will be tested in a Claude Desktop application using the remote-mcp tool (https://github.com/latentsp/remote-mcp). It's crucial that the implementation properly supports the MCP Server-Sent Events (SSE) transport and that the Docker container works correctly to pass testing. 