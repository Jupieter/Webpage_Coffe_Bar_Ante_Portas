from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
import datetime
from raw_material.models import ProductAcquisition
from .models import CoffeeMake
from .forms import CoffeeMakerForm


def coffee_home(request):
    return render(request, 'shop/coffee_home.html', {})

def coffee_make(request):
    wares1 = ProductAcquisition.objects.filter(store_status=3)
    stock_min = 40
    wares=[]
    dt= datetime.datetime.now().date()
    for ind, ware in enumerate(wares1):
        if ware.ware_type.ware_type.ware_types == 'Kávé':
            wares.append(ware)
    return render(request, 'shop/coffee_make.html', {'wares':wares,'dt':dt, 'stock_min':stock_min})


def coffee_make_form(request, pkey):
    ware = get_object_or_404(ProductAcquisition, pk=pkey)
    dose_weight = ware.ware_type.ware_type.ware_wght
    stock_min = 40
    alrt ='';    cm = None
    if  ware.stock < stock_min:
        alrt = "Nagyon kevés a kibontott anyag készlet. Kérem ellenőrizze!"
    dt= datetime.datetime.now()  
    if request.method == "POST":
        form = CoffeeMakerForm(request.POST)
        if form.is_valid():
            cm = form.cleaned_data
            dtd = cm['c_make_date'];  dtt = cm['c_make_time']
            dt_h = dtt.hour;  dt_m = dtt.minute
            dt_change = datetime.timedelta(hours=dt_h, minutes=dt_m)
            dtf = dtd + dt_change
            dt=[dtd, dtt, dtf]
            coffe_new = CoffeeMake(
                c_make_ware = ware,
                c_make_dose = cm['c_make_dose'],
                c_make_user = request.user,
                c_make_date = dtf,
                c_reg_time = timezone.now(),
                )
            coffe_new.save()
            wght = ware.stock
            ware.stock = wght - dose_weight * cm['c_make_dose']
            ware.save()
            
            field_names = [f.name for f in CoffeeMake._meta.get_fields()]

            return redirect('shop:coffee_home')
            '''return render(request, 'shop/coffee_make_form.html', 
            {'form': form, 'ware':ware,'dt':dt, 'alrt':alrt,
             'stock_min':stock_min,'dt':dt, 'cm':cm, 
             'field_names':field_names, 'coffe_new':coffe_new })
        else:
            cm = form.cleaned_data
            return render(request, 'shop/coffee_make_form.html', 
            {'form': form, 'ware':ware,'dt':dt, 'alrt':alrt, 
            'stock_min':stock_min, 'dt':dt,'cm':cm, 'coffe_new':coffe_new})'''
    else:
        form = CoffeeMakerForm()
        form.fields['c_make_date'].initial = dt
    return render(request, 'shop/coffee_make_form.html', 
    {'form': form, 'ware':ware,'dt':dt, 'alrt':alrt, 'stock_min':stock_min})


def coffee_order(request):
    dt= datetime.datetime.now()
    start = dt; end = dt + datetime.timedelta(days=1)
    coffees1 = CoffeeMake.objects.filter(c_make_date__range =(start, end))
    coffees = coffees1.order_by('c_make_date')
    

    return render(request, 'shop/coffee_order.html', {'coffees':coffees,'dt':dt, 'end':end})
