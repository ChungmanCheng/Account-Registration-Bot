
import json
import os
from dotenv import load_dotenv
import logging

def load_config():
    """Load .env and account_registration.json configurations."""
    # Load .env
    load_dotenv()
    emails = os.getenv("EMAILS")
    password = os.getenv("PASSWORD")

    # Parse emails into a list
    email_list = [email.strip() for email in emails.split(",")] if emails else []
    if not email_list:
        logging.warning("No emails found in .env. Using default dummy email.")
        email_list = ["default@example.com"]

    return email_list, password