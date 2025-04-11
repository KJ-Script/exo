# Tools Module

The tools module provides a framework for creating and using tools in the AI Scraper library.

## Prebuilt Tools

### Web Search Tool

A tool that searches the web for a query and returns relevant URLs.

```python
from ai_scraper.tools.search import search_tool

# Search the web
results = await search_tool("What is Python?")
for result in results:
    print(f"{result['title']}: {result['url']}")
```

### Content Extractor Tool

A tool that extracts content from a website.

```python
from ai_scraper.tools.extract import extract_tool

# Extract content from a website
result = await extract_tool("https://example.com")
print(result["text"])

# Extract specific elements
result = await extract_tool(
    "https://example.com",
    selector="h1"
)
for text in result["texts"]:
    print(text)
```

## Creating Custom Tools

You can create your own custom tools by defining functions and wrapping them with the `Tool` class:

```python
from ai_scraper.tools import Tool

# Define your function
async def my_tool(input: str) -> dict:
    # Your tool's logic here
    return {
        "input": input,
        "output": f"Processed: {input}"
    }

# Create the tool
my_tool = Tool(
    my_tool,
    name="my_tool",
    description="A custom tool that processes input"
)

# Use the tool
result = await my_tool("Hello, World!")
print(result["output"])
```

## Tool Functions

Tool functions should:
1. Be asynchronous (use `async def`)
2. Return a dictionary with the results
3. Have clear parameter names and types
4. Include docstrings describing what they do

## Examples

See the `examples` directory for more examples of custom tools. 