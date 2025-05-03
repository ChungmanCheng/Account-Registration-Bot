from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from browser import get_driver, type_with_delay
import time

def search_registration_urls(max_results=10):
    query = "site:*.com inurl:(signup | register)"
    driver = get_driver()
    try:
        driver.get("https://www.google.com")
        time.sleep(1)

        search_box = driver.find_element(By.NAME, "q")
        type_with_delay(search_box, query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        urls = []
        result_elements = driver.find_elements(By.CSS_SELECTOR, "div.g a")
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