from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
import datetime
from raw_material.models import WareData, ProductAcquisition
from .forms import CoffeeMaker


def coffee_home(request):
    return render(request, 'shop/coffee_home.html', {})

def coffee_make(request):
    wares = ProductAcquisition.objects.filter(store_status=3)
    choice = []
    for ind, ware in enumerate(wares):
        ware_name = str(ware.ware_type.ware_brand)+' ' + str(ware.ware_type.ware_brand_name)+' ' + str(ware.ware_type.ware_weight) +'g (' +str(ware.ware_type.ware_type) +')'
        
        # choice[ind] = (ware,ware_name)
    
    if request.method == "POST":
        form = CoffeeMaker(request.POST)
        if form.is_valid():
            cm = form.cleaned_data
            form.save()
            return redirect('shop:coffee_home')
    else:
        form = CoffeeMaker(initial={'c_make_ware':choice})
    return render(request, 'shop/coffee_make.html',
        {'form': form, 'wares':wares, 'ind':ind, 'ware_name':ware_name})

