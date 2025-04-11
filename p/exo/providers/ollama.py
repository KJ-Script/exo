"""
Ollama provider implementation using LangChain.
"""
import logging
from typing import Dict, Any, List, Optional

from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from exo.agents.models import BaseModel

logger = logging.getLogger(__name__)

class OllamaModel(BaseModel):
    """
    Ollama model implementation using LangChain.
    """
    
    def __init__(self, model_name: str, base_url: Optional[str] = None, 
                 temperature: float = 0.7, top_p: float = 0.9, 
                 top_k: int = 40, num_ctx: int = 4096, 
                 repeat_penalty: float = 1.1, **kwargs):
        """
        Initialize an Ollama model.
        
        Args:
            model_name: The name of the Ollama model to use
            base_url: The base URL for the Ollama API (default: http://localhost:11434)
            temperature: The temperature for sampling (default: 0.7)
            top_p: The top-p value for sampling (default: 0.9)
            top_k: The top-k value for sampling (default: 40)
            num_ctx: The context window size (default: 4096)
            repeat_penalty: The repeat penalty (default: 1.1)
            **kwargs: Additional arguments to pass to the Ollama model
        """
        self.model_name = model_name
        self.base_url = base_url or "http://localhost:11434"
        
        # Create a callback manager for streaming output
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        
        # Initialize the Ollama model
        self.llm = Ollama(
            model=model_name,
            base_url=self.base_url,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            num_ctx=num_ctx,
            repeat_penalty=repeat_penalty,
            callback_manager=callback_manager,
            **kwargs
        )
        
        logger.info(f"Initialized Ollama model: {model_name}")
    
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
            response = self.llm.invoke(prompt)
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
            "provider": "ollama",
            "model_name": self.model_name,
            "base_url": self.base_url,
            "parameters": {
                "temperature": self.llm.temperature,
                "top_p": self.llm.top_p,
                "top_k": self.llm.top_k,
                "num_ctx": self.llm.num_ctx,
                "repeat_penalty": self.llm.repeat_penalty,
            }
        }


class OllamaProvider:
    """
    Provider for Ollama models.
    """
    
    def __init__(self):
        """Initialize the Ollama provider."""
        logger.info("Initialized Ollama provider")
    
    def get_model(self, model_name: str, **kwargs) -> BaseModel:
        """
        Get an Ollama model instance.
        
        Args:
            model_name: The name of the model to use
            **kwargs: Additional arguments to pass to the model
            
        Returns:
            An instance of OllamaModel
        """
        return OllamaModel(model_name=model_name, **kwargs)
    
    def list_models(self) -> List[str]:
        """
        List all available Ollama models.
        
        This is a placeholder implementation. In a real implementation,
        you would query the Ollama API to get the list of available models.
        
        Returns:
            A list of available model names
        """
        # This would be implemented to query the Ollama API
        # For now, return a list of common Ollama models
        return [
            "llama2",
            "llama2:13b",
            "llama2:70b",
            "mistral",
            "mistral:7b",
            "mistral:13b",
            "codellama",
            "codellama:7b",
            "codellama:13b",
            "codellama:34b",
            "neural-chat",
            "orca-mini",
            "phi",
            "starling-lm",
            "vicuna",
            "zephyr",
        ] 