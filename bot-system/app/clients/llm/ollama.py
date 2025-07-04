"""
Ollama LLM client for the BlackWave Bot Service.
Implements the BaseLLMClient interface for Ollama's API.
"""

import aiohttp
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
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(
                limit=10,
                limit_per_host=5,
                keepalive_timeout=30,
                enable_cleanup_closed=True,
            )
            self._session = aiohttp.ClientSession(
                connector=connector,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )
        return self._session

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
            session = await self._get_session()
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

            async with session.post(url, json=payload) as response:
                response.raise_for_status()
                
                try:
                    result = await response.json()
                except (json.JSONDecodeError, aiohttp.ContentTypeError) as e:
                    text = await response.text()
                    raise LLMError(f"Invalid JSON response from Ollama: {str(e)}. Response: {text[:200]}")

                raw_text = result.get("response", "").strip()

                if not raw_text:
                    raise LLMError("Ollama returned empty response")

                return strip_think_tags(raw_text)

        except aiohttp.ClientResponseError as e:
            raise LLMError(f"Ollama API HTTP error: {e.status} - {e.message}")
        except aiohttp.ClientConnectionError as e:
            raise LLMError(f"Ollama API connection error: {str(e)}")
        except aiohttp.ClientError as e:
            raise LLMError(f"Ollama API client error: {str(e)}")
        except asyncio.TimeoutError:
            raise LLMError("Ollama API request timed out")
        except Exception as e:
            raise LLMError(f"Ollama text generation error: {str(e)}")

    async def close(self):
        """Close the HTTP session."""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()