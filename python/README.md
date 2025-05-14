# Python Implementation - GenAI News Assistant MCP Server

This directory contains the Python implementation of the GenAI News Assistant MCP Server. The server provides tools for fetching and analyzing news information using NewsAPI.org and a Large Language Model.

## Overview

This implementation:
- Serves as a Model Context Protocol (MCP) server with SSE transport
- Integrates with NewsAPI.org for retrieving news data
- Uses OpenAI API for natural language processing tasks
- Exposes three MCP tools for news search and analysis

## Project Structure

```
python/
├── src/                    # Source code
├── tests/                  # Test files
├── .env.example            # Example environment variables
├── .env                    # Environment variables (not in repo)
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
├── requirements-test.txt   # Testing dependencies
└── docker_build_run.sh     # Helper script for Docker
```

## Quick Start

### Setup

1. Clone the repository
2. Create a `.env` file based on `.env.example`:
   ```
   NEWS_API_KEY=your_newsapi_org_key
   OPENAI_API_KEY=your_openai_api_key
   ```

### Running Locally

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server (from the src directory):
   ```bash
   python -m src.main
   ```

### Running with Docker
```bash
docker build -t news-assistant-python .
docker run -p 3000:3000 --env-file .env news-assistant-python
```

## Implemented MCP Tools

The server implements three MCP tools:

1. **search_news**: Search for recent news articles matching a specific query
2. **extract_information_from_article**: Extract structured information from a news article
3. **extract_key_info_and_sentiment**: Analyze news articles for key entities and sentiment

## Testing

Run tests with:
```bash
pip install -r requirements-test.txt
pytest
```

## Notes

- News API has a limit of 100 requests per day on the free tier
- Use the OpenAI API calls efficiently to manage costs 

## Demo

[🎥 Watch the demo video](mcp-proof.mp4)

