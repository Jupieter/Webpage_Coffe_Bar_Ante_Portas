from django.contrib import admin
from .models import WareTypes, WareData, ProductIngredient, ProductAcquisition


@admin.register(WareTypes)
class WareTypesAdmin(admin.ModelAdmin):
  list_display = ('id', 'ware_types')

class WareDataAdmin(admin.ModelAdmin):
  list_display = ('id', 'ware_type', 'ware_brand', 'ware_brand_name', 'ware_weight', 'ware_price', 'pub_date')

admin.site.register(ProductIngredient)
admin.site.register(ProductAcquisition)