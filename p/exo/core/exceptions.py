"""
Custom exceptions for the exo package.
"""

class ExoError(Exception):
    """Base exception for all exo errors."""
    pass

class ProviderError(ExoError):
    """Raised when there's an error with an AI provider."""
    pass

class ScraperError(ExoError):
    """Raised when there's an error with web scraping."""
    pass

class BrowserError(ScraperError):
    """Raised when there's an error with browser operations."""
    pass

class ParserError(ScraperError):
    """Raised when there's an error parsing content."""
    pass

class AgentError(ExoError):
    """Raised when there's an error with an agent."""
    pass

class ConfigError(ExoError):
    """Raised when there's an error with configuration."""
    pass 