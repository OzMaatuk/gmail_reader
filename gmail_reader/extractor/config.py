"""Configuration management for the extractor."""
import logging
from typing import Dict
from ..config import config

logger = logging.getLogger(__name__)


class ExtractorConfig:
    """Handles configuration for the verification code extractor."""
    
    def load_llm_config(self) -> Dict:
        """Load LLM configuration from config file."""
        llm_config = {}
        
        if config.has_section("llm"):
            llm_config["model"] = config.get("llm", "model", fallback="gpt-3.5-turbo")
            llm_config["model_provider"] = config.get("llm", "provider", fallback="openai")
            
            if config.has_option("llm", "base_url"):
                llm_config["base_url"] = config.get("llm", "base_url")
            
            if config.has_option("llm", "api_key"):
                llm_config["api_key"] = config.get("llm", "api_key")
            
            if config.has_option("llm", "temperature"):
                llm_config["temperature"] = config.getfloat("llm", "temperature")
        else:
            # Default configuration
            llm_config = {
                "model": "mistral",
                "model_provider": "ollama",
                "temperature": 0.0,
                "base_url": "http://host.docker.internal:11434"
            }
        
        return llm_config