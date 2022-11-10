from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from raw_material.views import ware_choice, ware_list
from raw_material.urls import *

class TestUrls(SimpleTestCase):

    def test_ware_choice_url_resolves(self):
        url = "még semmi"
        # url = reverse('ware_choice')
        print(url)
        # print(resolve(url))
        # self.assertEqual(resolve(url).func, ware_list)