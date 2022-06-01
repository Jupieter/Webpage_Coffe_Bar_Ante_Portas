from django.contrib import admin
from .models import CoffeeMake, CoffeeOrder

# Register your models here.
admin.site.register(CoffeeMake)
admin.site.register(CoffeeOrder)