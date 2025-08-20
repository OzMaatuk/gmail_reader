# Gmail Reader

A simple, clean, and secure Python package for reading emails from Gmail using OAuth 2.0 authentication.

## Features

- OAuth 2.0 authentication for secure access
- Simple and intuitive API
- Configurable settings via config files
- Comprehensive logging
- Type hints for better code clarity
- Token persistence to avoid repeated authentication

## Project Structure

```
gmail-reader/
├── gmail_reader/          # Main package directory
│   ├── __init__.py       # Package initialization and exports
│   ├── auth.py           # OAuth 2.0 authentication handler
│   ├── client.py         # Gmail API client implementation
│   └── config.py         # Configuration management
├── config.ini            # Application configuration
├── requirements.txt      # Package dependencies
├── setup.py             # Package setup file
├── main.py              # Example usage script
└── README.md            # This file
```

## Setup Instructions

1. **Create Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable Gmail API

2. **Create OAuth 2.0 Credentials**:
   - Go to APIs & Services > Credentials
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app"
   - Download the credentials JSON file
   - Save it as `credentials.json` in your project root
   - Add your account as tester in "OAuth Consent Screen Configuration" > "Audience"

3. **First Run**:
   - The app will open a browser for authentication
   - Grant the requested permissions
   - The `token.json` will be created automatically
   - Future runs will use the saved token

## Security Notes
- Never commit `credentials.json` or `token.json` to version control
- Add both files to `.gitignore`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/gmail-reader.git
cd gmail-reader
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package:
```bash
pip install -e .
```

Or install dependencies directly:
```bash
pip install -r requirements.txt
```

## Configuration

1. **Config File**: The `config.ini` file contains application settings:
```ini
[oauth]
redirect_uri = http://localhost:8080
cred_file = cert/credentials.json

[app]
token_file = cert/token.json
max_results = 10

[logging]
level = INFO
format = %(asctime)s - %(name)s - %(levelname)s - %(message)s
```

## Usage

### Basic Usage

```python
from gmail_reader import GmailClient

# Initialize client
client = GmailClient()

# Connect to Gmail
client.connect()

# List recent emails
messages = client.list_messages(max_results=5)

# Read a specific email
if messages:
    email_content = client.get_message(messages[0]['id'])
    print(f"Subject: {email_content['subject']}")
    print(f"From: {email_content['sender']}")
    print(f"Body: {email_content['body']}")

# Search emails
search_results = client.search_messages(
    query="from:example@gmail.com subject:important",
    max_results=10
)
```

### Advanced Usage

```python
from gmail_reader import GmailClient, GmailAuthenticator
from pathlib import Path

# Custom token file location
auth = GmailAuthenticator(token_file=Path("custom_token.json"))
client = GmailClient(authenticator=auth)

# Connect with custom settings
client.connect()

# Get emails with attachments
messages_with_attachments = client.search_messages(
    query="has:attachment",
    max_results=5
)

# Get labels
labels = client.get_labels()
```

## First Run

On the first run, the application will:
1. Open your default web browser
2. Ask you to log in to your Google account
3. Request permission to read your Gmail
4. Save the authentication token locally

Subsequent runs will use the saved token automatically.

## API Reference

### GmailClient

#### Methods

- `connect()`: Establish connection to Gmail API
- `list_messages(query="", max_results=10)`: List messages, optionally filtered by query
- `get_message(message_id)`: Get full message content by ID
- `search_messages(query, max_results=10)`: Search messages with Gmail query syntax
- `get_labels()`: Get all Gmail labels
- `get_message_raw(message_id)`: Get raw message data

### GmailAuthenticator

#### Methods

- `authenticate()`: Perform OAuth 2.0 authentication and return credentials

## Security Notes

- Never commit your `credentials.json` file or `token.json` to version control
- The `token.json` file contains sensitive authentication data
- Use appropriate file permissions for credential files
- Consider encrypting stored tokens in production environments

## Gmail Search Query Examples

- `from:sender@example.com` - Emails from specific sender
- `to:me` - Emails sent to you
- `subject:meeting` - Emails with "meeting" in subject
- `has:attachment` - Emails with attachments
- `is:unread` - Unread emails
- `after:2024/1/1` - Emails after a specific date
- `label:important` - Emails with specific label

## Troubleshooting

### Common Issues

1. **"Credentials not found" error**
   - Ensure `credentials.json` file exists with correct credentials
   - Check that `GMAIL_CLIENT_ID` and `GMAIL_CLIENT_SECRET` are set

2. **"Access blocked" error**
   - Make sure Gmail API is enabled in Google Cloud Console
   - Check that OAuth consent screen is configured

3. **Token refresh issues**
   - Delete `token.json` and re-authenticate
   - Ensure your OAuth app is not in testing mode with expired refresh tokens