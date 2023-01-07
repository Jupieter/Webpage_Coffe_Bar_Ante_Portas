from django.test import TestCase
from tests.test_model import DB_Creator



class Test_Account_0_User_View(TestCase):

    def setUp(self) -> None:
        usr = DB_Creator.user_creator(self)
        usr.save()
    
    def test_login_view_deny_anonymous(self):
        response = self.client.get('/accounts/login')
        self.assertRedirects(response, '/login/')
        response = self.client.post('/accounts', follow=True)
        self.assertRedirects(response, '/login/')

    

