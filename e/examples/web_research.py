"""
Example script demonstrating how to use the AI Scraper library.
"""

import asyncio
import os
from typing import Dict, Any

from ai_scraper.agents.web_research_agent import WebResearchAgent
from ai_scraper.providers.ollama import OllamaProvider
from ai_scraper.providers.gemini import GeminiProvider

async def main():
    """Run the example."""
    # Choose a provider
    provider_type = input("Choose a provider (ollama/gemini): ").lower()
    
    if provider_type == "ollama":
        # Initialize the Ollama provider
        provider = OllamaProvider(model="llama2")
    elif provider_type == "gemini":
        # Get the API key from environment variable
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Error: GEMINI_API_KEY environment variable not set")
            return
        
        # Initialize the Gemini provider
        provider = GeminiProvider(api_key=api_key)
    else:
        print(f"Error: Unknown provider '{provider_type}'")
        return
    
    # Initialize the agent
    agent = WebResearchAgent(provider=provider, max_results=3)
    
    # Get the query from the user
    query = input("Enter your research query: ")
    
    # Run the agent
    print(f"Researching: {query}")
    results = await agent.run(query=query)
    
    # Print the results
    print("\nSearch Results:")
    for result in results["search_results"]:
        print(f"- {result['title']}: {result['url']}")
    
    print("\nSummary:")
    print(results["summary"])

if __name__ == "__main__":
    asyncio.run(main()) 