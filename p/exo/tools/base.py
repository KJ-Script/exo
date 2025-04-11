"""
Base interface for tools that agents can use.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseTool(ABC):
    """Base class for all tools that agents can use."""
    
    @abstractmethod
    async def initialize(self, **kwargs) -> None:
        """Initialize the tool with configuration."""
        pass
    
    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """Execute the tool's main functionality."""
        pass
    
    @abstractmethod
    async def get_tool_info(self) -> Dict[str, Any]:
        """Get information about the tool."""
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """Clean up resources."""
        pass 