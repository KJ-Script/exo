"""
Example demonstrating how to use the web tools to scrape Cursor's valuation history.
"""
import asyncio
import logging
import json
from exo.tools.web_tools import web_search, scrape_website

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def search_cursor_info():
    """Search for general information about Cursor."""
    query = "Cursor code editor company information founding date"
    logger.info(f"Searching for: {query}")
    
    result = await web_search(query, num_results=5)
    logger.info("Search results:")
    logger.info(result)
    return result

async def search_cursor_valuation():
    """Search specifically for Cursor's valuation history."""
    query = "Cursor code editor valuation funding rounds investors"
    logger.info(f"Searching for: {query}")
    
    result = await web_search(query, num_results=5)
    logger.info("Search results:")
    logger.info(result)
    return result

async def search_cursor_recent_news():
    """Search for recent news about Cursor."""
    query = "Cursor code editor latest news funding 2023 2024"
    logger.info(f"Searching for: {query}")
    
    result = await web_search(query, num_results=3)
    logger.info("Search results:")
    logger.info(result)
    return result

async def scrape_cursor_website():
    """Scrape Cursor's official website for information."""
    url = "https://cursor.sh"
    logger.info(f"Scraping website: {url}")
    
    result = await scrape_website(url)
    logger.info("Scraping result:")
    logger.info(result)
    return result

async def scrape_crunchbase():
    """Scrape Crunchbase for Cursor's funding information."""
    url = "https://www.crunchbase.com/organization/cursor-ai"
    logger.info(f"Scraping website: {url}")
    
    result = await scrape_website(url, selector=".funding-rounds")
    logger.info("Scraping result:")
    logger.info(result)
    return result

async def main():
    # Collect information from various sources
    cursor_info = await search_cursor_info()
    cursor_valuation = await search_cursor_valuation()
    cursor_recent_news = await search_cursor_recent_news()
    
    # Try to scrape specific websites
    try:
        cursor_website = await scrape_cursor_website()
    except Exception as e:
        logger.error(f"Error scraping Cursor website: {e}")
        cursor_website = "Failed to scrape Cursor website"
    
    try:
        crunchbase_info = await scrape_crunchbase()
    except Exception as e:
        logger.error(f"Error scraping Crunchbase: {e}")
        crunchbase_info = "Failed to scrape Crunchbase"
    
    # Compile all information
    all_info = {
        "general_info": cursor_info,
        "valuation_history": cursor_valuation,
        "recent_news": cursor_recent_news,
        "website_info": cursor_website,
        "crunchbase_info": crunchbase_info
    }
    
    # Save to file
    with open("cursor_valuation_data.json", "w") as f:
        json.dump(all_info, f, indent=2)
    
    logger.info("All information has been collected and saved to cursor_valuation_data.json")

if __name__ == "__main__":
    asyncio.run(main()) 