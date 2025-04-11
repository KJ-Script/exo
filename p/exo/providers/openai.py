"""
OpenAI provider implementation using the OpenAI SDK.
"""
import os
import logging
from typing import Dict, Any, List, Optional, Union

from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessage

from exo.agents.models import BaseModel

logger = logging.getLogger(__name__)

class OpenAIModel(BaseModel):
    """
    OpenAI model implementation using the OpenAI SDK.
    """
    
    def __init__(self, model_name: str, api_key: Optional[str] = None, 
                 temperature: float = 0.7, top_p: float = 0.9, 
                 max_tokens: int = 2048, presence_penalty: float = 0.0,
                 frequency_penalty: float = 0.0, **kwargs):
        """
        Initialize an OpenAI model.
        
        Args:
            model_name: The name of the OpenAI model to use
            api_key: The API key for the OpenAI API (default: from OPENAI_API_KEY env var)
            temperature: The temperature for sampling (default: 0.7)
            top_p: The top-p value for sampling (default: 0.9)
            max_tokens: The maximum number of tokens to generate (default: 2048)
            presence_penalty: The presence penalty (default: 0.0)
            frequency_penalty: The frequency penalty (default: 0.0)
            **kwargs: Additional arguments to pass to the OpenAI model
        """
        self.model_name = model_name
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("API key is required. Set it as an argument or in the OPENAI_API_KEY environment variable.")
        
        # Initialize the OpenAI client
        self.client = OpenAI(api_key=self.api_key)
        
        # Store the configuration for later use
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        
        logger.info(f"Initialized OpenAI model: {model_name}")
    
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
            # Create a chat completion
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=self.max_tokens,
                presence_penalty=self.presence_penalty,
                frequency_penalty=self.frequency_penalty,
                **kwargs
            )
            
            # Extract the response text
            return response.choices[0].message.content
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
            "provider": "openai",
            "model_name": self.model_name,
            "parameters": {
                "temperature": self.temperature,
                "top_p": self.top_p,
                "max_tokens": self.max_tokens,
                "presence_penalty": self.presence_penalty,
                "frequency_penalty": self.frequency_penalty,
            }
        }


class OpenAIProvider:
    """
    Provider for OpenAI models.
    """
    
    def __init__(self):
        """Initialize the OpenAI provider."""
        logger.info("Initialized OpenAI provider")
    
    def get_model(self, model_name: str, **kwargs) -> BaseModel:
        """
        Get an OpenAI model instance.
        
        Args:
            model_name: The name of the model to use
            **kwargs: Additional arguments to pass to the model
            
        Returns:
            An instance of OpenAIModel
        """
        return OpenAIModel(model_name=model_name, **kwargs)
    
    def list_models(self) -> List[str]:
        """
        List all available OpenAI models.
        
        Returns:
            A list of available model names
        """
        # List of available OpenAI models
        return [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
            "gpt-4",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k",
        ] 