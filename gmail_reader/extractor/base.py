"""Main verification code extractor implementation."""
import logging
from typing import Optional, Dict, List
from langchain.chat_models.base import BaseChatModel

from .config import ExtractorConfig
from .patterns import RegexPatterns
from .prompts import PromptManager
from .llm_extractor import LLMExtractor

logger = logging.getLogger(__name__)


class VerificationCodeExtractor:
    """Extracts verification codes from email content using LLM."""
    
    def __init__(
        self,
        llm_config: Optional[Dict] = None,
        prompt_template: Optional[str] = None,
        fallback_patterns: Optional[List[str]] = None
    ):
        """
        Initialize the VerificationCodeExtractor.
        
        Args:
            llm_config: Configuration for the LLM model
            prompt_template: Custom prompt template (must include {content} placeholder)
            fallback_patterns: Regex patterns to use as fallback
        """
        logger.info("Initializing VerificationCodeExtractor")
        
        # Initialize configuration
        self.config = ExtractorConfig()
        
        # Load LLM configuration
        if llm_config is None:
            llm_config = self.config.load_llm_config()
        
        # Initialize components
        self.prompt_manager = PromptManager(custom_template=prompt_template)
        self.regex_patterns = RegexPatterns(custom_patterns=fallback_patterns)
        self.llm_extractor = LLMExtractor(llm_config, self.prompt_manager)
        
    def extract_code(self, content: str, use_fallback: bool = True) -> Optional[str]:
        """
        Extract a single verification code from email content.
        
        Args:
            content: Email content to extract code from
            use_fallback: Whether to use regex patterns if LLM fails
            
        Returns:
            Extracted verification code or None
        """
        logger.debug("Extracting verification code from content")
        
        if not content or not content.strip():
            logger.warning("Empty content provided")
            return None
        
        # Try LLM extraction first
        if self.llm_extractor.is_available():
            code = self.llm_extractor.extract_single_code(content)
            if code:
                return code
        
        # Use fallback regex patterns
        if use_fallback:
            logger.debug("Using fallback regex patterns")
            return self.regex_patterns.extract_code(content)
        
        return None
    
    def extract_multiple_codes(self, content: str) -> List[str]:
        """Extract multiple verification codes from email content."""
        logger.debug("Extracting multiple verification codes")
        
        if not content or not content.strip():
            return []
        
        # Try LLM extraction
        if self.llm_extractor.is_available():
            codes = self.llm_extractor.extract_multiple_codes(content)
            if codes:
                return codes
        
        # Fallback to regex
        logger.debug("Using regex for multiple code extraction")
        return self.regex_patterns.extract_multiple_codes(content)