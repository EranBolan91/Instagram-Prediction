from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.service import Service
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


if _name_ == "_main_":
    base_url = "http://instagram.com"
    explore_url = "https://www.instagram.com/explore/"

    # Defining the webdriver
    options = Options()
    options.page_load_strategy = 'eager'
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-notifications")

    chrome_options = webdriver.ChromeOptions()
    mobile_emulation = {"deviceName": "Nexus 5"}
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    #driver = webdriver.Chrome(service=Service('C:/Users/123/Desktop/HIT/Data Science Project/chromedriver.exe'), options=options)
    #driver = webdriver.Chrome(service=Service("C:\\Users\\123\\Desktop\\HIT\\Data Science Project\\chromedriver.exe"), options=options)
    driver = webdriver.Chrome('chromedriver.exe', options=options, chrome_options=chrome_options)
    wait = WebDriverWait(driver, 7)

    # Login to Instagram
    driver.get('{}/accounts/login/'.format(base_url))
    wait.until(EC.element_to_be_clickable((By.NAME, 'username'))).send_keys(USERNAME)
    driver.find_element(by=By.NAME, value='password').send_keys(PASSWORD + Keys.RETURN)
    time.sleep(3)
    driver.get(explore_url)

    # Click on the first post on the 'Explore' window
    posts = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'pKKVh')))
    for post in posts:
        post.click()
        try:
            # Get the username
            username = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/section/div[1]/div/article[1]/div/div[1]/div/header/div[2]/div[1]/div[1]/div/a'))).text
            print(username)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/nav[1]/div/header/div/div[1]/button'))).click()
            time.sleep(3)
        except:
            pass
        # while 1:
        #     pass
    #first_post = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'pKKVh')))
    #first_post.click()

    #scraping comments