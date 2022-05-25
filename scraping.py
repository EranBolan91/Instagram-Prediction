# from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
# from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from selenium.webdriver.support import expected_conditions as EC
# from msrest.authentication import CognitiveServicesCredentials
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
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
API_KEY = os.getenv('COMPUTER_VISION_KEY')
ENDPOINT = os.getenv('COMPUTER_VISION_END_POINT')


if __name__ == "__main__":
    base_url = "http://instagram.com"
    explore_url = "https://www.instagram.com/explore/"
    # cv_client = ComputerVisionClient(
    # ENDPOINT, CognitiveServicesCredentials(API_KEY))

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
    driver = webdriver.Chrome(
        'chromedriver.exe', options=options, chrome_options=chrome_options)
    wait = WebDriverWait(driver, 7)

    # Login to Instagram
    driver.get('{}/accounts/login/'.format(base_url))
    wait.until(EC.element_to_be_clickable(
        (By.NAME, 'username'))).send_keys(USERNAME)
    driver.find_element(by=By.NAME, value='password').send_keys(
        PASSWORD + Keys.RETURN)
    time.sleep(5)
    driver.get(explore_url)
    # driver.get(test_url)

    # Click on the first post on the 'Explore' window
    first_post = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'pKKVh')))
    first_post.click()

    # Open csv file
    # file = open('eran_data.csv', 'a+', newline="")
    # header = ['id', 'like', 'following', 'followers', 'post', 'celeb', 'sex', 'pic_vid', 'pCo', 'hashtag', 'content', 'predict']
    # writer = csv.writer(file, delimiter='\t')
    # writer.writerow(header)
    post_num = 1
    # Open csv file
    with open('eran_data.csv', 'a+', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file, delimiter='\t', lineterminator='\n')
        row = []
        data_dict = {}
        while 1:
            print("@@@@@@@@@@ Post number: {} @@@@@@@@@@@".format(str(post_num)))
            # Get the username
            username = Functions().get_username(wait)
            print("Username: " + username)
            row.append(username)

            # Get post likes
            post_likes = Functions().get_post_likes(wait)
            # This func remove 'likes' String
            postLikesNum = Functions().get_number_post_likes(post_likes)
            clean_post_likes = Functions().clean_number(postLikesNum)
            print("Post Likes: " + str(clean_post_likes))
            row.append(clean_post_likes)

            # Get post text
            post_text = Functions().get_post_text(wait)
            print("Post Text: " + str(post_text))
            row.append(post_text)

            # Checking if the post is video
            is_video = Functions().check_if_video(wait)
            print("Is Video: " + str(is_video))
            row.append(is_video)

            # get post hashtags
            hashtags = Functions().post_hashtags(post_text)
            print("\nThe hashtags in \"" + post_text + "\" are :")
            for hashtag in hashtags:
                print(hashtag)

            # Get image URL
            img = Functions().get_img_url(wait)
            print("Image URL: " + str(img))
            #res = cv_client.describe_image(img, 3)
            # print(res)
            row.append(img)

            # Get post date
            post_date = Functions().get_time(wait)
            print("Post Date: " + str(post_date))
            row.append(post_date)
            # Open new tab and nav to the username
            Functions().nav_user_new_tab(driver, username, wait, base_url)
            # Get user data
            posts, following, followers = Functions().get_posts_following_followers_amount(wait)
            print("Posts: " + str(Functions().clean_number(posts)))
            print("followers_amount: " + str(Functions().clean_number(followers)))
            print("following_amount: " + str(Functions().clean_number(following)))
            row.append(Functions().clean_number(posts))
            row.append(Functions().clean_number(following))
            row.append(Functions().clean_number(followers))
            # get True for Verified badge or 0 for none
            is_verified = Functions().verified_badge(wait)
            print("Is Verified: " + str(is_verified))
            # Close the tab and nav back
            Functions().close_new_tab(driver)
            # Write to CSV
            print(row)
            csv_writer.writerow(row)
            row.clear()
            # Click on the next post (Arrow right)
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[name()="svg" and @aria-label="Next"]'))).click()
            time.sleep(3)
            post_num += 1
