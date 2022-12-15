from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from mysite.views import home_page, proba, contact_page


class TestMainUrls(SimpleTestCase):
    print("TestMainUrls")

    def test_home_url_resolves(self):
        url = reverse('home_url')
        self.assertEqual(resolve(url).func, home_page)

    def test_proba_url_resolves(self):
        url = reverse('proba')
        self.assertEqual(resolve(url).func, proba)
        
    def test_contact_url_resolves(self):
        url = reverse('contact_page')
        self.assertEqual(resolve(url).func, contact_page)

class TestsMainViews(TestCase):
    print("TestsMainViews")

    def setUp(self) -> None:
        self.client = Client()        
        self.urls_list = ['/raw_material/', '/contact/', '/shop/', '/accounts/login/']
    
    def test_urls_loop(self):
        for urls in self.urls_list:
            response = self.client.get(urls)
            if response.status_code != 200:
                print("problem with urls: ", urls)
            self.assertEqual(response.status_code, 200)
        
    def test_url_admin(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)

