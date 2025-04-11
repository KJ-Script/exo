"""
Base interface for browser automation.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseBrowser(ABC):
    """Base class for browser automation."""
    
    @abstractmethod
    async def initialize(self, **kwargs) -> None:
        """Initialize the browser with configuration."""
        pass
    
    @abstractmethod
    async def new_page(self) -> Any:
        """Create a new browser page."""
        pass
    
    @abstractmethod
    async def goto(self, url: str, **kwargs) -> None:
        """Navigate to a URL."""
        pass
    
    @abstractmethod
    async def get_content(self, selector: Optional[str] = None, **kwargs) -> str:
        """Get content from the current page."""
        pass
    
    @abstractmethod
    async def wait_for_selector(self, selector: str, **kwargs) -> None:
        """Wait for an element to appear on the page."""
        pass
    
    @abstractmethod
    async def screenshot(self, path: str, **kwargs) -> None:
        """Take a screenshot of the current page."""
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """Close the browser and clean up resources."""
        pass 