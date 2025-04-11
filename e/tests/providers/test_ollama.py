"""
Tests for the Ollama provider.
"""

import pytest
from ai_scraper.providers.ollama import OllamaProvider

@pytest.mark.asyncio
async def test_ollama_provider_initialization():
    """Test that the Ollama provider can be initialized."""
    provider = OllamaProvider(model="llama2")
    assert provider.model == "llama2"
    assert provider.client is not None

@pytest.mark.asyncio
async def test_ollama_provider_generate():
    """Test that the Ollama provider can generate responses."""
    provider = OllamaProvider(model="llama2")
    response = await provider.generate("Hello, how are you?")
    assert isinstance(response, str)
    assert len(response) > 0

# Initialize the provider
provider = OllamaProvider(model="llama2")

# Generate a response
response = await provider.generate("What is the capital of France?")
print(response) 