import pytest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestMainModule:
    """Tests for the main module that starts the MCP server."""
    
    def setup_method(self):
        """Set up the test by patching modules."""
        if 'src.main' in sys.modules:
            del sys.modules['src.main']
        
        # Create the mock modules
        self.mock_search_news = MagicMock()
        self.mock_extract_tool = MagicMock()
        self.mock_sentiment_tool = MagicMock()
        self.mock_config = MagicMock()
        self.mock_config.PORT = 3000
    
    @pytest.mark.skip_if_no_openai
    @patch('fastmcp.FastMCP')
    def test_mcp_initialization(self, mock_fast_mcp):
        """Test that the MCP server is initialized correctly."""
        mock_mcp = MagicMock()
        mock_fast_mcp.return_value = mock_mcp
        
        mock_modules = {
            'config': self.mock_config,
            'tools.search_news': MagicMock(search_news=self.mock_search_news),
            'tools.extract_tool': MagicMock(extract_information_from_article=self.mock_extract_tool),
            'tools.sentiment_tool': MagicMock(extract_key_info_and_sentiment=self.mock_sentiment_tool)
        }
        
        with patch.dict('sys.modules', mock_modules):
            with patch('src.main.search_news', self.mock_search_news):
                with patch('src.main.extract_information_from_article', self.mock_extract_tool):
                    with patch('src.main.extract_key_info_and_sentiment', self.mock_sentiment_tool):
                        from src import main
                        
                        mock_fast_mcp.assert_called_once_with("news_assistant_mcp")
                        
                        assert mock_mcp.tool.call_count == 3
                        mock_mcp.run.assert_not_called()
    
    @pytest.mark.skip_if_no_openai
    @patch('fastmcp.FastMCP')
    def test_mcp_run(self, mock_fast_mcp):
        """Test that the MCP server runs with the correct parameters when executed as script."""
        mock_mcp = MagicMock()
        mock_fast_mcp.return_value = mock_mcp
        
        # Fix path to main.py - use more specific path construction
        main_file_path = os.path.abspath(os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
            'src', 
            'main.py'
        ))
        
        # Skip test if main.py doesn't exist
        if not os.path.exists(main_file_path):
            pytest.skip(f"Skipping test as main.py not found at {main_file_path}")
        
        module_globals = {
            '__name__': '__main__',
            '__file__': main_file_path,
            'FastMCP': mock_fast_mcp,
            'logging': MagicMock(),
            'os': os,
            'sys': sys,
            'config': self.mock_config,
            'search_news': self.mock_search_news,
            'extract_information_from_article': self.mock_extract_tool,
            'extract_key_info_and_sentiment': self.mock_sentiment_tool
        }
        
        with open(main_file_path, 'r') as f:
            main_code = f.read()
            
        exec(main_code, module_globals)
        
        mock_mcp.run.assert_called_once_with(
            transport="sse", 
            host="0.0.0.0", 
            port=3000, 
            path="/"
        )