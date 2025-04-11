# AI Scraper

A modular and extensible web scraping library for AI agents.

## Features

- **Providers**: Unified interface for different LLM backends (Ollama, Gemini, OpenAI)
- **Tools**: Web scraping capabilities built with Playwright
- **Agents**: Customizable agents that combine providers and tools

## Installation

```bash
pip install ai-scraper
```

## Quick Start

```python
from ai_scraper.agents import BaseAgent
from ai_scraper.providers import BaseProvider
from ai_scraper.tools import BaseTool

# Create your custom agent
class MyAgent(BaseAgent):
    async def run(self, **kwargs):
        # Your agent logic here
        pass
```

## Development

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run tests:
   ```bash
   pytest
   ```

## License

MIT 