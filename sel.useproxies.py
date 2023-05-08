import csv
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pytube import YouTube
import os
import requests

# Load proxies from a CSV file
with open("proxy_list.csv", "r") as f:
    proxies = f.read().split("\n")

# Remove empty lines and whitespace from the proxies list
proxies = [p.strip() for p in proxies if p.strip()]

# Initialize proxy counter
proxy_counter = 0

# Set up Chrome driver
options = Options()
options.headless = True
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

# Define function to get a proxy from the list
def get_proxy():
    global proxy_counter
    proxy = proxies[proxy_counter]
    proxy_counter = (proxy_counter + 1) % len(proxies)  # Rotate proxy
    return proxy

# Define function to make a request through a proxy
def make_request(url):
    proxy = get_proxy()
    print(f"Using proxy: {proxy}")
    try:
        res = requests.get(url, proxies={"http": proxy, "https": proxy})
        res.raise_for_status()  # Raise an error if the response is not OK
        return res.text
    except Exception as e:
        print(f"Request failed with proxy {proxy}: {e}")
        # Retry with a different proxy
        if proxy_counter < len(proxies) - 1:
            return make_request(url)
        else:
            print("All proxies failed")
            return None

# Start scraping process
url = input("Enter the URL to scrape: ")
html = make_request(url)

if html:
    # Process the HTML content using BeautifulSoup or other libraries
    # ...
    # End of scraping process
    print(html)
    driver.quit()
"http://ipinfo.io/json"