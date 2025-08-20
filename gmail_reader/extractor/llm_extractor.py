# gmail_reader/extractor/llm_extractor.py

"""LLM-based extraction logic."""
import logging
from typing import Optional, List, Dict
from langchain.chat_models.base import init_chat_model, BaseChatModel

from .prompts import PromptManager

logger = logging.getLogger(__name__)


class LLMExtractor:
    """Handles LLM-based verification code extraction."""
    
    def __init__(self, llm_config: Dict, prompt_manager: PromptManager):
        """Initialize the LLM extractor."""
        self.prompt_manager = prompt_manager
        self.llm: Optional[BaseChatModel] = None
        
        # Initialize LLM
        try:
            self.llm = init_chat_model(**llm_config)
            logger.info("LLM model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
    
    def is_available(self) -> bool:
        """Check if LLM is available."""
        return self.llm is not None
    
    def extract_single_code(self, content: str) -> Optional[str]:
        """Extract a single verification code using LLM."""
        if not self.llm:
            return None
        
        try:
            prompt = self.prompt_manager.get_single_code_prompt(content)
            response = self.llm.invoke(prompt)
            
            # Extract response content
            result = str(response.content) if hasattr(response, 'content') else str(response)
            result = result.strip()
            
            # Clean and validate the result
            if result and result != "NONE":
                result = result.strip('"\'')
                if len(result) <= 20 and (result.isalnum() or '-' in result or '_' in result):
                    logger.info(f"Successfully extracted code with LLM: {result}")
                    return result
            
        except Exception as e:
            logger.error(f"LLM extraction failed: {e}")
        
        return None
    
    def extract_multiple_codes(self, content: str) -> List[str]:
        """Extract multiple verification codes using LLM."""
        if not self.llm:
            return []
        
        try:
            prompt = self.prompt_manager.get_multi_code_prompt(content)
            response = self.llm.invoke(prompt)
            result = str(response.content) if hasattr(response, 'content') else str(response)
            
            if result and result != "NONE":
                codes = [code.strip() for code in result.split(',') if code.strip()]
                logger.info(f"Extracted {len(codes)} codes with LLM")
                return codes
                
        except Exception as e:
            logger.error(f"LLM multi-extraction failed: {e}")
        
        return []