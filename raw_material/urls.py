from django.urls import path

from . import views

app_name = 'raw_material'

urlpatterns = [
    path('', views.ware_choice, name='ware_choice'),
    path('(<int:pk>)', views.ware_list, name='ware_list'),
    path('new/', views.ware_new, name='ware_new'),
    path('(<int:pk>)/(<int:pkey>)/edit/', 
        views.ware_edit, name='ware_edit'),
    path('(<int:pk>)/(<int:pkey>)/remove/', 
        views.ware_remove, name='ware_remove'),
    path('(<int:pk>)/(<int:pkey>)/acquisition_new/', 
        views.acquisition_new, name='acquisition_new'),
    path('acquisition_list/', 
        views.acquisition_list, name='acquisition_list'),
    path('acquisition_list/(<int:pkey>)/remove/', 
        views.acquisition_remove, name='acquisition_remove'),
    path('acquisition_list/(<int:pkey>)/edit/', 
        views.acquisition_edit, name='acquisition_edit'),
    path('acquisition_list/(<int:pkey>)/storing/', 
        views.acquisition_storing, name='acquisition_storing'),
    path('acquisition_list/(<int:pkey>)/box_open/', 
        views.box_open, name='box_open'),
    path('acquisition_list/(<int:pkey>)/box_empty/', 
        views.box_empty, name='box_empty'),
]