from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from dotenv import load_dotenv
import time
import os
load_dotenv()

os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
USERNAME = os.getenv('USERNAMEWORK')


if __name__ == "__main__":
    base_url = "http://instagram.com"
    explore_url = "https://www.instagram.com/explore/"

    # Defining the webdriver
    driver = webdriver.Firefox()
    options = Options()
    webdriver.firefox.profile = "iphone"
    options.page_load_strategy = 'eager'
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-notifications")

    # Login to Instagram
    driver.get('{}/accounts/login/'.format(base_url))
    WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.NAME, 'username'))).send_keys(USERNAME)
    driver.find_element(by=By.NAME, value='password').send_keys(PASSWORD + Keys.RETURN)
    time.sleep(3)
    driver.get(explore_url)
