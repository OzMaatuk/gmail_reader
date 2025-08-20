#!/usr/bin/env python3
"""
Gmail Reader - Example usage script
"""
import logging
import sys
from gmail_reader import GmailClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating Gmail Reader usage."""
    try:
        # Initialize Gmail client
        logger.info("Initializing Gmail client...")
        client = GmailClient()
        
        # Connect to Gmail
        logger.info("Connecting to Gmail...")
        client.connect()
        
        # List recent messages
        logger.info("Fetching recent messages...")
        messages = client.list_messages(max_results=5)
        
        if not messages:
            logger.info("No messages found.")
            return
        
        print(f"\nFound {len(messages)} messages:\n")
        
        # Display message summaries
        for msg in messages:
            print(f"ID: {msg['id']}")
            print(f"Subject: {msg.get('subject', 'No subject')}")
            print(f"From: {msg.get('sender', 'Unknown')}")
            print(f"Date: {msg.get('date', 'Unknown')}")
            print("-" * 50)
        
        # Read first message in detail
        if messages:
            logger.info("Reading first message in detail...")
            first_msg = client.get_message(messages[0]['id'])
            
            print("\nFirst message details:")
            print(f"Subject: {first_msg.get('subject', 'No subject')}")
            print(f"From: {first_msg.get('sender', 'Unknown')}")
            print(f"To: {first_msg.get('recipient', 'Unknown')}")
            print(f"Date: {first_msg.get('date', 'Unknown')}")
            print(f"Body preview: {first_msg.get('body', '')[:200]}...")
        
        # Demonstrate search
        print("\n" + "="*50)
        search_query = "is:unread"
        logger.info(f"Searching for: {search_query}")
        search_results = client.search_messages(query=search_query, max_results=3)
        
        print(f"\nSearch results for '{search_query}':")
        print(f"Found {len(search_results)} unread messages")
        
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
