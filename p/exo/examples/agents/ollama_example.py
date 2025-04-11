"""
Example script demonstrating how to use the Ollama provider with the model importer.
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
    
    # Register the Ollama provider
    importer.register_provider('ollama', 'exo.agents.providers.ollama', 'OllamaProvider')
    
    # List available providers
    providers = importer.list_available_providers()
    logger.info(f"Available providers: {providers}")
    
    # List available models for the Ollama provider
    ollama_models = importer.list_available_models('ollama')
    logger.info(f"Available Ollama models: {ollama_models}")
    
    # Get an Ollama model
    model_name = "llama2"  # Change this to a model you have installed
    model = importer.get_model('ollama', model_name, temperature=0.7)
    
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