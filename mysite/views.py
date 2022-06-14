from django.shortcuts import render
from shop.models import CoffeeMake
from raw_material.models import ProductAcquisition, WareTypes
import datetime


def home_page(request):
    sub_site_logo = "src=static/image/coffe_bean_heart.png"
    dt= datetime.datetime.now()
    dt_start = dt
    dt_end = dt + datetime.timedelta(hours=36)
    wares = []
    coffees1 = CoffeeMake.objects.filter(c_make_date__range =(dt_start, dt_end))
    coffees2 = CoffeeMake.objects.filter(c_book__isnull=True)
    coffees = coffees1.order_by('c_make_date')
    wares1 = ProductAcquisition.objects.filter(store_status=3)
    for ware in wares1:
        if ware.stock / ware.ware_type.ware_weight < 0.08:
            wares.append(ware)
    return render(request, "home.html", {'sub_site_logo':sub_site_logo, 
        'coffees':coffees,'coffees2':coffees2, 'wares':wares})

def contact_page(request):
    sub_site_logo = "src=static/image/coffe_bean_heart.png"
    return render(request, "contact.html", {'sub_site_logo':sub_site_logo})