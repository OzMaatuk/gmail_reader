import logging
from pathlib import Path
from typing import Optional, cast
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from .config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPES, TOKEN_FILE

logger = logging.getLogger(__name__)


class GmailAuthenticator:
    def __init__(self, token_file: Path = TOKEN_FILE):
        self.token_file = Path(token_file)
        self.creds: Optional[Credentials] = None
        
    def authenticate(self) -> Credentials:
        """Authenticate and return Gmail credentials."""
        if self.token_file.exists():
            try:
                self.creds = Credentials.from_authorized_user_file(str(self.token_file), SCOPES)
                logger.info("Loaded credentials from token file")
            except Exception as e:
                logger.error(f"Error loading credentials: {e}")
                self.creds = None
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                logger.info("Refreshing expired credentials")
                self.creds.refresh(Request())
            else:
                logger.info("Starting OAuth flow")
                flow = InstalledAppFlow.from_client_config(
                    {
                        "installed": {
                            "client_id": CLIENT_ID,
                            "client_secret": CLIENT_SECRET,
                            "redirect_uris": [REDIRECT_URI],
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                        }
                    },
                    SCOPES
                )
                # Explicitly cast the result to the expected type
                result = flow.run_local_server(port=8080)
                self.creds = cast(Credentials, result)
            
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