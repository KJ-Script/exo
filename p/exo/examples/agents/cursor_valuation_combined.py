"""
Example demonstrating how to use both the web agent and web tools to analyze Cursor's valuation history.
"""
import asyncio
import logging
import json
import argparse
from exo.agents.web_agent import WebAgent
from exo.tools.web_tools import web_search, scrape_website

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def collect_raw_data():
    """Collect raw data using web tools."""
    logger.info("Collecting raw data using web tools...")
    
    # Search for general information
    general_query = "Cursor code editor company information founding date"
    general_results = await web_search(general_query, num_results=3)
    
    # Search for valuation information
    valuation_query = "Cursor code editor valuation funding rounds investors"
    valuation_results = await web_search(valuation_query, num_results=3)
    
    # Search for recent news
    news_query = "Cursor code editor latest news funding 2023 2024"
    news_results = await web_search(news_query, num_results=3)
    
    # Try to scrape specific websites
    try:
        cursor_website = await scrape_website("https://cursor.sh")
    except Exception as e:
        logger.error(f"Error scraping Cursor website: {e}")
        cursor_website = "Failed to scrape Cursor website"
    
    # Compile raw data
    raw_data = {
        "general_info": general_results,
        "valuation_info": valuation_results,
        "recent_news": news_results,
        "website_info": cursor_website
    }
    
    return raw_data

async def analyze_with_agent(raw_data, model_name):
    """Analyze the raw data using the web agent."""
    logger.info("Analyzing data using web agent...")
    
    agent = WebAgent(model_name=model_name)
    
    try:
        # Convert raw data to a format the agent can understand
        data_str = json.dumps(raw_data, indent=2)
        
        # Ask the agent to analyze the general information
        general_analysis_query = f"""
        Based on the following information about Cursor code editor, provide a summary of what Cursor is and when it was founded:
        
        {data_str}
        """
        general_analysis = await agent.process_message(general_analysis_query)
        logger.info("General Analysis:")
        logger.info(general_analysis)
        
        # Ask the agent to analyze the valuation information
        valuation_analysis_query = f"""
        Based on the following information, provide a detailed analysis of Cursor's valuation history, including funding rounds, investors, and dates:
        
        {data_str}
        """
        valuation_analysis = await agent.process_message(valuation_analysis_query)
        logger.info("Valuation Analysis:")
        logger.info(valuation_analysis)
        
        # Ask the agent to analyze recent developments
        recent_analysis_query = f"""
        Based on the following information, summarize the most recent developments and news about Cursor:
        
        {data_str}
        """
        recent_analysis = await agent.process_message(recent_analysis_query)
        logger.info("Recent Developments Analysis:")
        logger.info(recent_analysis)
        
        # Ask the agent to compare with competitors
        competitor_analysis_query = f"""
        Based on the following information, compare Cursor's valuation and market position with its competitors in the AI code editor market:
        
        {data_str}
        """
        competitor_analysis = await agent.process_message(competitor_analysis_query)
        logger.info("Competitor Analysis:")
        logger.info(competitor_analysis)
        
        # Ask the agent to provide a comprehensive summary
        summary_query = f"""
        Based on all the information provided, create a comprehensive summary of Cursor's valuation history, funding rounds, and current market position. Include a timeline of key events.
        
        {data_str}
        """
        summary = await agent.process_message(summary_query)
        logger.info("Comprehensive Summary:")
        logger.info(summary)
        
        # Compile all analyses
        analyses = {
            "general_analysis": general_analysis,
            "valuation_analysis": valuation_analysis,
            "recent_developments": recent_analysis,
            "competitor_analysis": competitor_analysis,
            "comprehensive_summary": summary
        }
        
        return analyses
    
    finally:
        await agent.close()

async def main():
    parser = argparse.ArgumentParser(description="Cursor Valuation History Analyzer")
    parser.add_argument("--model", type=str, default="meta-llama/Llama-2-7b-chat-hf",
                        help="Hugging Face model to use")
    parser.add_argument("--output", type=str, default="cursor_valuation_analysis.json",
                        help="Output file for the analysis")
    args = parser.parse_args()
    
    # Collect raw data
    raw_data = await collect_raw_data()
    
    # Analyze with agent
    analyses = await analyze_with_agent(raw_data, args.model)
    
    # Combine raw data and analyses
    final_output = {
        "raw_data": raw_data,
        "analyses": analyses
    }
    
    # Save to file
    with open(args.output, "w") as f:
        json.dump(final_output, f, indent=2)
    
    logger.info(f"Analysis complete. Results saved to {args.output}")

if __name__ == "__main__":
    asyncio.run(main()) 