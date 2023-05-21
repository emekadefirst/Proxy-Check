import csv
import time
import threading
import queue
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

# Open the existing CSV file in read mode and read the data (if any)
existing_data = []
with open("rawproxies.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        existing_data.append(row)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = "https://free-proxy-list.net/#"
driver.get(url)
driver.maximize_window()
driver.execute_script(
    "window.scrollTo(0, document.documentElement.scrollHeight);")
time.sleep(2)

modal = driver.find_element(
    By.XPATH, '/html/body/section[1]/div/div[1]/ul/li[5]/a')
modal.send_keys(Keys.RETURN)
time.sleep(10)
print("ok")
p_list = driver.find_element(
    By.XPATH, '/html/body/div[1]/div/div/div[2]/textarea')
p_list.send_keys(Keys.PAGE_DOWN)
new_data = p_list.text.split("\n")

# Append the new data to the existing data list
existing_data.extend([row.split(",") for row in new_data])

# Write the updated data list to the CSV file, overwriting the previous content
with open("rawproxies.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for row in existing_data:
        writer.writerow(row)

print("CSV file updated successfully.")

# IDAN

q = queue.Queue()
lock = threading.Lock()

with open("rawproxies.csv", "r") as f:
    proxies = f.read().split("\n")
    for p in proxies:
        q.put(p)


def check_proxies():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get("http://ipinfo.io/json",
                               proxies={"http": proxy,
                                        "https": proxy})
        except:
            continue
        if res.status_code == 200:
            print(proxy)
            with lock:
                with open('validproxies.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([proxy])


for _ in range(10):
    threading.Thread(target=check_proxies).start()

print("Completed")
