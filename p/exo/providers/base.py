"""
Base interface for AI providers.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseProvider(ABC):
    """Base class for all AI providers."""
    
    @abstractmethod
    async def initialize(self, **kwargs) -> None:
        """Initialize the provider with configuration."""
        pass
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the model."""
        pass
    
    @abstractmethod
    async def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        pass
    
    @abstractmethod
    async def list_models(self) -> List[str]:
        """List available models."""
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """Clean up resources."""
        pass

class BaseModel(ABC):
    """Base class for AI models."""
    
    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.config = kwargs
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the model."""
        pass
    
    @abstractmethod
    async def get_model_info(self) -> Dict[str, Any]:
        """Get information about the model."""
        pass 