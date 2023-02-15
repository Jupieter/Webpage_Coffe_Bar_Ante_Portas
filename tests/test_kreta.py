from unittest import skip

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
from tests.test_pages import SeleniumTestCase


class HomeTest(SeleniumTestCase):

    def setUp(self) -> None:
        self.wait_time = 20
        self.highlight_time = 0.2
    
    def highlight(self,element, effect_time, color, border):
        """Highlights (blinks) a Selenium Webdriver element"""
        driver = element._parent
        def apply_style(s):
            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                element, s)
        original_style = element.get_attribute('style')
        apply_style("border: {0}px solid {1};".format(border, color))
        sleep(effect_time)
        apply_style(original_style)
    
    def contains_word(s, w):
        return f' {w} ' in f' {s} '

    
    # @skip
    def homepage_title(self):
        self.driver.get(' https://pszc-angster.e-kreta.hu/')
        element = WebDriverWait(self.driver, self.wait_time).until(lambda x: x.find_element(By.ID, "dataProtection"))

    def login_staff(self):
        user_name = self.driver.find_element(by=By.NAME, value='UserName')
        user_password = self.driver.find_element(by=By.NAME, value='Password')
        submit_button = self.driver.find_element(by=By.ID, value="submit-btn")
        user_name.send_keys('')
        user_password.send_keys('')
        self.driver.set_page_load_timeout(30)
        submit_button.click()
    
    def go_to_e_naplo(self):
        self.driver.get('https://pszc-angster.e-kreta.hu/Orarend/TanariOrarend')
        self.driver.set_page_load_timeout(30)
        # element = WebDriverWait(self.driver, self.wait_time).until(lambda x: x.find_element(By.CLASS_NAME, "main-footer2"))

    def back_one(self):
        submit_button = self.driver.find_element(by=By.XPATH, value="//*[@class='fc-prev-button fc-button fc-state-default fc-corner-left']")
        # <button type="button" class="fc-today-button fc-button fc-state-default fc-corner-left fc-corner-right fc-state-disabled" disabled="disabled">ma</button>
        #<button type="button" class="fc-prev-button fc-button fc-state-default fc-corner-left"><span class="fc-icon fc-icon-left-single-arrow"></span></button>
        submit_button.click()
        self.driver.set_page_load_timeout(30)

    def book_the_lesson(self, class_button, book=False):
        self.driver.implicitly_wait(2)
        class_button.click()
        self.driver.set_page_load_timeout(30)
        cancel_btn = WebDriverWait(self.driver, self.wait_time).until(lambda x: x.find_element(By.ID, 'BtnCancel'))
        tanora_btn = WebDriverWait(self.driver, self.wait_time).until(lambda x: x.find_element(By.ID, "6"))
        self.highlight(tanora_btn, self.highlight_time, "orange", 5)
        print(tanora_btn.text)
        tanora_btn.click()
        altalanos_btn = WebDriverWait(self.driver, self.wait_time).until(lambda x: x.find_element(By.LINK_TEXT, value='ÁLTALÁNOS'))
        print(altalanos_btn.text)
        altalanos_btn.click()
        check_box = WebDriverWait(self.driver, self.wait_time).until(lambda x: x.find_element(by=By.XPATH, value = '//label[@for="IKTTanora"]'))
        print(check_box.text)
        check_box.click()
        check_box = WebDriverWait(self.driver, self.wait_time).until(lambda x: x.find_element(by=By.XPATH, value = '//label[@for="Differencialt"]'))
        print(check_box.text)
        check_box.click()
        check_box = WebDriverWait(self.driver, self.wait_time).until(lambda x: x.find_element(by=By.XPATH, value = '//label[@for="Kooperativ"]'))
        print(check_box.text)
        check_box.click()
        if book == True:
            naplozas_btn = WebDriverWait(self.driver, self.wait_time).until(lambda x: x.find_element(By.ID, 'naplozas'))
            self.highlight(naplozas_btn, self.highlight_time, "orange", 5)
            naplozas_btn.click()
        else:
            self.highlight(cancel_btn, self.highlight_time, "orange", 5)
            cancel_btn.click()
        naplozas_btn = WebDriverWait(self.driver, 5).until_not(lambda x: x.find_element(By.ID, 'naplozas'))


    def click_on_red_block(self):
        self.driver.implicitly_wait(10)
        class_buttons = None
        act_num = 0
        red_block = []
        red_block_txt = []
        print("")            
        xpath_value = "//*[@class='fc-time-grid-event fc-v-event fc-event fc-start fc-end']"
        class_buttons = WebDriverWait(self.driver, self.wait_time).until(lambda x: x.find_elements(By.XPATH, xpath_value))        
        
        print("len(class_buttons):  ", len(class_buttons))
        for class_button in class_buttons:
            cl_btn_style = class_button.get_attribute("style")
            word = 'rgb(185,'
            list_of_words = cl_btn_style.split()
            if word in list_of_words:               
                red_block.append(str(cl_btn_style))
        for block in red_block:
            print(block)
       
        for block in red_block:
            act_num += 1
            block_id = xpath_value + "[@style='" + block + "']"
            print("len(block_id):  ", len(block_id))
            # print(block_id)
            test_btn = WebDriverWait(self.driver, self.wait_time).until(lambda x: x.find_element(By.XPATH, block_id))
            test_btn_txt = test_btn.text
            print("test_btn" , act_num , ":    ", test_btn_txt)
            self.highlight(test_btn, self.highlight_time, "orange", 5)
            self.book_the_lesson(test_btn, book=True)

    def test_0_all(self):
        self.homepage_title()
        self.login_staff()
        self.go_to_e_naplo()
        # self.back_one()
        self.click_on_red_block()
        sleep(4)
