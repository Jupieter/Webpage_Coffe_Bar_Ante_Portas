from django.contrib import admin
from .models import CoffeeMake, CoffeeOrder

# Register your models here.
@admin.register(CoffeeMake)
class CoffeeMakeAdmin(admin.ModelAdmin):
  list_display = ('id', 'c_make_ware', 'c_make_dose', 'c_make_date')

# admin.site.register(CoffeeMake)
admin.site.register(CoffeeOrder)