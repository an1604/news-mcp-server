# GenAI News Assistant MCP Server

This repository contains a template for building a Model Context Protocol (MCP) server that provides tools for fetching and analyzing news information using NewsAPI.org and a Large Language Model.

## Project Structure

```
.
├── python/                # Python implementation
│   ├── Dockerfile         # Python Docker configuration
│   └── src/               # Python source code
├── typescript/            # TypeScript implementation
│   ├── Dockerfile         # TypeScript Docker configuration
│   └── src/               # TypeScript source code
└── README.md              # This file
```

## Prerequisites

- Docker installed on your system
- NewsAPI.org API key
- LLM API key (provided separately)

## Environment Variables

The following environment variables are required:

- `NEWS_API_KEY`: Your NewsAPI.org API key
- `LLM_API_KEY`: Your LLM API key

## Building and Running

### Python Version

```bash
# Build the Docker image
cd python
docker build -t news-assistant-python .

# Run the container
docker run -p 3000:3000 \
  -e NEWS_API_KEY=your_news_api_key \
  -e LLM_API_KEY=your_llm_api_key \
  news-assistant-python
```

### TypeScript Version

```bash
# Build the Docker image
cd typescript
docker build -t news-assistant-typescript .

# Run the container
docker run -p 3000:3000 \
  -e NEWS_API_KEY=your_news_api_key \
  -e LLM_API_KEY=your_llm_api_key \
  news-assistant-typescript
```

### Testing

You can validate that the server works as intended in development using the MCP Inspector https://github.com/modelcontextprotocol/inspector

## MCP Tools

The server should implement the following MCP tools:

1. `search_news`: Search for recent news articles matching a specific query
2. `extract_information_from_article`: Extract structured information from a news article
3. `extract_key_info_and_sentiment`: Analyze news articles for key entities and sentiment

For detailed specifications of each tool, please refer to the assignment documentation.

## Development

Choose either the Python or TypeScript implementation based on your preference. Both implementations provide the same functionality through the MCP interface.

## License

This is a private repository for take-home assignment purposes only.