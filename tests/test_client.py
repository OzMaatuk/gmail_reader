# tests/test_client.py (fix the mock_gmail_service usage)
import pytest
from unittest.mock import Mock, patch, MagicMock
from googleapiclient.errors import HttpError

from gmail_reader.client import GmailClient
from gmail_reader.auth import GmailAuthenticator

class TestGmailClient:
    
    @pytest.mark.unit
    def test_init(self):
        """Test client initialization."""
        client = GmailClient()
        assert client.authenticator is not None
        assert client.service is None
    
    @pytest.mark.unit
    def test_init_with_authenticator(self):
        """Test client initialization with custom authenticator."""
        auth = Mock(spec=GmailAuthenticator)
        client = GmailClient(authenticator=auth)
        assert client.authenticator == auth
    
    @pytest.mark.unit
    @patch('gmail_reader.client.build')
    def test_connect(self, mock_build, mock_credentials, mock_gmail_service):
        """Test connecting to Gmail API."""
        mock_build.return_value = mock_gmail_service
        auth = Mock(spec=GmailAuthenticator)
        auth.authenticate.return_value = mock_credentials
        
        client = GmailClient(authenticator=auth)
        client.connect()
        
        auth.authenticate.assert_called_once()
        mock_build.assert_called_once_with("gmail", "v1", credentials=mock_credentials)
        assert client.service == mock_gmail_service
    
    @pytest.mark.unit
    def test_list_messages(self, mock_gmail_service):
        """Test listing messages."""
        client = GmailClient()
        client.service = mock_gmail_service
        
        # Call _get_message_summary with proper mock
        with patch.object(client, '_get_message_summary') as mock_summary:
            mock_summary.side_effect = lambda msg_id: {
                "id": msg_id,
                "subject": f"Message {msg_id}",
                "sender": "test@example.com",
                "date": "2024-01-01",
                "snippet": "Test snippet"
            }
            
            messages = client.list_messages(max_results=3)
            
            assert len(messages) == 3
            assert all('id' in msg for msg in messages)
            mock_gmail_service.users().messages().list.assert_called_with(
                userId="me", q="", maxResults=3
            )
    
    @pytest.mark.unit
    def test_list_messages_auto_connect(self, mock_gmail_service, mock_credentials):
        """Test list messages with automatic connection."""
        with patch('gmail_reader.client.build') as mock_build:
            mock_build.return_value = mock_gmail_service
            auth = Mock(spec=GmailAuthenticator)
            auth.authenticate.return_value = mock_credentials
            
            client = GmailClient(authenticator=auth)
            
            with patch.object(client, '_get_message_summary') as mock_summary:
                mock_summary.side_effect = lambda msg_id: {"id": msg_id, "subject": f"Message {msg_id}"}
                messages = client.list_messages()
                
                assert client.service is not None
                assert len(messages) == 3
    
    @pytest.mark.unit
    def test_search_messages(self, mock_gmail_service):
        """Test searching messages."""
        client = GmailClient()
        client.service = mock_gmail_service
        
        with patch.object(client, '_get_message_summary') as mock_summary:
            mock_summary.return_value = {"id": "msg1", "subject": "Test"}
            messages = client.search_messages(query="is:unread", max_results=5)
            
            mock_gmail_service.users().messages().list.assert_called_with(
                userId="me", q="is:unread", maxResults=5
            )
    
    @pytest.mark.unit
    def test_get_message(self, mock_gmail_service):
        """Test getting a single message."""
        client = GmailClient()
        client.service = mock_gmail_service
        
        message = client.get_message("msg1")
        
        assert message["id"] == "msg1"
        assert message["subject"] == "Verification Code"
        assert message["sender"] == "noreply@example.com"
        assert "123456" in message["body"]
    
    @pytest.mark.unit
    def test_get_message_raw(self, mock_gmail_service):
        """Test getting raw message data."""
        # Create a new mock for raw format
        raw_mock = Mock()
        raw_mock.execute.return_value = {"raw": "base64data"}
        mock_gmail_service.users().messages().get.return_value = raw_mock
        
        client = GmailClient()
        client.service = mock_gmail_service
        
        raw_message = client.get_message_raw("msg1")
        
        assert raw_message == {"raw": "base64data"}
        mock_gmail_service.users().messages().get.assert_called_with(
            userId="me", id="msg1", format="raw"
        )
    
    @pytest.mark.unit
    def test_get_labels(self, mock_gmail_service):
        """Test getting Gmail labels."""
        client = GmailClient()
        client.service = mock_gmail_service
        
        labels = client.get_labels()
        
        assert len(labels) == 2
        assert labels[0]["name"] == "INBOX"
        assert labels[1]["name"] == "Important"
    
    @pytest.mark.unit
    def test_parse_message_with_parts(self):
        """Test parsing message with multiple parts."""
        message_data = {
            "id": "msg2",
            "threadId": "thread2",
            "snippet": "Test snippet",
            "payload": {
                "headers": [
                    {"name": "Subject", "value": "Test Email"},
                    {"name": "From", "value": "test@example.com"}
                ],
                "parts": [
                    {
                        "mimeType": "text/plain",
                        "body": {"data": "VGVzdCBib2R5"}  # "Test body"
                    },
                    {
                        "mimeType": "text/html",
                        "body": {"data": "PGh0bWw+VGVzdDwvaHRtbD4="}
                    }
                ]
            },
            "labelIds": ["INBOX"]
        }
        
        client = GmailClient()
        parsed = client._parse_message(message_data)
        
        assert parsed["subject"] == "Test Email"
        assert parsed["sender"] == "test@example.com"
        assert "Test body" in parsed["body"]
    
    @pytest.mark.unit
    def test_decode_base64(self):
        """Test base64 decoding."""
        encoded = "SGVsbG8gV29ybGQ="  # "Hello World"
        decoded = GmailClient._decode_base64(encoded)
        assert decoded == "Hello World"
    
    @pytest.mark.unit
    def test_error_handling(self, mock_gmail_service):
        """Test error handling for API errors."""
        # Create HTTP error response
        resp = Mock()
        resp.status = 404
        error = HttpError(resp, b"Not found")
        
        mock_gmail_service.users().messages().list().execute.side_effect = error
        
        client = GmailClient()
        client.service = mock_gmail_service
        
        messages = client.list_messages()
        assert messages == []