"""
Base interface for agents that can use providers and tools.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from ..providers.base import BaseProvider
from ..tools.base import BaseTool

class BaseAgent(ABC):
    """Base class for all agents."""
    
    def __init__(self, provider: BaseProvider, tools: List[BaseTool] = None):
        self.provider = provider
        self.tools = tools or []
        self.initialized = False
    
    async def initialize(self, **kwargs) -> None:
        """Initialize the agent and its components."""
        if self.initialized:
            return
            
        # Initialize provider
        await self.provider.initialize(**kwargs.get('provider_config', {}))
        
        # Initialize tools
        for tool in self.tools:
            await tool.initialize(**kwargs.get('tool_config', {}))
            
        self.initialized = True
    
    @abstractmethod
    async def execute(self, task: str, **kwargs) -> Any:
        """Execute the agent's main task."""
        if not self.initialized:
            raise RuntimeError("Agent not initialized. Call initialize() first.")
        pass
    
    async def get_agent_info(self) -> Dict[str, Any]:
        """Get information about the agent."""
        return {
            "name": self.__class__.__name__,
            "provider": await self.provider.get_model_info(),
            "tools": [await tool.get_tool_info() for tool in self.tools],
            "initialized": self.initialized
        }
    
    async def close(self) -> None:
        """Clean up resources."""
        if self.initialized:
            await self.provider.close()
            for tool in self.tools:
                await tool.close()
            self.initialized = False 