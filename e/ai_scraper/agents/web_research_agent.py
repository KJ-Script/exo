"""
Web research agent that uses a provider and tools to research topics on the web.
"""

from typing import Any, Dict, List, Optional

from ai_scraper.agents import Agent
from ai_scraper.providers import BaseProvider
from ai_scraper.tools import Tool
from ai_scraper.tools.search import search_tool
from ai_scraper.tools.extract import extract_tool

async def web_research_agent(
    provider: BaseProvider,
    tools: List[Tool],
    query: str,
    max_results: int = 5,
    **kwargs
) -> Dict[str, Any]:
    """
    An agent that researches topics on the web.
    
    Args:
        provider: The provider to use for generating responses
        tools: List of tools the agent can use
        query: The search query
        max_results: Maximum number of search results to process
        **kwargs: Additional arguments
        
    Returns:
        A dictionary containing the research results
    """
    # Step 1: Search the web for the query
    search_results = await search_tool(query=query, max_results=max_results)
    
    # Step 2: Extract content from each search result
    contents = []
    for result in search_results:
        content = await extract_tool(url=result["url"])
        contents.append({
            "url": result["url"],
            "title": result["title"],
            "content": content
        })
    
    # Step 3: Generate a summary using the provider
    summary_prompt = f"""
    I've researched the following query: "{query}"
    
    Here are the search results:
    
    {contents}
    
    Please provide a comprehensive summary of the research results.
    """
    
    summary = await provider.generate(summary_prompt)
    
    # Return the results
    return {
        "query": query,
        "search_results": search_results,
        "contents": contents,
        "summary": summary
    }

# Create the agent instance
web_research_agent = Agent(
    web_research_agent,
    name="web_research_agent",
    description="An agent that researches topics on the web"
) 