"""
Ollama LLM client for the BlackWave Bot Service.
Handles text generation using Ollama API.
"""

import httpx
from app.clients.llm.base import BaseLLMClient
from app.core.exceptions import LLMError
from app.core.logging import setup_logging
from app.core.settings import OLLAMA_URL, OLLAMA_MODEL
from app.clients.llm.strip_think import strip_think_tags

# Setup logging
logger = setup_logging()


class OllamaClient(BaseLLMClient):
    """Client for interacting with Ollama API."""

    def __init__(self, api_base: str=OLLAMA_URL, model: str=OLLAMA_MODEL):
        """
        Initialize the Ollama client.

        Args:
            api_base: URL to Ollama client
            model: Model name to use
        """
        self.api_base = api_base
        self.model = model

    async def generate_text(
        self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7
    ) -> str:
        """
        Generate text using Ollama.

        Args:
            prompt: Text prompt
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for generation

        Returns:
            Generated text

        Raises:
            LLMError: If generation fails
        """
        try:
            # Create a generative model
            body = {
                "model": self.model,
                "temperature": temperature,
                "max_output_tokens": max_tokens,
                "top_p": 0.95,
                "top_k": 40,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            }


            # Generate content
            async with httpx.AsyncClient(timeout=None, verify=False) as client:
                response = await client.post(f"{self.api_base}/api/chat", json=body)
                response.raise_for_status()

                # Extract and return text
                answer = response.json()
                answer = answer.get("message", {})
                answer = answer.get("content", None)
            if answer:
                return strip_think_tags(answer.strip())
            else:
                raise LLMError("Ollama returned empty response")

        except Exception as e:
            logger.error(f"Ollama text generation error: {str(e)}")
            raise LLMError(f"Ollama text generation error: {str(e)}")