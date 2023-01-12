from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from raw_material.views import ware_choice, ware_list, ware_new
from raw_material.urls import *
from raw_material.models import WareTypes, WareData, ProductAcquisition
from raw_material.forms import WareDataForm, WareListChoice, AquisitionForm, AquisitionStockedForm
from accounts.models import User
from shop.models import CoffeeMake, CoffeeOrder
from tests.test_model import DB_Creator



class Test_Raw_material_Urls(TestCase):

    def setUp(self) -> None:
        self.ware_types1 = WareTypes.objects.create(
        ware_types = "Coffee",
        ware_wght = 7
        )


    def test_01_ware_choice_url_resolves(self):
        url = reverse('raw_material:ware_choice')
        self.assertEqual(resolve(url).func, ware_choice)
        self.assertEqual(resolve(url).route, "raw_material/")

    def test_02_ware_new_url_resolves(self):
        url = reverse('raw_material:ware_new')
        self.assertEqual(resolve(url).func, ware_new)
        self.assertEqual(resolve(url).route, "raw_material/new/")

    def test_03_ware_list_url_resolves(self):
        url = "/raw_material/(1)/"
        self.assertEqual(resolve(url).func, ware_list)
        self.assertEqual(resolve(url).route, "raw_material/(<int:pk>)/")

    def test_04_ware_edit_url_resolves(self):
        url = "/raw_material/(1)/(2)/edit/"
        self.assertEqual(resolve(url).func, ware_edit)
        self.assertEqual(resolve(url).route, 'raw_material/(<int:pk>)/(<int:pkey>)/edit/')

    def test_05_acquisition_new_url_resolves(self):
        url = "/raw_material/(1)/(2)/acquisition_new/"
        self.assertEqual(resolve(url).func, acquisition_new)
        self.assertEqual(resolve(url).route, 'raw_material/(<int:pk>)/(<int:pkey>)/acquisition_new/')

    def test_06_acquisition_new_url_resolves(self):
        url = "/raw_material/acquisition_list/"
        self.assertEqual(resolve(url).func, acquisition_list)
        self.assertEqual(resolve(url).route, 'raw_material/acquisition_list/')

    def test_07_acquisition_remove_url_resolves(self):
        url = "/raw_material/acquisition_list/(1)/remove/"
        self.assertEqual(resolve(url).func, acquisition_remove)
        self.assertEqual(resolve(url).route, 'raw_material/acquisition_list/(<int:pkey>)/remove/')

    def test_08_acquisition_edit_url_resolves(self):
        url = "/raw_material/acquisition_list/(1)/edit/"
        self.assertEqual(resolve(url).func, acquisition_edit)
        self.assertEqual(resolve(url).route, 'raw_material/acquisition_list/(<int:pkey>)/edit/')

    def test_09_acquisition_storing_url_resolves(self):
        url = "/raw_material/acquisition_list/(1)/storing/"
        self.assertEqual(resolve(url).func, acquisition_storing)
        self.assertEqual(resolve(url).route, 'raw_material/acquisition_list/(<int:pkey>)/storing/')

    def test_10_acquisition_box_open_url_resolves(self):
        url = "/raw_material/acquisition_list/(1)/box_open/"
        self.assertEqual(resolve(url).func, box_open)
        self.assertEqual(resolve(url).route, 'raw_material/acquisition_list/(<int:pkey>)/box_open/')

    def test_11_acquisition_box_empty_url_resolves(self):
        url = "/raw_material/acquisition_list/(1)/box_empty/"
        #   print("url: ", url)
        #   print("resolve(url)", resolve(url))
        self.assertEqual(resolve(url).func, box_empty)
        self.assertEqual(resolve(url).route, 'raw_material/acquisition_list/(<int:pkey>)/box_empty/')


class Tests_Raw_material_Views(TestCase):

    def setUp(self) -> None:
        DB_Creator.full_DB_begin(self)
        self.client = Client()        
        self.urls_200_list = [
            ['', "ware_choice.html"], 
            ['new/', "ware_edit.html"], 
            ['(1)/',  "ware_list.html"],
            ['(1)/(2)/edit/', "ware_edit.html"], 
            ['(1)/(2)/acquisition_new/', "acquisition_new.html"],
            ['acquisition_list/', "acquisition_list.html"],
            ['acquisition_list/(1)/edit/', "acquisition_new.html"],
            ]
        self.urls_302_list = [
            ['acquisition_list/(1)/storing/', "acquisition_list.html"],
            ['acquisition_list/(1)/box_open/', "acquisition_list.html"],
            ['acquisition_list/(1)/box_empty/', "acquisition_list.html"],
            ['acquisition_list/(1)/remove/', "acquisition_list.html"],
            ]

    def  test_12_raw_material_200_response(self):
        # print("********************")
        for url in self.urls_200_list:
            long_url = "/raw_material/" + url[0]
            test_url = "raw_material/" +  url[1]
            #   print("raw_material:    ",long_url, "    ", test_url)
            response = self.client.get(long_url)
            #   print(response)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, test_url)

    def  test_13_raw_material_302_response(self):
        # print("********************")
        for url in self.urls_302_list:
            long_url = "/raw_material/" + url[0]
            test_url = "raw_material/" +  url[1]
            # print("raw_material:    ",long_url, "    ", test_url)
            response = self.client.get(long_url)
            #   print(response)
            self.assertEqual(response.status_code, 302)
    
    def  test_14_raw_material_ware_edit_form(self):
        w_type = WareTypes.objects.get(id=1)
        data = {'ware_type' : w_type,
        'ware_brand' : "TestBrand", 
        'ware_brand_name': "TestBandName",
        'ware_weight' : 10,
        'ware_price': 20, 
        }
        form = WareDataForm(data=data)
        # ware = get_object_or_404(WareData, pk=1) 
        # print(ware)
        # form = WareDataForm(instance=ware) 
        self.assertTrue(form.is_valid())
        # self.assertEqual(WareTypes.objects.count(), 4)
        # wd = WareData.objects.all()
        # print("WareData", wd)