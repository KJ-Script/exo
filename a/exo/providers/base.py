"""
    Base blueprint for providers
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseModel(ABC):
    """
        Base model for providers
    """
    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.config = kwargs

    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """ Generate a response from the model """
        pass

    @abstractmethod
    async def get_model_info(self) -> Dict[str, Any]:
        """ Get the model info """
        pass


class BaseProvider(ABC):
    """
        Base provider for providers
    """
    def __init__(self,  **kwargs):
        self.initialized = False
        self.models = {}
        self.config = kwargs

    @abstractmethod
    async def initialize(self, **kwargs) -> None:
        """ Initialize the provider """
        pass

    @abstractmethod
    async def generate_response(self, model_name: str, prompt: str, **kwargs) -> str:
        """ Generate a response from the provider """
        pass

    @abstractmethod
    async def get_model(self, model_name: str) -> BaseModel:
        """ Get the model from the provider """
        pass

    @abstractmethod
    async def list_models(self) -> List[str]:
        """ List the models from the provider """
        pass

    @abstractmethod
    async def close(self) -> None:
        """ Close the provider """
        pass

    def check_initialized(self) -> None:
        """ Check if the provider is initialized """
        if not self.initialized:
            raise Exception("Provider not initialized")


    