import os
from enum import Enum
from typing import Optional, Dict, Any
import logging

# Configure logging
logger = logging.getLogger(__name__)

class ProviderType(str, Enum):
    LOCAL = "local"
    OPENAI = "openai"
    TOGETHER = "together"

class ProviderRouter:
    """
    Handles routing of inference requests to the appropriate provider.
    Validates availability and logs usage.
    """
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.together_api_key = os.getenv("TOGETHER_API_KEY")
        
        # Check for local model availability (simplified check)
        self.local_model_available = True 
        try:
            import transformers
            import torch
        except ImportError:
            self.local_model_available = False
            logger.warning("Local model dependencies (transformers, torch) not found.")

    def validate_provider(self, provider: str) -> str:
        """
        Validates if the requested provider is available and configured.
        Returns the validated provider string or raises ValueError.
        """
        provider = provider.lower()
        
        if provider == ProviderType.OPENAI:
            if not self.openai_api_key:
                raise ValueError("OpenAI provider requested but OPENAI_API_KEY is not set.")
            return ProviderType.OPENAI
            
        elif provider == ProviderType.TOGETHER:
            if not self.together_api_key:
                raise ValueError("Together API provider requested but TOGETHER_API_KEY is not set.")
            return ProviderType.TOGETHER
            
        elif provider == ProviderType.LOCAL:
            if not self.local_model_available:
                raise ValueError("Local provider requested but dependencies are missing.")
            return ProviderType.LOCAL
            
        else:
            raise ValueError(f"Unknown provider: {provider}. Valid options: {', '.join([p.value for p in ProviderType])}")

    def get_api_key(self, provider: str) -> Optional[str]:
        """Returns the API key for the specified provider."""
        if provider == ProviderType.OPENAI:
            return self.openai_api_key
        elif provider == ProviderType.TOGETHER:
            return self.together_api_key
        return None

    def log_usage(self, provider: str, operation: str, details: Dict[str, Any] = None):
        """Logs provider usage for audit and debugging."""
        logger.info(f"Provider Usage: {provider} | Operation: {operation} | Details: {details or {}}")
