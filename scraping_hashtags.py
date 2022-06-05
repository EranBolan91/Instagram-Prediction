from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from selenium.webdriver.support import expected_conditions as EC
from msrest.authentication import CognitiveServicesCredentials
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from functions import Functions
from selenium import webdriver
from dotenv import load_dotenv
from datetime import datetime
import time
import os
load_dotenv()

os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
USERNAME = os.getenv('USERNAMEWORK')
API_KEY = os.getenv('COMPUTER_VISION_KEY')
ENDPOINT = os.getenv('COMPUTER_VISION_END_POINT')


if __name__ == "__main__":
    base_url = "http://instagram.com"
    hashtag_url = "https://www.instagram.com/explore/tags/"
    hashtag_list = ['sport', 'tlv', 'food', 'gym', 'train', 'money', 'dog', 'nature', 'cars', 'pool', 'swim', 'cat',
                    'baby', 'running', 'tree', 'sea', 'nails', 'bikini', 'woman', 'man', 'fitguys', 'swimwear',
                    'fitness', 'model', 'view', 'beach', 'football', 'happy', 'kids', 'sweet', 'party', 'alcohol',
                    'fitnessmodel', 'motivation', 'sunday', 'style', 'fashion', 'power']
    cv_client = ComputerVisionClient(
    ENDPOINT, CognitiveServicesCredentials(API_KEY))

    # Defining the webdriver
    options = Options()
    options.page_load_strategy = 'eager'
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-notifications")

    chrome_options = webdriver.ChromeOptions()
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

    # Open csv file
    headers = ['id', 'likes', 'following', 'followers', 'posts_amount', 'celeb', 'pic_vid', 'hashtag', 'hashtag_amount','pCo', 'content', 'post_date', 'curr_date','predict']
    post_num = 1
    post_obj = {'id': "", 'likes': "", 'following': "", 'followers': "", 'posts_amount': "", 'celeb': "",
                'pic_vid': "", 'hashtag': "", 'hashtag_amount': "", 'pCo': "", 'content': "", 'post_date': "",
                'curr_date': "", 'predict': ""}

    for hashtag in hashtag_list:
        # Nav to hashtag page
        driver.get(hashtag_url + '{}'.format(hashtag))

        # Click on the first post on the 'Explore' window
        first_post = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, '_aagw')))
        first_post.click()

        for x in range(9):
            try:
                print("@@@@@@@@@@ Post number: {} @@@@@@@@@@@".format(str(post_num)))
                # Get the username
                username = Functions().get_username(wait)
                print("Username: " + str(username))

                # Get post id
                post_id = Functions().get_post_id(driver)
                post_obj['id'] = post_id
                print("Post id: " + str(post_id))

                # Get post likes
                post_likes = Functions().get_post_likes(wait)
                # This func remove 'likes' String
                postLikesNum = Functions().get_number_post_likes(post_likes)
                clean_post_likes = Functions().clean_number(postLikesNum)
                post_obj['likes'] = clean_post_likes
                print("Post Likes: " + str(clean_post_likes))

                # Get post text - If there is no text in the post, func will return empty string
                post_text = Functions().get_post_text(wait)
                # Cleaning post text from all hashtags label and special characters
                clean_post = Functions().clean_post_text(post_text)
                post_obj['content'] = clean_post
                print("Post Text: " + str(clean_post))

                # Count how many hashtags exists - Func return a number.
                # IF there are no hashtags it will return 0
                hashtag_amount = Functions().count_hashtags(post_text)
                print("Hashtags amount: " + str(hashtag_amount))
                post_obj['hashtag_amount'] = hashtag_amount

                # get post hashtags
                hashtags = Functions().post_hashtags(post_text)
                print("Hashtags string: " + str(hashtags))
                post_obj['hashtag'] = hashtags

                # Checking if the post is video. Video - 1 , Picture - 0
                is_video = Functions().check_if_video(wait)
                if is_video:
                    post_obj['pic_vid'] = 1
                else:
                    post_obj['pic_vid'] = 0
                print("Is Video: " + str(is_video))

                # Open new tab to current post
                Functions().nav_post_new_tab(driver, post_id, base_url)

                # Get image URL
                img = Functions().get_img_url(wait)
                print("Image URL: " + str(img))

                # This func return a one string of tags, separate by space.
                # If the picture has no tags, it will return None or if image link is not found
                pCo = Functions().get_tags_from_image(cv_client, img)
                post_obj['pCo'] = pCo
                print("pCo: " + str(pCo))

                Functions().close_new_tab(driver)

                # Get post date
                post_date = Functions().get_time(wait)
                print("Post Date: " + str(post_date))
                post_obj['post_date'] = post_date

                # Open new tab and nav to the username
                Functions().nav_user_new_tab(driver, username, base_url)

                # Get user data
                posts, following, followers = Functions().get_posts_following_followers_amount(wait)
                clean_posts = Functions().clean_number(posts)
                clean_followers = Functions().clean_number(followers)
                clean_following = Functions().clean_number(following)
                print("Posts: " + str(clean_posts))
                print("followers_amount: " + str(clean_followers))
                print("following_amount: " + str(clean_following))
                post_obj['posts_amount'] = clean_posts
                post_obj['followers'] = clean_followers
                post_obj['following'] = clean_following

                # get True for Verified badge or 0 for none
                is_verified = Functions().verified_badge(wait)
                print("Is Verified: " + str(is_verified))
                post_obj['celeb'] = is_verified

                # Close the tab and nav back
                Functions().close_new_tab(driver)

                # Get current date
                curr_date = datetime.today().strftime('%d-%m-%Y')
                post_obj['curr_date'] = curr_date
                print("Current Date: " + str(curr_date))

                # Func that gets the post likes and followers and calc if the post has more then 30%
                # IF `posts_likes` or `clean_followers` is None, then func will return None
                prediction = Functions().calc_prediction(clean_post_likes, clean_followers)
                print("Prediction: " + str(prediction))
                post_obj['predict'] = prediction

                # Write to CSV
                print(post_obj)
                Functions().write_to_csv(post_obj, headers)

                # Click on the next post (Arrow right)
                wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[name()="svg" and @aria-label="Next"]'))).click()
                time.sleep(20)
                post_num += 1
            except:
                pass