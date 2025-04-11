"""
Example script demonstrating how to use the web research agent.
"""

import asyncio
from ai_scraper.agents.web_research_agent import web_research_agent
from ai_scraper.providers.openai import OpenAIProvider

async def main():
    # Initialize the Gemini provider with your API key and custom settings
    provider = GeminiProvider(
        api_key="your-api-key-here",
        model="gemini-pro-vision",  # Using vision model instead of default
        temperature=0.7,  # Add some creativity
        top_p=0.9,  # Control response diversity
        max_output_tokens=2048  # Allow longer responses
    )
    
    # Create a list of tools (in this case, we don't need to pass any as they're used internally)
    tools = []
    
    # Example research query
    query = "What are the latest developments in artificial intelligence?"
    
    try:
        # Run the web research agent
        results = await web_research_agent(
            provider=provider,
            tools=tools,
            query=query,
            max_results=3  # Limit to 3 results for this example
        )
        
        # Print the results in a structured way
        print("\n=== Research Results ===")
        print(f"Query: {results['query']}\n")
        
        print("=== Search Results ===")
        for i, result in enumerate(results['search_results'], 1):
            print(f"\n{i}. {result['title']}")
            print(f"   URL: {result['url']}")
        
        print("\n=== Content Summaries ===")
        for i, content in enumerate(results['contents'], 1):
            print(f"\n{i}. {content['title']}")
            print(f"   URL: {content['url']}")
            print(f"   Content Preview: {content['content'][:200]}...")
        
        print("\n=== Overall Summary ===")
        print(results['summary'])
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main()) 