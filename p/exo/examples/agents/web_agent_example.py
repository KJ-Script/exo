"""
Example demonstrating how to use the web agent with Hugging Face and Playwright.
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

async def interactive_session(model_name: str = "meta-llama/Llama-2-7b-chat-hf"):
    """
    Run an interactive session with the web agent.
    
    Args:
        model_name: The name of the Hugging Face model to use
    """
    agent = WebAgent(model_name=model_name)
    
    try:
        print("\n=== Web Agent Interactive Session ===")
        print("Type 'exit' to quit the session.")
        print("Ask any question, and the agent will search the web for answers.\n")
        
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit", "q"]:
                break
            
            print("\nAgent is thinking...")
            response = await agent.process_message(user_input)
            print(f"\nAgent: {response}")
    
    finally:
        await agent.close()
        print("\nSession ended.")

async def run_example_queries(model_name: str = "meta-llama/Llama-2-7b-chat-hf"):
    """
    Run some example queries with the web agent.
    
    Args:
        model_name: The name of the Hugging Face model to use
    """
    agent = WebAgent(model_name=model_name)
    
    try:
        example_queries = [
            "What are the latest news about artificial intelligence?",
            "What is the current weather in New York?",
            "Who won the last World Cup?",
            "What are the top 3 movies right now?",
            "Tell me about the latest iPhone model."
        ]
        
        for query in example_queries:
            print(f"\n\nQuery: {query}")
            print("Agent is thinking...")
            response = await agent.process_message(query)
            print(f"\nAgent: {response}")
    
    finally:
        await agent.close()

async def main():
    parser = argparse.ArgumentParser(description="Web Agent Example")
    parser.add_argument("--model", type=str, default="meta-llama/Llama-2-7b-chat-hf",
                        help="Hugging Face model to use")
    parser.add_argument("--interactive", action="store_true",
                        help="Run in interactive mode")
    args = parser.parse_args()
    
    if args.interactive:
        await interactive_session(args.model)
    else:
        await run_example_queries(args.model)

if __name__ == "__main__":
    asyncio.run(main()) 