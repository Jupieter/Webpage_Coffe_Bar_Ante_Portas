from django.shortcuts import render
from django.utils import timezone

def shop_page(request):
    
    return render(request, 'shop/home.html', {})

