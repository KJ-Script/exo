"""
Web scraping agent that uses a provider and tools to scrape content from websites.
"""

from typing import Any, Dict, List, Optional

from ai_scraper.agents import Agent
from ai_scraper.providers import BaseProvider
from ai_scraper.tools import Tool
from ai_scraper.tools.extract import extract_tool

async def web_scraping_agent(
    provider: BaseProvider,
    tools: List[Tool],
    url: str,
    **kwargs
) -> Dict[str, Any]:
    """
    An agent that scrapes content from websites.
    
    Args:
        provider: The provider to use for generating responses
        tools: List of tools the agent can use
        url: The URL to scrape
        **kwargs: Additional arguments
        
    Returns:
        A dictionary containing the scraped content
    """
    # Step 1: Extract content from the URL
    content = await extract_tool(url=url)
    
    # Step 2: Generate a summary using the provider
    summary_prompt = f"""
    I've scraped the following URL: "{url}"
    
    Here is the content:
    
    {content}
    
    Please provide a summary of the content.
    """
    
    summary = await provider.generate(summary_prompt)
    
    # Return the results
    return {
        "url": url,
        "content": content,
        "summary": summary
    }

# Create the agent instance
web_scraping_agent = Agent(
    web_scraping_agent,
    name="web_scraping_agent",
    description="An agent that scrapes content from websites"
) 