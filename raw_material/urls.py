from django.urls import path

# from . import views
from raw_material.views import *

app_name = 'raw_material'

urlpatterns = [
    path('', ware_choice, name='ware_choice'),
    path('(<int:pk>)', ware_list, name='ware_list'),
    path('new/', ware_new, name='ware_new'),
    path('(<int:pk>)/(<int:pkey>)/edit/', 
        ware_edit, name='ware_edit'),
    path('(<int:pk>)/(<int:pkey>)/remove/', 
        ware_remove, name='ware_remove'),
    path('(<int:pk>)/(<int:pkey>)/acquisition_new/', 
        acquisition_new, name='acquisition_new'),
    path('acquisition_list/', 
        acquisition_list, name='acquisition_list'),
    path('acquisition_list/(<int:pkey>)/remove/', 
        acquisition_remove, name='acquisition_remove'),
    path('acquisition_list/(<int:pkey>)/edit/', 
        acquisition_edit, name='acquisition_edit'),
    path('acquisition_list/(<int:pkey>)/storing/', 
        acquisition_storing, name='acquisition_storing'),
    path('acquisition_list/(<int:pkey>)/box_open/', 
        box_open, name='box_open'),
    path('acquisition_list/(<int:pkey>)/box_empty/', 
        box_empty, name='box_empty'),
]