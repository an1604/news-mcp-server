import logging
from typing import Dict, Any
import os

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

from src.config import config

logger = logging.getLogger(__name__)

EXTRACT_INFO_SCHEMAS = [
    ResponseSchema(name="people", description="List of people mentioned in the article", type="list"),
    ResponseSchema(name="organizations", description="List of organizations mentioned in the article", type="list"),
    ResponseSchema(name="locations", description="List of locations mentioned in the article", type="list"),
    ResponseSchema(name="key_quotes", description="List of important quotes from the article", type="list")
]

SENTIMENT_ANALYSIS_SCHEMAS = [
    ResponseSchema(name="overall_sentiment", description="Overall sentiment of the articles: positive, negative, or neutral", type="string"),
    ResponseSchema(name="sentiment_confidence", description="Confidence level of the sentiment analysis: high, medium, or low", type="string"),
    ResponseSchema(name="key_entities", description="Dictionary containing lists of people, organizations, and locations mentioned", type="object"),
    ResponseSchema(name="key_takeaway_summary", description="A brief summary of the key takeaways from the articles", type="string")
]

class LLMService:
    """Service for interacting with language models for text analysis and generation."""
    
    def __init__(self):
        """Initialize the LLM service with OpenAI."""
        self.llm = self._initialize_llm()
        self.extract_parser = StructuredOutputParser.from_response_schemas(EXTRACT_INFO_SCHEMAS)
        self.sentiment_parser = StructuredOutputParser.from_response_schemas(SENTIMENT_ANALYSIS_SCHEMAS)
        logger.info("Initialized LLM service with OpenAI model")
    
    def _initialize_llm(self) -> ChatOpenAI:
        """Initialize the OpenAI language model."""
        try:
            if not config.OPENAI_API_KEY:
                raise ValueError("No OpenAI API key provided in configuration")
                
            return ChatOpenAI(
                temperature=config.TEMPERATURE,
                model_name="gpt-4o-mini",
                openai_api_key=config.OPENAI_API_KEY
            )
                
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI LLM: {str(e)}")
            raise
    
    def extract_article_information(self, title: str, description: str) -> Dict[str, Any]:
        """
        Extract structured information from a news article.
        
        Args:
            title: The article title
            description: The article description
            
        Returns:
            Dictionary with extracted entities and quotes
            
        Raises:
            Exception: If the LLM fails to generate a valid response or the parsing fails
        """
        format_instructions = self.extract_parser.get_format_instructions()
        
        template = """
        Analyze the following news article and extract key information into a structured format:

        Title: {title}
        Description: {description}

        {format_instructions}
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["title", "description"],
            partial_variables={"format_instructions": format_instructions}
        )
        
        formatted_prompt = prompt.format(title=title, description=description)
        
        try:
            logger.info(f"Extracting information from article: {title}")
            response = self.llm.invoke(formatted_prompt)
            
            try:
                return self.extract_parser.parse(response.content)
            except Exception as parse_error:
                error_msg = f"Failed to parse LLM response: {str(parse_error)}"
                logger.error(error_msg)
                raise ValueError(error_msg)
                
        except Exception as e:
            error_msg = f"Error extracting information from article: {str(e)}"
            logger.error(error_msg)
            raise
    
    def analyze_sentiment(self, query: str, articles: list) -> Dict[str, Any]:
        """
        Analyze sentiment and extract key information from multiple articles.
        
        Args:
            query: The original search query
            articles: List of article dictionaries with title and description
            
        Returns:
            Dictionary with sentiment analysis and key information
            
        Raises:
            Exception: If the LLM fails to generate a valid response or the parsing fails
        """
        format_instructions = self.sentiment_parser.get_format_instructions()
        
        articles_text = "\n\n".join([
            f"Article {i+1}:\nTitle: {article['title']}\n"
            f"Description: {article['description']}"
            for i, article in enumerate(articles)
        ])
        
        template = """
        Analyze the following news articles about "{query}" and determine the overall sentiment as well as key entities:

        Articles:
        {articles}

        In your analysis, provide:
        1. Overall sentiment (positive, negative, or neutral)
        2. Sentiment confidence (high, medium, or low)
        3. Key entities mentioned (people, organizations, locations)
        4. A brief summary of the key takeaways

        {format_instructions}
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["query", "articles"],
            partial_variables={"format_instructions": format_instructions}
        )
        
        formatted_prompt = prompt.format(query=query, articles=articles_text)
        
        try:
            logger.info(f"Analyzing sentiment for query: {query}")
            response = self.llm.invoke(formatted_prompt)
            
            try:
                return self.sentiment_parser.parse(response.content)
            except Exception as parse_error:
                error_msg = f"Failed to parse sentiment analysis response: {str(parse_error)}"
                logger.error(error_msg)
                raise ValueError(error_msg)
                
        except Exception as e:
            error_msg = f"Error analyzing sentiment for query '{query}': {str(e)}"
            logger.error(error_msg)
            raise


llm_service = LLMService()
