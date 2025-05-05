from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from undetected_geckodriver import Firefox
import time

def get_driver():
    options = Options()
    # options.add_argument("--headless")  # Enable headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--private")
    driver = Firefox(options=options)
    return driver

def type_with_delay(element, text, delay=0.05):
    for char in text:
        element.send_keys(char)
        time.sleep(delay)