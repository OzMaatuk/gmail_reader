# gmail_reader/__init__.py

from .client import GmailClient
from .auth import GmailAuthenticator
from .extractor import VerificationCodeExtractor

__version__ = "0.1.0"
__all__ = ["GmailClient", "GmailAuthenticator", "VerificationCodeExtractor"]