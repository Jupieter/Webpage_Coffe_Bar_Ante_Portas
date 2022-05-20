from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path('', views.coffee_home, name='coffee_home'),
    path('make/', views.coffee_make, name='coffee_make'),
]