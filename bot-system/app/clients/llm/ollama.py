"""
Ollama LLM client for the BlackWave Bot Service.
Implements the BaseLLMClient interface for Ollama's API.
"""

import httpx
import json
from typing import Optional

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
        timeout: float = 200.0,
    ):
        """
        Initialize the Ollama client.

        Args:
            base_url: Base URL for Ollama API
            model: Model to use
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(self.timeout),
                limits=httpx.Limits(max_connections=10, max_keepalive_connections=5)
            )
        return self._client

    async def generate_text(
        self, 
        prompt: str, 
        max_tokens: int = 1024, 
        temperature: float = 0.7
    ) -> str:
        """
        Generate text from a prompt using Ollama.

        Args:
            prompt: The prompt to generate text from
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for text generation

        Returns:
            Generated text

        Raises:
            LLMError: If the API request fails or returns invalid response
        """
        if not prompt.strip():
            raise LLMError("Empty prompt provided")

        try:
            client = await self._get_client()
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

            response = await client.post(url, json=payload)
            response.raise_for_status()

            try:
                result = response.json()
            except json.JSONDecodeError as e:
                raise LLMError(f"Invalid JSON response from Ollama: {str(e)}")

            raw_text = result.get("response", "").strip()

            if not raw_text:
                raise LLMError("Ollama returned empty response")

            return strip_think_tags(raw_text)

        except httpx.HTTPStatusError as e:
            raise LLMError(f"Ollama API HTTP error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            raise LLMError(f"Ollama API request error: {str(e)}")
        except Exception as e:
            raise LLMError(f"Ollama text generation error: {str(e)}")

    async def close(self):
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()