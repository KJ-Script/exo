"""
Example demonstrating how to use the Hugging Face provider.
"""
import logging
from exo.agents.providers import HuggingFaceProvider

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    # Initialize the Hugging Face provider
    provider = HuggingFaceProvider()
    
    # List available models
    models = provider.list_models()
    logger.info("Available models:")
    for model in models:
        logger.info(f"- {model}")
    
    # Initialize a specific model
    model_name = "meta-llama/Llama-2-7b-chat-hf"
    model = provider.get_model(
        model_name=model_name,
        temperature=0.7,
        top_p=0.9,
        max_tokens=100
    )
    
    # Generate a response
    prompt = "What is the capital of France?"
    logger.info(f"Prompt: {prompt}")
    response = model.generate(prompt)
    logger.info(f"Response: {response}")
    
    # Get model information
    model_info = model.get_model_info()
    logger.info("Model information:")
    for key, value in model_info.items():
        logger.info(f"- {key}: {value}")

if __name__ == "__main__":
    main() 