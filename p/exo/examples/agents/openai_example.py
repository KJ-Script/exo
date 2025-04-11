"""
Example script demonstrating how to use the OpenAI provider with the model importer.
"""
import os
import sys
import logging

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from exo.agents.models import ModelImporter

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Run the example."""
    # Create a model importer
    importer = ModelImporter()
    
    # Register the OpenAI provider
    importer.register_provider('openai', 'exo.agents.providers.openai', 'OpenAIProvider')
    
    # List available providers
    providers = importer.list_available_providers()
    logger.info(f"Available providers: {providers}")
    
    # List available models for the OpenAI provider
    openai_models = importer.list_available_models('openai')
    logger.info(f"Available OpenAI models: {openai_models}")
    
    # Get an OpenAI model
    model_name = "gpt-3.5-turbo"  # Change this to a model you want to use
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        logger.error("OPENAI_API_KEY environment variable is not set. Please set it to use the OpenAI API.")
        return
    
    model = importer.get_model('openai', model_name, api_key=api_key, temperature=0.7)
    
    # Generate a response
    prompt = "What is the capital of France?"
    logger.info(f"Prompt: {prompt}")
    
    try:
        response = model.generate(prompt)
        logger.info(f"Response: {response}")
    except Exception as e:
        logger.error(f"Error generating response: {e}")
    
    # Get model information
    model_info = model.get_model_info()
    logger.info(f"Model info: {model_info}")

if __name__ == "__main__":
    main() 