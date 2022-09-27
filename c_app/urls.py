from django.urls import path
# from rest_framework.authtoken import views as authtoken_views
from . import views
from .views import LoginAPI, RegisterAPI
from knox import views as knox_views

app_name = 'c_app'

urlpatterns = [
    # path('api-token-auth/', authtoken_views.obtain_auth_token),
    path('coffee_notify/', views.coffee_notify, name='coffee_notify'),
    path('coffe_friends/', views.coffe_friends, name='coffe_friends'),
    path('act_ware/', views.active_coffe_ware, name='active_coffe_ware'),
    path('todaytcoffee/', views.todaytcoffee, name='todaytcoffee'),
    path('coffe_make/', views.coffe_make, name='coffe_make'),
    path('read_tasks/', views.all_tasks, name='all_tasks'),
    path('create_task/', views.create_task, name='create_task'),
    path('logins/', views.logins, name='logins'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='knox_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_login'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_login'),
]