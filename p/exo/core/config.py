"""
Core configuration settings for the exo package.
"""
import os
from typing import Dict, Any

# Default configuration
DEFAULT_CONFIG = {
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    },
    "browser": {
        "headless": True,
        "timeout": 30000,  # milliseconds
        "viewport": {"width": 1280, "height": 720}
    },
    "scraping": {
        "max_retries": 3,
        "delay_between_requests": 1.0,  # seconds
        "max_content_length": 1000000  # characters
    }
}

# Environment-specific configuration
ENV_CONFIG = {
    "development": {
        "logging": {"level": "DEBUG"},
        "browser": {"headless": False}
    },
    "production": {
        "logging": {"level": "INFO"},
        "browser": {"headless": True}
    }
}

def get_config(env: str = "development") -> Dict[str, Any]:
    """
    Get the configuration for the specified environment.
    
    Args:
        env: The environment to get configuration for ("development" or "production")
        
    Returns:
        Dict containing the configuration
    """
    config = DEFAULT_CONFIG.copy()
    
    # Override with environment-specific settings
    if env in ENV_CONFIG:
        for key, value in ENV_CONFIG[env].items():
            if key in config:
                config[key].update(value)
            else:
                config[key] = value
    
    # Override with environment variables
    for key in config:
        env_key = f"EXO_{key.upper()}"
        if env_key in os.environ:
            config[key] = eval(os.environ[env_key])
    
    return config 