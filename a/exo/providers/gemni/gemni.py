import os

from typing import Dict, Any, List, Optional
from exo.providers.base import BaseProvider, BaseModel

from google import genai
from google.genai import types

class GemniModel(BaseModel):
    def __init__(self, model_name: str, api_key: Optional[str] = None, temperature: Optional[float] = 0.7,
                 max_tokens: Optional[int] = 1000, top_p: Optional[float] = 1.0, top_k: Optional[int] = 40,
                 max_retries: Optional[int] = 3, timeout: Optional[int] = 10, saftey_settings: Optional[Dict[str, Any]] = None, 
                 **kwargs):
        
        """
        Initialize a Gemini model.
        
        Args:
            model_name: The name of the Gemini model to use
            api_key: The API key for the Gemini API (default: from GOOGLE_API_KEY env var)
            temperature: The temperature for sampling (default: 0.7)
            top_p: The top-p value for sampling (default: 0.9)
            top_k: The top-k value for sampling (default: 40)
            max_tokens: The maximum number of tokens to generate (default: 2048)
            max_retries: The maximum number of retries (default: 3)
            safety_settings: Safety settings for the model (default: None)
            **kwargs: Additional arguments to pass to the Gemini model

        """

        self.model_name = model_name
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")


        if not self.api_key:
            raise ValueError("API key is required")

        #create the client
        client = genai.Client(api_key=self.api_key)

        if saftey_settings is None:
            saftey_settings = types.SafetySettings(
                category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            )

        #create the model
        self.model = client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config= types.GenerateContentConfig(
            temperature=self.temperature,
            top_p=self.top_p,
            top_k=self.top_k,
            max_tokens=self.max_tokens,
            )
        )

        #store the following for later use
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        self.timeout = timeout
        self.saftey_settings = saftey_settings


    async def generate_response(self, prompt: str, **kwargs) -> str:
        """
        Generate a response from the model.
        
        Args:
            prompt: The prompt to generate a response for
            **kwargs: Additional arguments to pass to the model
            
        Returns:
            The generated response
        """
                
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise e
