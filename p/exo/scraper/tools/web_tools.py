"""
Web tools for the agent to use.
"""
import logging
from typing import Dict, Any, List, Optional
from exo.agents.tools.scraper import scrape_url, search_and_scrape, close_scraper

logger = logging.getLogger(__name__)

async def web_search(query: str, num_results: int = 3) -> Dict[str, Any]:
    """
    Search the web for information and return the results.
    
    Args:
        query: The search query
        num_results: Number of results to return
        
    Returns:
        Dictionary with search results
    """
    logger.info(f"Web search for: {query}")
    results = await search_and_scrape(query, num_results)
    
    # Format the results for the agent
    formatted_results = []
    for result in results:
        if "error" in result:
            formatted_results.append(f"Error: {result['error']}")
        elif "content" in result:
            # Truncate content to avoid overwhelming the agent
            content = result["content"]
            if len(content) > 1000:
                content = content[:1000] + "..."
            formatted_results.append(f"From {result['url']}:\n{content}")
        elif "results" in result:
            formatted_results.append(f"From {result['url']} ({result['count']} results):")
            for i, item in enumerate(result["results"][:5]):  # Limit to 5 items
                if len(item) > 200:
                    item = item[:200] + "..."
                formatted_results.append(f"  {i+1}. {item}")
    
    return {
        "query": query,
        "results": formatted_results
    }

async def scrape_website(url: str, selector: Optional[str] = None) -> Dict[str, Any]:
    """
    Scrape a specific website.
    
    Args:
        url: The URL to scrape
        selector: CSS selector to target specific elements
        
    Returns:
        Dictionary with scraping results
    """
    logger.info(f"Scraping website: {url}")
    result = await scrape_url(url, selector)
    
    # Format the result for the agent
    if "error" in result:
        return {
            "url": url,
            "error": result["error"]
        }
    elif "content" in result:
        # Truncate content to avoid overwhelming the agent
        content = result["content"]
        if len(content) > 1000:
            content = content[:1000] + "..."
        return {
            "url": url,
            "content": content
        }
    elif "results" in result:
        formatted_results = []
        for i, item in enumerate(result["results"][:5]):  # Limit to 5 items
            if len(item) > 200:
                item = item[:200] + "..."
            formatted_results.append(f"{i+1}. {item}")
        
        return {
            "url": url,
            "selector": selector,
            "count": result["count"],
            "results": formatted_results
        }
    
    return result

# Tool definitions for the agent
WEB_TOOLS = [
    {
        "name": "web_search",
        "description": "Search the web for information on a specific topic",
        "parameters": {
            "query": {
                "type": "string",
                "description": "The search query"
            },
            "num_results": {
                "type": "integer",
                "description": "Number of results to return",
                "default": 3
            }
        },
        "function": web_search
    },
    {
        "name": "scrape_website",
        "description": "Scrape content from a specific website",
        "parameters": {
            "url": {
                "type": "string",
                "description": "The URL to scrape"
            },
            "selector": {
                "type": "string",
                "description": "CSS selector to target specific elements",
                "optional": True
            }
        },
        "function": scrape_website
    }
] 