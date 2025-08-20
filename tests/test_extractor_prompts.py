# tests/test_extractor_prompts.py
import pytest

from gmail_reader.extractor.prompts import PromptManager

class TestPromptManager:
    
    @pytest.mark.unit
    def test_init_default_template(self):
        """Test initialization with default template."""
        manager = PromptManager()
        assert "{content}" in manager.verification_template
        assert "verification code" in manager.verification_template

    @pytest.mark.unit
    def test_init_custom_template(self):
        """Test initialization with custom template."""
        custom_template = "Extract the code from: {content}"
        manager = PromptManager(custom_template=custom_template)
        assert manager.verification_template == custom_template
    
    @pytest.mark.unit
    def test_get_single_code_prompt(self):
        """Test single code prompt generation."""
        manager = PromptManager()
        content = "Your verification code is 123456"
        
        prompt = manager.get_single_code_prompt(content)
        
        assert content in prompt
        assert "{content}" not in prompt
    
    @pytest.mark.unit
    def test_get_multi_code_prompt(self):
        """Test multiple code prompt generation."""
        manager = PromptManager()
        content = "Multiple codes: ABC123, XYZ789"
        
        prompt = manager.get_multi_code_prompt(content)
        
        assert content in prompt
        assert "comma-separated" in prompt
        assert "NONE" in prompt