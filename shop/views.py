import json
import datetime
# from asyncio.windows_events import NULL
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from raw_material.models import ProductAcquisition, WareTypes
from .models import CoffeeMake, CoffeeOrder
from .forms import CoffeeMakerForm, CoffeeOrderForm, CoffeeTimeForm


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

def coffee_make_remove(request, pkey):
    coffee4 = get_object_or_404(CoffeeMake, pk=pkey)
    coffee4.delete()
    return redirect('shop:coffee_order')
    # context = {'adat':coffee4}
    # return render(request, 'shop/c_error.html', context)

def date_time_add(cm):
        ''' Date picker and Tim picker values add to dateTime'''
        dtd = cm['c_make_date'];  dtt = cm['c_make_time']
        dt_h = dtt.hour;  dt_m = dtt.minute
        dt_change = datetime.timedelta(hours=dt_h, minutes=dt_m)
        dtf = dtd + dt_change
        return dtf


def coffee_make_form(request, pkey):
    ware = get_object_or_404(ProductAcquisition, pk=pkey)
    dose_weight = ware.ware_type.ware_type.ware_wght
    stock_min = 40
    alrt ='';    cm = None
    if  ware.stock < dose_weight*0.08:
        alrt = "Nagyon kevés a kibontott anyag készlet. Kérem ellenőrizze!"
    dt= datetime.datetime.now()  
    if request.method == "POST":
        form = CoffeeMakerForm(request.POST)
        if form.is_valid():
            cm = form.cleaned_data
            dtf = date_time_add(cm)
            # dt=[dtd, dtt, dtf]
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



def coffee_make_time(request, pk):
    coffee4 = get_object_or_404(CoffeeMake, pk=pk)
    if request.method == "POST":
        form = CoffeeTimeForm(request.POST)
        if form.is_valid():
            cm = form.cleaned_data
            dtf = date_time_add(cm)
            coffee4.c_make_user = request.user 
            coffee4.c_make_date = dtf
            coffee4.c_reg_time = timezone.now() 
            coffee4.save()
            adat = "jel"
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "coffeeTableChanged": None,
                        "showMessage": f"{adat} updated."
                    })
                }
            )
            # return redirect('shop:coffee_order')
            # context = {'adat':cm, 'adat2':coffee4.c_make_date, 'adat3':dtf}
            # return render(request, 'shop/c_time_back.html', context)
        else:
            proba = form.errors.as_data() # here you print errors to terminal
            context = {'adat':coffee4, 'adat2':pk, 'adat3':proba}
            return render(request, 'shop/c_error.html', context)

    else:
        form = CoffeeTimeForm()
        # form.fields['c_make_date'].initial = dt
    context = {'form': form, 'coffee4':coffee4, 'adat':pk, 'adat2':coffee4.c_make_dose, 'adat3':coffee4.c_make_date }
    return render(request,'shop/c_time_form.html', context) 
    #TypeError: fromisoformat: argument must be str => just one comma behind dtf 22.06.19!

def coffee_order(request):
    return render(request, 'shop/coffee_order.html')

def coffee_order_table(request):
    dt= datetime.datetime.now()
    dt_start = dt
    dt_end = dt + datetime.timedelta(hours=36)
    coffees1 = CoffeeMake.objects.filter(c_make_date__range =(dt_start, dt_end))
    coffees = coffees1.order_by('id')
    adat = []
    for coffee in coffees:
        adat.append(coffee.id)
    ordered = CoffeeOrder.objects.filter(coffee_selected__in = adat)
    for coffee in coffees:
        coffee.c_order_yes = False
        for order in ordered:
            if order.coffee_selected.id == coffee.id:
                coffee.c_order_yes = True
        coffee.save()        
    coffees = coffees.order_by('c_make_date')
    return render(request, 'shop/coffee_order_table.html', 
        {'coffees':coffees,'dt':dt, 'dt_end':dt_end, 'adat':adat, 'ordered':ordered,})


def coffee_order_remove(request, pk):
    coffee2 = get_object_or_404(CoffeeOrder, pk=pk)
    coffee1 = get_object_or_404(CoffeeMake, pk=coffee2.coffee_selected.id)
    dose = coffee1.c_make_dose
    coffee1.c_make_dose = dose + coffee2.coffee_dose
    coffee1.save()
    coffee2.delete()
    return redirect('shop:coffee_order')
    ''' context = {'coffees':coffee1, 'adat':dose,'adat2':coffee2.coffee_dose,  'adat3':coffee1.c_make_dose }
    return  render(request, 'shop/c_error.html', context ) '''

