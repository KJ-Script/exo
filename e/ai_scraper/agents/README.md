# Agents Module

The agents module provides a framework for creating agents that use providers and tools.

## Prebuilt Agents

### Web Research Agent

An agent that researches topics on the web by searching and extracting content.

```python
from ai_scraper.agents.web_research_agent import WebResearchAgent
from ai_scraper.providers.ollama import OllamaProvider

# Initialize the provider
provider = OllamaProvider(model="llama2")

# Initialize the agent
agent = WebResearchAgent(provider=provider, max_results=3)

# Run the agent
results = await agent.run(query="What is Python?")
print(results["summary"])
```

## Creating Custom Agents

You can create your own custom agents by extending the `Agent` class:

```python
from ai_scraper.agents import Agent
from ai_scraper.tools import Tool

# Define your tools
async def my_tool(input: str) -> dict:
    # Your tool's logic here
    return {
        "input": input,
        "output": f"Processed: {input}"
    }

my_tool = Tool(
    my_tool,
    name="my_tool",
    description="A custom tool that processes input"
)

# Create your agent
class MyAgent(Agent):
    def __init__(self, provider, **kwargs):
        super().__init__(
            provider=provider,
            tools=[my_tool],
            **kwargs
        )
    
    async def run(self, input: str, **kwargs) -> dict:
        # Step 1: Process the input
        processed = await my_tool(input=input)
        
        # Step 2: Generate a response using the provider
        response = await this.provider.generate(
            f"Processed input: {processed['output']}"
        )
        
        # Return the results
        return {
            "input": input,
            "processed": processed,
            "response": response
        }

# Use your agent
agent = MyAgent(provider=provider)
results = await agent.run(input="Hello, World!")
print(results["response"])
```

## Agent Interface

All agents must:

1. Extend the `Agent` class
2. Initialize with a provider and optional tools
3. Implement the `run` method

## Examples

See the `examples` directory for more examples of custom agents. 