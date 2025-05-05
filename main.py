
import argparse
from search import search_registration_urls
from config import load_config
from register import register_accounts

def main():
    parser = argparse.ArgumentParser(
        description="Account Registration Bot: Automatically searches Google for registration URLs, verifies them, and registers accounts using emails from .env. Configure account_registration.json with form field selectors before running."
    )
    # No explicit -h/--help; argparse provides it automatically

    args = parser.parse_args()

    email_list, password = load_config()

    # Step 1: Search Google for registration URLs
    print("Searching Google for registration URLs...")
    urls = search_registration_urls()
    register_accounts( urls, email_list, password )


if __name__ == "__main__":
    main()
