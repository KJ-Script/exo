"""
Example of how to create a custom agent.
"""

from typing import Any, Dict, List, Optional

from ai_scraper.agents import Agent
from ai_scraper.tools.examples.custom_tools import text_tool, analyze_tool

class TextAnalysisAgent(Agent):
    """An agent that analyzes text using custom tools."""
    
    def __init__(
        self,
        provider,
        **kwargs
    ):
        """
        Initialize the text analysis agent.
        
        Args:
            provider: The provider to use for generating responses
            **kwargs: Additional arguments to pass to the agent
        """
        # Initialize with custom tools
        super().__init__(
            provider=provider,
            tools=[text_tool, analyze_tool],
            **kwargs
        )
    
    async def run(
        self,
        text: str,
        uppercase: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Run the text analysis agent.
        
        Args:
            text: The text to analyze
            uppercase: Whether to convert the text to uppercase
            **kwargs: Additional arguments
            
        Returns:
            A dictionary containing the analysis results
        """
        # Step 1: Process the text
        processed = await text_tool(text=text, uppercase=uppercase)
        
        # Step 2: Analyze the processed text
        analysis = await analyze_tool(text=processed["output"])
        
        # Step 3: Generate insights using the provider
        insights_prompt = f"""
        I've analyzed the following text: "{text}"
        
        Here are the analysis results:
        
        {analysis}
        
        Please provide insights about this text.
        """
        
        insights = await self.provider.generate(insights_prompt)
        
        # Return the results
        return {
            "original_text": text,
            "processed_text": processed["output"],
            "analysis": analysis,
            "insights": insights
        } 