def coffee_order_form(request, pkey):
    proba = ''
    coffee_1 = get_object_or_404(CoffeeMake, pk=pkey)
    dose = coffee_1.c_make_dose
    wares = ProductAcquisition.objects.filter(store_status=3)
    sugar = []; milk = []; flavour = []; adat = []
    for ware in wares:
        if ware.ware_type.ware_type.ware_types == 'Cukor':
            dt1 = ware.id
            dt2 = ware
            dt = (dt1,dt2)
            sugar.append(dt)
        elif ware.ware_type.ware_type.ware_types == 'Tej': 
            dt1 = ware.id
            dt2 = ware
            dt = (dt1,dt2)
            milk.append(dt)
        elif ware.ware_type.ware_type.ware_types == 'Ízesítő': 
            dt1 = ware.id
            dt2 = ware
            dt = (dt1,dt2)
            flavour.append(dt)

    if request.method == "POST":
        form = CoffeeOrderForm(request.POST)
        if form.is_valid():
            coffee2 = form.cleaned_data
            coffee2 = form.save(commit=False)
            coffee2.coffee_selected = coffee_1
            coffee2.coffe_user = request.user
            coffee2.coffee_reg = timezone.now()
            if coffee2.sugar_dose == 0:
                coffee2.sugar_choice = None
            if coffee2.milk_dose == 0:
                coffee2.milk_choice = None
            if coffee2.flavour_dose == 0:
                coffee2.flavour_choice = None
            coffee2.save()
            coffee_1.c_make_dose = dose-coffee2.coffee_dose
            coffee_1.save()
            return redirect('shop:coffee_order')
            ''' return  render(request, 'shop/c_order_form_copy.html',
                {'form': form, 'wares':wares, 'dose':dose, 'coffee_1':coffee_1, 'coffee2':coffee2,
                'sugar_s':sugar_s, 'milk_s':milk_s, 'flavour_s':flavour_s, 'proba':proba, 
                'sugar_min':sugar_min, 'milk_min':milk_min, 'flavour_min':flavour_min})'''
        else:
            proba = form.errors.as_data() # here you print errors to terminal
            ''' coffee2 = form.save()
            coffee2.coffee_selected = coffee_1
            coffee2.coffe_user = request.user
            coffee2.coffee_reg = timezone.now() 
            sugar_s =  get_object_or_404(ProductAcquisition, pk=coffee2.sugar_choice.pk)
            milk_s = get_object_or_404(ProductAcquisition, pk=coffee2.milk_choice.pk)
            flavour_s = get_object_or_404(ProductAcquisition, pk=coffee2.flavour_choice.pk)'''
            context = {'form': form, 'wares':wares,  'proba':proba}
            return  render(request, 'shop/c_error.html', context )
    else:
        form = CoffeeOrderForm()
        form.fields['sugar_choice'].choices  = sugar
        # form.fields['sugar_choice'].initial  = None
        form.fields['milk_choice'].choices  = milk
        # form.fields['milk_choice'].initial  = [1]
        form.fields['flavour_choice'].choices  = flavour
        # form.fields['flavour_choice'].initial  = [1]
        form.fields['coffee_dose'].widget.attrs['max'] = dose
        # proba = "Betölt else ág"
        # context = {'form': form, 'wares':wares, 'dose':dose, 'coffee_1':coffee_1,'sugar':sugar, 'milk':milk, 'falvour':flavour, 'proba':proba}
        context = {'form': form, 'wares':wares, 'dose':dose, 'coffee_1':coffee_1}
    return render(request, 'shop/c_order_form.html', context )

def coffee_booking(request):
    dt= datetime.datetime.now()
    dt_start = dt
    dt_end = dt + datetime.timedelta(hours=36)
    coffees1 = CoffeeMake.objects.filter(c_book__isnull=True).filter(c_make_date__lt=dt)
    # coffees1 = CoffeeMake.objects.filter(c_make_date__range =(dt_start, dt_end))
    coffees = coffees1.order_by('id')
    adat = []
    for coffee in coffees:
        adat.append(coffee.id)
    coffees = coffees.order_by('c_make_date')
    ordered = CoffeeOrder.objects.filter(coffee_selected__in = adat)
    context = {'coffees':coffees,'dt':dt, 'dt_end':dt_end, 'adat':adat, 'ordered':ordered}
    return render(request, 'shop/coffee_booking.html', context)

def coffee_booking_pk(request, pkey):
    coffees3 = get_object_or_404(CoffeeMake, pk=pkey)
    orders3 = CoffeeOrder.objects.filter(coffee_selected = pkey)
    sugar_ss = get_object_or_404(WareTypes, id=1).ware_wght
    milk_ss = get_object_or_404(WareTypes, id=3).ware_wght
    flavour_ss = get_object_or_404(WareTypes, id=4).ware_wght
    alap = [1234 ,sugar_ss, milk_ss, flavour_ss]
    adat = []
    
    for order3 in orders3:
        milk_s = 0
        flavour_s = 0
        if order3.sugar_choice != None:
            sugar_s =  get_object_or_404(ProductAcquisition, pk=order3.sugar_choice.pk)
            sugar_s.stock -= sugar_ss * order3.sugar_dose
            sugar_s.save()
        if order3.milk_choice != None:
            milk_s = get_object_or_404(ProductAcquisition, pk=order3.milk_choice.pk)
            milk_s.stock -= milk_ss * order3.milk_dose
            milk_s.save()
        if order3.flavour_choice != None:
            flavour_s = get_object_or_404(ProductAcquisition, pk=order3.flavour_choice.pk)
            flavour_s.stock -= flavour_ss * order3.flavour_dose
            flavour_s.save()
        adat.append([sugar_s, milk_s, flavour_s])   
    coffees3.c_book = timezone.now()
    coffees3.save()
    return redirect('shop/coffee_booking.html')
    ''' return render(request, 'shop/booking_pk.html', 
    {'pkey':pkey, 'coffees3':coffees3, 'orders3':orders3, 'adat':adat, 'alap':alap})'''

