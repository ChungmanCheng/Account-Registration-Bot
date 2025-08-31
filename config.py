
import json
import os
from dotenv import load_dotenv
import logging

def load_config(mode='register'):
    """Load .env and account_registration.json configurations."""
    # Load .env
    load_dotenv()
    emails = os.getenv("EMAILS")
    password = os.getenv("PASSWORD")

    # Parse emails into a list
    email_list = [email.strip() for email in emails.split(",")] if emails else []
    
    # Load JSON config
    config_path = 'account_registration.json'
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            site_configs = json.load(f)  # Parse JSON into list of dicts
    else:
        logging.warning("No account_registration.json found. Using defaults.")
        site_configs = []  # Empty list if no file

    return email_list, password, site_configs