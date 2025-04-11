"""
Logging configuration for the exo package.
"""
import logging
from typing import Optional
from ..core.config import get_config

def setup_logging(level: Optional[str] = None) -> None:
    """
    Set up logging configuration.
    
    Args:
        level: Optional logging level to override config
    """
    config = get_config()
    log_config = config["logging"]
    
    if level:
        log_config["level"] = level
    
    logging.basicConfig(
        level=getattr(logging, log_config["level"]),
        format=log_config["format"]
    )

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Name of the logger
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name) 