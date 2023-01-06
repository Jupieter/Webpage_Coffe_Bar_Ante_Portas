from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from raw_material.views import ware_choice, ware_list, ware_new
from raw_material.urls import *
from raw_material.models import WareTypes



class Test_Raw_material_Urls(TestCase):

    def setUp(self) -> None:
        self.ware_types1 = WareTypes.objects.create(
        ware_types = "Coffee",
        ware_wght = 7
        )


    def test_1_ware_choice_url_resolves(self):
        url = reverse('raw_material:ware_choice')
        self.assertEqual(resolve(url).func, ware_choice)
        self.assertEqual(resolve(url).route, "raw_material/")

    def test_2_ware_new_url_resolves(self):
        url = reverse('raw_material:ware_new')
        self.assertEqual(resolve(url).func, ware_new)
        self.assertEqual(resolve(url).route, "raw_material/new/")

    def test_3_ware_list_url_resolves(self):
        url = "/raw_material/(1)/"
        self.assertEqual(resolve(url).func, ware_list)
        self.assertEqual(resolve(url).route, "raw_material/(<int:pk>)/")

    def test_4_ware_edit_url_resolves(self):
        url = "/raw_material/(1)/(2)/edit/"
        self.assertEqual(resolve(url).func, ware_edit)
        self.assertEqual(resolve(url).route, 'raw_material/(<int:pk>)/(<int:pkey>)/edit/')

    def test_5_acquisition_new_url_resolves(self):
        url = "/raw_material/(1)/(2)/acquisition_new/"
        self.assertEqual(resolve(url).func, acquisition_new)
        self.assertEqual(resolve(url).route, 'raw_material/(<int:pk>)/(<int:pkey>)/acquisition_new/')

    def test_5_acquisition_new_url_resolves(self):
        url = "/raw_material/acquisition_list/"
        self.assertEqual(resolve(url).func, acquisition_list)
        self.assertEqual(resolve(url).route, 'raw_material/acquisition_list/')

    def test_6_acquisition_remove_url_resolves(self):
        url = "/raw_material/acquisition_list/(1)/remove/"
        self.assertEqual(resolve(url).func, acquisition_remove)
        self.assertEqual(resolve(url).route, 'raw_material/acquisition_list/(<int:pkey>)/remove/')

    def test_7_acquisition_edit_url_resolves(self):
        url = "/raw_material/acquisition_list/(1)/edit/"
        self.assertEqual(resolve(url).func, acquisition_edit)
        self.assertEqual(resolve(url).route, 'raw_material/acquisition_list/(<int:pkey>)/edit/')

    def test_8_acquisition_storing_url_resolves(self):
        url = "/raw_material/acquisition_list/(1)/storing/"
        self.assertEqual(resolve(url).func, acquisition_storing)
        self.assertEqual(resolve(url).route, 'raw_material/acquisition_list/(<int:pkey>)/storing/')

    def test_9_acquisition_box_open_url_resolves(self):
        url = "/raw_material/acquisition_list/(1)/box_open/"
        self.assertEqual(resolve(url).func, box_open)
        self.assertEqual(resolve(url).route, 'raw_material/acquisition_list/(<int:pkey>)/box_open/')

    def test_10_acquisition_box_empty_url_resolves(self):
        url = "/raw_material/acquisition_list/(1)/box_empty/"
        #   print("url: ", url)
        #   print("resolve(url)", resolve(url))
        self.assertEqual(resolve(url).func, box_empty)
        self.assertEqual(resolve(url).route, 'raw_material/acquisition_list/(<int:pkey>)/box_empty/')


class Tests_Raw_material_Views(TestCase):

    def setUp(self) -> None:
        self.client = Client()        
        # self.urls_list = ['/raw_material/', '/contact/', '/shop/', '/accounts/login/', '/api/login/']

    def  test_raw_material_page(self):
        response = self.client.get("/raw_material/")
        print("raw_material", response)
        self.assertTemplateUsed(response, "raw_material/ware_choice.html")