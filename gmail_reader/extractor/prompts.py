"""Prompt templates for LLM-based extraction."""
from typing import Optional


class PromptManager:
    """Manages prompt templates for verification code extraction."""
    
    DEFAULT_PROMPTS = {
        "verification_code": """
Extract the verification code from the following email content.
The code might be labeled as: verification code, OTP, PIN, confirmation code, security code, or similar.
Return ONLY the code itself, nothing else.

Email content:
{content}
""",
        "multi_code": """
Extract ALL verification codes from the following email content.
Return them as a comma-separated list.
If no codes found, return "NONE".

Email content:
{content}
"""}
    
    def __init__(self, custom_template: Optional[str] = None):
        """Initialize with default or custom prompt template."""
        self.verification_template = custom_template or self.DEFAULT_PROMPTS["verification_code"]
    
    def get_single_code_prompt(self, content: str) -> str:
        """Get prompt for single code extraction."""
        return self.verification_template.format(content=content)
    
    def get_multi_code_prompt(self, content: str) -> str:
        """Get prompt for multiple code extraction."""
        return self.DEFAULT_PROMPTS["multi_code"].format(content=content)