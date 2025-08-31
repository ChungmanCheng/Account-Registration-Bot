from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browser import get_driver, type_with_delay
import logging
import time
import random

logging.getLogger('selenium.webdriver').setLevel(logging.ERROR)

def register_account(url, email, password, form_config=None):
    """
    Register an account on a given URL using provided email and password.
    
    Args:
        url (str): The registration page URL
        email (str): Email address for registration
        password (str): Password for registration
        form_config (dict): Optional configuration for form field selectors
    Returns:
        bool: True if registration attempt was successful, False otherwise
    """
    # Skip if URL appears to be a login page
    if any(term in url.lower() for term in ['login', 'signin', 'sign-in']):
        print(f"Skipping {url}: Appears to be a login page, not a registration page.")
        return False

    driver = get_driver()
    try:
        driver.get(url)
        print(f"Attempting registration on {url} with email {email}")

        # Default form field selectors if no config provided
        default_config = {
            'email_field': [
                'input[type="email"]',
                'input[name="email"]',
                'input[id*="email"]',
                'input[name="username"]'
            ],
            'text_field': [
                'input[type="text"]',
                'input[id*="text"]',
                'input[name="text"]',
                'input[id*="text"]'
            ],
            'username_field': [
                'input[name="username"]',
                'input[id*="username"]',
                'input[name="user"]',
                'input[id*="user"]'
            ],
            'first_name_field': [
                'input[name="first_name"]',
                'input[name="firstname"]',
                'input[name="fname"]',
                'input[id*="first_name"]'
            ],
            'last_name_field': [
                'input[name="last_name"]',
                'input[name="lastname"]',
                'input[name="lname"]',
                'input[id*="last_name"]'
            ],
            'password_field': [
                'input[type="password"]',
                'input[name="password"]',
                'input[id*="password"]'
            ],
            'confirm_password_field': [
                'input[name="confirm_password"]',
                'input[name="password_confirm"]',
                'input[name="password2"]',
                'input[id*="confirm_password"]'
            ],
            'phone_field': [
                'input[type="tel"]',
                'input[name="phone"]',
                'input[name="telephone"]',
                'input[id*="phone"]'
            ],
            'terms_checkbox': [
                'input[type="checkbox"][name*="terms"]',
                'input[type="checkbox"][name*="agree"]',
                'input[type="checkbox"][id*="terms"]'
            ],
            'submit_button': [
                'button[type="submit"]',
                'input[type="submit"]',
                'button[id*="submit"]',
                'button[class*="submit"]',
                'button:contains("Sign Up")',
                'button:contains("Register")'
            ]
        }

        # Ensure config is valid
        config = form_config if isinstance(form_config, dict) else default_config
        if not all(key in config for key in ['email_field', 'password_field', 'submit_button']):
            print(f"Invalid form_config for {url}: Missing required keys. Using default config.")
            config = default_config

        # Define values for additional fields
        username_value = email.split('@')[0]
        first_name_value = random.choice(['John', 'Jane', 'Alex', 'Chris', 'Pat'])
        last_name_value = random.choice(['Doe', 'Smith', 'Johnson', 'Lee', 'Brown'])
        phone_value = f"555-{random.randint(100,999)}-{random.randint(1000,9999)}"
        confirm_password_value = password

        text_field = None
        for selector in config.get('text_field', []):
            try:
                text_field = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if text_field:
                    type_with_delay(text_field, username_value)
                    break
            except Exception as e:
                print(f"Failed to find text field with selector '{selector}' on {url}: {e}")
                continue
        if not text_field:
            print(f"No text field found on {url}. Continuing.")

        # Find and fill username field (optional)
        username_field = None
        for selector in config.get('username_field', []):
            try:
                username_field = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if username_field:
                    type_with_delay(username_field, username_value)
                    break
            except Exception as e:
                print(f"Failed to find username field with selector '{selector}' on {url}: {e}")
                continue
        if not username_field:
            print(f"No username field found on {url}. Continuing.")

        # Find and fill first name field (optional)
        first_name_field = None
        for selector in config.get('first_name_field', []):
            try:
                first_name_field = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if first_name_field:
                    type_with_delay(first_name_field, first_name_value)
                    break
            except Exception as e:
                print(f"Failed to find first name field with selector '{selector}' on {url}: {e}")
                continue
        if not first_name_field:
            print(f"No first name field found on {url}. Continuing.")

        # Find and fill last name field (optional)
        last_name_field = None
        for selector in config.get('last_name_field', []):
            try:
                last_name_field = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if last_name_field:
                    type_with_delay(last_name_field, last_name_value)
                    break
            except Exception as e:
                print(f"Failed to find last name field with selector '{selector}' on {url}: {e}")
                continue
        if not last_name_field:
            print(f"No last name field found on {url}. Continuing.")

        # Find and fill email field
        email_field = None
        for selector in config['email_field']:
            try:
                email_field = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if email_field:
                    type_with_delay(email_field, email)
                    break
            except Exception as e:
                print(f"Failed to find email field with selector '{selector}' on {url}: {e}")
                continue

        if not email_field:
            print(f"Could not find email field on {url}. Continuing with other fields.")

        # Find and fill password field
        password_field = None
        for selector in config['password_field']:
            try:
                password_field = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if password_field:
                    type_with_delay(password_field, password)
                    break
            except Exception as e:
                print(f"Failed to find password field with selector '{selector}' on {url}: {e}")
                continue

        if not password_field:
            print(f"Could not find password field on {url}. Continuing with submit attempt.")

        # Find and fill confirm password field (optional)
        confirm_password_field = None
        for selector in config.get('confirm_password_field', []):
            try:
                confirm_password_field = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if confirm_password_field:
                    type_with_delay(confirm_password_field, confirm_password_value)
                    break
            except Exception as e:
                print(f"Failed to find confirm password field with selector '{selector}' on {url}: {e}")
                continue
        if not confirm_password_field:
            print(f"No confirm password field found on {url}. Continuing.")

        # Find and fill phone field (optional)
        phone_field = None
        for selector in config.get('phone_field', []):
            try:
                phone_field = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if phone_field:
                    type_with_delay(phone_field, phone_value)
                    break
            except Exception as e:
                print(f"Failed to find phone field with selector '{selector}' on {url}: {e}")
                continue
        if not phone_field:
            print(f"No phone field found on {url}. Continuing.")

        # Find and check terms checkbox (optional)
        terms_checkbox = None
        for selector in config.get('terms_checkbox', []):
            try:
                terms_checkbox = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if terms_checkbox and not terms_checkbox.is_selected():
                    driver.execute_script("arguments[0].click();", terms_checkbox)
                    break
            except Exception as e:
                print(f"Failed to find terms checkbox with selector '{selector}' on {url}: {e}")
                continue
        if not terms_checkbox:
            print(f"No terms checkbox found on {url}. Continuing.")

        # Find and click submit button
        submit_button = None
        submitted = False
        for selector in config['submit_button']:
            try:
                submit_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                if submit_button:
                    break
            except Exception as e:
                print(f"Failed to find submit button with selector '{selector}' on {url}: {e}")
                continue

        if submit_button:
            driver.execute_script("arguments[0].click();", submit_button)
            submitted = True
            print(f"Submitted form on {url}")
        else:
            print(f"Could not find submit button on {url}. Checking for success anyway.")

        # Wait for potential redirect or success indicator
        time.sleep(2)
        
        # Check for successful registration
        success_indicators = ['dashboard', 'profile', 'welcome', 'success']
        if submitted and any(indicator in driver.current_url.lower() for indicator in success_indicators):
            print(f"Registration likely successful for {email} on {url}")
            return True
        else:
            print(f"Registration may have failed for {email} on {url}")
            return False

    except Exception as e:
        print(f"Error during registration on {url}: {type(e).__name__}: {e}")
        return False
    finally:
        driver.quit()

def register_accounts(urls, email_list, password, form_config=None):
    """
    Register accounts for all URLs using provided emails and password.
    
    Args:
        urls (list): List of registration URLs
        email_list (list): List of email addresses
        password (str): Password for all registrations
        form_config (dict): Optional configuration for form field selectors
    Returns:
        dict: Summary of registration attempts
    """
    results = {'successful': [], 'failed': []}
    
    for url in urls:
        for email in email_list:
            success = register_account(url, email, password, form_config)
            if success:
                results['successful'].append({'url': url, 'email': email})
            else:
                results['failed'].append({'url': url, 'email': email})
            # Respectful delay between attempts
            time.sleep(1)
    
    print(f"Registration complete. Successful: {len(results['successful'])}, Failed: {len(results['failed'])}")
    return results