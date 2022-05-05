from django.urls import path

from . import views

urlpatterns = [
    path('', views.ware_list, name='ware_list'),
    path('new/', views.ware_new, name='ware_new'),
    
]