from django.shortcuts import render
from django.utils import timezone
from .models import WareData, ProductIngredient

def ware_list(request):
    milks = WareData.objects.filter(ware_type='milks').order_by('ware_brand')
    coffees = WareData.objects.filter(ware_type='coffe').order_by('ware_brand')
    return render(request, 'raw_material/ware_list.html', {'milks': milks, 'coffees':coffees})

