from django.shortcuts import render
# from .forms import ContactForm
from django.http import JsonResponse, HttpResponse


def home_page(request):
    sub_site_logo = "src=static/image/coffe_bean_heart.png"
    return render(request, "home.html", {'sub_site_logo':sub_site_logo})