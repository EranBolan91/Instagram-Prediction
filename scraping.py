from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from functions import Functions
from selenium import webdriver
from dotenv import load_dotenv
import time
import csv
import os
load_dotenv()

os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
USERNAME = os.getenv('USERNAMEWORK')


if __name__ == "__main__":
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
    #driver = webdriver.Chrome(service=Service('C:/Users/123/Desktop/HIT/Data Science Project/chromedriver.exe'), options=options)
    #driver = webdriver.Chrome(service=Service("C:\\Users\\123\\Desktop\\HIT\\Data Science Project\\chromedriver.exe"), options=options)
    driver = webdriver.Chrome('chromedriver.exe', options=options, chrome_options=chrome_options)
    wait = WebDriverWait(driver, 7)

    # Login to Instagram
    driver.get('{}/accounts/login/'.format(base_url))
    wait.until(EC.element_to_be_clickable((By.NAME, 'username'))).send_keys(USERNAME)
    driver.find_element(by=By.NAME, value='password').send_keys(PASSWORD + Keys.RETURN)
    time.sleep(5)
    driver.get(explore_url)

    # Click on the first post on the 'Explore' window
    first_post = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'pKKVh')))
    first_post.click()

    # Open csv file
    file = open('eran_data.csv', 'w', newline="")
    header = ['id', 'like', 'following', 'followers', 'post', 'celeb', 'sex', 'pic_vid', 'pCo', 'hashtag', 'content', 'predict']
    writer = csv.writer(file, delimiter='\t')
    writer.writerow(header)
    row = list()
    while 1:
        # Get the username
        username = Functions().get_username(wait)
        print(username)
        row.append(username)

        # Get post likes
        post_likes = Functions().get_post_likes(wait)
        print(post_likes)
        row.append(post_likes)

        # Get post text
        post_text = Functions().get_post_text(wait)
        print(post_text)
        row.append(post_text)

        # Checking if the post is video
        is_video = Functions().check_if_video(wait)
        print(is_video)
        row.append(is_video)

        # Get image URL
        img = Functions().get_img_url(wait)
        print(img)
        row.append(img)

        # Open new tab and nav to the username
        Functions().nav_user_new_tab(driver, username, wait, base_url)

        # Get user data
        posts, following, followers = Functions().get_posts_following_followers_amount(wait)
        row.append(posts)
        row.append(following)
        row.append(followers)
        # Close the tab and nav back
        Functions().close_new_tab(driver)

        # Write to CSV
        writer.writerow(row)
        row.clear()
        # Click on the next post (Arrow right)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[name()="svg" and @aria-label="Next"]'))).click()
        time.sleep(3)
