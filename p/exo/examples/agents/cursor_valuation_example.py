"""
Example demonstrating how to use the web agent to scrape Cursor's valuation history.
"""
import asyncio
import logging
import argparse
from exo.agents.web_agent import WebAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def scrape_cursor_valuation(model_name: str = "meta-llama/Llama-2-7b-chat-hf"):
    """
    Use the web agent to scrape Cursor's valuation history.
    
    Args:
        model_name: The name of the Hugging Face model to use
    """
    agent = WebAgent(model_name=model_name)
    
    try:
        # Initial query to get general information about Cursor
        initial_query = "What is Cursor code editor and when was it founded?"
        logger.info(f"Query: {initial_query}")
        initial_response = await agent.process_message(initial_query)
        logger.info(f"Response: {initial_response}")
        
        # Query specifically about valuation history
        valuation_query = "What is the valuation history of Cursor code editor? Include funding rounds, investors, and dates."
        logger.info(f"Query: {valuation_query}")
        valuation_response = await agent.process_message(valuation_query)
        logger.info(f"Response: {valuation_response}")
        
        # Query about recent developments
        recent_query = "What are the most recent developments or funding news about Cursor code editor?"
        logger.info(f"Query: {recent_query}")
        recent_response = await agent.process_message(recent_query)
        logger.info(f"Response: {recent_response}")
        
        # Query about competitors and market position
        market_query = "How does Cursor's valuation compare to its competitors in the AI code editor market?"
        logger.info(f"Query: {market_query}")
        market_response = await agent.process_message(market_query)
        logger.info(f"Response: {market_response}")
        
        # Compile all information
        summary_query = "Based on all the information gathered, provide a comprehensive summary of Cursor's valuation history, funding rounds, and current market position."
        logger.info(f"Query: {summary_query}")
        summary_response = await agent.process_message(summary_query)
        logger.info(f"Final Summary: {summary_response}")
        
    finally:
        await agent.close()

async def main():
    parser = argparse.ArgumentParser(description="Cursor Valuation History Scraper")
    parser.add_argument("--model", type=str, default="meta-llama/Llama-2-7b-chat-hf",
                        help="Hugging Face model to use")
    args = parser.parse_args()
    
    await scrape_cursor_valuation(args.model)

if __name__ == "__main__":
    asyncio.run(main()) 