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

def search_registration_urls(max_results=10):
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

        urls = []
        result_elements = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf a")
        for element in result_elements[:max_results]:
            url = element.get_attribute("href")
            if url and ("signup" in url.lower() or "register" in url.lower() or "join" in url.lower()):
                parsed_url = urlparse(url)
                clean_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
                if clean_url not in urls:
                    urls.append(clean_url)

        print(f"Found {len(urls)} potential registration URLs.")
        return urls
    except Exception as e:
        print(f"Failed to search Google: {e}")
        return []
    finally:
        driver.quit()