from django.urls import path

from . import views

app_name = 'raw_material'

urlpatterns = [
    path('', views.ware_choice, name='ware_choice'),
    path('(<int:pk>)', views.ware_list, name='ware_list'),
    path('new/', views.ware_new, name='ware_new'),
    path('(<int:pk>)/(<int:pkey>)/edit/', views.ware_edit, name='ware_edit'),
    path('(<int:pk>)/(<int:pkey>)/remove/', views.ware_remove, name='ware_remove'),
    path('(<int:pk>)/(<int:pkey>)/acquisition_new/', views.acquisition_new, name='acquisition_new'),
]