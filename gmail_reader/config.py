# gmail_reader/config.py

import logging
import configparser
from pathlib import Path

# Load config
config = configparser.ConfigParser()
config_path = Path(__file__).parent.parent / "config.ini"
if config_path.exists():
    config.read(config_path)

# OAuth settings
# CLIENT_ID = os.getenv("GMAIL_CLIENT_ID")
# CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET")
REDIRECT_URI = config.get("oauth", "redirect_uri", fallback="http://localhost:8080")
CRED_FILE = Path(config.get("oauth", "cred_file", fallback="cert/credentials.json"))
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# App settings
TOKEN_FILE = Path(config.get("app", "token_file", fallback="cert/token.json"))
MAX_RESULTS = config.getint("app", "max_results", fallback=3)

# Logging configuration
LOG_LEVEL = config.get("logging", "level", fallback="INFO")
LOG_FORMAT = config.get("logging", "format", 
                       fallback="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)