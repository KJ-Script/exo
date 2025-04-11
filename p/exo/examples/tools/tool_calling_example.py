"""
Example demonstrating how to use providers with tool calling (web search and web scraping).
"""
import asyncio
import os
import logging
from typing import Dict, Any, List

from exo.providers.openai import OpenAIProvider
from exo.agents.web_agent import WebAgent
from exo.scraper.tools import web_search, scrape_website

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_web_search_example(api_key: str = None) -> None:
    """
    Run an example of web search using a provider.
    
    Args:
        api_key: API key for the provider (if required)
    """
    # Create provider instance
    provider = OpenAIProvider()
    config = {"api_key": api_key or os.environ.get("OPENAI_API_KEY")}
    
    try:
        # Initialize the provider
        await provider.initialize(**config)
        logger.info("Initialized OpenAI provider")
        
        # Create a web agent with the provider
        agent = WebAgent(provider=provider)
        await agent.initialize()
        logger.info("Initialized WebAgent")
        
        # Example query for web search
        query = "What are the latest developments in quantum computing?"
        logger.info(f"Sending query: {query}")
        
        # Process the message with the agent
        response = await agent.process_message(query)
        logger.info("Response from WebAgent:")
        print(response)
        
    except Exception as e:
        logger.error(f"Error in web search example: {e}")
    finally:
        # Clean up
        await agent.close()
        logger.info("Closed WebAgent")

async def run_web_scraping_example(api_key: str = None) -> None:
    """
    Run an example of web scraping using a provider.
    
    Args:
        api_key: API key for the provider (if required)
    """
    # Create provider instance
    provider = OpenAIProvider()
    config = {"api_key": api_key or os.environ.get("OPENAI_API_KEY")}
    
    try:
        # Initialize the provider
        await provider.initialize(**config)
        logger.info("Initialized OpenAI provider")
        
        # Create a web agent with the provider
        agent = WebAgent(provider=provider)
        await agent.initialize()
        logger.info("Initialized WebAgent")
        
        # Example query for web scraping
        query = "What is the current price of Bitcoin on CoinGecko?"
        logger.info(f"Sending query: {query}")
        
        # Process the message with the agent
        response = await agent.process_message(query)
        logger.info("Response from WebAgent:")
        print(response)
        
    except Exception as e:
        logger.error(f"Error in web scraping example: {e}")
    finally:
        # Clean up
        await agent.close()
        logger.info("Closed WebAgent")

async def main():
    """Run examples of tool calling."""
    # Example of web search
    await run_web_search_example()
    
    # Example of web scraping
    await run_web_scraping_example()

if __name__ == "__main__":
    asyncio.run(main()) 