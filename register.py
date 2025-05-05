from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browser import get_driver, type_with_delay
import logging
import time

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
            'password_field': [
                'input[type="password"]',
                'input[name="password"]',
                'input[id*="password"]'
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

        # Find and fill email field
        email_field = None
        for selector in config['email_field']:
            try:
                email_field = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if email_field:
                    break
            except Exception as e:
                print(f"Failed to find email field with selector '{selector}' on {url}: {e}")
                continue

        if email_field:
            type_with_delay(email_field, email)
        else:
            print(f"Could not find email field on {url}. Continuing with other fields.")

        # Find and fill password field
        password_field = None
        for selector in config['password_field']:
            try:
                password_field = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if password_field:
                    break
            except Exception as e:
                print(f"Failed to find password field with selector '{selector}' on {url}: {e}")
                continue

        if password_field:
            type_with_delay(password_field, password)
        else:
            print(f"Could not find password field on {url}. Continuing with submit attempt.")

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