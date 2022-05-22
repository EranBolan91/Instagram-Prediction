from posixpath import split
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re


class Functions:

    def get_username(self, wait):
        username = -1
        try:
            username = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                              '/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[1]/div/span/a'))).text
        except:
            print('Error - username!')
        return username

    def get_post_likes(self, wait):
        post_likes = -1
        # Looking for 'likes' with the format of "likes", for example "767 likes" or anything with the word "likes"
        try:
            post_likes = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/div/a/div'))).text
        except:
            print('Error! - post likes 1')

        try:
            post_likes = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div[2]/div/a/div/span'))).text
        except:
            print('Error! - post likes 2')

        # Looking for 'likes' with the format of "others", for example "767 others" or anything with the word "others"
        try:
            post_likes = wait.until(EC.element_to_be_clickable(
                (By.CLASS_NAME, '_7UhW9   xLCgt        qyrsm KV-D4               fDxYl    T0kll '))).text
        except:
            print('Error! - post likes 3')

        if post_likes:
            return post_likes
        return '0'

    def get_post_text(self, wait):
        post_text = -1
        try:
            post_text = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/span'))).text
        except:
            print('Error! - post text ')
        return post_text

    def get_img_url(self, wait):
        img_url = -1
        try:
            img_url = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[6]/div[3]/div/article/div/div[1]/div/div/div[1]/img'))).get_attribute("srcset")
            img_url = img_url.split(" ")[0]
        except:
            print('Error! - image url 1')

        try:
            img_url = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//div[@class="KL4Bh"]/img'))).get_attribute("srcset")
            img_url = img_url.split(" ")[0]
        except:
            print('Error! - image url 2')
        return img_url

    def check_if_video(self, wait):
        is_video = False
        try:
            is_video = wait.until(EC.element_to_be_clickable(
                (By.TAG_NAME, 'video'))).is_displayed()
        except:
            print('Error! - is video ')
        return is_video

    def nav_user_new_tab(self, driver, username, wait, base_url):
        driver.execute_script(
            "window.open('{}');".format(base_url + '/' + username))
        driver.switch_to.window(driver.window_handles[1])

    def close_new_tab(self, driver):
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    def get_posts_following_followers_amount(self, wait):
        posts_amount = -1
        following_amount = -1
        followers_amount = -1
        try:
            user_data = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".g47SY ")))
            posts_amount = user_data[0].text
            followers_amount = user_data[1].text
            following_amount = user_data[2].text
            print("Posts: " + posts_amount)
            print("followers_amount: " + followers_amount)
            print("following_amount: " + following_amount)
        except:
            print('Error! - posts following followers amount ')
        return posts_amount, following_amount, followers_amount

    def clean_number(self, number):
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

    def verified_badge(self, wait):
        is_verified = False
        try:
            is_verified = wait.until(EC.element_to_be_clickable(
                (By.CLASS_NAME, 'mTLOB Szr5J coreSpriteVerifiedBadge '))).is_displayed()
        except:
            print('Error! - No badge ')
        return is_verified

    def get_number_post_likes(self, post_likes):
        numOfLikes = None
        if post_likes:
            numOfLikes = post_likes.split(' ')
        if type(numOfLikes[0]) == str:
            return numOfLikes[0]
        return numOfLikes