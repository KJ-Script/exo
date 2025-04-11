"""
Search tool that uses Playwright to search the internet.
"""

import asyncio
from typing import List, Dict, Any, Optional

from playwright.async_api import async_playwright, Browser, Page
from . import Tool

async def search_web(
    query: str,
    num_results: int = 5,
    headless: bool = True,
    **kwargs
) -> List[Dict[str, str]]:
    """
    Search the web for a query and return relevant URLs.
    
    Args:
        query: The search query
        num_results: Number of results to return
        headless: Whether to run the browser in headless mode
        **kwargs: Additional arguments to pass to the browser
        
    Returns:
        A list of dictionaries containing search results
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless, **kwargs)
        page = await browser.new_page()
        
        # Navigate to Google
        await page.goto("https://www.google.com")
        
        # Accept cookies if the dialog appears
        try:
            await page.click('button:has-text("Accept all")')
        except:
            pass
        
        # Type the search query
        await page.fill('textarea[name="q"]', query)
        await page.press('textarea[name="q"]', "Enter")
        
        # Wait for results
        await page.wait_for_selector("div#search")
        
        # Extract search results
        results = []
        elements = await page.query_selector_all("div.g")
        
        for element in elements[:num_results]:
            try:
                title_element = await element.query_selector("h3")
                link_element = await element.query_selector("a")
                
                if title_element and link_element:
                    title = await title_element.text_content()
                    url = await link_element.get_attribute("href")
                    
                    if title and url:
                        results.append({
                            "title": title.strip(),
                            "url": url
                        })
            except:
                continue
        
        await browser.close()
        return results

# Create the tool
search_tool = Tool(
    search_web,
    name="web_search",
    description="Search the web for a query and return relevant URLs"
) 