# tests/test_extractor_patterns.py
import pytest

from gmail_reader.extractor.patterns import RegexPatterns

class TestRegexPatterns:
    
    @pytest.mark.unit
    def test_init_default_patterns(self):
        """Test initialization with default patterns."""
        patterns = RegexPatterns()
        assert len(patterns.patterns) > 0
        assert patterns.patterns == RegexPatterns.DEFAULT_PATTERNS
    
    @pytest.mark.unit
    def test_init_custom_patterns(self):
        """Test initialization with custom patterns."""
        custom = [r'\d{6}', r'[A-Z]{3}-\d{3}']
        patterns = RegexPatterns(custom_patterns=custom)
        assert patterns.patterns == custom
    
    @pytest.mark.unit
    @pytest.mark.parametrize("content,expected", [
        ("Your code is 123456", "123456"),
        ("OTP: ABC123", "ABC123"),
        ("Verification code: XYZ789", "XYZ789"),
        ("PIN: 9876", "9876"),
        ("No code here", None),
    ])
    def test_extract_code(self, content, expected):
        """Test single code extraction with various inputs."""
        patterns = RegexPatterns()
        result = patterns.extract_code(content)
        assert result == expected
    
    @pytest.mark.unit
    def test_extract_multiple_codes(self):
        """Test extracting multiple codes."""
        patterns = RegexPatterns()
        content = "Codes: 1234, ABC567, and 890XYZ"
        
        codes = patterns.extract_multiple_codes(content)
        
        assert "1234" in codes
        assert len(codes) >= 2
    
    @pytest.mark.unit
    def test_extract_multiple_codes_no_duplicates(self):
        """Test that duplicate codes are removed."""
        patterns = RegexPatterns()
        content = "Code 1234 and again 1234, plus 5678"
        
        codes = patterns.extract_multiple_codes(content)
        
        assert codes.count("1234") == 1
        assert "5678" in codes