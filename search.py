from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browser import get_driver, type_with_delay
import time
import os
import logging

logging.getLogger('selenium.webdriver').setLevel(logging.ERROR)

def search_registration_urls(max_results=50):
    query = "site:*.com inurl:(signup | register)"
    driver = get_driver()
    try:
        driver.get("https://www.google.com")

        search_box = driver.find_element(By.NAME, "q")
        type_with_delay(search_box, query)
        search_box.send_keys(Keys.RETURN)

        # Wait for search results page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.yuRUbf"))
        )

        urls = set()
        pages_processed = 0
        max_pages = max_results / 8 + 1

        while len(urls) < max_results and pages_processed < max_pages:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            result_elements = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf a")
            for element in result_elements:
                url = element.get_attribute("href")
                if url:
                    parsed_url = urlparse(url)
                    if parsed_url.scheme and parsed_url.netloc:
                        clean_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}".rstrip('/')
                        urls.add(clean_url)
                        if len(urls) >= max_results:
                            break
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a#pnnext"))
                )
                driver.execute_script("arguments[0].click();", next_button)
                print(f"Waiting for page {pages_processed + 2} to load...")
                # Wait for next page to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.yuRUbf"))
                )
                print(f"Page {pages_processed + 2} loaded.")
                pages_processed += 1
            except Exception as e:
                print(f"Unexpected error during pagination: {type(e).__name__}: {e}")
                print("No more pages to process or 'Next' button not found.")
                break

        urls = list(urls)[:max_results]
        print(f"Found {len(urls)} potential registration URLs after processing {pages_processed + 1} page(s).")
        return urls

    except Exception as e:
        print(f"Failed to search Google: {e}")
        return []
    finally:
        driver.quit()