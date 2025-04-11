"""
Gemini provider implementation using the Google Gemini SDK.
"""
import os
import logging
from typing import Dict, Any, List, Optional

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from exo.agents.models import BaseModel

logger = logging.getLogger(__name__)

class GeminiModel(BaseModel):
    """
    Gemini model implementation using the Google Gemini SDK.
    """
    
    def __init__(self, model_name: str, api_key: Optional[str] = None, 
                 temperature: float = 0.7, top_p: float = 0.9, 
                 top_k: int = 40, max_output_tokens: int = 2048, 
                 safety_settings: Optional[Dict[str, Any]] = None, **kwargs):
        """
        Initialize a Gemini model.
        
        Args:
            model_name: The name of the Gemini model to use
            api_key: The API key for the Gemini API (default: from GOOGLE_API_KEY env var)
            temperature: The temperature for sampling (default: 0.7)
            top_p: The top-p value for sampling (default: 0.9)
            top_k: The top-k value for sampling (default: 40)
            max_output_tokens: The maximum number of tokens to generate (default: 2048)
            safety_settings: Safety settings for the model (default: None)
            **kwargs: Additional arguments to pass to the Gemini model
        """
        self.model_name = model_name
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        
        if not self.api_key:
            raise ValueError("API key is required. Set it as an argument or in the GOOGLE_API_KEY environment variable.")
        
        # Configure the Gemini API
        genai.configure(api_key=self.api_key)
        
        # Set default safety settings if not provided
        if safety_settings is None:
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            }
        
        # Initialize the Gemini model
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config={
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "max_output_tokens": max_output_tokens,
            },
            safety_settings=safety_settings,
            **kwargs
        )
        
        # Store the configuration for later use
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.max_output_tokens = max_output_tokens
        self.safety_settings = safety_settings
        
        logger.info(f"Initialized Gemini model: {model_name}")
    
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
            response = self.model.generate_content(prompt)
            return response.text
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
            "provider": "gemini",
            "model_name": self.model_name,
            "parameters": {
                "temperature": self.temperature,
                "top_p": self.top_p,
                "top_k": self.top_k,
                "max_output_tokens": self.max_output_tokens,
            }
        }


class GeminiProvider:
    """
    Provider for Google Gemini models.
    """
    
    def __init__(self):
        """Initialize the Gemini provider."""
        logger.info("Initialized Gemini provider")
    
    def get_model(self, model_name: str, **kwargs) -> BaseModel:
        """
        Get a Gemini model instance.
        
        Args:
            model_name: The name of the model to use
            **kwargs: Additional arguments to pass to the model
            
        Returns:
            An instance of GeminiModel
        """
        return GeminiModel(model_name=model_name, **kwargs)
    
    def list_models(self) -> List[str]:
        """
        List all available Gemini models.
        
        Returns:
            A list of available model names
        """
        # List of available Gemini models
        return [
            "gemini-pro",
            "gemini-pro-vision",
            "gemini-1.5-pro",
            "gemini-1.5-pro-vision",
            "gemini-1.5-flash",
            "gemini-1.5-flash-vision",
        ] 