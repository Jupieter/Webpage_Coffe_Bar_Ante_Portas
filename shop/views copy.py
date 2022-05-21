from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
import datetime
from raw_material.models import WareData, ProductAcquisition
from .forms import CoffeeMaker


def coffee_home(request):
    return render(request, 'shop/coffee_home.html', {})

def coffee_make(request):
    wares1 = ProductAcquisition.objects.filter(store_status=3)
    wares=[]
    choice = []
    ware_name = ''
    dt= datetime.datetime.now().date()
    for ind, ware in enumerate(wares1):
        if ware.ware_type.ware_type.ware_types == 'Kávé':
            ware_name = str(ware.ware_type.ware_brand)+' ' + str(ware.ware_type.ware_brand_name)+' ' + str(ware.ware_type.ware_weight) +'g (' +str(ware.id) +')'
            block = (ware, ware_name)
            choice.append(block)
            wares.append(ware)
    
    if request.method == "POST":
        form = CoffeeMaker(request.POST)
        if form.is_valid():
            cm = form.cleaned_data
            
            form.save()
            return redirect('shop:coffee_home')
    else:
        form = CoffeeMaker()
        form.fields['c_make_ware'].choices = choice
        form.fields['c_make_date'].initial = dt
    return render(request, 'shop/coffee_make.html', {'form': form, 'wares':wares,'dt':dt})

