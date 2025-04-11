"""
Provider module for different LLM backends.
"""

from abc import ABC, abstractmethod

class BaseProvider(ABC):
    """Base class for all providers."""
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the model."""
        pass 