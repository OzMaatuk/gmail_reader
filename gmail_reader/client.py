import logging
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .auth import GmailAuthenticator
from .config import MAX_RESULTS

logger = logging.getLogger(__name__)


class GmailClient:
    def __init__(self, authenticator: Optional[GmailAuthenticator] = None):
        self.authenticator = authenticator or GmailAuthenticator()
        self.service = None
        
    def connect(self):
        """Connect to Gmail API."""
        creds = self.authenticator.authenticate()
        self.service = build("gmail", "v1", credentials=creds)
        logger.info("Connected to Gmail API")
        
    def list_messages(self, query: str = "", max_results: int = MAX_RESULTS) -> List[Dict]:
        """List messages matching the query."""
        if not self.service:
            self.connect()
            
        try:
            results = self.service.users().messages().list(
                userId="me",
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get("messages", [])
            return [self._get_message_summary(msg["id"]) for msg in messages]
            
        except HttpError as error:
            logger.error(f"An error occurred: {error}")
            return []
    
    def search_messages(self, query: str, max_results: int = MAX_RESULTS) -> List[Dict]:
        """Search messages with Gmail query syntax."""
        return self.list_messages(query=query, max_results=max_results)
    
    def get_message(self, message_id: str) -> Dict:
        """Get full message content by ID."""
        if not self.service:
            self.connect()
            
        try:
            message = self.service.users().messages().get(
                userId="me",
                id=message_id
            ).execute()
            
            return self._parse_message(message)
            
        except HttpError as error:
            logger.error(f"An error occurred: {error}")
            return {}
    
    def get_message_raw(self, message_id: str) -> Dict:
        """Get raw message data."""
        if not self.service:
            self.connect()
            
        try:
            return self.service.users().messages().get(
                userId="me",
                id=message_id,
                format="raw"
            ).execute()
            
        except HttpError as error:
            logger.error(f"An error occurred: {error}")
            return {}
    
    def get_labels(self) -> List[Dict]:
        """Get all Gmail labels."""
        if not self.service:
            self.connect()
            
        try:
            results = self.service.users().labels().list(userId="me").execute()
            return results.get("labels", [])
            
        except HttpError as error:
            logger.error(f"An error occurred: {error}")
            return []
    
    def _get_message_summary(self, message_id: str) -> Dict:
        """Get message summary with basic info."""
        message = self.get_message(message_id)
        return {
            "id": message_id,
            "subject": message.get("subject", ""),
            "sender": message.get("sender", ""),
            "date": message.get("date", ""),
            "snippet": message.get("snippet", "")
        }
    
    def _parse_message(self, message: Dict) -> Dict:
        """Parse message to extract relevant information."""
        payload = message.get("payload", {})
        headers = payload.get("headers", [])
        
        # Extract header information
        header_dict = {header["name"]: header["value"] for header in headers}
        
        parsed = {
            "id": message.get("id", ""),
            "thread_id": message.get("threadId", ""),
            "subject": header_dict.get("Subject", ""),
            "sender": header_dict.get("From", ""),
            "recipient": header_dict.get("To", ""),
            "date": header_dict.get("Date", ""),
            "snippet": message.get("snippet", ""),
            "body": self._get_message_body(payload),
            "label_ids": message.get("labelIds", [])
        }
        
        return parsed
    
    def _get_message_body(self, payload: Dict) -> str:
        """Extract message body from payload."""
        body = ""
        
        if "parts" in payload:
            for part in payload["parts"]:
                if part["mimeType"] == "text/plain":
                    data = part["body"].get("data", "")
                    if data:
                        body = self._decode_base64(data)
                        break
                elif part["mimeType"] == "text/html" and not body:
                    data = part["body"].get("data", "")
                    if data:
                        body = self._decode_base64(data)
        else:
            # Single part message
            if payload["body"].get("data"):
                body = self._decode_base64(payload["body"]["data"])
        
        return body
    
    @staticmethod
    def _decode_base64(data: str) -> str:
        """Decode base64 string."""
        import base64
        return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")