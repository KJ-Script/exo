"""
Example demonstrating how to use different AI providers.
"""
import asyncio
import os
import logging
from typing import Dict, Any

from exo.providers.huggingface import HuggingFaceProvider
from exo.providers.openai import OpenAIProvider
from exo.providers.gemini import GeminiProvider
from exo.providers.ollama import OllamaProvider

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_provider_example(provider_name: str, api_key: str = None) -> None:
    """
    Run an example with a specific provider.
    
    Args:
        provider_name: Name of the provider to use (huggingface, openai, gemini, ollama)
        api_key: API key for the provider (if required)
    """
    # Create provider instance
    if provider_name == "huggingface":
        provider = HuggingFaceProvider()
        config = {"api_key": api_key or os.environ.get("HUGGINGFACE_API_KEY")}
        model_name = "meta-llama/Llama-2-7b-chat-hf"
    elif provider_name == "openai":
        provider = OpenAIProvider()
        config = {"api_key": api_key or os.environ.get("OPENAI_API_KEY")}
        model_name = "gpt-3.5-turbo"
    elif provider_name == "gemini":
        provider = GeminiProvider()
        config = {"api_key": api_key or os.environ.get("GEMINI_API_KEY")}
        model_name = "gemini-pro"
    elif provider_name == "ollama":
        provider = OllamaProvider()
        config = {}  # Ollama doesn't require an API key
        model_name = "llama2"
    else:
        raise ValueError(f"Unknown provider: {provider_name}")
    
    try:
        # Initialize the provider
        await provider.initialize(**config)
        logger.info(f"Initialized {provider_name} provider")
        
        # Get a model from the provider
        model = provider.get_model(model_name=model_name)
        logger.info(f"Got model: {model_name}")
        
        # Generate a response
        prompt = "What are three interesting facts about artificial intelligence?"
        logger.info(f"Sending prompt: {prompt}")
        
        response = await provider.generate(prompt)
        logger.info(f"Response from {provider_name}:")
        print(response)
        
    except Exception as e:
        logger.error(f"Error with {provider_name} provider: {e}")
    finally:
        # Clean up
        await provider.close()
        logger.info(f"Closed {provider_name} provider")

async def main():
    """Run examples with different providers."""
    # Example with HuggingFace
    await run_provider_example("huggingface")
    
    # Example with OpenAI
    await run_provider_example("openai")
    
    # Example with Gemini
    await run_provider_example("gemini")
    
    # Example with Ollama
    await run_provider_example("ollama")

if __name__ == "__main__":
    asyncio.run(main()) 