from django.shortcuts import render
from django.utils import timezone

def main_page(request):
    
    return render(request, 'shop/main.html', {})

