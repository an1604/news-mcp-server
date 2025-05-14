# Tests Directory

This directory contains the test suite for the GenAI News Assistant MCP Server. The tests ensure that all components of the application work correctly, both individually (unit tests) and together (integration tests).

## Current Test Coverage

The test suite currently provides **86% code coverage** across the codebase, with particularly strong coverage in:
- Configuration management (100%)
- News search tools (94%)
- Article extraction tools (90%)
- Sentiment analysis tools (90%)

## Test Structure

The test files are organized to match the structure of the source code:

- **Configuration Tests**
  - `test_config.py` - Tests for environment variable loading and configuration management

- **Core Service Tests**
  - `test_main.py` - Tests for the MCP server initialization and startup
  - `test_llm_service.py` - Tests for the LLM integration service

- **Tool-specific Tests**
  - `test_search_news_api.py` - Integration tests for the NewsAPI client
  - `test_search_news_method.py` - Tests for the search_news tool implementation
  - `test_extract_tool.py` - Tests for the article information extraction tool
  - `test_sentiment_tool.py` - Tests for the sentiment analysis tool

- **Edge Cases**
  - `test_tools_edge_cases.py` - Tests for error handling and edge cases in the tools

- **Support Files**
  - `conftest.py` - Shared pytest fixtures and configuration
  - `pytest.ini` - Pytest configuration settings

## Running Tests

### Basic Test Run

To run all tests:

```bash
cd python
pytest
```

### Code Coverage

To run tests with coverage reporting:

```bash
cd python
pytest --cov=src tests/
```

For a detailed HTML coverage report:

```bash
cd python
pytest --cov=src --cov-report=html tests/
```

This creates a `htmlcov` directory with an interactive coverage report.

### Running Specific Tests

Run tests from a specific file:

```bash
pytest tests/test_config.py
```

Run a specific test:

```bash
pytest tests/test_config.py::TestConfig::test_environment_variables
```

### Continuous Integration

The test suite is integrated with GitHub Actions to ensure code quality on each push.

## Test Categories

The tests are organized into these categories:

1. **Unit Tests** - Testing individual components in isolation
2. **Integration Tests** - Testing interactions between components
3. **API Tests** - Testing external API interactions (NewsAPI, OpenAI)
4. **Error Handling Tests** - Testing error conditions and edge cases
