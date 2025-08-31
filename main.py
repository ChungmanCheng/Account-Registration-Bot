#!/home/erwin/venv/3.10.13/bin/python
import argparse
from search import search_registration_urls
from config import load_config
from register import register_accounts

def main():
    parser = argparse.ArgumentParser(
        description="Account Registration Bot: Automatically searches Google for registration URLs, verifies them, and registers accounts using emails from .env. Configure account_registration.json with form field selectors before running."
    )
    parser.add_argument('--mode', choices=['register', 'login'], default='register', help="Mode: register (default) or login")
    parser.add_argument('--cognition', action='store_true', help="Enable cognition mode for dynamic field detection")
    # Optional: Add this if you have login mode with custom search
    # parser.add_argument('--search-login', action='store_true', help="Search for login URLs instead of registration (for login mode)")

    args = parser.parse_args()

    email_list, password, site_configs = load_config(mode=args.mode)

    # If no search, use JSON URLs; else search and append
    urls = [site['url'] for site in site_configs] if site_configs else []
    if args.mode == 'register':  # Or always search if flag set
        print("Searching Google for registration URLs...")
        searched_urls = search_registration_urls()
        urls.extend(searched_urls)

    if args.mode == 'register':
        register_accounts(urls, email_list, password, site_configs)


if __name__ == "__main__":
    main()