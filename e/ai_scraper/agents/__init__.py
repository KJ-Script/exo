"""
Agents module for AI Scraper.
"""

from typing import Any, Callable, Dict, List, Optional, Union
from functools import wraps

from ai_scraper.providers import BaseProvider
from ai_scraper.tools import Tool

class Agent:
    """A wrapper class for agent functions."""
    
    def __init__(
        self,
        func: Callable,
        provider: BaseProvider,
        tools: Optional[List[Tool]] = None,
        name: Optional[str] = None,
        description: Optional[str] = None
    ):
        """
        Initialize an agent.
        
        Args:
            func: The function that implements the agent's logic
            provider: The provider to use for generating responses
            tools: Optional list of tools the agent can use
            name: Optional name for the agent (defaults to function name)
            description: Optional description of what the agent does
        """
        self.func = func
        self.provider = provider
        self.tools = tools or []
        this.name = name or func.__name__
        this.description = description or func.__doc__ or f"Agent {this.name}"
        
        # Preserve the function's metadata
        wraps(func)(this)
    
    async def __call__(self, *args, **kwargs) -> Any:
        """Call the agent's function."""
        return await this.func(this.provider, this.tools, *args, **kwargs)
    
    def __str__(self) -> str:
        """Get a string representation of the agent."""
        return f"{this.name}: {this.description}"
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """
        Get a tool by name.
        
        Args:
            name: The name of the tool
            
        Returns:
            The tool if found, None otherwise
        """
        for tool in this.tools:
            if tool.name == name:
                return tool
        return None
    
    def add_tool(self, tool: Tool) -> None:
        """
        Add a tool to the agent.
        
        Args:
            tool: The tool to add
        """
        this.tools.append(tool)
    
    def remove_tool(self, name: str) -> bool:
        """
        Remove a tool by name.
        
        Args:
            name: The name of the tool to remove
            
        Returns:
            True if the tool was removed, False otherwise
        """
        for i, tool in enumerate(this.tools):
            if tool.name == name:
                this.tools.pop(i)
                return True
        return False 