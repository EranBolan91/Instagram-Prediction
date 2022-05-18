from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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
        try:
            post_likes = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/div/a/div'))).text
        except:
            print('Error! - post likes 1')

        try:
            post_likes = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div[2]/div/a/div/span'))).text
        except:
            print('Error! - post likes 2')

        return post_likes


    def get_post_text(self, wait):
        post_text = -1
        try:
            post_text = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/span'))).text
        except:
            print('Error! - post text ')
        return post_text
