from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from raw_material.views import ware_choice, ware_list, ware_new
from raw_material.urls import *


class Test_Raw_material_Urls(SimpleTestCase):

    def test_ware_choice_url_resolves(self):
        url = reverse('raw_material:ware_choice')
        # print("resolve(url)", resolve(url))
        self.assertEqual(resolve(url).func, ware_choice)
        self.assertEqual(resolve(url).route, "raw_material/")

    def test_ware_new_url_resolves(self):
        url = reverse('raw_material:ware_new')
        print("resolve(url)", resolve(url))
        self.assertEqual(resolve(url).func, ware_new)
        self.assertEqual(resolve(url).route, "raw_material/new/")

    def test_ware_new_url_resolves(self):
        url = reverse('raw_material:ware_new')
        print("resolve(url)", resolve(url))
        self.assertEqual(resolve(url).func, ware_new)
        self.assertEqual(resolve(url).route, "raw_material/new/")


class Tests_Raw_material_Views(TestCase):

    def setUp(self) -> None:
        self.client = Client()        
        # self.urls_list = ['/raw_material/', '/contact/', '/shop/', '/accounts/login/', '/api/login/']

    def  test_raw_material_page(self):
        response = self.client.get("/raw_material/")
        print("raw_material", response)
        self.assertTemplateUsed(response, "raw_material/ware_choice.html")