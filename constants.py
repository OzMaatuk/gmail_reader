"""Constants for Gmail Reader package."""

# Email operation constants
DEFAULT_MAX_RESULTS = 10
RECENT_EMAILS_DISPLAY_LIMIT = 5
VERIFICATION_EMAILS_PROCESS_LIMIT = 10
VERIFICATION_CODES_DISPLAY_LIMIT = 5

# Search queries
SEARCH_QUERIES = {
    "unread": "is:unread",
    "important": "is:important",
    "with attachments": "has:attachment",
    "from last week": "newer_than:7d"
}

# Verification keywords
VERIFICATION_KEYWORDS = ["verification", "confirm", "code", "OTP", "2FA", "PIN", "authenticate"]

# Sample content for demos
SAMPLE_VERIFICATIONS = [
    "Your verification code is: 123456",
    "Please use OTP: ABC-789 to continue",
    "Security PIN: 9876"
]

BATCH_EXTRACTION_SAMPLE = """
Here are your access codes:
Primary code: ABC123
Backup code: XYZ789
Emergency PIN: 4567
"""

# Display constants
SEPARATOR_WIDTH = 60
SEPARATOR_CHAR = "="

# Exit codes
EXIT_SUCCESS = 0
EXIT_ERROR = 1

# Messages
MSG_NO_EMAILS = "No messages found."
MSG_NO_VERIFICATION_EMAILS = "No potential verification emails found"
MSG_NO_CODES_FOUND = "No verification codes found in recent emails"
MSG_OPERATION_CANCELLED = "Operation cancelled by user"
MSG_ALL_COMPLETED = "All demonstrations completed successfully!"

# Application info
APP_NAME = "Gmail Reader Demo Application"
APP_VERSION = "0.1.0"