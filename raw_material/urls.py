from django.urls import path

from . import views

app_name = 'raw_material'

urlpatterns = [
    path('', views.ware_list, name='ware_list'),
    path('new/', views.ware_new, name='ware_new'),
    path('(<int:pk>)/edit/', views.ware_edit, name='ware_edit'),
    path('(<int:pk>)/remove/', views.ware_remove, name='ware_remove'),
]