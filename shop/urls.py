from django.urls import path

from shop import views

app_name = "shop"

urlpatterns = [
    path('', views.coffee_home, name='coffee_home'),
    path('make/', views.coffee_make, name='coffee_make'),
    path('make/(<int:pkey>)/remove', views.coffee_make_remove, name='coffee_make_remove'),
    path('make/(<int:pkey>)', views.coffee_make_form, name='coffee_make_form'),
    path('order/', views.coffee_order, name='coffee_order'),
    path('order/(<int:pkey>)', views.coffee_order_form, name='coffee_order_form'),
    path('order/delete/(<int:pk>)', views.coffee_order_remove, name='coffee_order_remove'),
    path('booking/', views.coffee_booking, name='coffee_booking'),
    path('booking/(<int:pkey>)', views.coffee_booking_pk, name='coffee_booking_pk'),
]
htmx_patterns = [
    path('make/(<int:pk>)/time', views.coffee_make_time, name='coffee_make_time'),
    path('order/list/', views.coffee_order_table, name='coffee_order_table'),
]

urlpatterns += htmx_patterns