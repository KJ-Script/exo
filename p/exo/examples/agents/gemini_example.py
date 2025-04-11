"""
Example script demonstrating how to use the Gemini provider with the model importer.
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
    
    # Register the Gemini provider
    importer.register_provider('gemini', 'exo.agents.providers.gemini', 'GeminiProvider')
    
    # List available providers
    providers = importer.list_available_providers()
    logger.info(f"Available providers: {providers}")
    
    # List available models for the Gemini provider
    gemini_models = importer.list_available_models('gemini')
    logger.info(f"Available Gemini models: {gemini_models}")
    
    # Get a Gemini model
    model_name = "gemini-pro"  # Change this to a model you want to use
    api_key = os.environ.get("GOOGLE_API_KEY")
    
    if not api_key:
        logger.error("GOOGLE_API_KEY environment variable is not set. Please set it to use the Gemini API.")
        return
    
    model = importer.get_model('gemini', model_name, api_key=api_key, temperature=0.7)
    
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