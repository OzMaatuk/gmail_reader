import os
import configparser
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load config
config = configparser.ConfigParser()
config_path = Path(__file__).parent.parent / "config.ini"
config.read(config_path)

# OAuth settings
CLIENT_ID = os.getenv("GMAIL_CLIENT_ID")
CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET")
REDIRECT_URI = config.get("oauth", "redirect_uri", fallback="http://localhost:8080")
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# App settings
TOKEN_FILE = Path(config.get("app", "token_file", fallback="token.json"))
MAX_RESULTS = config.getint("app", "max_results", fallback=10)