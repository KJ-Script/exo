"""
Ollama provider implementation.
"""

from typing import Any, Dict, Optional

import ollama
from . import BaseProvider

class OllamaProvider(BaseProvider):
    """Provider implementation for Ollama models."""
    
    def __init__(
        self,
        model: str = "llama2",
        base_url: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the Ollama provider.
        
        Args:
            model: The name of the Ollama model to use
            base_url: Optional base URL for the Ollama API
            **kwargs: Additional arguments to pass to the Ollama client
        """
        self.model = model
        self.client = ollama.Client(host=base_url) if base_url else ollama.Client()
        self.default_params = kwargs
    
    async def generate(
        self,
        prompt: str,
        **kwargs
    ) -> str:
        """
        Generate a response using the Ollama model.
        
        Args:
            prompt: The input prompt
            **kwargs: Additional parameters to pass to the model
            
        Returns:
            The generated response as a string
        """
        # Merge default parameters with provided kwargs
        params = {**self.default_params, **kwargs}
        
        # Generate response
        response = await self.client.generate(
            model=self.model,
            prompt=prompt,
            **params
        )
        
        return response.response 