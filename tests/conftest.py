# tests/conftest.py
import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import Resource

@pytest.fixture
def mock_credentials():
    """Mock Google OAuth2 credentials."""
    creds = Mock(spec=Credentials)
    creds.valid = True
    creds.expired = False
    creds.refresh_token = "mock_refresh_token"
    creds.to_json.return_value = '{"token": "mock_token"}'
    return creds

@pytest.fixture
def mock_gmail_service():
    """Mock Gmail API service."""
    service = MagicMock()
    
    # Set up the messages().list() response
    list_response = {
        "messages": [
            {"id": "msg1"},
            {"id": "msg2"},
            {"id": "msg3"}
        ]
    }
    service.users().messages().list().execute.return_value = list_response
    
    # Set up the messages().get() response
    get_response = {
        "id": "msg1",
        "threadId": "thread1",
        "snippet": "Your verification code is 123456",
        "payload": {
            "headers": [
                {"name": "Subject", "value": "Verification Code"},
                {"name": "From", "value": "noreply@example.com"},
                {"name": "To", "value": "user@example.com"},
                {"name": "Date", "value": "2024-01-01 12:00:00"}
            ],
            "body": {
                "data": "WW91ciB2ZXJpZmljYXRpb24gY29kZSBpczogMTIzNDU2"  # Base64: "Your verification code is: 123456"
            }
        },
        "labelIds": ["INBOX", "UNREAD"]
    }
    service.users().messages().get().execute.return_value = get_response
    
    # Set up the labels().list() response
    labels_response = {
        "labels": [
            {"id": "INBOX", "name": "INBOX", "type": "system"},
            {"id": "Label_1", "name": "Important", "type": "user"}
        ]
    }
    service.users().labels().list().execute.return_value = labels_response
    
    return service

@pytest.fixture
def mock_flow():
    """Mock OAuth flow."""
    flow = Mock()
    flow.run_local_server.return_value = Mock(spec=Credentials)
    return flow

@pytest.fixture
def temp_token_file(tmp_path):
    """Temporary token file path."""
    return tmp_path / "token.json"

@pytest.fixture
def temp_cred_file(tmp_path):
    """Temporary credentials file path."""
    cred_file = tmp_path / "credentials.json"
    cred_file.write_text('{"installed": {"client_id": "test", "client_secret": "test"}}')
    return cred_file

@pytest.fixture
def mock_llm():
    """Mock LLM model."""
    llm = Mock()
    llm.invoke.return_value = Mock(content="123456")
    return llm

@pytest.fixture
def sample_email_content():
    """Sample email content for testing."""
    return {
        "simple_verification": "Your verification code is: 123456",
        "otp_code": "Please use OTP: ABC789 to continue",
        "pin_code": "Your security PIN is 9876",
        "multiple_codes": "Primary code: ABC123\nBackup code: XYZ789\nEmergency PIN: 4567",
        "no_code": "This email contains no verification codes.",
        "complex_html": "<html><body>Your code: <b>HTML456</b></body></html>"
    }