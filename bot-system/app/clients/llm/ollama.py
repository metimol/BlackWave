"""
Ollama LLM client for the BlackWave Bot Service.
Implements the BaseLLMClient interface for Ollama's API.
Supports both local Ollama instances and API key authentication.
"""

import ollama
from typing import Optional

from app.clients.llm.base import BaseLLMClient
from app.clients.llm.strip_think import strip_think_tags
from app.core.settings import (
    OLLAMA_API_KEY, 
    OLLAMA_API_BASE, 
    OLLAMA_MODEL,
    OLLAMA_TIMEOUT
)
from app.core.exceptions import LLMError


class OllamaClient(BaseLLMClient):
    """Client for Ollama's API."""

    def __init__(
        self,
        api_key: Optional[str] = OLLAMA_API_KEY,
        api_base: str = OLLAMA_API_BASE,
        model: str = OLLAMA_MODEL,
        timeout: int = OLLAMA_TIMEOUT,
    ):
        """
        Initialize the Ollama client.

        Args:
            api_key: Optional API key for Ollama (for remote instances)
            api_base: API base URL for Ollama
            model: Model to use
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.api_base = api_base
        self.model = model
        self.timeout = timeout
        
        # Initialize the client with optional authentication
        client_kwargs = {
            'host': self.api_base,
            'timeout': self.timeout
        }
        
        # Add authentication headers if API key is provided
        if self.api_key:
            client_kwargs['headers'] = {
                'Authorization': f'Bearer {self.api_key}'
            }
        
        self.client = ollama.Client(**client_kwargs)

    async def generate_text(
        self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7
    ) -> str:
        """
        Generate text from a prompt using Ollama.

        Args:
            prompt: The prompt to generate text from
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for text generation

        Returns:
            Generated text
        """
        try:
            # Ollama API parameters
            options = {
                'temperature': temperature,
                'num_predict': max_tokens,
            }
            
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options=options,
                stream=False
            )
            
            raw_text = response['response'].strip()
            return strip_think_tags(raw_text)
            
        except Exception as e:
            raise LLMError(f"Ollama text generation error: {str(e)}")