# main.py
#!/usr/bin/env python3
"""
Gmail Reader - Example usage script
"""
import logging
import sys
from gmail_reader import GmailClient
from gmail_reader.extractor import VerificationCodeExtractor
from constants import (
    DEFAULT_MAX_RESULTS,
    RECENT_EMAILS_DISPLAY_LIMIT,
    VERIFICATION_EMAILS_PROCESS_LIMIT,
    VERIFICATION_CODES_DISPLAY_LIMIT,
    SEARCH_QUERIES,
    VERIFICATION_KEYWORDS,
    SAMPLE_VERIFICATIONS,
    BATCH_EXTRACTION_SAMPLE,
    SEPARATOR_WIDTH,
    SEPARATOR_CHAR,
    EXIT_SUCCESS,
    EXIT_ERROR,
    MSG_NO_EMAILS,
    MSG_NO_VERIFICATION_EMAILS,
    MSG_NO_CODES_FOUND,
    MSG_OPERATION_CANCELLED,
    MSG_ALL_COMPLETED,
    APP_NAME,
    APP_VERSION,
    LOG_LEVEL,
    LOG_FORMAT
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT
)
logger = logging.getLogger(__name__)


def print_separator(title: str = "") -> None:
    """Print a formatted separator with optional title."""
    print("\n" + SEPARATOR_CHAR * SEPARATOR_WIDTH)
    if title:
        print(title)
        print(SEPARATOR_CHAR * SEPARATOR_WIDTH)


def demonstrate_email_operations(client: GmailClient) -> None:
    """
    Demonstrate basic email reading and searching operations.
    
    Args:
        client: Connected GmailClient instance
    """
    logger.info("Starting email operations demonstration")
    
    print_separator("EMAIL OPERATIONS DEMONSTRATION")
    
    # Fetch recent emails
    recent_emails = client.list_messages(max_results=DEFAULT_MAX_RESULTS)
    print(f"\n✓ Found {len(recent_emails)} recent emails")
    
    if recent_emails:
        # Display summary
        print("\nRecent emails summary:")
        for i, msg in enumerate(recent_emails[:RECENT_EMAILS_DISPLAY_LIMIT], 1):
            print(f"\n{i}. {msg.get('subject', 'No subject')}")
            print(f"   From: {msg.get('sender', 'Unknown')}")
            print(f"   Date: {msg.get('date', 'Unknown')}")
    
    # Demonstrate search capabilities
    print("\n\nSearch demonstrations:")
    for description, query in SEARCH_QUERIES.items():
        results = client.search_messages(query=query, max_results=RECENT_EMAILS_DISPLAY_LIMIT)
        print(f"\n• {description.title()}: {len(results)} emails found")
        if results:
            print(f"  Latest: {results[0].get('subject', 'No subject')}")
    
    # Get labels
    labels = client.get_labels()
    user_labels = [label for label in labels if label.get('type') == 'user']
    print(f"\n✓ Found {len(user_labels)} user labels")
    
    logger.info("Email operations demonstration completed")


def demonstrate_verification_extraction(client: GmailClient) -> None:
    """
    Demonstrate verification code extraction from emails.
    
    Args:
        client: Connected GmailClient instance
    """
    logger.info("Starting verification code extraction demonstration")
    
    print_separator("VERIFICATION CODE EXTRACTION DEMONSTRATION")
    
    # Initialize extractor
    extractor = VerificationCodeExtractor()
    
    # Search for potential verification emails
    query = " OR ".join([f"subject:{keyword}" for keyword in VERIFICATION_KEYWORDS])
    
    potential_emails = client.search_messages(
        query=query, 
        max_results=VERIFICATION_EMAILS_PROCESS_LIMIT * 2
    )
    print(f"\n✓ Found {len(potential_emails)} potential verification emails")
    
    # Extract codes
    extracted_codes = []
    for email in potential_emails[:VERIFICATION_EMAILS_PROCESS_LIMIT]:
        try:
            full_email = client.get_message(email['id'])
            body = full_email.get('body', '')
            
            if body:
                code = extractor.extract_code(body)
                if code:
                    extracted_codes.append({
                        'subject': full_email.get('subject', 'No subject'),
                        'sender': full_email.get('sender', 'Unknown'),
                        'code': code,
                        'date': full_email.get('date', 'Unknown')
                    })
        except Exception as e:
            logger.error(f"Error processing email {email['id']}: {e}")
    
    # Display results
    if extracted_codes:
        print(f"\n✓ Successfully extracted {len(extracted_codes)} verification codes:\n")
        for item in extracted_codes[:VERIFICATION_CODES_DISPLAY_LIMIT]:
            print(f"• Code: {item['code']}")
            print(f"  From: {item['sender']}")
            print(f"  Subject: {item['subject']}")
            print(f"  Date: {item['date']}\n")
    else:
        print(f"\n✗ {MSG_NO_CODES_FOUND}")
        
        # Demo with samples
        print("\nDemo with sample content:")
        for sample in SAMPLE_VERIFICATIONS:
            code = extractor.extract_code(sample)
            print(f"• Sample: '{sample}' → Code: {code}")
    
    # Demonstrate batch extraction
    print("\n\nBatch extraction demo:")
    multiple_codes = extractor.extract_multiple_codes(BATCH_EXTRACTION_SAMPLE)
    print(f"✓ Found {len(multiple_codes)} codes: {', '.join(multiple_codes)}")
    
    logger.info("Verification extraction demonstration completed")


def main():
    """Main function orchestrating the demonstrations."""
    try:
        # Initialize and connect
        logger.info("Initializing Gmail client...")
        client = GmailClient()
        
        logger.info("Connecting to Gmail...")
        client.connect()
        
        print(f"\n{APP_NAME} v{APP_VERSION}")
        print("=" * len(APP_NAME))
        
        # Run demonstrations
        demonstrate_email_operations(client)
        demonstrate_verification_extraction(client)
        
        print(f"\n✓ {MSG_ALL_COMPLETED}")
        
    except KeyboardInterrupt:
        logger.info(MSG_OPERATION_CANCELLED)
        sys.exit(EXIT_SUCCESS)
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"\n✗ Error: {e}")
        sys.exit(EXIT_ERROR)


if __name__ == "__main__":
    main()