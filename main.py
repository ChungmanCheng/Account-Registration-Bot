
import argparse
from search import search_registration_urls


def main():
    parser = argparse.ArgumentParser(
        description="Account Registration Bot: Automatically searches Google for registration URLs, verifies them, and registers accounts using emails from .env. Configure account_registration.json with form field selectors before running."
    )
    # No explicit -h/--help; argparse provides it automatically

    args = parser.parse_args()

    # Step 1: Search Google for registration URLs
    print("Searching Google for registration URLs...")
    urls = search_registration_urls()
    for url in urls:
        print( url )


if __name__ == "__main__":
    main()
