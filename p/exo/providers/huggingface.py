"""
Hugging Face provider implementation using the transformers library.
"""
import os
import logging
from typing import Dict, Any, List, Optional

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

from exo.agents.models import BaseModel

logger = logging.getLogger(__name__)

class HuggingFaceModel(BaseModel):
    """
    Hugging Face model implementation using the transformers library.
    """
    
    def __init__(self, model_name: str, device: str = "cuda" if torch.cuda.is_available() else "cpu",
                 temperature: float = 0.7, top_p: float = 0.9, 
                 max_tokens: int = 2048, **kwargs):
        """
        Initialize a Hugging Face model.
        
        Args:
            model_name: The name of the Hugging Face model to use
            device: The device to run the model on (default: cuda if available, else cpu)
            temperature: The temperature for sampling (default: 0.7)
            top_p: The top-p value for sampling (default: 0.9)
            max_tokens: The maximum number of tokens to generate (default: 2048)
            **kwargs: Additional arguments to pass to the model
        """
        self.model_name = model_name
        self.device = device
        
        # Store the configuration for later use
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        
        # Load the model and tokenizer
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
            logger.info(f"Loaded Hugging Face model: {model_name} on {device}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a response from the model.
        
        Args:
            prompt: The prompt to generate a response for
            **kwargs: Additional arguments to pass to the model
            
        Returns:
            The generated response
        """
        try:
            # Tokenize the input
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            # Generate the response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=self.max_tokens,
                    temperature=self.temperature,
                    top_p=self.top_p,
                    **kwargs
                )
            
            # Decode the response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove the prompt from the response
            response = response[len(prompt):].strip()
            
            return response
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the model.
        
        Returns:
            A dictionary containing model information
        """
        return {
            "provider": "huggingface",
            "model_name": self.model_name,
            "device": self.device,
            "parameters": {
                "temperature": self.temperature,
                "top_p": self.top_p,
                "max_tokens": self.max_tokens,
            }
        }


class HuggingFaceProvider:
    """
    Provider for Hugging Face models.
    """
    
    def __init__(self):
        """Initialize the Hugging Face provider."""
        logger.info("Initialized Hugging Face provider")
    
    def get_model(self, model_name: str, **kwargs) -> BaseModel:
        """
        Get a Hugging Face model instance.
        
        Args:
            model_name: The name of the model to use
            **kwargs: Additional arguments to pass to the model
            
        Returns:
            An instance of HuggingFaceModel
        """
        return HuggingFaceModel(model_name=model_name, **kwargs)
    
    def list_models(self) -> List[str]:
        """
        List all available Hugging Face models.
        
        Returns:
            A list of available model names
        """
        # List of some popular Hugging Face models
        return [
            "meta-llama/Llama-2-7b-chat-hf",
            "meta-llama/Llama-2-13b-chat-hf",
            "meta-llama/Llama-2-70b-chat-hf",
            "mistralai/Mistral-7B-Instruct-v0.1",
            "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "google/gemma-7b-it",
            "google/gemma-2b-it",
        ] 