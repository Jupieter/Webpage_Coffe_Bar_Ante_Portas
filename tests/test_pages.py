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
        # options = webdriver.ChromeOptions()
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # self.driver = webdriver.Chrome(options=options)
        # self.driver.set_window_size(1920 ,1080)

        # Staff User create
        user_saff = User.objects.create_staff_user(
        email = "staff@admin.com",
        username = "STAFF",
        password = "XYZ999",
        first_name = "Stefi", 
        last_name = "Stafi"
        )
        user_saff.save()
        # User create

        user_list = [
        ["test@acquisition.com", "Acquisitor", "ABC001", "Ac", "Qu"],
        ["test@store.com", "Storer", "ABC002", "St0", "Re"],
        ["test@open.com", "Opener", "ABC003", "Op", "En"],
        ["test@make.com", "Maker", "ABC004", "Ma", "Ker"],
        ["test@drink.com", "Drinker", "ABC005", "Dr", "Ink"],
        ]

        for i in range(5): 
            u_ser = DB_Creator.user_creator(self, user_list[i][0], user_list[i][1], user_list[i][2], user_list[i][3])
            u_ser.save()

        # WareTypes load with Data
        ware_type_list = [ ["Coffee", 7, "coffee_bag.jpg"], ["Sugar", 50, "sugar.jpg"], ["Milk", 50, "milk.jpg"], ["Flavour", 50, "dijo.jpg"] ]
        for ware_type_data in ware_type_list: 
            wt_types = ware_type_data[0]
            wt_wght = ware_type_data[1]
            wt = DB_Creator.ware_type_creator(wt_types, wt_wght)
            wt.ware_image = ware_type_data[2]
            wt.save()
        # WareData load with Data
        ware_data_list = [
            ["Brand_Coffee", "Brand_Name_Coffee", 250, 900,],
            ["Brand_Sugar", "Brand_Name_Sugar", 100, 700,],
            ["Brand_Milk", "Brand_Name_Milk", 500, 800,],
            ["Brand_Flavour", "Brand_Name_Flavour", 450, 600,]
            ]
        for i in range(4): 
            wt = WareTypes.objects.get(id=i+1)
            wd = DB_Creator.ware_data_creator(wt, ware_data_list[i][0], ware_data_list[i][1], ware_data_list[i][2], ware_data_list[i][3])
            wd.save()
        # ProductAcquisition load with Data
        price_list = [699, 399, 299, 599]
        for i in range(4): 
            ware_pa = WareData.objects.get(id=i+1)
            u_ser = User.objects.get(id=1)
            pa = DB_Creator.ware_product_creator(ware_pa, price_list[i], u_ser)
            pa.store_user = User.objects.get(id=2)
            pa.open_user = User.objects.get(id=3)
            pa.save()
        
        cm = CoffeeMake.objects.create(
            c_make_ware = ProductAcquisition.objects.get(id=1),
            c_make_dose = 4,
            c_make_user = User.objects.get(id=4),
            c_make_date = datetime(2022, 2, 22, 6, 6, 6, 0)
        )
        cm.save()

        co = CoffeeOrder.objects.create(
            coffee_selected = cm,
            coffee_dose = 0.5,
            sugar_choice = ProductAcquisition.objects.get(id=2),
            sugar_dose = 1.0,
            milk_choice = ProductAcquisition.objects.get(id=3),
            milk_dose = 2.0,
            flavour_choice = ProductAcquisition.objects.get(id=4),
            flavour_dose = 1.5,
            coffe_user = User.objects.get(id=5),
        )
        co.save()

        user_c = User.objects.all()
        print("")
        print("User:  ", user_c)
    
    # @skip
    def homepage_title(self):
        # self.driver.get('http://127.0.0.1:8000/')
        # self.driver.get('http://127.0.0.1:64432/')
        self.driver.get(self.live_server_url)
        sleep(0.1)
        assert "CoffeeBar" in self.driver.title

    def homepage_to_contact(self):
        contact_button = self.driver.find_element(by=By.LINK_TEXT, value='Contact')
        contact_button.click()
        sleep(0.1)
        assert "Contact Page" in self.driver.page_source
        assert " staff login:    boss@staff.com" in self.driver.page_source

    # @skip
    def login_staff(self):
        login_button = self.driver.find_element(by=By.LINK_TEXT, value='Login')
        login_button.click()
        assert "Login" in self.driver.title
        sleep(0.1)
        user_name = self.driver.find_element(by=By.NAME, value='email')
        user_password = self.driver.find_element(by=By.NAME, value='password')
        submit_button = self.driver.find_element(by=By.NAME, value="submit")
        # user_name.send_keys('boss@staff.com')
        # user_password.send_keys('Enter1')
        user_name.send_keys('staff@admin.com')
        user_password.send_keys('XYZ999')
        sleep(2)
        submit_button.click()
        assert "Welcome: STAFF" in self.driver.page_source
        sleep(2)
    
    def back_to_homepage(self):
        contact_button = self.driver.find_element(by=By.XPATH, value='//a[@href="/"]')
        contact_button.click()
        sleep(0.1)
        # assert " staff login:    staff@admin.com" in self.driver.page_source
        
    def raw_material_menu_button(self):
        rw_button = self.driver.find_element(by=By.LINK_TEXT, value='Raw materials')
        rw_button.click()
        sleep(1)
        procurement_button = self.driver.find_element(by=By.LINK_TEXT, value='Procurement of goods')
        procurement_button.click()
        sleep(0.1)
        # print(self.driver.title)
        assert "ware choice" in self.driver.title
        sleep(0.1)
    
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
        sleep(0.5)
        self.driver.find_element(by=By.NAME, value='ware_weight').send_keys(25)
        self.driver.find_element(by=By.NAME, value='ware_price').send_keys(59)
        sleep(1)
        submit_button = self.driver.find_element(by=By.ID, value='submit')
        
        sleep(2)
        submit_button.click()
        wd_1 = WareData.objects.get(id=5)
        print("Ware Data",wd_1)
        self.assertEqual(wd_1.ware_brand, "Test_Brand_Coffee")
        self.assertEqual(wd_1.ware_brand_name, "Test_Name_Coffee")
        self.assertEqual(wd_1.ware_weight, 250)
        self.assertEqual(wd_1.ware_price,  590)
        sleep(1)


    def test_0_all(self):
        self.homepage_title()
        # self.homepage_to_contact()
        # self.back_to_homepage()
        self.login_staff()
        self.raw_material_menu_button()
        wd_0 = WareTypes.objects.all()
        print("Ware Type", wd_0)
        self.click_four_ware_type()
        self.add_new_ware()

        sleep(3)
        self.driver.quit()
