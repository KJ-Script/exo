"""
Example demonstrating how to use the web scraper tool.
"""
import asyncio
import logging
from exo.tools.scraper import WebScraper, scrape_url, search_and_scrape

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def scrape_example():
    """Example of basic URL scraping."""
    url = "https://example.com"
    logger.info(f"Scraping URL: {url}")
    
    result = await scrape_url(url)
    logger.info("Scraping result:")
    logger.info(result)

async def search_example():
    """Example of search and scrape functionality."""
    query = "Python programming"
    logger.info(f"Searching for: {query}")
    
    results = await search_and_scrape(query, num_results=3)
    logger.info("Search results:")
    for i, result in enumerate(results, 1):
        logger.info(f"\nResult {i}:")
        logger.info(result)

async def advanced_scraping_example():
    """Example of advanced scraping with selectors."""
    scraper = WebScraper()
    try:
        # Scrape a specific element using CSS selector
        url = "https://example.com"
        selector = "h1"
        logger.info(f"Scraping element '{selector}' from {url}")
        
        result = await scraper.scrape_url(
            url=url,
            selector=selector,
            wait_for="h1",
            extract_text=True
        )
        logger.info("Scraping result:")
        logger.info(result)
        
    finally:
        await scraper.close()

async def main():
    # Run basic scraping example
    await scrape_example()
    
    # Run search example
    await search_example()
    
    # Run advanced scraping example
    await advanced_scraping_example()

if __name__ == "__main__":
    asyncio.run(main()) 