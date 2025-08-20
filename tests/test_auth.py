# tests/test_auth.py
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from google.auth.exceptions import RefreshError

from gmail_reader.auth import GmailAuthenticator

class TestGmailAuthenticator:
    
    @pytest.mark.unit
    def test_init(self, temp_token_file, temp_cred_file):
        """Test authenticator initialization."""
        auth = GmailAuthenticator(
            credentials_file=temp_cred_file,
            token_file=temp_token_file
        )
        assert auth.credentials_file == temp_cred_file
        assert auth.token_file == temp_token_file
        assert auth.creds is None
    
    @pytest.mark.unit
    @patch('gmail_reader.auth.Credentials.from_authorized_user_file')
    def test_authenticate_with_valid_token(self, mock_from_file, mock_credentials, temp_token_file, temp_cred_file):
        """Test authentication with existing valid token."""
        temp_token_file.write_text('{"token": "test"}')
        mock_from_file.return_value = mock_credentials
        
        auth = GmailAuthenticator(token_file=temp_token_file)
        creds = auth.authenticate()
        
        assert creds == mock_credentials
        mock_from_file.assert_called_once()
    
    @pytest.mark.unit
    @patch('gmail_reader.auth.Credentials.from_authorized_user_file')
    @patch('gmail_reader.auth.Request')
    def test_authenticate_refresh_expired(self, mock_request, mock_from_file, mock_credentials, temp_token_file):
        """Test refreshing expired credentials."""
        temp_token_file.write_text('{"token": "expired"}')
        mock_credentials.valid = False
        mock_credentials.expired = True
        mock_from_file.return_value = mock_credentials
        
        auth = GmailAuthenticator(token_file=temp_token_file)
        creds = auth.authenticate()
        
        mock_credentials.refresh.assert_called_once()
        assert creds == mock_credentials
    
    @pytest.mark.unit
    @patch('gmail_reader.auth.InstalledAppFlow.from_client_secrets_file')
    def test_authenticate_new_flow(self, mock_flow_factory, mock_flow, temp_token_file, temp_cred_file):
        """Test authentication with new OAuth flow."""
        mock_flow_factory.return_value = mock_flow
        mock_new_creds = Mock()
        mock_new_creds.to_json.return_value = '{"token": "new"}'
        mock_flow.run_local_server.return_value = mock_new_creds
        
        auth = GmailAuthenticator(
            credentials_file=temp_cred_file,
            token_file=temp_token_file
        )
        creds = auth.authenticate()
        
        assert creds == mock_new_creds
        assert temp_token_file.exists()
        mock_flow.run_local_server.assert_called_once_with(port=0)
    
    @pytest.mark.unit
    def test_authenticate_missing_credentials_file(self, temp_token_file):
        """Test authentication with missing credentials file."""
        auth = GmailAuthenticator(
            credentials_file=Path("nonexistent.json"),
            token_file=temp_token_file
        )
        
        with pytest.raises(FileNotFoundError):
            auth.authenticate()
    
    @pytest.mark.unit
    @patch('gmail_reader.auth.Credentials.from_authorized_user_file')
    def test_save_credentials(self, mock_from_file, mock_credentials, temp_token_file):
        """Test saving credentials to file."""
        auth = GmailAuthenticator(token_file=temp_token_file)
        auth.creds = mock_credentials
        auth._save_credentials()
        
        assert temp_token_file.exists()
        mock_credentials.to_json.assert_called_once()