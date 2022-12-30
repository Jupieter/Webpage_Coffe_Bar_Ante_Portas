from unittest import skip
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep


class HomeTest(LiveServerTestCase):
    
    # @skip
    def test_1_homepage_title(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        driver.get('http://127.0.0.1:8000/')
        sleep(1)
        assert "CoffeeBar" in driver.title
    
    def test_2_homepage_title(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        driver.get('http://127.0.0.1:8000/accounts/login/')
        sleep(1)
        user_name = driver.find_element(by=By.NAME, value='email')
        user_password = driver.find_element(by=By.NAME, value='password')
        submit_button = driver.find_element(by=By.NAME, value="submit")
        user_name.send_keys('boss@staff.com')
        user_password.send_keys('Enter1')
        sleep(1)
        submit_button.click()
        # driver.maximize_window()
        assert "Welcome: BigBoss" in driver.page_source
        sleep(3)