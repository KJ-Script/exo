"""
Simple web scraper implementation that extracts text content from a webpage.
"""
from typing import Dict, Any
from .web_scraper import WebScraper

class SimpleScraper(WebScraper):
    """A simple web scraper that extracts text content from a webpage."""
    
    async def _scrape(self, **kwargs) -> str:
        """Extract text content from the webpage."""
        # Wait for the page to load
        await self.page.wait_for_load_state("networkidle")
        
        # Get all text content
        content = await self.page.evaluate("""
            () => {
                // Get all text nodes
                const textNodes = document.evaluate(
                    '//text()[normalize-space(.)!=""]',
                    document.body,
                    null,
                    XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
                    null
                );
                
                // Extract text from nodes
                let texts = [];
                for (let i = 0; i < textNodes.snapshotLength; i++) {
                    const node = textNodes.snapshotItem(i);
                    // Skip script and style tags
                    if (!node.parentElement.closest('script, style')) {
                        texts.push(node.textContent.trim());
                    }
                }
                
                return texts.join('\\n');
            }
        """)
        
        return content 