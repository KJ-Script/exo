"""
Base web scraper tool using Playwright.
"""
from typing import Dict, Any, Optional
from playwright.async_api import async_playwright, Browser, Page
from .base import BaseTool

class WebScraper(BaseTool):
    """Base class for web scraping tools using Playwright."""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.playwright = None
    
    async def initialize(self, **kwargs) -> None:
        """Initialize the web scraper with Playwright."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=kwargs.get('headless', True)
        )
        self.page = await self.browser.new_page()
    
    async def execute(self, **kwargs) -> Any:
        """Execute the web scraping operation."""
        if not self.page:
            raise RuntimeError("Web scraper not initialized. Call initialize() first.")
        
        url = kwargs.get('url')
        if not url:
            raise ValueError("URL is required for web scraping")
        
        await self.page.goto(url)
        return await self._scrape(**kwargs)
    
    async def _scrape(self, **kwargs) -> Any:
        """Implement specific scraping logic in subclasses."""
        raise NotImplementedError("Subclasses must implement _scrape method")
    
    async def get_tool_info(self) -> Dict[str, Any]:
        """Get information about the web scraper."""
        return {
            "name": self.__class__.__name__,
            "type": "web_scraper",
            "browser": "chromium",
            "initialized": self.browser is not None
        }
    
    async def close(self) -> None:
        """Clean up Playwright resources."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        self.browser = None
        self.page = None
        self.playwright = None 