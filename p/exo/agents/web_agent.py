"""
Web agent implementation that can use any provider and web scraping tools.
"""
import logging
import json
from typing import Dict, Any, List, Optional

from ..core.exceptions import AgentError
from ..providers.base import BaseProvider
from ..scraper.tools import web_search, scrape_website
from .base import BaseAgent

logger = logging.getLogger(__name__)

class WebAgent(BaseAgent):
    """
    Agent that can use any AI provider and web scraping tools.
    """
    
    def __init__(self, provider: BaseProvider, **kwargs):
        """
        Initialize the web agent.
        
        Args:
            provider: The AI provider to use
            **kwargs: Additional configuration
        """
        super().__init__(provider, **kwargs)
        self.tools = [
            {
                "name": "web_search",
                "description": "Search the web for information",
                "parameters": {
                    "query": "The search query",
                    "num_results": "Number of results to return (default: 3)"
                },
                "function": web_search
            },
            {
                "name": "scrape_website",
                "description": "Scrape content from a website",
                "parameters": {
                    "url": "The URL to scrape",
                    "selector": "Optional CSS selector to target specific content"
                },
                "function": scrape_website
            }
        ]
        logger.info(f"Initialized WebAgent with provider: {provider.__class__.__name__}")
    
    async def initialize(self) -> None:
        """Initialize the agent with configuration."""
        await self.provider.initialize(**self.config)
    
    def _create_system_prompt(self) -> str:
        """Create the system prompt for the agent."""
        tools_description = "\n".join([
            f"- {tool['name']}: {tool['description']}" for tool in self.tools
        ])
        
        return f"""You are a helpful AI assistant with access to web tools.
You can search the web and scrape websites to find information.

Available tools:
{tools_description}

When a user asks a question that requires up-to-date information from the web, use the web_search tool.
When a user asks for specific information from a website, use the scrape_website tool.

After using a tool, analyze the results and provide a helpful response to the user.
If the tool results don't fully answer the question, you can use another tool or provide a partial answer based on what you know.

Always be helpful, accurate, and concise in your responses.
"""
    
    async def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools for the agent."""
        return self.tools
    
    async def use_tool(self, tool_name: str, **kwargs) -> Any:
        """Use a specific tool."""
        tool = next((t for t in self.tools if t["name"] == tool_name), None)
        if not tool:
            raise AgentError(f"Tool {tool_name} not found")
        
        try:
            result = await tool["function"](**kwargs)
            return result
        except Exception as e:
            logger.error(f"Error using tool {tool_name}: {e}")
            raise AgentError(f"Error using tool {tool_name}: {str(e)}")
    
    async def process_message(self, message: str, **kwargs) -> str:
        """
        Process a user message and return a response.
        
        Args:
            message: The user message
            **kwargs: Additional arguments for the provider
            
        Returns:
            The agent's response
        """
        # Create the initial prompt
        system_prompt = self._create_system_prompt()
        prompt = f"{system_prompt}\n\nUser: {message}\n\nAssistant:"
        
        # Generate an initial response
        response = await self.provider.generate(prompt, **kwargs)
        
        # Check if the response indicates tool usage
        if any(tool["name"] in response for tool in self.tools):
            # Extract tool name and parameters
            tool_name = None
            tool_params = {}
            
            for tool in self.tools:
                if tool["name"] in response:
                    tool_name = tool["name"]
                    # Extract parameters from response
                    for param_name in tool["parameters"]:
                        param_marker = f"{param_name}:"
                        if param_marker in response:
                            param_start = response.find(param_marker) + len(param_marker)
                            param_end = response.find("\n", param_start)
                            if param_end > param_start:
                                tool_params[param_name] = response[param_start:param_end].strip()
                            else:
                                tool_params[param_name] = response[param_start:].strip()
                    break
            
            if tool_name and tool_params:
                try:
                    # Use the tool
                    tool_result = await self.use_tool(tool_name, **tool_params)
                    
                    # Format the tool result
                    tool_result_str = json.dumps(tool_result, indent=2)
                    
                    # Create a new prompt with the tool result
                    new_prompt = f"{system_prompt}\n\nUser: {message}\n\nAssistant: I'll search for information about that.\n\nTool result:\n{tool_result_str}\n\nBased on this information, here's my answer:"
                    
                    # Generate a final response
                    final_response = await self.provider.generate(new_prompt, **kwargs)
                    return final_response
                except Exception as e:
                    logger.error(f"Error processing tool result: {e}")
                    return f"I encountered an error while searching for information: {str(e)}"
        
        return response
    
    async def close(self) -> None:
        """Clean up resources."""
        await self.provider.close()
        logger.info("WebAgent closed")