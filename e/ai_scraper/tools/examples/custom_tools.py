"""
Examples of how to create custom tools.
"""

from typing import Dict, Any, List

from ai_scraper.tools import Tool

# Example 1: A simple text processing tool
async def process_text(text: str, uppercase: bool = False) -> Dict[str, Any]:
    """
    Process text by optionally converting it to uppercase.
    
    Args:
        text: The text to process
        uppercase: Whether to convert the text to uppercase
        
    Returns:
        A dictionary containing the processed text
    """
    result = text.upper() if uppercase else text
    
    return {
        "input": text,
        "output": result,
        "uppercase": uppercase
    }

# Create the tool
text_tool = Tool(
    process_text,
    name="process_text",
    description="Process text by optionally converting it to uppercase"
)

# Example 2: A tool that combines multiple operations
async def analyze_text(text: str) -> Dict[str, Any]:
    """
    Analyze text by counting words and characters.
    
    Args:
        text: The text to analyze
        
    Returns:
        A dictionary containing the analysis results
    """
    words = text.split()
    characters = list(text)
    
    return {
        "text": text,
        "word_count": len(words),
        "character_count": len(characters),
        "words": words
    }

# Create the tool
analyze_tool = Tool(
    analyze_text,
    name="analyze_text",
    description="Analyze text by counting words and characters"
) 