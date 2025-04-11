"""
Example demonstrating how to use the web tools.
"""
import asyncio
import logging
from exo.tools.web_tools import web_search, scrape_website

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def web_search_example():
    """Example of using the web search tool."""
    query = "Latest AI developments"
    logger.info(f"Performing web search for: {query}")
    
    result = await web_search(query, num_results=3)
    logger.info("Search results:")
    logger.info(result)

async def scrape_website_example():
    """Example of using the website scraping tool."""
    url = "https://example.com"
    selector = "article"  # Example CSS selector
    logger.info(f"Scraping website: {url}")
    
    result = await scrape_website(url, selector)
    logger.info("Scraping result:")
    logger.info(result)

async def main():
    # Run web search example
    await web_search_example()
    
    # Run website scraping example
    await scrape_website_example()

if __name__ == "__main__":
    asyncio.run(main()) 