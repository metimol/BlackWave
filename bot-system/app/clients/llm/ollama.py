"""
Ollama LLM client for the BlackWave Bot Service.
Implements the BaseLLMClient interface for Ollama's API.
"""

import requests
import json

from app.clients.llm.base import BaseLLMClient
from app.clients.llm.strip_think import strip_think_tags
from app.core.settings import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.core.exceptions import LLMError


class OllamaClient(BaseLLMClient):
    """Client for Ollama's API."""

    def __init__(
        self,
        base_url: str = OLLAMA_BASE_URL,
        model: str = OLLAMA_MODEL,
    ):
        """
        Initialize the Ollama client.

        Args:
            base_url: Base URL for Ollama API
            model: Model to use
        """
        self.base_url = base_url
        self.model = model

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
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                },
            }
            
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            raw_text = result.get("response", "").strip()
            
            if not raw_text:
                raise LLMError("Ollama returned empty response")
                
            return strip_think_tags(raw_text)
        except requests.RequestException as e:
            raise LLMError(f"Ollama API request error: {str(e)}")
        except Exception as e:
            raise LLMError(f"Ollama text generation error: {str(e)}")