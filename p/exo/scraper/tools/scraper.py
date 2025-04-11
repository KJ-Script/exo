"""
Web scraping tool using Playwright.
"""
import logging
import asyncio
from typing import Dict, Any, Optional, List
from playwright.async_api import async_playwright, Browser, Page

logger = logging.getLogger(__name__)

class WebScraper:
    """
    Web scraping tool using Playwright.
    """
    
    def __init__(self):
        """Initialize the web scraper."""
        self.browser = None
        self.context = None
        self.page = None
        logger.info("Initialized WebScraper")
    
    async def _ensure_browser(self):
        """Ensure the browser is initialized."""
        if self.browser is None:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(headless=True)
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
            logger.info("Browser initialized")
    
    async def scrape_url(self, url: str, selector: Optional[str] = None, 
                         wait_for: Optional[str] = None, 
                         extract_text: bool = True) -> Dict[str, Any]:
        """
        Scrape content from a URL.
        
        Args:
            url: The URL to scrape
            selector: CSS selector to target specific elements
            wait_for: Selector to wait for before scraping
            extract_text: Whether to extract text content
            
        Returns:
            Dictionary with scraping results
        """
        await self._ensure_browser()
        
        try:
            logger.info(f"Scraping URL: {url}")
            await self.page.goto(url, wait_until="networkidle")
            
            if wait_for:
                await self.page.wait_for_selector(wait_for)
            
            if selector:
                elements = await self.page.query_selector_all(selector)
                results = []
                
                for element in elements:
                    if extract_text:
                        text = await element.text_content()
                        results.append(text.strip())
                    else:
                        html = await element.inner_html()
                        results.append(html)
                
                return {
                    "url": url,
                    "selector": selector,
                    "count": len(results),
                    "results": results
                }
            else:
                # Scrape the entire page
                if extract_text:
                    content = await self.page.text_content()
                else:
                    content = await self.page.content()
                
                return {
                    "url": url,
                    "content": content
                }
                
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return {
                "url": url,
                "error": str(e)
            }
    
    async def search_and_scrape(self, query: str, num_results: int = 3) -> List[Dict[str, Any]]:
        """
        Search for a query and scrape the top results.
        
        Args:
            query: The search query
            num_results: Number of results to scrape
            
        Returns:
            List of scraping results
        """
        await self._ensure_browser()
        
        try:
            # Use Google search
            search_url = f"https://www.google.com/search?q={query}"
            logger.info(f"Searching for: {query}")
            
            await self.page.goto(search_url, wait_until="networkidle")
            
            # Extract search results
            results = []
            search_results = await self.page.query_selector_all("div.g")
            
            for i, result in enumerate(search_results[:num_results]):
                try:
                    link_element = await result.query_selector("a")
                    if link_element:
                        href = await link_element.get_attribute("href")
                        if href and href.startswith("http"):
                            # Scrape the actual page
                            scrape_result = await self.scrape_url(href)
                            results.append(scrape_result)
                except Exception as e:
                    logger.error(f"Error processing search result: {e}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error during search: {e}")
            return [{"error": str(e)}]
    
    async def close(self):
        """Close the browser."""
        if self.browser:
            await self.browser.close()
            self.browser = None
            self.context = None
            self.page = None
            logger.info("Browser closed")

# Singleton instance
_scraper = None

async def get_scraper() -> WebScraper:
    """Get the singleton scraper instance."""
    global _scraper
    if _scraper is None:
        _scraper = WebScraper()
    return _scraper

async def scrape_url(url: str, selector: Optional[str] = None, 
                    wait_for: Optional[str] = None, 
                    extract_text: bool = True) -> Dict[str, Any]:
    """Convenience function to scrape a URL."""
    scraper = await get_scraper()
    return await scraper.scrape_url(url, selector, wait_for, extract_text)

async def search_and_scrape(query: str, num_results: int = 3) -> List[Dict[str, Any]]:
    """Convenience function to search and scrape."""
    scraper = await get_scraper()
    return await scraper.search_and_scrape(query, num_results)

async def close_scraper():
    """Close the scraper."""
    global _scraper
    if _scraper:
        await _scraper.close()
        _scraper = None 