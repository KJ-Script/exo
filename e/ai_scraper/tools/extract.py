"""
Content extractor tool that uses Playwright to extract content from websites.
"""

import asyncio
from typing import Dict, Any, Optional, List

from playwright.async_api import async_playwright, Browser, Page
from . import Tool

async def extract_content(
    url: str,
    selector: Optional[str] = None,
    headless: bool = True,
    timeout: int = 30000,
    **kwargs
) -> Dict[str, Any]:
    """
    Extract content from a website.
    
    Args:
        url: The URL to extract content from
        selector: Optional CSS selector to target specific elements
        headless: Whether to run the browser in headless mode
        timeout: Timeout in milliseconds for navigation
        **kwargs: Additional arguments to pass to the browser
        
    Returns:
        A dictionary containing the extracted content
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless, **kwargs)
        page = await browser.new_page()
        
        try:
            # Navigate to the URL
            await page.goto(url, timeout=timeout)
            
            # Extract content based on selector or entire page
            if selector:
                # Get elements matching the selector
                elements = await page.query_selector_all(selector)
                texts = []
                
                for element in elements:
                    text = await element.text_content()
                    if text:
                        texts.append(text.strip())
                
                result = {
                    "url": url,
                    "selector": selector,
                    "count": len(texts),
                    "texts": texts
                }
            else:
                # Get all text content from the page
                text = await page.content()
                result = {
                    "url": url,
                    "text": text
                }
            
            return result
            
        finally:
            await browser.close()

# Create the tool
extract_tool = Tool(
    extract_content,
    name="extract_content",
    description="Extract content from a website"
) 