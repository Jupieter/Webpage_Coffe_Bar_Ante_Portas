from unittest import skip

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
from tests.test_pages import SeleniumTestCase


class HomeTest(SeleniumTestCase):
    
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

    
    # @skip
    def homepage_title(self):
        self.driver.get(' https://pszc-angster.e-kreta.hu/')

    def login_staff(self):
        user_name = self.driver.find_element(by=By.NAME, value='UserName')
        user_password = self.driver.find_element(by=By.NAME, value='Password')
        submit_button = self.driver.find_element(by=By.ID, value="submit-btn")
        user_name.send_keys('Jung Péter')
        user_password.send_keys('azazazaz')
        sleep(0.2)
        submit_button.click()
    
    def go_to_e_naplo(self):
        self.driver.get('https://pszc-angster.e-kreta.hu/Orarend/TanariOrarend')
        element = WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.CLASS_NAME, "main-footer2"))

    def click_on_red_block(self):
        class_buttons = None
        try:                
            # class_buttons = self.driver.find_elements(by=By.XPATH, value="//a[@style='border-color: rgb(185, 85, 85); color: rgb(0, 0, 0); background: rgb(185, 85, 85); ']")  #inset: 573.5px 0% -648.667px; z-index: 1;
            class_buttons = self.driver.find_elements(by=By.XPATH, value="//*[@class='fc-time-grid-event fc-v-event fc-event fc-start fc-end fc-hover']")
            # print(class_buttons)
            for class_button in class_buttons:
                red = None
                cl_btn_style = class_button.get_attribute("style")
                red = cl_btn_style.find("rgb(185, 85, 85)")
                if red != None:
                    sign = "True"
                else:
                    sign = "False"

                print(sign, " : ",  class_button.text, " : ", cl_btn_style)
                self.highlight(class_button, 0.5, "orange", 5)

                # class_button.click()
                # self.driver.implicitly_wait(10)
                # sleep(1)
                # # naplozas_btn = self.driver.find_element(By.ID, 'naplozas')
                # cancel_btn = self.driver.find_element(By.ID, 'BtnCancel')
                # self.highlight(cancel_btn, 2, "orange", 5)
                # sleep(0.5)
                # cancel_btn.click()
                # sleep(2)
        except:
            print("I didn't find opened lessons.")

# <a class="fc-time-grid-event fc-v-event fc-event fc-start fc-end fc-hover" style="border-color: rgb(150, 150, 150); color: rgb(150, 150, 150); background: transparent; border-style: dashed; inset: 0px 0% -74.6667px; z-index: 1;"><div class="fc-content"><div class="fc-time" data-start="0:00" data-full="0:00 - 0:00"></div><div class="fc-orasorszam">0</div></div><div class="fc-bg"></div></a>
        
    
    def test_0_all(self):
        self.homepage_title()
        self.login_staff()
        self.go_to_e_naplo()
        self.click_on_red_block()
        sleep(4)

# <a class="fc-time-grid-event fc-v-event fc-event fc-start fc-end k-state-border-down" style="border-color: rgb(185, 85, 85); color: rgb(0, 0, 0); background: rgb(185, 85, 85); inset: 573.5px 0% -648.667px; z-index: 1;" data-role="tooltip"><div class="fc-content"><div class="fc-time" data-start="0:07" data-full="0:07 - 0:07"></div><div class="fc-title">gép.alism - 1/9-3<br>213<br>Jung Péter</div></div><div class="fc-bg"></div></a>