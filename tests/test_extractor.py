# tests/test_extractor.py
import pytest
from unittest.mock import Mock, patch, MagicMock

from gmail_reader.extractor import VerificationCodeExtractor
from gmail_reader.extractor.config import ExtractorConfig
from gmail_reader.extractor.patterns import RegexPatterns
from gmail_reader.extractor.prompts import PromptManager
from gmail_reader.extractor.llm_extractor import LLMExtractor

class TestVerificationCodeExtractor:
    
    @pytest.mark.unit
    def test_init_default(self):
        """Test extractor initialization with defaults."""
        extractor = VerificationCodeExtractor()
        assert extractor.config is not None
        assert extractor.prompt_manager is not None
        assert extractor.regex_patterns is not None
        assert extractor.llm_extractor is not None
    
    @pytest.mark.unit
    def test_init_custom_config(self, mock_llm):
        """Test extractor initialization with custom config."""
        llm_config = {"model": "custom-model"}
        prompt_template = "Extract code: {content}"
        patterns = [r'\d{6}']
        
        with patch('gmail_reader.extractor.llm_extractor.init_chat_model', return_value=mock_llm):
            extractor = VerificationCodeExtractor(
                llm_config=llm_config,
                prompt_template=prompt_template,
                fallback_patterns=patterns
            )
            
            assert extractor.prompt_manager.verification_template == prompt_template
            assert extractor.regex_patterns.patterns == patterns
    
    @pytest.mark.unit
    def test_extract_code_empty_content(self):
        """Test extraction with empty content."""
        extractor = VerificationCodeExtractor()
        
        assert extractor.extract_code("") is None
        assert extractor.extract_code("   ") is None
        assert extractor.extract_code(None) is None
    
    @pytest.mark.unit
    def test_extract_code_with_llm(self, mock_llm):
        """Test code extraction using LLM."""
        with patch('gmail_reader.extractor.llm_extractor.init_chat_model', return_value=mock_llm):
            extractor = VerificationCodeExtractor()
            code = extractor.extract_code("Your verification code is: 123456")
            
            assert code == "123456"
            mock_llm.invoke.assert_called_once()
    
    @pytest.mark.unit
    def test_extract_code_fallback_to_regex(self):
        """Test fallback to regex when LLM fails."""
        with patch('gmail_reader.extractor.llm_extractor.init_chat_model', return_value=None):
            extractor = VerificationCodeExtractor()
            code = extractor.extract_code("Your code is 789012")
            
            assert code == "789012"
    
    @pytest.mark.unit
    def test_extract_code_no_fallback(self):
        """Test extraction without fallback."""
        with patch('gmail_reader.extractor.llm_extractor.init_chat_model', return_value=None):
            extractor = VerificationCodeExtractor()
            code = extractor.extract_code("Your code is 789012", use_fallback=False)
            
            assert code is None
    
    @pytest.mark.unit
    def test_extract_multiple_codes(self, mock_llm):
        """Test extracting multiple codes."""
        mock_llm.invoke.return_value = Mock(content="ABC123,XYZ789,456DEF")
        
        with patch('gmail_reader.extractor.llm_extractor.init_chat_model', return_value=mock_llm):
            extractor = VerificationCodeExtractor()
            codes = extractor.extract_multiple_codes("Multiple codes: ABC123, XYZ789, 456DEF")
            
            assert len(codes) == 3
            assert "ABC123" in codes
            assert "XYZ789" in codes
            assert "456DEF" in codes
    
    @pytest.mark.unit
    def test_extract_multiple_codes_fallback(self):
        """Test multiple code extraction with regex fallback."""
        with patch('gmail_reader.extractor.llm_extractor.init_chat_model', return_value=None):
            extractor = VerificationCodeExtractor()
            codes = extractor.extract_multiple_codes("Codes: 1234, 5678, 9012")
            
            assert len(codes) >= 3
            assert "1234" in codes
            assert "5678" in codes
            assert "9012" in codes