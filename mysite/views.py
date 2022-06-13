from asyncio.windows_events import NULL
from django.shortcuts import render
# from .forms import ContactForm
from django.http import JsonResponse, HttpResponse
from shop.models import CoffeeOrder, CoffeeMake
import datetime


def home_page(request):
    sub_site_logo = "src=static/image/coffe_bean_heart.png"
    dt= datetime.datetime.now()
    dt_start = dt
    dt_end = dt + datetime.timedelta(hours=36)
    coffees1 = CoffeeMake.objects.filter(c_make_date__range =(dt_start, dt_end))
    coffees2 = CoffeeMake.objects.filter(c_book__isnull=True)
    coffees = coffees1.order_by('c_make_date')
    return render(request, "home.html", {'sub_site_logo':sub_site_logo, 
        'coffees':coffees,'coffees2':coffees2,})

def contact_page(request):
    sub_site_logo = "src=static/image/coffe_bean_heart.png"
    return render(request, "contact.html", {'sub_site_logo':sub_site_logo})