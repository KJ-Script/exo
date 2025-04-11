"""
Gemini provider implementation.
"""

from typing import Any, Dict, Optional

import google.generativeai as genai
from . import BaseProvider

class GeminiProvider(BaseProvider):
    """Provider implementation for Google's Gemini models."""
    
    def __init__(
        self,
        api_key: str,
        model: str = "gemini-pro",
        **kwargs
    ):
        """
        Initialize the Gemini provider.
        
        Args:
            api_key: Google API key for Gemini
            model: The name of the Gemini model to use
            **kwargs: Additional arguments to pass to the model
        """
        self.model = model
        self.default_params = kwargs
        
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        self.model_instance = genai.GenerativeModel(model)
    
    async def generate(
        self,
        prompt: str,
        **kwargs
    ) -> str:
        """
        Generate a response using the Gemini model.
        
        Args:
            prompt: The input prompt
            **kwargs: Additional parameters to pass to the model
            
        Returns:
            The generated response as a string
        """
        # Merge default parameters with provided kwargs
        params = {**self.default_params, **kwargs}
        
        # Generate response
        response = self.model_instance.generate_content(prompt, **params)
        
        # Extract the text from the response
        return response.text 