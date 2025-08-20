"""Regex patterns for verification code extraction."""
import re
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


class RegexPatterns:
    """Manages regex patterns for fallback code extraction."""
    
    DEFAULT_PATTERNS = [
        r'\b\d{4,8}\b',  # 4-8 digit codes
        r'\b[A-Z0-9]{4,8}\b',  # Alphanumeric codes
        r'(?:code|otp|pin)[\s:]+([A-Z0-9]+)',  # Labeled codes
        r'(?:verification|confirm)[\s\w]*:?\s*([A-Z0-9]+)',  # Verification codes
    ]
    
    def __init__(self, custom_patterns: Optional[List[str]] = None):
        """Initialize with default or custom patterns."""
        self.patterns = custom_patterns or self.DEFAULT_PATTERNS
    
    def extract_code(self, content: str) -> Optional[str]:
        """Extract a single code using regex patterns."""
        for pattern in self.patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                # Get the full match or first capture group
                code = match.group(1) if match.groups() else match.group(0)
                logger.debug(f"Regex pattern '{pattern}' found code: {code}")
                return code
        
        logger.debug("No verification code found with regex patterns")
        return None
    
    def extract_multiple_codes(self, content: str) -> List[str]:
        """Extract multiple codes using regex patterns."""
        codes = []
        
        for pattern in self.patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            codes.extend(matches)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_codes = []
        for code in codes:
            if code not in seen:
                seen.add(code)
                unique_codes.append(code)
        
        return unique_codes