from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from mysite.views import home_page, proba, contact_page, view_modal_mess
from django.http import HttpRequest

class Test_Main_Urls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home_url')
        self.assertEqual(resolve(url).func, home_page)

    def test_proba_url_resolves(self):
        url = reverse('proba')
        self.assertEqual(resolve(url).func, proba)
        
    def test_contact_url_resolves(self):
        url = reverse('contact_page')
        self.assertEqual(resolve(url).func, contact_page)

    def test_contact_url_proba(self):
        url = reverse('proba')
        self.assertEqual(resolve(url).func, proba)

class Tests_Main_Views(TestCase):

    def setUp(self) -> None:
        self.client = Client()        
        self.urls_list = ['/raw_material/', '/contact/', '/shop/', '/accounts/login/', '/api/login/', '/proba/']

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "Next Coffee:")

    
    def  test_raw_material_page(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)

    def test_urls_loop(self):
        for urls in self.urls_list:
            response = self.client.get(urls)
            if response.status_code != 200:
                print("problem with urls: ", urls)
            self.assertEqual(response.status_code, 200)

    def test_htmx_modal(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['headx'] = 'Test_HEAD'
        request.POST['txtx'] = 'Test_Text'
        request.POST['background'] = 'red'
        response = view_modal_mess(request)                         
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Close')
        headx = "test_H"
        txtx = "Test_T"
        backg = "yellow"
        stylex = 'style=background:' + str(backg) 
        from django.shortcuts import render
        respo_2 = render(request, "modal_mess.html", {'headx':headx, 'txtx':txtx, 'stylex':stylex})
        self.assertEqual(respo_2.status_code, 200)
        self.assertContains(respo_2, 'Test_T')

        
 

