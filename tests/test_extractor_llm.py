# tests/test_extractor_llm.py
import pytest
from unittest.mock import Mock, patch

from gmail_reader.extractor.llm_extractor import LLMExtractor
from gmail_reader.extractor.prompts import PromptManager

class TestLLMExtractor:
    
    @pytest.mark.unit
    def test_init_success(self, mock_llm):
        """Test successful LLM initialization."""
        llm_config = {"model": "test-model"}
        prompt_manager = PromptManager()
        
        with patch('gmail_reader.extractor.llm_extractor.init_chat_model', return_value=mock_llm):
            extractor = LLMExtractor(llm_config, prompt_manager)
            
            assert extractor.llm == mock_llm
            assert extractor.prompt_manager == prompt_manager
    
    @pytest.mark.unit
    def test_init_failure(self):
        """Test LLM initialization failure."""
        llm_config = {"model": "invalid"}
        prompt_manager = PromptManager()
        
        with patch('gmail_reader.extractor.llm_extractor.init_chat_model', side_effect=Exception("Failed")):
            extractor = LLMExtractor(llm_config, prompt_manager)
            
            assert extractor.llm is None
    
    @pytest.mark.unit
    def test_is_available(self, mock_llm):
        """Test LLM availability check."""
        prompt_manager = PromptManager()
        
        with patch('gmail_reader.extractor.llm_extractor.init_chat_model', return_value=mock_llm):
            extractor = LLMExtractor({}, prompt_manager)
            assert extractor.is_available() is True
        
        with patch('gmail_reader.extractor.llm_extractor.init_chat_model', side_effect=Exception()):
            extractor = LLMExtractor({}, prompt_manager)
            assert extractor.is_available() is False
    
    @pytest.mark.unit
    def test_extract_single_code_success(self, mock_llm):
        """Test successful single code extraction."""
        mock_llm.invoke.return_value = Mock(content="ABC123")
        prompt_manager = PromptManager()
        
        with patch('gmail_reader.extractor.llm_extractor.init_chat_model', return_value=mock_llm):
            extractor = LLMExtractor({}, prompt_manager)
            code = extractor.extract_single_code("Your code is ABC123")
            
            assert code == "ABC123"
            mock_llm.invoke.assert_called_once()
    
    @pytest.mark.unit
    def test_extract_single_code_none(self, mock_llm):
        """Test when LLM returns NONE."""
        mock_llm.invoke.return_value = Mock(content="NONE")
        prompt_manager = PromptManager()
        
        with patch('gmail_reader.extractor.llm_extractor.init_chat_model', return_value=mock_llm):
            extractor = LLMExtractor({}, prompt_manager)
            code = extractor.extract_single_code("No code here")
            
            assert code is None
    
    @pytest.mark.unit
    def test_extract_single_code_invalid(self, mock_llm):
        """Test validation of extracted codes."""
        prompt_manager = PromptManager()
        
        with patch('gmail_reader.extractor.llm_extractor.init_chat_model', return_value=mock_llm):
            extractor = LLMExtractor({}, prompt_manager)
            
            # Too long
            mock_llm.invoke.return_value = Mock(content="A" * 25)
            assert extractor.extract_single_code("Test") is None
            
            # Invalid characters
            mock_llm.invoke.return_value = Mock(content="ABC@123!")
            assert extractor.extract_single_code("Test") is None
    
    @pytest.mark.unit
    def test_extract_single_code_exception(self, mock_llm):
        """Test exception handling during extraction."""
        mock_llm.invoke.side_effect = Exception("API Error")
        prompt_manager = PromptManager()
        
        with patch('gmail_reader.extractor.llm_extractor.init_chat_model', return_value=mock_llm):
            extractor = LLMExtractor({}, prompt_manager)
            code = extractor.extract_single_code("Test content")
            
            assert code is None
    
    @pytest.mark.unit
    def test_extract_multiple_codes_success(self, mock_llm):
        """Test successful multiple code extraction."""
        mock_llm.invoke.return_value = Mock(content="ABC123, XYZ789, DEF456")
        prompt_manager = PromptManager()
        
        with patch('gmail_reader.extractor.llm_extractor.init_chat_model', return_value=mock_llm):
            extractor = LLMExtractor({}, prompt_manager)
            codes = extractor.extract_multiple_codes("Multiple codes")
            
            assert len(codes) == 3
            assert "ABC123" in codes
            assert "XYZ789" in codes
            assert "DEF456" in codes
    
    @pytest.mark.unit
    def test_extract_multiple_codes_none(self, mock_llm):
        """Test when no codes are found."""
        mock_llm.invoke.return_value = Mock(content="NONE")
        prompt_manager = PromptManager()
        
        with patch('gmail_reader.extractor.llm_extractor.init_chat_model', return_value=mock_llm):
            extractor = LLMExtractor({}, prompt_manager)
            codes = extractor.extract_multiple_codes("No codes")
            
            assert codes == []