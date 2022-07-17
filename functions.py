from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import re
import os


class Functions:
    # getting the username of the post
    def get_username(self, wait):
        username = None
        try:
            username = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                              '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[1]/div/div/span/a'))).text
        except:
            print('Error - username - 1')

        try:
            username = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                              '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div/div/span[1]/a'))).text
        except:
            print('Error - username - 2')

        try:
            username = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div/div/span[1]/a'))).text
        except:
            print('Error - username - 3')
        return username

    # getting the post likes
    def get_post_likes(self, wait):
        post_likes = None
        # Looking for 'likes' with the format of "likes", for example "767 likes" or anything with the word "likes"
        try:
            post_likes = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/div/a/div/span'))).text
        except:
            pass
            #print('Error! - post likes 2')

        # Looking for 'likes' with the format of "others", for example "767 others" or anything with the word "others"
        try:
            post_likes = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div[2]/div/a/div/span'))).text
        except:
            pass
            #print('Error! - post likes 2.1')

        # Looking for 'likes' with the format of "likes", on videos posts
        try:
            post_likes = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/div/a/div/span'))).text
        except:
            pass
            #print('Error! - post likes 2.2')

        # This XPATH is for 'views'
        try:
            post_likes = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[2]/div/span/div/span'))).text
        except:
            pass
            #print('Error! - post views 3')
        return post_likes

    # getting the content of the post
    def get_post_text(self, wait):
        post_text = ""
        try:
            post_text = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/span'))).text
        except:
            print('Error! - post text')

        return post_text

    def clean_post_text(self, post_text):
        if post_text:
            hashtag_pattern = "#\w+"  # pattern for hashtags
            label_tiugim = "@\w+"  # pattern for labels (Tiyugim)

            # Getting all hashtags from text
            hashtags_list = re.findall(hashtag_pattern, post_text)
            for hashtag in hashtags_list:
                # Removing \n from hashtags
                post_text = post_text.replace('\n', '')

                post_text = post_text.replace(hashtag, '')

            labels = re.findall(label_tiugim, post_text)
            for label in labels:
                # Removing \n from labels
                post_text = post_text.replace('\n', '')
                # Replacing label with empty string
                post_text = post_text.replace(label, '')

            # Removing all special characters from text
            clean_post_text = re.sub("\W+", ' ', post_text)
            return clean_post_text
        else:
            return ' '

    # getting the img url (for computer vision)
    def get_img_url(self, wait):
        img_url = None
        try:
            img_url = wait.until(EC.visibility_of_element_located(
                (By.TAG_NAME, "img"))).get_attribute("src")
        except:
            pass
            # print('Error! - No Image')
        try:
            img_url = wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "img"))).get_attribute("src")[0]
        except:
            pass
            # print('Error! - No Image')
        return img_url

    # checking if the post is a picture or video
    # IF its video - it will return True
    # IF not - it will return False
    def check_if_video(self, wait):
        is_video = False
        try:
            is_video = wait.until(EC.element_to_be_clickable(
                (By.TAG_NAME, 'video'))).is_displayed()
        except:
            pass
            # print('Error! - is video ')
        return is_video

    # going to the user profile tab to get more information
    def nav_user_new_tab(self, driver, username, base_url):
        driver.execute_script(
            "window.open('{}');".format(base_url + '/' + username))
        driver.switch_to.window(driver.window_handles[1])

    # open new tab of the post
    def nav_post_new_tab(self, driver, post_id, base_url):
        driver.execute_script(
            "window.open('{}');".format(base_url + '/p/' + post_id))
        driver.switch_to.window(driver.window_handles[1])

    # closing the tab opened to returning to continue the code
    def close_new_tab(self, driver):
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    # getting user data : posts, following and followers
    def get_posts_following_followers_amount(self, wait):
        posts_amount = None
        following_amount = None
        followers_amount = None
        try:
            user_data = wait.until(EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, "._ac2a")))
            posts_amount = user_data[0].text
            followers_amount = user_data[1].text
            following_amount = user_data[2].text
        except:
            print('Error! - posts following followers amount ')
        return posts_amount, following_amount, followers_amount

    # Need to ask Oren, how is it return 0 or 1
    def verified_badge(self, wait):
        # initialization
        is_verified = 0
        try:
            # getting the verified badge
            is_verified = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@title, 'Verified')]")))
            if is_verified:
                is_verified = 1
        except:
            return is_verified
        return is_verified

    # getting only the hashtags from the post text (content)
    # If 'post_text' is empty string, then it will return empty string (it happenes when post does not have any hashtags)
    def post_hashtags(self, post_text):
        # initial list variable
        hashtags_string = ""
        if post_text:
            # splitting the text into words
            for word in post_text.split():
                # checking the first character of every word
                if word[0] == '#':
                    # adding the word to the list
                    hashtags_string += word[1:] + " "
            return hashtags_string
        else:
            return " "

    # seperating the number from the string
    def get_number_post_likes(self, post_likes):
        if post_likes:
            # splitting the number from the word "likes"
            numOfLikes = re.split(r'\s', post_likes)
            # removing "," from the number with empty character
            numOfLikes = re.sub(r",", "", numOfLikes[0])
            # checking that we got number and not string incase of single like
            if numOfLikes.isnumeric():
                return numOfLikes
        return None

    # Get number as a String, if the number is between 0 - 999, this func should return the number it self
    # IF the number is with K or M. Then this func calc the right number
    # IT also knows how to handle with this kind of numbers "1,445 , 22,455 , 111,059"
    def clean_number(self, number):
        # Checking if number is not None
        if number:
            number = number.lower()
            # check if the number is thousands example: 1,454 , 2,888 , 9,999
            thousands = number.find(',')
            # check if the number is more then ten thousands example: 10k , 20.8k , 90.9k
            ten_thousands = number.find('k')
            # check if the number is millions example: 10.1m , 20m , 90.9m
            millions = number.find('m')
            if thousands != -1:
                clean_num = int(number.replace(',', ''))
                return clean_num
            elif ten_thousands != -1:
                if number.find('.') != -1:
                    num_no_dot = number.replace('.', '')
                    clean_num = int(num_no_dot.replace('k', ''))
                    return clean_num * 100
                else:
                    clean_num = int(number.replace('k', ''))
                    return clean_num * 1000
            elif millions != -1:
                if number.find('.') != -1:
                    num_no_dot = number.replace('.', '')
                    clean_num = int(num_no_dot.replace('m', ''))
                    return clean_num * 100000
                else:
                    clean_num = int(number.replace('m', ''))
                    return clean_num * 100000
            else:
                return int(number)
            # if we got 0 like so nothing to clean and return none
        else:
            return None

    # getting post date publishment
    def get_time(self, wait):
        # initialize
        post_time = None
        try:
            # searching for "time" tag
            post_time = wait.until(
                EC.element_to_be_clickable((By.TAG_NAME, 'time'))).text
        except:
            print('Error! - No time')
        return post_time

    # This func count how many hashtag the post has. It returns a number between 0 to infinity
    def count_hashtags(self, post_text):
        pattern = "#\w+"
        if post_text:
            # if there are no hashtags, it will return 0 (empty list has 0 objects)
            return len(re.findall(pattern, post_text))
        else:
            return 0

    # seperating the url and getting the last part of it - the ID of the post
    def get_post_id(self, driver):
        url = driver.current_url
        post_id = url.split('/')[-2]
        return post_id

    # This func calc if the post has more then 30% likes....
    # Returns 1 if the post has more then 30% likes , and 0 if not
    def calc_prediction(self, likes_amount, followers_amount):
        if likes_amount and followers_amount:
            calc = int(likes_amount) / int(followers_amount)
            if calc > 0.3:
                return 1
            else:
                return 0
        else:
            # Return 'None' only when the 'likes_amount' or 'followers_amount' are None
            return None

    def get_tags_from_image(self, cv_client, image):
        tags_string = ""
        if image:
            res = cv_client.tag_image(image)
            if len(res.tags) == 0:
                return None
            else:
                for tag in res.tags:
                    if tag.confidence * 100 > 90:
                        tags_string += tag.name + " "
                return tags_string
        else:
            return None

    # Write to csv
    def write_to_csv(self, post_obj, headers):
        df = pd.DataFrame([post_obj])
        # If file is not exists, then create it and write the headers for the columns
        if not os.path.isfile('data.csv'):
            df.to_csv('data.csv', header=headers, index=False)
        else:  # else it exists so append without writing the header
            df.to_csv('data.csv', mode='a', header=False, index=False)

    # 0 - Blocked
    # 1 - Not blocked
    def check_if_blocked(self, wait):
        try:
            error_text = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Sorry, this page isn't available.')]")))
            para_text = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'The link you followed may be broken, or the page may have been removed. ')]")))
            #error_text = self.driver.find_element_by_xpath('/html/body/div/div[1]/div/div/h2').text
            #para_text = self.driver.find_element_by_xpath('/html/body/div/div[1]/div/div/p').text
            if error_text == "Sorry, this page isn't available.":
                return 0
            if error_text and para_text:
                print(error_text)
                print(para_text)
                return 0
        except Exception as e:
            return 1