"""
AI client module for interacting with Ollama models.
Handles model selection, fallbacks, and error handling.
"""

import requests
from typing import Optional
from .config import Config
from .logger import logger


class AIClient:
    """Client for interacting with Ollama AI models."""
    
    def __init__(self):
        self.base_url = Config.OLLAMA_BASE_URL
        self.primary_model = Config.PRIMARY_MODEL
        self.fallback_model = Config.FALLBACK_MODEL
    
    def _send_request(self, prompt: str, model: str) -> Optional[str]:
        """Send a request to the specified model."""
        url = f"{self.base_url}/api/generate"
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            logger.debug(f"Sending request to {model}")
            response = requests.post(url, json=data, timeout=60)
            response.raise_for_status()
            result = response.json().get("response", "")
            logger.debug(f"Received response from {model}, length: {len(result)}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for model {model}: {e}")
            return None
    
    def generate_response(self, prompt: str) -> str:
        """
        Generate a response using primary model with fallback.
        
        Args:
            prompt: The prompt to send to the AI
            
        Returns:
            The AI response or error message
        """
        logger.info(f"Generating response for prompt: {prompt[:50]}...")
        
        # Try primary model
        response = self._send_request(prompt, self.primary_model)
        if response is not None:
            logger.info("Response generated successfully with primary model")
            return response
        
        # Try fallback model
        logger.warning(f"Primary model {self.primary_model} failed, trying fallback {self.fallback_model}")
        response = self._send_request(prompt, self.fallback_model)
        if response is not None:
            logger.info("Response generated successfully with fallback model")
            return response
        
        # Both failed
        error_msg = f"Failed to generate response: both {self.primary_model} and {self.fallback_model} unavailable"
        logger.error(error_msg)
        return error_msg


# Global instance
ai_client = AIClient()
