from unittest import skip
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from accounts.models import User
from raw_material.models import WareTypes, WareData, ProductAcquisition
from time import sleep


class HomeTest(LiveServerTestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1920 ,1080)
        user_c = User.objects.all()
        print("")
        print("User", user_c)
    
    # @skip
    def homepage_title(self):
        self.driver.get('http://127.0.0.1:8000/')
        sleep(1)
        assert "CoffeeBar" in self.driver.title

    def homepage_to_contact(self):
        contact_button = self.driver.find_element(by=By.LINK_TEXT, value='Contact')
        contact_button.click()
        sleep(1)
        assert "Contact Page" in self.driver.page_source

    def back_to_homepage(self):
        contact_button = self.driver.find_element(by=By.XPATH, value='//a[@href="/"]')
        contact_button.click()
        sleep(1)
        assert " staff login:    boss@staff.com" in self.driver.page_source

    # @skip
    def login_staff(self):
        login_button = self.driver.find_element(by=By.LINK_TEXT, value='Login')
        login_button.click()
        assert "Login" in self.driver.title
        sleep(1)
        user_name = self.driver.find_element(by=By.NAME, value='email')
        user_password = self.driver.find_element(by=By.NAME, value='password')
        submit_button = self.driver.find_element(by=By.NAME, value="submit")
        user_name.send_keys('boss@staff.com')
        user_password.send_keys('Enter1')
        sleep(1)
        submit_button.click()
        assert "Welcome: BigBoss" in self.driver.page_source
        sleep(1)
    
    def raw_material_menu_button(self):
        rw_button = self.driver.find_element(by=By.LINK_TEXT, value='Raw materials')
        rw_button.click()
        sleep(1)
        procurement_button = self.driver.find_element(by=By.LINK_TEXT, value='Procurement of goods')
        procurement_button.click()
        sleep(1)
        # print(self.driver.title)
        assert "ware choice" in self.driver.title
        sleep(1)
    
    def click_four_ware_type(self):
        href_list = [
            ['//a[@href="/raw_material/(1)"]', "Coffee list"],
            ['//a[@href="/raw_material/(2)"]', "Sugar list"],
            ['//a[@href="/raw_material/(3)"]', "Milk list"],
            ['//a[@href="/raw_material/(4)"]',"Flavour list"],
            ]
        for href_act in href_list:
            variable_button = self.driver.find_element(by=By.XPATH, value = href_act[0])
            variable_button.click()
            assert href_act[1] in self.driver.page_source
            sleep(1)
            WebDriverWait(self.driver, timeout=10).until(lambda d: d.find_element(by=By.ID, value='END of table'))
            back_button = self.driver.find_element(by=By.ID, value='back_link')
            back_button.click()
            sleep(1)

    def add_new_ware(self):
        coffee_button = self.driver.find_element(by=By.XPATH, value = '//a[@href="/raw_material/(1)"]')
        coffee_button.click()
        new_button = self.driver.find_element(by=By.XPATH, value = '//a[@href="/raw_material/new/"]')
        new_button.click()
        select_element = self.driver.find_element(By.ID, 'id_ware_type')
        select = Select(select_element)
        select.select_by_visible_text('Coffee')
        self.driver.find_element(by=By.NAME, value='ware_brand').send_keys('Test_Brand_Coffee')
        self.driver.find_element(by=By.NAME, value='ware_brand_name').send_keys('Test_Name_Coffee')
        sleep(1)
        self.driver.find_element(by=By.NAME, value='ware_weight').send_keys(25)
        self.driver.find_element(by=By.NAME, value='ware_price').send_keys(599)
        sleep(1)
        submit_button = self.driver.find_element(by=By.ID, value='submit')
        
        sleep(2)
        submit_button.click()
        wd_1 = WareData.objects.all()
        print("Ware Data",wd_1)
        # self.assertEqual(wd_1.ware_brand, "Brand_1")
        # self.assertEqual(wd_1.ware_brand_name, "Brand_Name_1")
        # self.assertEqual(wd_1.ware_weight, 99)
        # self.assertEqual(wd_1.ware_price, 9)
        sleep(1)


    def test_0_all(self):
        self.homepage_title()
        self.homepage_to_contact()
        self.back_to_homepage()
        self.login_staff()
        self.raw_material_menu_button()
        wd_0 = WareTypes.objects.all()
        print("Ware Type", wd_0)
        self.click_four_ware_type()
        self.add_new_ware()


        sleep(3)
        self.driver.quit()
