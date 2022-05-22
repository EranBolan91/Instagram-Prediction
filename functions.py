from curses.ascii import isdigit
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
        post_likes = 0
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
        return post_likes

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
                (By.XPATH, '/html/body/div[6]/div[3]/div/article/div/div[1]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/img'))).get_attribute("srcset")
        except:
            print('Error! - image url 1')

        try:
            img_url = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//div[@class="KL4Bh"]/img'))).get_attribute("srcset")
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
            user_data = wait.until(EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, ".g47SY ")))
            posts_amount = user_data[0].text
            followers_amount = user_data[1].text
            following_amount = user_data[2].text
            print("Posts: " + posts_amount)
            print("followers_amount: " + followers_amount)
            print("following_amount: " + following_amount)
        except:
            print('Error! - posts following followers amount ')
        return posts_amount, following_amount, followers_amount

    def verified_badge(self, wait):
        is_verified = 0
        try:
            is_verified = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                 '/html/body/div/section/main/div/header/section/div/div/span'))).text
        except:
            print('Error! - No badge ')
        return is_verified

    def get_number_post_likes(self, post_likes):
        # numOfLikes = re.findall('\d+,\d+', post_likes)
        numOfLikes = re.split(r'\s', post_likes)
        numOfLikes = re.sub(r",", "", numOfLikes[0])
        if numOfLikes.isnumeric():
            return numOfLikes
        return None

    def clean_number(self, number):
        try:
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
        except:
            return None

    def get_time(self, wait):
        post_time = 0
        try:
            post_time = wait.until(EC.element_to_be_clickable(
                (By.TAG_NAME, 'time'))).text
        except:
            print('Error! - No time')
        return post_time
