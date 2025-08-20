import logging
from pathlib import Path
from typing import Optional, cast
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from .config import CRED_FILE, SCOPES, TOKEN_FILE

logger = logging.getLogger(__name__)


class GmailAuthenticator:
    def __init__(self, 
                 credentials_file: Path = Path(CRED_FILE),
                 token_file: Path = TOKEN_FILE):
        self.credentials_file = Path(credentials_file)
        self.token_file = Path(token_file)
        self.creds: Optional[Credentials] = None
        
    def authenticate(self) -> Credentials:
        """Authenticate and return Gmail credentials."""
        # Check for existing token
        if self.token_file.exists():
            try:
                self.creds = Credentials.from_authorized_user_file(str(self.token_file), SCOPES)
                logger.info("Loaded credentials from token file")
            except Exception as e:
                logger.error(f"Error loading token: {e}")
                self.creds = None
        
        # Validate or refresh credentials
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                logger.info("Refreshing expired credentials")
                self.creds.refresh(Request())
            else:
                # Use credentials.json file directly
                if not self.credentials_file.exists():
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_file}\n"
                        "Download it from Google Cloud Console"
                    )
                
                logger.info("Starting OAuth flow")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_file), 
                    SCOPES
                )
                self.creds = cast(Credentials, flow.run_local_server(port=0))
            
            self._save_credentials()
        
        if not self.creds:
            raise ValueError("Failed to obtain valid credentials")
            
        return self.creds
    
    def _save_credentials(self) -> None:
        """Save credentials to token file."""
        if self.creds:
            self.token_file.parent.mkdir(parents=True, exist_ok=True)
            self.token_file.write_text(self.creds.to_json())
            logger.info(f"Saved credentials to {self.token_file}")