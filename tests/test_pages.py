from unittest import skip
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from datetime import timezone, datetime
from raw_material.models import WareTypes, WareData, ProductAcquisition
from accounts.models import User
from shop.models import CoffeeMake, CoffeeOrder
from tests.test_model import DB_Creator
from time import sleep


class SeleniumTestCase(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--start-maximized")
        # service = Service(f"{settings.BASE_DIR}/chromedriver")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.set_window_size(1920 ,1080)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


class HomeTest(SeleniumTestCase):

    def setUp(self):
        DB_Creator.full_DB_begin(self)
    
    def highlight(self, element, effect_time, color, border):
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
        # self.driver.get('http://127.0.0.1:8000/')
        self.driver.get(self.live_server_url)
        sleep(0.1)
        assert "CoffeeBar" in self.driver.title

    def homepage_to_contact(self):
        contact_button = self.driver.find_element(by=By.LINK_TEXT, value='Contact')
        contact_button.click()
        sleep(0.1)
        assert "Contact Page" in self.driver.page_source
        assert " staff login:    boss@staff.com" in self.driver.page_source

    def back_to_homepage(self):
        contact_button = self.driver.find_element(by=By.XPATH, value='//a[@href="/"]')
        self.highlight(contact_button, 0.5, "orange", 5)
        contact_button.click()

    def login_staff(self):
        login_button = self.driver.find_element(by=By.LINK_TEXT, value='Login')
        login_button.click()
        assert "Login" in self.driver.title
        user_name = self.driver.find_element(by=By.NAME, value='email')
        user_password = self.driver.find_element(by=By.NAME, value='password')
        submit_button = self.driver.find_element(by=By.NAME, value="submit")
        # user_name.send_keys('boss@staff.com')
        # user_password.send_keys('Enter1')
        user_name.send_keys('staff@admin.com')
        user_password.send_keys('XYZ999')
        self.highlight(submit_button, 1, "orange", 5)
        submit_button.click()
        assert "Welcome: STAFF" in self.driver.page_source
    
        
    def raw_material_menu_button(self):
        rw_button = self.driver.find_element(by=By.LINK_TEXT, value='Raw materials')
        self.highlight(rw_button, 0.5, "orange", 5)
        rw_button.click()
        sleep(0.1)
        procurement_button = self.driver.find_element(by=By.LINK_TEXT, value='Procurement of goods')
        self.highlight(procurement_button, 0.5, "orange", 5)
        procurement_button.click()
        # print(self.driver.title)
        assert "ware choice" in self.driver.title
    
    def click_four_ware_type(self):
        href_list = [
            ['//a[@href="/raw_material/(1)/"]', "Coffee list"],
            ['//a[@href="/raw_material/(2)/"]', "Sugar list"],
            ['//a[@href="/raw_material/(3)/"]', "Milk list"],
            ['//a[@href="/raw_material/(4)/"]',"Flavour list"],
            ]
        for href_act in href_list:
            # print(href_act[0])
            variable_button = self.driver.find_element(by=By.XPATH, value = href_act[0])
            variable_button.click()
            assert href_act[1] in self.driver.page_source
            sleep(0.1)
            WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value='END of table'))
            back_button = self.driver.find_element(by=By.ID, value='back_link')
            back_button.click()
            sleep(0.1)

    def add_new_ware(self):
        url = str(self.live_server_url) + "/raw_material/(1)/"
        self.driver.get(url)
        # coffee_button = self.driver.find_element(by=By.XPATH, value = '//a[@href="/raw_material/(1)/"]')
        # coffee_button.click()
        new_button = self.driver.find_element(by=By.XPATH, value = '//a[@href="/raw_material/new/"]')
        new_button.click()
        select_element = self.driver.find_element(By.ID, 'id_ware_type')
        select = Select(select_element)
        select.select_by_visible_text('Coffee')
        self.driver.find_element(by=By.NAME, value='ware_brand').send_keys('Test_Brand_Coffee')
        self.driver.find_element(by=By.NAME, value='ware_brand_name').send_keys('Test_Name_Coffee')
        sleep(0.3)
        self.driver.find_element(by=By.NAME, value='ware_weight').send_keys(25)
        self.driver.find_element(by=By.NAME, value='ware_price').send_keys(59)
        submit_button = self.driver.find_element(by=By.ID, value='submit')
        self.highlight(submit_button, 0.5, "orange", 5)
        submit_button.click()
        wd_1 = WareData.objects.get(id=5)
        self.assertEqual(wd_1.ware_brand, "Test_Brand_Coffee")
        self.assertEqual(wd_1.ware_brand_name, "Test_Name_Coffee")
        self.assertEqual(wd_1.ware_weight, 250)
        self.assertEqual(wd_1.ware_price,  590)
        self.assertEqual(WareData.objects.count(), 5)
    
    def edit_new_ware(self):
        url = str(self.live_server_url) + "/raw_material/(1)/"
        self.driver.get(url)
        edit_button = self.driver.find_element(by=By.XPATH, value = '//a[@href="/raw_material/(1)/(5)/edit/"]')
        self.highlight(edit_button, 0.5, "orange", 5)
        edit_button.click()
        brand_input = self.driver.find_element(by=By.NAME, value='ware_brand')
        brand_input.clear()
        brand_input.send_keys('Test_Brand_Rewrited')
        self.highlight(brand_input, 0.5, "orange", 5)
        submit_button = self.driver.find_element(by=By.ID, value='submit')
        self.highlight(submit_button, 0.5, "orange", 5)
        submit_button.click()
        wd_1 = WareData.objects.get(id=5)
        self.assertEqual(wd_1.ware_brand, "Test_Brand_Rewrited")
        sleep(1)
    
    def delete_new_ware(self):
        url = str(self.live_server_url) + "/raw_material/(1)/"
        self.driver.get(url)
        edit_button = self.driver.find_element(by=By.XPATH, value = '//a[@href="/raw_material/(1)/(5)/remove/"]')
        self.highlight(edit_button, 0.5, "orange", 5)
        edit_button.click()
        self.assertEqual(WareData.objects.count(), 4)
        sleep(1)

    def acquisition_new_ware(self):
        url = str(self.live_server_url) + "/raw_material/(1)/"
        self.driver.get(url)
        edit_button = self.driver.find_element(by=By.XPATH, value = '//a[@href="/raw_material/(1)/(1)/acquisition_new/"]')
        self.highlight(edit_button, 0.5, "orange", 5)
        edit_button.click()
        price_input = self.driver.find_element(by=By.NAME, value='acquisition_price')
        price_input.clear()
        price_input.send_keys(987)
        submit_button = self.driver.find_element(by=By.ID, value='submit')
        self.highlight(submit_button, 1.5, "orange", 5)
        submit_button.click()
        self.assertEqual(ProductAcquisition.objects.count(), 5)
        sleep(1)

    def test_0_all(self):
        self.homepage_title()
        self.homepage_to_contact()
        self.back_to_homepage()
        self.login_staff()
        self.raw_material_menu_button()
        self.click_four_ware_type()
        self.add_new_ware()
        self.edit_new_ware()
        self.delete_new_ware()
        self.acquisition_new_ware()

        sleep(3)
        # self.driver.quit()
