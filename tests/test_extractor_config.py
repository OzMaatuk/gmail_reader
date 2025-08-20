# tests/test_extractor_config.py
import pytest
from unittest.mock import patch, MagicMock
import configparser

from gmail_reader.extractor.config import ExtractorConfig

class TestExtractorConfig:
    
    @pytest.mark.unit
    def test_load_llm_config_default(self):
        """Test loading default LLM config when no config file exists."""
        with patch('gmail_reader.extractor.config.config', new=configparser.ConfigParser()):
            config = ExtractorConfig()
            llm_config = config.load_llm_config()
            
            assert llm_config["model"] == "mistral"
            assert llm_config["model_provider"] == "ollama"
            assert llm_config["temperature"] == 0.0
            assert llm_config["base_url"] == "http://host.docker.internal:11434"
    
    @pytest.mark.unit
    def test_load_llm_config_from_file(self):
        """Test loading LLM config from config file."""
        mock_config = configparser.ConfigParser()
        mock_config.add_section("llm")
        mock_config.set("llm", "model", "gpt-4")
        mock_config.set("llm", "provider", "openai")
        mock_config.set("llm", "api_key", "test-key")
        mock_config.set("llm", "temperature", "0.7")
        mock_config.set("llm", "base_url", "https://api.openai.com")
        
        with patch('gmail_reader.extractor.config.config', mock_config):
            config = ExtractorConfig()
            llm_config = config.load_llm_config()
            
            assert llm_config["model"] == "gpt-4"
            assert llm_config["model_provider"] == "openai"
            assert llm_config["api_key"] == "test-key"
            assert llm_config["temperature"] == 0.7
            assert llm_config["base_url"] == "https://api.openai.com"