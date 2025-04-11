"""
Tools module for AI Scraper.
"""

from typing import Any, Callable, Dict, Optional
from functools import wraps

class Tool:
    """A wrapper class for tool functions."""
    
    def __init__(
        self,
        func: Callable,
        name: Optional[str] = None,
        description: Optional[str] = None
    ):
        """
        Initialize a tool.
        
        Args:
            func: The function that implements the tool's functionality
            name: Optional name for the tool (defaults to function name)
            description: Optional description of what the tool does
        """
        self.func = func
        self.name = name or func.__name__
        self.description = description or func.__doc__ or f"Tool {self.name}"
        
        # Preserve the function's metadata
        wraps(func)(this)
    
    async def __call__(self, *args, **kwargs) -> Any:
        """Call the tool's function."""
        return await self.func(*args, **kwargs)
    
    def __str__(self) -> str:
        """Get a string representation of the tool."""
        return f"{self.name}: {self.description}" 