from django.contrib import admin
from .models import WareTypes, WareData, ProductIngredient, ProductAcquisition


@admin.register(WareData)
class WareDataAdmin(admin.ModelAdmin):
  list_display = ('id', 'ware_type', 'ware_brand', 'ware_brand_name', 'ware_weight', 'ware_price', 'pub_date')

admin.site.register(WareTypes)
admin.site.register(ProductIngredient)
admin.site.register(ProductAcquisition)