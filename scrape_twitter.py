from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import uuid
import random
import requests
import pymongo

client = pymongo.MongoClient(os.getenv('MONGO_URI'))
db = client[os.getenv('DB_NAME')]
collection = db[os.getenv('COLLECTION_NAME')]
print("Connected to the database")

def get_proxy_address():
    proxy_api_url = "https://proxymesh.com/api/proxies/"
    response = requests.get(proxy_api_url, auth=(os.getenv('PROXY_USERNAME'), os.getenv('PROXY_PASSWORD')))
    print(response)
    if response.status_code == 200:
        proxies = response.json().get('proxies', [])
        if proxies:
            print(proxies)
            proxy = random.choice(proxies)
            return f"http://{os.getenv('PROXY_USERNAME')}:{os.getenv('PROXY_PASSWORD')}@{proxy}", proxy.split('@')[-1].split(':')[0]
        else:
            raise Exception("No proxies available")
    else:
        raise Exception(f"Failed to get proxies: {response.status_code}")

# Initialize the Chrome WebDriver
chromeOptions = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chromeOptions)

try:
    # Set the options to run Chrome WebDriver in headless mode
    chromeOptions.add_argument("--headless")

    # Set the options to run Chrome WebDriver in background mode
    chromeOptions.add_argument("--disable-gpu")
    chromeOptions.add_argument("--no-sandbox")

    # Set the options to run Chrome WebDriver without opening a window
    chromeOptions.add_argument("--window-size=1920x1080")

    proxy_address, proxy_ip = get_proxy_address()

    # chromeOptions.add_argument('--proxy-server=%s' % proxy_address)
    
    driver = webdriver.Chrome(options=chromeOptions)
    
    print(f"Using proxy: {proxy_address}")
    
    driver.get("https://x.com/login")

    username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@type="text"]')))
    username_input.send_keys(os.getenv('USERID'))
    print("username entered")
    next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Next')]")))
    next_button.click()
    password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))
    password_input.send_keys(os.getenv('PASSWORD'))
    print("password entered")
    login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"Log in")]')))
    login_button.click()
    print("login button clicked")


    # Wait for the homepage to load
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Timeline: Trending now']")))
    print("Logged in Successfully")
    trends = driver.find_elements(By.XPATH, "//div[@aria-label='Timeline: Trending now']//span")

    trending_topics = ["none","none","none","none","none"]
    index=0
    for trend in trends[2:]:
        if(trend.text not in trending_topics and len(trend.text) > 0 and 'posts' not in trend.text and 'Trending' not in trend.text):
            trending_topics[index] = trend.text
            index+=1
            if index >= len(trending_topics):
                break
    # Create a unique ID
    unique_id = uuid.uuid4().hex

    # Output data
    data = {
        "_id": unique_id,
        "trend1": trending_topics[0],
        "trend2": trending_topics[1],
        "trend3": trending_topics[2],
        "trend4": trending_topics[3],
        "trend5": trending_topics[4],
        "date_time": datetime.now(),
        "ip_address": proxy_ip

        # "ip_address": driver.execute_script("return document.ip_address")
    }
    collection.insert_one(data)
    print("Data inserted")
except Exception as e:
    print("ERROR : ",e)

finally:
    driver.quit()
