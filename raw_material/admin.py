from django.contrib import admin
from .models import WareTypes, WareData, ProductIngredient

admin.site.register(WareTypes)
admin.site.register(WareData)
admin.site.register(ProductIngredient)