"""
Example of a custom web scraping agent that takes a URL as input.
This example demonstrates how to use the provider and tools without classes.
"""
import asyncio
from typing import Dict, Any
from ..providers.openai import OpenAIProvider
from ..tools.simple_scraper import SimpleScraper

async def create_scraping_agent(api_key: str) -> Dict[str, Any]:
    """Create a scraping agent with OpenAI provider and web scraper tool."""
    # Initialize components
    provider = OpenAIProvider()
    scraper = SimpleScraper()
    
    # Initialize with configuration
    await provider.initialize(api_key=api_key)
    await scraper.initialize(headless=True)
    
    return {
        "provider": provider,
        "scraper": scraper
    }

async def scrape_website(agent: Dict[str, Any], url: str, prompt: str) -> str:
    """Scrape a website and get AI analysis of the content."""
    try:
        # First, scrape the website
        content = await agent["scraper"].execute(url=url)
        
        # Then, use the AI provider to analyze the content
        analysis_prompt = f"""
        Analyze the following website content and provide a summary:
        
        URL: {url}
        Content: {content}
        
        Task: {prompt}
        """
        
        analysis = await agent["provider"].generate(analysis_prompt)
        return analysis
        
    except Exception as e:
        return f"Error during scraping: {str(e)}"

async def main():
    # Example usage
    api_key = "your-openai-api-key"  # Replace with actual API key
    url = input("Enter the website URL to scrape: ")
    prompt = input("Enter what you want to know about the website: ")
    
    # Create the agent
    agent = await create_scraping_agent(api_key)
    
    try:
        # Scrape and analyze
        result = await scrape_website(agent, url, prompt)
        print("\nAnalysis Result:")
        print(result)
        
    finally:
        # Clean up resources
        await agent["provider"].close()
        await agent["scraper"].close()

if __name__ == "__main__":
    asyncio.run(main()) 