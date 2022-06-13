from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path('', views.coffee_home, name='coffee_home'),
    path('make/', views.coffee_make, name='coffee_make'),
    path('make/(<int:pkey>)', views.coffee_make_form, name='coffee_make_form'),
    path('order/', views.coffee_order, name='coffee_order'),
    path('order/(<int:pkey>)', views.coffee_order_form, name='coffee_order_form'),
    path('order/delete/(<int:pk>)', views.coffee_order_remove, name='coffee_order_remove'),
    path('booking/', views.coffee_booking, name='coffee_booking'),
]