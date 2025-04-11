"""
Tests for the Gemini provider.
"""

import os
import pytest
from ai_scraper.providers.gemini import GeminiProvider

# Get API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

@pytest.mark.skipif(not API_KEY, reason="GEMINI_API_KEY environment variable not set")
@pytest.mark.asyncio
async def test_gemini_provider_initialization():
    """Test that the Gemini provider can be initialized."""
    provider = GeminiProvider(api_key=API_KEY)
    assert provider.model == "gemini-pro"
    assert provider.model_instance is not None

@pytest.mark.skipif(not API_KEY, reason="GEMINI_API_KEY environment variable not set")
@pytest.mark.asyncio
async def test_gemini_provider_generate():
    """Test that the Gemini provider can generate responses."""
    provider = GeminiProvider(api_key=API_KEY)
    response = await provider.generate("Hello, how are you?")
    assert isinstance(response, str)
    assert len(response) > 0 