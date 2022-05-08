from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path('', views.shop_page, name='shop_page'),

]