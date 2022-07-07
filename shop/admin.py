from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(CoffeeMake)
class CoffeeMakeAdmin(admin.ModelAdmin):
  list_display = ('id', 'c_make_ware', 'c_make_dose', 'c_make_date', 'c_book')

@admin.register(CoffeeOrder)
class CoffeeOrderAdmin(admin.ModelAdmin):
  list_display = ('id', 'coffee_selected', 'coffe_user', 'coffee_reg')

