# gmail_reader/extractor/patterns.py (fix for regex patterns)
"""Regex patterns for verification code extraction."""
import re
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


class RegexPatterns:
    """Manages regex patterns for fallback code extraction."""
    
    DEFAULT_PATTERNS = [
        # More specific patterns first
        r'(?:verification\s+code|otp|pin|code)[\s:]+([A-Z0-9]{4,8})\b',  # Labeled codes
        r'(?:is|:)\s+([A-Z0-9]{4,8})\b',  # After "is" or ":"
        r'\b([A-Z0-9]{6})\b',  # Exactly 6 alphanumeric
        r'\b(\d{4,8})\b',  # 4-8 digits
    ]
    
    def __init__(self, custom_patterns: Optional[List[str]] = None):
        """Initialize with default or custom patterns."""
        self.patterns = custom_patterns or self.DEFAULT_PATTERNS
    
    def extract_code(self, content: str) -> Optional[str]:
        """Extract a single code using regex patterns."""
        # Common words to exclude
        exclude_words = {'is', 'here', 'the', 'your', 'code', 'pin', 'otp', 'to', 'of', 'in', 'for'}
        
        for pattern in self.patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                code = match.group(1) if match.groups() else match.group(0)
                # Skip common words and check length
                if code.lower() not in exclude_words and len(code) >= 4:
                    logger.debug(f"Regex pattern '{pattern}' found code: {code}")
                    return code
        
        logger.debug("No verification code found with regex patterns")
        return None
    
    def extract_multiple_codes(self, content: str) -> List[str]:
        """Extract multiple codes using regex patterns."""
        codes = []
        exclude_words = {'is', 'here', 'the', 'your', 'code', 'pin', 'otp', 'to', 'of', 'in', 'for'}
        
        for pattern in self.patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                code = match if isinstance(match, str) else match[0]
                if code.lower() not in exclude_words and len(code) >= 4:
                    codes.append(code)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_codes = []
        for code in codes:
            if code not in seen:
                seen.add(code)
                unique_codes.append(code)
        
        return unique_codes