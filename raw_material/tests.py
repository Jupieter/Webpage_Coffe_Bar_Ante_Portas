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


    def test_ware_choice_url_resolves(self):
        url = reverse('raw_material:ware_choice')
        # print("resolve(url)", resolve(url))
        self.assertEqual(resolve(url).func, ware_choice)
        self.assertEqual(resolve(url).route, "raw_material/")

    def test_ware_new_url_resolves(self):
        # url = reverse('raw_material:ware_new')
        url = "/raw_material/new/"
        print("test_ware_new_url_resolve:   ", url)
        self.assertEqual(resolve(url).func, ware_new)
        self.assertEqual(resolve(url).route, "raw_material/new/")


    def test_ware_list_url_resolves(self):
        # url = reverse('raw_material:ware_list')
        url = "/raw_material/1/"
        print("url", url)
        print("resolve(url)", resolve(url))
        # self.assertEqual(resolve(url).func, ware_list)
        # self.assertEqual(resolve(url).route, "raw_material/ware_list/1")



class Tests_Raw_material_Views(TestCase):

    def setUp(self) -> None:
        self.client = Client()        
        # self.urls_list = ['/raw_material/', '/contact/', '/shop/', '/accounts/login/', '/api/login/']

    def  test_raw_material_page(self):
        response = self.client.get("/raw_material/")
        print("raw_material", response)
        self.assertTemplateUsed(response, "raw_material/ware_choice.html")